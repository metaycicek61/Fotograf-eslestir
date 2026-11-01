const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [inp,out]=process.argv.slice(2);const b=await chromium.launch();const p=await b.newPage();
await p.route(/cdn.jsdelivr.net/,r=>r.fulfill({contentType:'application/javascript',body:'export const pipeline=async()=>async()=>[];'}));
await p.goto('http://localhost:8766/Okuyucu.html');await p.waitForFunction(()=>window.__siteRaw);
const r=await p.evaluate(d=>window.__siteRaw(d),'data:image/png;base64,'+fs.readFileSync(inp).toString('base64'));
fs.writeFileSync(out,JSON.stringify(r));console.log(r.length);await b.close();})();
