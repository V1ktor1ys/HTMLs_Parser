
window.S24_OSA = window.S24_OSA || {};
window.S24_OSA.apsConfig = window.S24_OSA.apsConfig || [{
    slotName: '/4467/IS24_DE/expose/sky_right',
    sizes: [[300, 600], [160, 600]]
}, {
    slotName: '/4467/IS24_DE/expose/banner_top',
    sizes: [[970, 250], [728, 90]]
}, {
    slotName: '/4467/IS24_DE/expose/banner_content_1',
    sizes: [[300, 250], [728, 90]]
}, {
    slotName: '/4467/IS24_DE/expose/banner_right_1',
    sizes: [[300, 250]]
}, {
    slotName: '/4467/IS24_DE/expose/banner_right_2',
    sizes: [[300, 600], [160, 600]]
}, {
    slotName: '/4467/IS24_DE/expose_new/sky_1',
    sizes: [[300, 600], [120, 600], [160, 600]]
}, {
    slotName: '/4467/IS24_DE/expose_new/sky_2',
    sizes: [[300, 600], [120, 600], [160, 600]]
}, {
    slotName: '/4467/IS24_DE/expose_new/sky_3',
    sizes: [[300, 600], [120, 600], [160, 600]]
}, {
    slotName: '/4467/IS24_DE/expose_new/mr_4',
    sizes: [[300, 250], [120, 600], [160, 600]]
}, {
    slotName: '/4467/IS24_DE/expose_new/contentbanner_1',
    sizes: [[320, 100], [728, 90]]
}, {
    slotName: '/4467/IS24_DE/expose_new/bottom',
    sizes: [[300, 250],[320, 100],[320, 240], [336, 280], [970, 250], [728, 90], [800, 250]]
}];

