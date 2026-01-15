<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Simple Product Data Extractor (Safe)</title>
  <style>
    :root{
      --bg:#0b0f17; --card:#111827; --card2:#0f172a;
      --text:#e8eefc; --muted:#9fb0d0; --line:rgba(255,255,255,.12);
      --accent:#7aa2ff; --good:#3ddc97; --warn:#ffcc66; --bad:#ff6b6b;
      --radius:16px;
      --sans: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
      --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono","Courier New", monospace;
    }
    *{box-sizing:border-box}
    body{
      margin:0; font-family:var(--sans); color:var(--text);
      background:
        radial-gradient(1200px 600px at 10% 5%, rgba(122,162,255,.18), transparent 55%),
        radial-gradient(900px 500px at 90% 15%, rgba(61,220,151,.12), transparent 55%),
        var(--bg);
    }
    .wrap{max-width:1100px; margin:0 auto; padding:18px}
    .top{
      display:flex; align-items:center; justify-content:space-between; gap:10px; flex-wrap:wrap;
      padding:14px 16px; border:1px solid var(--line); border-radius:var(--radius);
      background:linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.02));
    }
    .title{display:flex; gap:10px; align-items:center}
    .dotlogo{
      width:34px; height:34px; border-radius:12px;
      background:linear-gradient(135deg, rgba(122,162,255,.95), rgba(61,220,151,.75));
    }
    h1{font-size:14px; margin:0}
    .sub{font-size:12px; color:var(--muted); margin-top:2px}
    .tabs{display:flex; gap:8px; align-items:center}
    .tab{
      padding:9px 12px; border-radius:12px; border:1px solid var(--line);
      background:rgba(255,255,255,.03); color:var(--muted); cursor:pointer; font-size:13px;
    }
    .tab.active{border-color:rgba(122,162,255,.45); background:rgba(122,162,255,.12); color:var(--text)}
    .btn{
      padding:9px 12px; border-radius:12px; border:1px solid var(--line);
      background:rgba(255,255,255,.04); color:var(--text); cursor:pointer; font-size:13px;
    }
    .btn.primary{border-color:rgba(122,162,255,.45); background:rgba(122,162,255,.12)}
    .btn:disabled{opacity:.55; cursor:not-allowed}
    .grid{display:grid; gap:12px; margin-top:12px}
    .card{
      border:1px solid var(--line); border-radius:var(--radius);
      background:linear-gradient(180deg, rgba(255,255,255,.05), rgba(255,255,255,.02));
      overflow:hidden;
    }
    .hd{padding:12px 14px; border-bottom:1px solid var(--line); display:flex; justify-content:space-between; align-items:center; gap:10px}
    .hd h2{margin:0; font-size:13px}
    .hint{color:var(--muted); font-size:12px; line-height:1.4}
    .bd{padding:12px 14px}
    .row{display:flex; gap:10px; flex-wrap:wrap; align-items:flex-start}
    .col{flex:1 1 280px}
    .box{
      border:1px solid var(--line); border-radius:12px; padding:10px 12px;
      background:rgba(0,0,0,.18);
    }
    input[type="text"], textarea, select{
      width:100%; border:0; outline:none; background:transparent; color:var(--text); font-size:13px;
    }
    textarea{min-height:110px; resize:vertical; font-family:var(--mono); font-size:12.5px}
    input[type="file"]{color:var(--muted)}
    .metrics{display:grid; gap:10px; grid-template-columns: repeat(4, 1fr);}
    @media (max-width:900px){ .metrics{grid-template-columns: repeat(2, 1fr);} }
    @media (max-width:520px){ .metrics{grid-template-columns: 1fr;} }
    .tile{border:1px solid var(--line); border-radius:14px; padding:10px 12px; background:rgba(255,255,255,.02)}
    .k{color:var(--muted); font-size:11.5px}
    .v{font-size:18px; margin-top:6px}
    .v.good{color:var(--good)} .v.warn{color:var(--warn)} .v.bad{color:var(--bad)}
    .badge{
      display:inline-flex; gap:8px; align-items:center;
      padding:6px 10px; border-radius:999px; border:1px solid rgba(255,255,255,.12);
      background:rgba(255,255,255,.03); font-size:12px; color:var(--muted);
    }
    .dot{width:8px; height:8px; border-radius:50%}
    .dot.good{background:var(--good)} .dot.bad{background:var(--bad)} .dot.warn{background:var(--warn)}
    .hidden{display:none !important;}
    .checklist{display:grid; gap:8px; grid-template-columns: 1fr 1fr;}
    @media (max-width:900px){ .checklist{grid-template-columns:1fr} }
    .ck{display:flex; gap:10px; align-items:flex-start; border:1px solid var(--line); border-radius:12px; padding:10px 12px; background:rgba(255,255,255,.02)}
    .ck input{margin-top:3px}
    .t{font-size:12.5px; font-weight:600}
    .d{font-size:11.5px; color:var(--muted); margin-top:2px}
    table{
      width:100%; border-collapse:separate; border-spacing:0; font-size:12.5px;
      border:1px solid var(--line); border-radius:14px; overflow:hidden; background:rgba(0,0,0,.15);
    }
    thead th{padding:10px; text-align:left; color:var(--muted); background:rgba(255,255,255,.02); border-bottom:1px solid var(--line); position:sticky; top:0}
    tbody td{padding:9px 10px; border-bottom:1px solid rgba(255,255,255,.06); vertical-align:top}
    tbody tr:last-child td{border-bottom:0}
    .tablewrap{max-height:260px; overflow:auto; border-radius:14px}
    footer{margin:14px 0 4px; text-align:center; color:rgba(255,255,255,.45); font-size:12px}
  </style>
