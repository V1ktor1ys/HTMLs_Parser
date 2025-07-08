from bs4 import BeautifulSoup
import json
import csv
import os
from pathlib import Path
import re

# Paths and settings
input_root = Path("./HTMLs")
output_file = "apartment_list.csv"
parsed_log_file = "parsed_files.txt"
headers = ["#", "Date", "Link", "", "", "Land Lord", "Published", "Rooms", "m²", "Price (Warm)", "Available From", "Address"]

# Load already parsed files
parsed_files = set()
if os.path.exists(parsed_log_file):
    with open(parsed_log_file, "r", encoding="utf-8") as f:
        parsed_files = set(line.strip() for line in f)

# Determine if headers should be written
write_headers = not os.path.exists(output_file)

# Detect site based on HTML content
def detect_site(soup):
    text = soup.get_text().lower()
    if "immobilienscout24" in text or "is24" in text:
        return "immoscout24"
    elif "immowelt" in text or "aviv germany" in text or "aviv.cdp" in text:
        return "immowelt"
    return "unknown"

# Parser for immobilienscout24.de
def parse_immoscout24(soup):
    json_ld = soup.find("script", type="application/ld+json")
    data = json.loads(json_ld.string)["@graph"]
    listing = next((item for item in data if item["@type"] == "RealEstateListing"), {})
    provider = listing.get("provider", {})
    offer = listing.get("offers", {})

    link = listing.get("url", "")

    contact_elem = soup.select_one('[data-qa="contactName"]')
    landlord = contact_elem.get_text(strip=True) if contact_elem else provider.get("name", "")

    published = listing.get("datePosted", "")

    rooms_meta = soup.find("meta", {"name": "branch:deeplink:expose-number-of-rooms"})
    rooms = rooms_meta.get("content", "") if rooms_meta else ""

    size_match = re.search(r"(\d{1,3}(?:,\d{1,3})?)\s*m²", soup.get_text())
    size = size_match.group(1).replace(",", ".") if size_match else ""

    warm_elem = soup.select_one(".is24qa-warmmiete-main span")
    warm_rent = warm_elem.get_text(strip=True) if warm_elem else ""

    available_from = ""
    label = soup.find(string=re.compile("Bezugsfrei ab", re.IGNORECASE))
    if label:
        parent = label.find_parent()
        if parent:
            next_elem = parent.find_next_sibling()
            if next_elem:
                available_from = next_elem.get_text(strip=True)

    address = ""
    address_block = soup.select_one(".address-block")
    if address_block:
        street_elem = address_block.select_one(".block")
        zip_elem = address_block.select_one(".zip-region-and-country")
        street = street_elem.get_text(strip=True).rstrip(",") if street_elem else ""
        zip_text = zip_elem.get_text(strip=True) if zip_elem else ""
        if "vollständige adresse" not in zip_text.lower():
            address = f"{street}, {zip_text}".strip(", ")
        elif street:
            address = street
        else:
            address = zip_text
    else:
        address = "München"

    return [link, "", "", landlord, published, rooms, size, warm_rent, available_from, address]

# Parser for immowelt.de
def parse_immowelt(soup, file):
    link_tag = soup.find("link", rel="canonical")
    link = link_tag["href"] if link_tag else f"https://www.immowelt.de/expose/{file.stem}"

    landlord_elem = soup.find("div", {"data-testid": "aviv.CDP.Contacting.ContactCard.Title"})
    landlord = landlord_elem.get_text(strip=True) if landlord_elem else ""

    published = ""

    rooms = ""
    room_elem = soup.find("span", class_="css-2bd70b", string=re.compile(r"^\d+(\.\d+)?$"))
    if room_elem:
        rooms = room_elem.get_text(strip=True)

    size = ""
    size_elem = soup.find("span", class_="css-2bd70b", string=re.compile(r"m²"))
    if size_elem:
        size = re.search(r"\d+", size_elem.get_text(strip=True)).group(0)

    # Try to extract from hidden <span class="css-9wpf20"> inside Warmmiete block
    warm_rent = ""
    warm_label_block = soup.find("div", class_="css-2bd70b", string=re.compile(r"Warmmiete", re.IGNORECASE))
    if warm_label_block:
        parent = warm_label_block.find_parent()
        if parent:
            price_span = parent.find_next_sibling()
            if price_span:
                hidden = price_span.find("span", class_="css-9wpf20")
                if hidden:
                    warm_rent = hidden.get_text(strip=True)

    available_from = ""
    avail_elem = soup.find("span", class_="css-2bd70b", string=re.compile(r"\d{2}\.\d{2}\.\d{4}"))
    if avail_elem:
        available_from = avail_elem.get_text(strip=True)

    address = ""
    address_elem = soup.find("div", class_="css-1ytyjyb")
    if address_elem:
        address = address_elem.get_text(" ", strip=True).replace("\xa0", " ")
        address = re.sub(r"\s*,\s*", ", ", address)

    return [link, "", "", landlord, published, rooms, size, warm_rent, available_from, address]

# Run extraction
html_files = []
for subfolder in sorted(input_root.iterdir()):
    if subfolder.is_dir() and subfolder.name.lower().startswith("htmls_"):
        date_part = subfolder.name.split("_")[1]
        for file in sorted(subfolder.glob("*.htm*"), key=lambda f: int(f.stem) if f.stem.isdigit() else f.stem):
            html_files.append((file, date_part))

with open(output_file, "a", newline="", encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile, delimiter=";")
    if write_headers:
        writer.writerow(headers)

    for file, date_str in html_files:
        if file.name in parsed_files:
            print(f"⏭️ Skipping already parsed file: {file.name}")
            continue

        try:
            with open(file, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")

            site = detect_site(soup)
            if site == "immoscout24":
                row = parse_immoscout24(soup)
            elif site == "immowelt":
                row = parse_immowelt(soup, file)
            else:
                print(f"❌ Unknown site structure: {file.name}")
                continue

            listing_number = Path(file).stem  # Extracts "1" from "1.html"
            writer.writerow([listing_number, date_str] + row)
            print(f"✔️ Processed: {file.name}")

            with open(parsed_log_file, "a", encoding="utf-8") as log:
                log.write(f"{file.name}\n")

        except Exception as e:
            print(f"❌ Error in {file.name}: {e}")