(()=>{var a=class{constructor(){this.adUnitPathsWithUnusedBids={}}hasUnusedBidsForAllSlots(i){for(let n=0;n<i.length;n++){let t=i[n];if(t.eligibleAdSizesForResolution&&t.eligibleAdSizesForResolution.length>0&&!this.adUnitPathsWithUnusedBids[t.adUnitPath+":"+t.container.id])return!1}return!0}markBidsAsUsed(i){i.forEach(n=>{n.isOutOfPage||(this.adUnitPathsWithUnusedBids[n.adUnitPath+":"+n.container.id]=!1)})}saveUnusedBidsFlags(i){i.forEach(n=>{this.adUnitPathsWithUnusedBids[n.adUnitPath+":"+n.container.id]=!0})}resetUnusedBids(){this.adUnitPathsWithUnusedBids={}}};var w=()=>{(function(e,i,n,t,r,o,u){if(i[e])return;function g(h,A){i[e]._Q.push([h,A])}i[e]={init:function(){g("i",arguments)},fetchBids:function(){g("f",arguments)},setDisplayBids:function(){},targetingKeys:function(){return[]},_Q:[]},o=n.createElement(t),o.async=!0,o.src=r,u=n.getElementsByTagName(t)[0],u.parentNode.insertBefore(o,u)})("apstag",window,document,"script","//c.amazon-adsystem.com/aax2/apstag.js")},C=()=>window.location;var s={middlewareId:"apsMiddleware",initialPromise:null,initialBidsRequested:!1,usedBidsTracker:new a,slotNameToSlotIdMapping:{},onMiddlewareRegistered:()=>{l()||(w(),window.apstag.init({pubID:"3620",adServer:"googletag"}),d("Init APS"))},onAdSlotCreated:e=>{l()||(p(e),s.initialBidsRequested||U())},onGptAdSlotDestroyed:e=>{l()||I(e)},onAdSlotsRefreshing:e=>{if(l())return Promise.resolve();if(s.initialPromise){let i=s.initialPromise.then(n=>(s.usedBidsTracker.markBidsAsUsed(e),n));return s.initialPromise=null,i}else return s.usedBidsTracker.hasUnusedBidsForAllSlots(e)?(d("APS: Using existing bids instead of rebidding.",s.usedBidsTracker.adUnitPathsWithUnusedBids),s.usedBidsTracker.markBidsAsUsed(e),Promise.resolve(!0)):(d("APS: Rebidding.",s.usedBidsTracker.adUnitPathsWithUnusedBids),e.forEach(p),f(P(e)))}},l=()=>window.S24_OSA.getConfigValue&&window.S24_OSA.getConfigValue("deactivateApsMiddleware"),c=null,U=()=>{c||(c=window.S24_OSA.debounce(()=>{s.initialBidsRequested=!0,s.initialPromise=f(m())},50)),c()},f=e=>!e||e.length===0?(d("No APS bids to load at this point",e),Promise.resolve()):(d("Loading APS bids",e),new Promise(i=>{let n=window.setTimeout(()=>{d("Amazon Bidder ran into hard timeout."),i([])},1200);window.apstag.fetchBids({slots:e,timeout:1e3},t=>{window.clearTimeout(n),i(t)})}).then(i=>{d("Got APS bids",i);let n=i.map(t=>window.S24_OSA.slotStore.getAdSlotByDomId(t.slotID)).filter(t=>!!t);s.usedBidsTracker.saveUnusedBidsFlags(n),window.googletag=window.googletag||{},window.googletag.cmd=window.googletag.cmd||[],window.googletag.cmd.push(()=>{window.apstag.setDisplayBids(),d("APS targeting set")})})),P=e=>m().filter(i=>!!e.find(n=>n.adUnitPath.toLowerCase()===i.slotName.toLowerCase())),m=()=>{let e=[];return(window.S24_OSA.apsConfig||[]).forEach(i=>{let n=window.S24_OSA.adjustAdUnitPath(i.slotName);(s.slotNameToSlotIdMapping[n.toLowerCase()]||[]).forEach(r=>{let o=Object.assign({},i);o.slotName=n,o.slotID=r,o.slotID&&(o.sizes=B(o)),e.push(o)})}),e.filter(i=>!!i.slotID&&i.sizes&&i.sizes.length>0)},B=e=>{if(!e.sizes)return e.sizes;let i=window.S24_OSA.slotStore.getAdSlotByDomId(e.slotID);if(i){let n=i.eligibleAdSizesForResolution;return e.sizes.filter(t=>n.find(r=>JSON.stringify(r)===JSON.stringify(t)))}else return e.sizes},p=e=>{if(!e.isOutOfPage){let i=e.adUnitPath.toLowerCase();s.slotNameToSlotIdMapping[i]?s.slotNameToSlotIdMapping[i].push(e.container.id):s.slotNameToSlotIdMapping[i]=[e.container.id]}},I=e=>{if(!e.isOutOfPage){let i=e.adUnitPath.toLowerCase(),n=s.slotNameToSlotIdMapping[i];n&&(s.slotNameToSlotIdMapping[i]=n.filter(t=>t!==e.container.id))}};function d(e,i){window.S24_OSA.logging.log({msg:e,cat:"aps",color:"#FFD208"},i)}var S=(e,i,n)=>{window.UC_UI&&window.UC_UI.isInitialized()?window.__tcfapi("addEventListener",2,t=>{(t.eventStatus==="tcloaded"||t.eventStatus==="useractioncomplete")&&t.vendor.consents[e]&&t.purpose.consents[1]&&t.purpose.consents[3]&&t.purpose.consents[5]&&t.purpose.consents[6]&&(i(),n())}):window.addEventListener("UC_UI_INITIALIZED",()=>{window.__tcfapi("addEventListener",2,t=>{(t.eventStatus==="tcloaded"||t.eventStatus==="useractioncomplete")&&t.vendor.consents[e]&&t.purpose.consents[1]&&t.purpose.consents[3]&&t.purpose.consents[5]&&t.purpose.consents[6]&&(i(),n())})})};var _=e=>window.__tcfapi?new Promise(i=>{S(e,()=>{window.S24_OSA.logging.log({msg:`\u2705 Usercentrics consent has been given to vendor ${e}`,cat:"lifecycle",color:"#ff8a0b"})},i)}):Promise.reject();window.S24_OSA=window.S24_OSA||{},window.S24_OSA.cmd=window.S24_OSA.cmd||[],window.S24_OSA.cmd.push(()=>{_(793).then(()=>{window.S24_OSA.registerMiddleware(s)})});})();