</head>
<body>
<div class="wrap">
  <div class="top">
    <div class="title">
      <div class="dotlogo" aria-hidden="true"></div>
      <div>
        <h1>Simple Product Data Extractor (Safe)</h1>
        <div class="sub" id="subhead">Page 1: Upload + Website Tests + Dashboard</div>
      </div>
    </div>

    <div class="tabs">
      <button class="tab active" id="tab1" type="button">Page 1</button>
      <button class="tab" id="tab2" type="button" disabled>Page 2</button>
      <button class="btn" id="btnReset" type="button">Reset</button>
      <button class="btn primary" id="btnNext" type="button" disabled>Next</button>
      <button class="btn hidden" id="btnBack" type="button">Back</button>
    </div>
  </div>

  <!-- PAGE 1 -->
  <section id="page1" class="grid">
    <div class="card">
      <div class="hd">
        <h2>1) Upload input file</h2>
        <span class="hint">CSV/TSV recommended (headers can be any case)</span>
      </div>
      <div class="bd">
        <div class="row">
          <div class="col">
            <div class="hint">
              Suggested columns: Product Name, ASIN (optional), UPC, EAN, URL (optional), Images (optional)
            </div>
          </div>
          <div class="col">
            <input id="file" type="file" accept=".csv,.tsv,text/csv,text/tab-separated-values" />
          </div>
        </div>

        <div style="height:10px"></div>

        <div class="row">
          <div class="col">
            <div class="box">
              <div class="hint" style="margin-bottom:6px;">(Optional) Paste input rows (CSV or TSV)</div>
              <textarea id="pasteInput" placeholder="Example TSV:
Product Name	UPC	EAN	URL
Milk Thistle 200mg	123456789012		https://brand.com/product"></textarea>
            </div>
          </div>
        </div>

        <div style="height:10px"></div>

        <div class="metrics">
          <div class="tile"><div class="k">Rows detected</div><div class="v" id="mRows">0</div></div>
          <div class="tile"><div class="k">Missing Product Name</div><div class="v bad" id="mMissingName">0</div></div>
          <div class="tile"><div class="k">Missing UPC/EAN</div><div class="v warn" id="mMissingCode">0</div></div>
          <div class="tile"><div class="k">Delimiter</div><div class="v" id="mDelim">—</div></div>
        </div>

        <div style="height:10px"></div>

        <button class="btn" id="btnDownloadTemplate" type="button">Download Template CSV</button>
        <button class="btn" id="btnDownloadPage1" type="button" disabled>Download Parsed Input (CSV)</button>
      </div>
    </div>

    <div class="card">
      <div class="hd">
        <h2>2) Test websites (Blocked / Unblocked)</h2>
        <span class="hint">Safe test only (no bypassing)</span>
      </div>
      <div class="bd">
        <div class="row">
          <div class="col">
            <div class="hint" style="margin-bottom:6px;">Test one website</div>
            <div class="box"><input id="testUrl" type="text" placeholder="https://example.com/product" /></div>
          </div>
          <div style="flex:0 0 auto; padding-top:22px">
            <button class="btn primary" id="btnTestOne" type="button">Test</button>
          </div>
        </div>

        <div style="height:10px"></div>
        <div class="badge" id="testBadge"><span class="dot warn"></span><span id="testStatus">Status: —</span></div>
        <div class="hint" id="testReason" style="margin-top:6px;">Reason: —</div>

        <div style="height:12px"></div>

        <div class="hint" style="margin-bottom:6px;">Paste multiple websites (one per line)</div>
        <div class="box">
          <textarea id="multiUrls" placeholder="https://site1.com/product
https://site2.com/item
https://site3.com/p/xyz"></textarea>
        </div>

        <div style="height:10px"></div>

        <div class="row">
          <button class="btn primary" id="btnTestMany" type="button">Test All</button>
          <button class="btn" id="btnClearTests" type="button">Clear Results</button>
        </div>

        <div style="height:10px"></div>

        <div class="tablewrap">
          <table>
            <thead>
              <tr>
                <th>URL</th>
                <th>Domain</th>
                <th>Status</th>
                <th>HTTP</th>
                <th>Reason</th>
              </tr>
            </thead>
            <tbody id="testsBody"></tbody>
          </table>
        </div>

        <div class="hint" style="margin-top:10px;">
          Note: This HTML can’t reliably test websites by itself due to browser security (CORS).
          For real testing, connect a backend endpoint (recommended): <span style="font-family:var(--mono)">http://127.0.0.1:8000/api/test-url</span>.
        </div>
      </div>
    </div>

    <div class="card">
      <div class="hd">
        <h2>3) Field checklist (what to extract)</h2>
        <span class="hint">Select what you need</span>
      </div>
      <div class="bd">
        <div class="checklist" id="checklist"></div>

        <div style="height:10px"></div>

        <!-- meaningful extras -->
        <div class="row">
          <div class="col">
            <div class="ck">
              <input type="checkbox" id="optEvidence" checked />
              <div>
                <div class="t">Include Evidence + Source columns (recommended)</div>
                <div class="d">Adds columns like Ingredients__source and Ingredients__evidence for QA.</div>
              </div>
            </div>
          </div>
          <div class="col">
            <div class="ck">
              <input type="checkbox" id="optSanitize" checked />
              <div>
                <div class="t">Sanitize output (remove special characters)</div>
                <div class="d">Makes copy/paste into Excel cleaner.</div>
              </div>
            </div>
          </div>
        </div>

        <div class="hint" style="margin-top:10px;">
          Safety note: this tool should skip blocked sites and use fallback sources. It should not try to bypass protections.
        </div>
      </div>
    </div>
  </section>

  <!-- PAGE 2 -->
  <section id="page2" class="grid hidden">
    <div class="card">
      <div class="hd">
        <h2>Paste data (input)</h2>
        <span class="hint">Paste product rows here if you didn’t upload on Page 1</span>
      </div>
      <div class="bd">
        <div class="box">
          <textarea id="pastePage2" placeholder="Paste CSV/TSV here..."></textarea>
        </div>
        <div class="hint" style="margin-top:8px;">
          Tip: TSV is easiest for Excel. Use tabs between columns.
        </div>
      </div>
    </div>

    <div class="card">
      <div class="hd">
        <h2>Output + Download</h2>
        <span class="hint" id="outHint">No output yet</span>
      </div>
      <div class="bd">
        <div class="row">
          <button class="btn primary" id="btnRun" type="button">Run (needs backend)</button>
          <button class="btn" id="btnDownloadOutCSV" type="button" disabled>Download Output CSV</button>
          <button class="btn" id="btnDownloadOutTSV" type="button" disabled>Download Output TSV</button>
        </div>

        <div style="height:10px"></div>

        <div class="tablewrap">
          <table>
            <thead><tr id="outHead"></tr></thead>
            <tbody id="outBody"></tbody>
          </table>
        </div>

        <div class="hint" style="margin-top:10px;">
          This UI is intentionally simple. Real extraction requires a backend service (FastAPI) that fetches allowed pages and returns structured fields.
        </div>
      </div>
    </div>
  </section>

  <footer>Creating by Prachi Rajak</footer>
</div>

<script>
  const $ = (id) => document.getElementById(id);

  // --- Fields you requested + a meaningful extra set ---
  const FIELDS = [
    {key:"Product_Expiration_Type", label:"Product Expiration Type", desc:"EXP / Best By / Use By (if explicitly present)"},
    {key:"Product_Expiry_YN", label:"Product Expiry (Y/N)", desc:"Y if expiration type is present"},
    {key:"Shelf_Life", label:"Shelf life", desc:"Only if stated on source"},
    {key:"Safety_Warning", label:"Safety Warning", desc:"Warnings / Caution"},
    {key:"Indications", label:"Indications", desc:"What it’s for (if listed)"},
    {key:"Directions", label:"Directions (How to take)", desc:"Suggested use"},
    {key:"Flavor", label:"Flavor", desc:"If stated"},
    {key:"Days_Of_Use", label:"Days of use", desc:"Can be derived from servings if stated"},
    {key:"Target_Gender", label:"Target Gender", desc:"Only if explicitly stated"},
    {key:"Product_Benefits", label:"Product Benefits", desc:"Benefits list (if listed)"},
    {key:"Specific_Uses", label:"Specific Uses for product", desc:"Use cases (if listed)"},
    {key:"Item_Form", label:"Item Form", desc:"Capsule / Tablet / Powder / Liquid etc."},
    {key:"Allergen_Information", label:"Allergen Information", desc:"Contains / free-from statements (only if listed)"},

    // Meaningful extras (helpful in real workflows)
    {key:"Ingredients", label:"Ingredients (extra)", desc:"Often best from label images/OCR or brand page"},
    {key:"Source_URL_Used", label:"Source URL Used (extra)", desc:"Which page actually provided the data"},
    {key:"Source_Status", label:"Source Status (extra)", desc:"Blocked / Unblocked / No URL"}
  ];

  // default selected (your requested fields + 3 extras)
  const DEFAULT_SELECTED = new Set(FIELDS.map(f=>f.key));

  function renderChecklist(){
    const host = $("checklist");
    host.innerHTML = "";
    FIELDS.forEach(f => {
      const row = document.createElement("div");
      row.className = "ck";
      const cb = document.createElement("input");
      cb.type = "checkbox";
      cb.checked = DEFAULT_SELECTED.has(f.key);
      cb.dataset.key = f.key;

      const text = document.createElement("div");
      text.innerHTML = `<div class="t">${f.label}</div><div class="d">${f.desc}</div>`;
      row.appendChild(cb);
      row.appendChild(text);
      host.appendChild(row);
    });
  }
  function selectedFields(){
    return Array.from($("checklist").querySelectorAll("input[type=checkbox]"))
      .filter(x=>x.checked)
      .map(x=>x.dataset.key);
  }

  // --- Case-insensitive parsing (CSV or TSV) ---
  function normKey(k){ return (k ?? "").toString().toLowerCase().replace(/[^a-z0-9]/g,""); }
  function detectDelim(line){
    const tabs = (line.match(/\t/g)||[]).length;
    const commas = (line.match(/,/g)||[]).length;
    return tabs > commas ? "\t" : ",";
  }
  function splitLine(line, delim){
    if(delim === "\t") return line.split("\t").map(s=>s.trim());
    // CSV with basic quotes
    const out=[]; let cur=""; let inQ=false;
    for(let i=0;i<line.length;i++){
      const ch=line[i];
      if(ch === '"'){
        if(inQ && line[i+1] === '"'){ cur+='"'; i++; }
        else inQ=!inQ;
      } else if(ch===delim && !inQ){
        out.push(cur); cur="";
      } else cur+=ch;
    }
    out.push(cur);
    return out.map(s=>s.trim());
  }
  function parseDelimited(text){
    const lines = text.split(/\r?\n/).filter(l=>l.trim().length>0);
    if(!lines.length) return {headers:[], rows:[], delim:","};
    const delim = detectDelim(lines[0]);
    const headers = splitLine(lines[0], delim);
    const rows=[];
    for(let i=1;i<lines.length;i++){
      const cols = splitLine(lines[i], delim);
      const obj={};
      headers.forEach((h, idx)=> obj[h] = (cols[idx] ?? "").trim());
      rows.push(obj);
    }
    return {headers, rows, delim};
  }
  async function loadInput(){
    const f = $("file").files?.[0];
    if(f){
      const t = await f.text();
      return parseDelimited(t);
    }
    const pasted = $("pasteInput").value.trim();
    if(pasted) return parseDelimited(pasted);
    return {headers:[], rows:[], delim:","};
  }

  // flexible header mapping
  const SYN = {
    name: ["productname","product","itemname","title","name","producttitle","productnametitle","product name"],
    upc: ["upc","gtin12"],
    ean: ["ean","gtin13","gtin"],
    asin:["asin"],
    url: ["url","link","producturl"],
    images: ["images","image","imageurls","img","photos"]
  };

  function buildHeaderMap(headers){
    const map={};
    headers.forEach(h => map[normKey(h)] = h);
    return map;
  }
  function getBySyn(row, hmap, synList){
    for(const s of synList){
      const actual = hmap[normKey(s)];
      if(actual && row[actual] != null && String(row[actual]).trim() !== "") return String(row[actual]).trim();
    }
    return "";
  }
  function normalizeRow(row, hmap){
    return {
      Product_Name: getBySyn(row, hmap, SYN.name),
      UPC: getBySyn(row, hmap, SYN.upc),
      EAN: getBySyn(row, hmap, SYN.ean),
      ASIN: getBySyn(row, hmap, SYN.asin),
      URL: getBySyn(row, hmap, SYN.url),
      Images: getBySyn(row, hmap, SYN.images)
    };
  }

  // --- Dashboard / validator ---
  async function refreshDashboard(){
    const parsed = await loadInput();
    $("mDelim").textContent = parsed.delim === "\t" ? "TSV" : (parsed.headers.length ? "CSV" : "—");

    const hmap = buildHeaderMap(parsed.headers);
    const rows = parsed.rows.map(r => normalizeRow(r, hmap))
      .filter(x => Object.values(x).some(v => (v||"").trim() !== ""));

    let missName=0, missCode=0;
    rows.forEach(r=>{
      if(!r.Product_Name) missName++;
      if(!r.UPC && !r.EAN) missCode++;
    });

    $("mRows").textContent = String(rows.length);
    $("mMissingName").textContent = String(missName);
    $("mMissingCode").textContent = String(missCode);

    $("btnNext").disabled = rows.length === 0;
    $("tab2").disabled = rows.length === 0;

    $("btnDownloadPage1").disabled = rows.length === 0;
    window.__PARSED_INPUT__ = rows;
  }

  // --- Downloads ---
  function toCSV(rows){
    if(!rows.length) return "";
    const headers = Object.keys(rows[0]);
    const esc = (v)=>{
      const s=(v ?? "").toString();
      return /[",\n\r]/.test(s) ? `"${s.replace(/"/g,'""')}"` : s;
    };
    return [headers.map(esc).join(","), ...rows.map(r=> headers.map(h=>esc(r[h])).join(","))].join("\n");
  }
  function toTSV(rows){
    if(!rows.length) return "";
    const headers = Object.keys(rows[0]);
    return [headers.join("\t"), ...rows.map(r=> headers.map(h=>(r[h]??"").toString().replace(/\t/g," ")).join("\t"))].join("\n");
  }
  function downloadText(text, filename, mime){
    const blob = new Blob([text], {type:mime});
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href=url; a.download=filename;
    document.body.appendChild(a); a.click(); a.remove();
    URL.revokeObjectURL(url);
  }

  // --- Page navigation ---
  function showPage(n){
    const p1 = n === 1;
    $("page1").classList.toggle("hidden", !p1);
    $("page2").classList.toggle("hidden", p1);
    $("tab1").classList.toggle("active", p1);
    $("tab2").classList.toggle("active", !p1);
    $("subhead").textContent = p1
      ? "Page 1: Upload + Website Tests + Dashboard"
      : "Page 2: Paste Data + Run + Download";
    $("btnBack").classList.toggle("hidden", p1);
    $("btnNext").classList.toggle("hidden", !p1);
  }

  // --- Website testing (UI tries backend first; if not available, shows a clear message) ---
  function setTestBadge(status, reason){
    const badge = $("testBadge");
    const dot = badge.querySelector(".dot");
    if(status === "Unblocked"){ dot.className = "dot good"; }
    else if(status === "Blocked"){ dot.className = "dot bad"; }
    else { dot.className = "dot warn"; }
    $("testStatus").textContent = `Status: ${status || "—"}`;
    $("testReason").textContent = `Reason: ${reason || "—"}`;
  }

  async function apiTestUrl(url){
    // If you run the FastAPI backend, use this:
    // POST http://127.0.0.1:8000/api/test-url  { "url": "..." }
    const res = await fetch("http://127.0.0.1:8000/api/test-url", {
      method:"POST",
      headers:{ "Content-Type":"application/json" },
      body: JSON.stringify({ url })
    });
    if(!res.ok) throw new Error("Backend not reachable");
    return await res.json(); // {status, http_status, reason, domain, ...}
  }

  async function testOne(){
    const url = $("testUrl").value.trim();
    if(!url){ setTestBadge(null, "Paste a URL first."); return; }
    setTestBadge(null, "Testing…");
    try{
      const r = await apiTestUrl(url);
      setTestBadge(r.status, `${r.reason} (HTTP ${r.http_status ?? "?"})`);
      addTestRow({url, domain:r.domain||"", status:r.status||"", http:r.http_status??"", reason:r.reason||""});
    }catch(e){
      setTestBadge("Blocked", "Backend not running. Start backend for real Blocked/Unblocked tests.");
      addTestRow({url, domain:"", status:"—", http:"—", reason:"Backend not running"});
    }
  }

  function addTestRow(t){
    const tr = document.createElement("tr");
    [t.url, t.domain, t.status, String(t.http), t.reason].forEach(v=>{
      const td=document.createElement("td");
      td.textContent = v || "";
      tr.appendChild(td);
    });
    $("testsBody").appendChild(tr);
  }

  async function testMany(){
    const urls = $("multiUrls").value.split(/\r?\n/).map(s=>s.trim()).filter(Boolean);
    if(!urls.length){ setTestBadge(null, "Paste at least 1 URL."); return; }
    setTestBadge(null, `Testing ${urls.length} URLs…`);
    for(const u of urls){
      try{
        const r = await apiTestUrl(u);
        addTestRow({url:u, domain:r.domain||"", status:r.status||"", http:r.http_status??"", reason:r.reason||""});
      }catch{
        addTestRow({url:u, domain:"", status:"—", http:"—", reason:"Backend not running"});
      }
    }
    setTestBadge(null, "Done. Review table.");
  }

  function clearTests(){
    $("testsBody").innerHTML = "";
    setTestBadge(null, "");
  }

  // --- Run extraction (needs backend) ---
  let OUTPUT = [];

  async function apiRun(payload){
    // POST http://127.0.0.1:8000/api/run
    const res = await fetch("http://127.0.0.1:8000/api/run", {
      method:"POST",
      headers:{ "Content-Type":"application/json" },
      body: JSON.stringify(payload)
    });
    if(!res.ok) throw new Error("Backend not reachable");
    return await res.json(); // { output_rows:[...], ... }
  }

  function renderOutput(rows){
    const head = $("outHead");
    const body = $("outBody");
    head.innerHTML = ""; body.innerHTML = "";
    $("outHint").textContent = rows.length ? `${rows.length} rows ready` : "No output yet";
    if(!rows.length) return;

    const headers = Object.keys(rows[0]);
    headers.forEach(h=>{
      const th=document.createElement("th");
      th.textContent = h;
      head.appendChild(th);
    });
    rows.forEach(r=>{
      const tr=document.createElement("tr");
      headers.forEach(h=>{
        const td=document.createElement("td");
        td.textContent = r[h] ?? "";
        tr.appendChild(td);
      });
      body.appendChild(tr);
    });

    $("btnDownloadOutCSV").disabled = false;
    $("btnDownloadOutTSV").disabled = false;
  }

  async function runExtraction(){
    // Input can come from Page 1 parsed input or Page 2 paste
    let inputRows = (window.__PARSED_INPUT__ || []).slice();

    const p2 = $("pastePage2").value.trim();
    if(p2){
      const parsed = parseDelimited(p2);
      const hmap = buildHeaderMap(parsed.headers);
      inputRows = parsed.rows.map(r => normalizeRow(r, hmap))
        .filter(x => Object.values(x).some(v => (v||"").trim() !== ""));
    }

    if(!inputRows.length){
      alert("No input rows found. Upload/paste on Page 1 or paste on Page 2.");
      return;
    }

    const fields = selectedFields();
    const includeEvidence = $("optEvidence").checked;
    const sanitize = $("optSanitize").checked;

    // Payload expected by backend:
    // { products:[{name, upc, ean, url, images}], selected_fields:[...], include_evidence:true/false, sanitize:true/false }
    const payload = {
      products: inputRows.map(r => ({
        name: r.Product_Name || "",
        upc: r.UPC || "",
        ean: r.EAN || "",
        asin: r.ASIN || "",
        url: r.URL || "",
        images: r.Images || ""
      })),
      selected_fields: fields,
      include_evidence: includeEvidence,
      sanitize: sanitize
    };

    try{
      const resp = await apiRun(payload);
      OUTPUT = resp.output_rows || [];
      renderOutput(OUTPUT);
    }catch(e){
      alert("Backend not running. This UI needs a backend to fetch pages and return extracted fields.");
      OUTPUT = [];
      renderOutput([]);
    }
  }

  // --- Template ---
  function downloadTemplate(){
    const t = [
      "Product Name,UPC,EAN,URL,Images",
      "Milk Thistle 200mg,123456789012,,https://brand.com/product,https://img1.jpg|https://img2.jpg"
    ].join("\n");
    downloadText(t, "input_template.csv", "text/csv;charset=utf-8");
  }

  // --- Reset ---
  function resetAll(){
    $("file").value = "";
    $("pasteInput").value = "";
    $("testUrl").value = "";
    $("multiUrls").value = "";
    $("pastePage2").value = "";
    clearTests();
    OUTPUT = [];
    renderOutput([]);
    window.__PARSED_INPUT__ = [];
    $("tab2").disabled = true;
    $("btnNext").disabled = true;
    $("btnDownloadPage1").disabled = true;
    showPage(1);
    renderChecklist();
    refreshDashboard();
  }

  // --- Events ---
  $("tab1").addEventListener("click", ()=>showPage(1));
  $("tab2").addEventListener("click", ()=>{ if(!$("tab2").disabled) showPage(2); });
  $("btnNext").addEventListener("click", ()=>{ if(!$("btnNext").disabled){ $("tab2").disabled=false; showPage(2);} });
  $("btnBack").addEventListener("click", ()=>showPage(1));
  $("btnReset").addEventListener("click", resetAll);

  $("file").addEventListener("change", refreshDashboard);
  $("pasteInput").addEventListener("input", refreshDashboard);

  $("btnDownloadTemplate").addEventListener("click", downloadTemplate);
  $("btnDownloadPage1").addEventListener("click", ()=>{
    const rows = window.__PARSED_INPUT__ || [];
    downloadText(toCSV(rows), "parsed_input.csv", "text/csv;charset=utf-8");
  });

  $("btnTestOne").addEventListener("click", testOne);
  $("btnTestMany").addEventListener("click", testMany);
  $("btnClearTests").addEventListener("click", clearTests);

  $("btnRun").addEventListener("click", runExtraction);
  $("btnDownloadOutCSV").addEventListener("click", ()=> downloadText(toCSV(OUTPUT), "output.csv", "text/csv;charset=utf-8"));
  $("btnDownloadOutTSV").addEventListener("click", ()=> downloadText(toTSV(OUTPUT), "output.tsv", "text/tab-separated-values;charset=utf-8"));

  // init
  renderChecklist();
  resetAll();
</script>
</body>
</html>
