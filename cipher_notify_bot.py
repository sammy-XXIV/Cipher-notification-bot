<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>CIPHER</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&family=Orbitron:wght@700;900&family=DM+Sans:wght@400;500;600&display=swap');

  :root {
    --bg: #020408;
    --bg2: #050c14;
    --bg3: #081219;
    --panel: #050e18;
    --border: #0d1f30;
    --border2: #0f2840;
    --accent: #00e87a;
    --accent2: #00b8e6;
    --accent3: #e8003d;
    --accent4: #e8a800;
    --dim: #1a3a5c;
    --text: #d0e8f8;
    --text2: #4a7a9a;
    --text3: #1e3d55;
    --glow: 0 0 12px #00e87a33;
    --glow2: 0 0 12px #00b8e633;
    --scan: rgba(0,232,122,0.018);
  }

  * { margin:0; padding:0; box-sizing:border-box; -webkit-tap-highlight-color:transparent; }

  html, body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Share Tech Mono', monospace;
    height: 100%;
    width: 100%;
    overflow: hidden;
    position: fixed;
  }

  body::before {
    content:''; position:fixed; inset:0; pointer-events:none; z-index:9999;
    background: repeating-linear-gradient(0deg,transparent,transparent 2px,var(--scan) 2px,var(--scan) 4px);
  }

  /* HEADER */
  .header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 16px; height: 50px;
    border-bottom: 1px solid var(--border);
    background: #030911; flex-shrink: 0;
    position: relative; z-index: 100;
  }

  .header-left { display:flex; align-items:center; gap:10px; }

  .back-btn {
    display: none; align-items: center; gap:5px;
    background: none; border: 1px solid var(--border2);
    color: var(--text2); font-family: 'DM Sans', sans-serif;
    font-size: 11px; font-weight: 500; letter-spacing: 0.5px; padding: 5px 12px;
    cursor: pointer; transition: all 0.2s;
  }
  .back-btn:hover { color: var(--accent); border-color: var(--accent); }
  .back-btn.show { display: flex; }

  .logo { display:flex; align-items:center; gap:10px; }
  .logo-hex {
    width: 26px; height: 26px;
    border: 1px solid var(--accent);
    clip-path: polygon(20% 0%,80% 0%,100% 20%,100% 80%,80% 100%,20% 100%,0% 80%,0% 20%);
    background: #001a0f; display: flex; align-items:center; justify-content:center;
    color: var(--accent); font-size:11px; box-shadow: var(--glow);
  }
  .logo-text {
    font-family: 'Orbitron', sans-serif; font-weight: 900;
    font-size: 16px; letter-spacing: 5px; color: var(--accent); text-shadow: var(--glow);
  }

  .header-right { display:flex; align-items:center; gap:8px; }
  .dot-pill { display:flex; align-items:center; gap:4px; font-size:9px; color:var(--text3); font-family:'DM Sans',sans-serif; letter-spacing:0.5px; }
  .dot { width:4px; height:4px; border-radius:50%; animation:pulse 2s infinite; }
  .dot.green { background:var(--accent); }
  .dot.blue  { background:var(--accent2); }
  @keyframes pulse { 0%,100%{opacity:1}50%{opacity:0.3} }

  /* APP SHELL */
  .app { display:flex; flex-direction:column; height:calc(100% - 52px); overflow:hidden; position:relative; }

  /* PAGES */
  .page {
    position:absolute; inset:0; display:flex; flex-direction:column; overflow:hidden;
    transition: transform 0.3s cubic-bezier(0.4,0,0.2,1), opacity 0.3s ease;
  }
  /* PAGES — see chart section for smooth transitions */

  /* HOME PAGE */
  .home-bar {
    display:flex; align-items:center; gap:10px; padding:10px 14px;
    border-bottom:1px solid var(--border); background:var(--panel); flex-shrink:0;
  }
  .mkt-count { font-size:9px; color:var(--text3); letter-spacing:2px; white-space:nowrap; }
  .mkt-count b { color:var(--accent); font-weight:normal; }

  .search-box {
    flex:1; display:flex; align-items:center;
    background:var(--bg3); border:1px solid var(--border2); padding:0 10px;
    transition:border-color 0.2s;
  }
  .search-box:focus-within { border-color:var(--accent); }
  .search-box span { color:var(--text3); font-size:12px; margin-right:6px; }
  .search-box input {
    flex:1; background:none; border:none; outline:none;
    color:var(--text); font-family:'Share Tech Mono',monospace;
    font-size:11px; padding:8px 0; letter-spacing:1px;
  }
  .search-box input::placeholder { color:var(--text3); }

  .token-list { flex:1; overflow-y:scroll; -webkit-overflow-scrolling:touch; overscroll-behavior:contain; min-height:0; touch-action:pan-y; }
  .token-list::-webkit-scrollbar { display:none; }

  .token-row {
    display:flex; align-items:center; padding:11px 16px;
    border-bottom:1px solid var(--border); cursor:pointer;
    transition:background 0.15s; gap:12px;
  }
  .token-row:active { background:#00e87a06; }

  .t-rank { font-size:9px; color:var(--text3); width:20px; text-align:right; flex-shrink:0; font-family:'DM Sans',sans-serif; }
  .t-icon {
    width:34px; height:34px; border-radius:4px;
    background:var(--bg3); border:1px solid var(--border2);
    display:flex; align-items:center; justify-content:center;
    font-family:'Orbitron',sans-serif; font-size:7px; font-weight:700;
    color:var(--text2); flex-shrink:0; letter-spacing:0.5px;
  }
  .t-info { flex:1; min-width:0; }
  .t-sym { font-family:'Orbitron',sans-serif; font-size:12px; font-weight:700; color:var(--text); letter-spacing:1.5px; }
  .t-name { font-size:9px; color:var(--text3); margin-top:2px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; font-family:'DM Sans',sans-serif; }
  .t-right { display:flex; flex-direction:column; align-items:flex-end; gap:4px; flex-shrink:0; }
  .t-price { font-family:'Rajdhani',sans-serif; font-size:14px; font-weight:600; color:var(--text); }
  .t-chg { font-size:9px; padding:1px 6px; font-family:'DM Sans',sans-serif; font-weight:500; }
  .t-chg.up   { background:#00e87a10; color:var(--accent);  border:1px solid #00e87a25; }
  .t-chg.down { background:#e8003d10; color:var(--accent3); border:1px solid #e8003d25; }
  .t-arrow { color:var(--text3); font-size:14px; flex-shrink:0; opacity:0.4; }

  /* DETAIL PAGE */
  .detail-tabs {
    display:flex; border-bottom:1px solid var(--border);
    background:var(--panel); flex-shrink:0;
  }
  .dtab {
    flex:1; padding:11px; text-align:center; font-size:9px; letter-spacing:2px;
    color:var(--text3); cursor:pointer; border:none; border-bottom:2px solid transparent;
    background:none; font-family:'DM Sans',sans-serif; font-weight:500;
    text-transform:uppercase;
    transition: color 0.28s cubic-bezier(0.32,0.72,0,1),
                border-color 0.28s cubic-bezier(0.32,0.72,0,1),
                background 0.28s cubic-bezier(0.32,0.72,0,1);
  }
  .dtab.active { color:var(--accent); border-bottom-color:var(--accent); background:#00e87a05; }

  .dcontent { display:none; flex:1; flex-direction:column; overflow:hidden; min-height:0; }
  .dcontent.active { display:flex; }

  /* Chart */
  .chart-topbar {
    display:flex; align-items:center; justify-content:space-between;
    padding:6px 10px; border-bottom:1px solid var(--border);
    background:var(--bg2); flex-shrink:0; gap:6px;
  }
  .c-info { display:flex; align-items:center; gap:6px; flex-shrink:0; min-width:0; overflow:hidden; }
  .c-sym { font-family:'Orbitron',sans-serif; font-size:14px; font-weight:900; color:var(--accent); text-shadow:var(--glow); letter-spacing:2px; flex-shrink:0; }
  .c-price { font-family:'Rajdhani',sans-serif; font-size:14px; font-weight:600; color:var(--text); flex-shrink:0; }
  .c-chg { font-size:9px; padding:1px 5px; border-radius:2px; flex-shrink:0; }
  .c-chg.up   { background:#00e87a15; color:var(--accent);  border:1px solid #00e87a30; }
  .c-chg.down { background:#e8003d15; color:var(--accent3); border:1px solid #e8003d30; }

  .tf-row {
    display:flex; align-items:center; gap:3px; flex-shrink:0;
  }
  .tf-btns { display:flex; gap:2px; }
  .tf-btn {
    background:none; border:1px solid var(--border2); color:var(--text3);
    font-family:'Share Tech Mono',monospace; font-size:9px; padding:4px 7px;
    cursor:pointer; letter-spacing:0.5px; flex-shrink:0;
    transition: color 0.25s cubic-bezier(0.25,0.46,0.45,0.94),
                border-color 0.25s cubic-bezier(0.25,0.46,0.45,0.94),
                background 0.25s cubic-bezier(0.25,0.46,0.45,0.94);
  }
  .tf-btn.active { border-color:var(--accent); color:var(--accent); background:#00e87a10; }

  /* Apple-smooth page transitions */
  .page {
    position:absolute; inset:0; display:flex; flex-direction:column; overflow:hidden;
    transition: transform 0.42s cubic-bezier(0.32, 0.72, 0, 1),
                opacity 0.42s cubic-bezier(0.32, 0.72, 0, 1);
    will-change: transform, opacity;
    -webkit-backface-visibility: hidden;
    backface-visibility: hidden;
  }
  .page.hidden-right { transform:translateX(100%); opacity:0; pointer-events:none; }
  .page.hidden-left  { transform:translateX(-20%); opacity:0; pointer-events:none; }
  .page.visible      { transform:translateX(0); opacity:1; pointer-events:all; }

  .chart-area { flex:1; position:relative; overflow:hidden; min-height:180px; }
  #chartCanvas { width:100%; height:100%; display:block; }
  .chart-tags { position:absolute; top:6px; left:8px; display:flex; flex-direction:column; gap:3px; pointer-events:none; }
  .ctag { font-size:7px; padding:1px 5px; border:1px solid; letter-spacing:1px; }
  .ctag.ema { border-color:#00c9ff40; color:var(--accent2); background:#00c9ff08; }
  .ctag.bb  { border-color:#ffbe0040; color:var(--accent4); background:#ffbe0008; }

  .ind-row { height:64px; border-top:1px solid var(--border); background:var(--bg2); display:grid; grid-template-columns:1fr 1fr; flex-shrink:0; }
  .ind-cell { padding:7px 12px; border-right:1px solid var(--border); }
  .ind-cell:last-child { border-right:none; }
  .ind-lbl { font-size:7px; color:var(--text3); letter-spacing:2px; margin-bottom:3px; }
  .ind-val { font-family:'Orbitron',sans-serif; font-size:13px; font-weight:700; }
  .ind-val.bullish { color:var(--accent); text-shadow:var(--glow); }
  .ind-val.bearish { color:var(--accent3); }
  .ind-val.neutral { color:var(--accent4); }
  .ind-bar { height:3px; background:var(--border2); border-radius:2px; margin-top:5px; overflow:hidden; }
  .ind-fill { height:100%; border-radius:2px; transition:width 0.5s ease; }

  /* AI Panel */
  .ai-wrap { flex:1; display:flex; flex-direction:column; overflow:hidden; background:var(--panel); min-height:0; }
  .ai-top { padding:10px 14px; border-bottom:1px solid var(--border); display:flex; align-items:center; justify-content:space-between; flex-shrink:0; }
  .ai-title { font-family:'Orbitron',sans-serif; font-size:10px; letter-spacing:3px; color:var(--accent2); text-shadow:var(--glow2); }
  .ai-badge { font-size:8px; padding:2px 6px; background:#00c9ff15; border:1px solid #00c9ff30; color:var(--accent2); letter-spacing:1px; animation:blink 2s step-end infinite; }
  @keyframes blink { 0%,100%{opacity:1}50%{opacity:0.3} }

  .pw-wrap { padding:10px 14px; border-bottom:1px solid var(--border); flex-shrink:0; }
  .pw-lbl { font-size:8px; color:var(--text3); letter-spacing:1px; margin-bottom:5px; }
  .pw-input {
    width:100%; background:var(--bg3); border:1px solid var(--border2);
    color:var(--text2); font-family:'Share Tech Mono',monospace;
    font-size:14px; padding:9px 12px; outline:none; letter-spacing:3px;
    -webkit-text-security:disc; transition:border-color 0.2s;
  }
  .pw-input:focus { border-color:var(--accent2); }

  .stats-g { display:grid; grid-template-columns:1fr 1fr; gap:1px; background:var(--border); margin:10px 14px; flex-shrink:0; }
  .stat-c { background:var(--bg3); padding:7px 10px; }
  .stat-l { font-size:7px; color:var(--text3); letter-spacing:1px; margin-bottom:2px; }
  .stat-v { font-family:'Rajdhani',sans-serif; font-size:14px; font-weight:600; color:var(--text); }

  .run-btn {
    margin:12px 16px; padding:12px;
    background:#00e87a08;
    border:1px solid var(--accent); color:var(--accent);
    font-family:'DM Sans',sans-serif; font-size:12px; font-weight:600; letter-spacing:3px;
    cursor:pointer; text-align:center; transition:all 0.2s;
    width:calc(100% - 32px); flex-shrink:0; text-transform:uppercase;
  }
  .run-btn:active { background:#00e87a15; box-shadow:var(--glow); }
  .run-btn:disabled { opacity:0.35; cursor:not-allowed; }

  .out-area { flex:1; overflow-y:scroll; -webkit-overflow-scrolling:touch; overscroll-behavior:contain; min-height:0; touch-action:pan-y; }
  .out-area::-webkit-scrollbar { display:none; }

  .out-block { padding:14px 16px; border-bottom:1px solid var(--border); animation:fadeUp 0.3s ease; }
  @keyframes fadeUp { from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)} }
  .out-meta { display:flex; align-items:center; justify-content:space-between; margin-bottom:10px; }
  .out-tag { font-size:8px; padding:2px 7px; background:#00e87a08; border:1px solid #00e87a20; color:var(--accent); letter-spacing:2px; font-family:'DM Sans',sans-serif; font-weight:600; text-transform:uppercase; }
  .out-time { font-size:8px; color:var(--text3); font-family:'DM Sans',sans-serif; }
  .out-txt { font-size:11px; line-height:1.8; color:var(--text2); font-family:'DM Sans',sans-serif; }

  .sig-block { margin-top:12px; padding:12px; background:var(--bg3); border:1px solid var(--border2); }
  .sig-lbl { font-size:8px; letter-spacing:2px; color:var(--text3); margin-bottom:6px; font-family:'DM Sans',sans-serif; text-transform:uppercase; }
  .sig-val { font-family:'Orbitron',sans-serif; font-size:20px; font-weight:700; letter-spacing:3px; }
  .sig-long  { color:var(--accent); text-shadow:var(--glow); }
  .sig-short { color:var(--accent3); }
  .sig-neut  { color:var(--accent4); }
  .conf-bar { margin-top:8px; height:3px; background:var(--border2); overflow:hidden; }
  .conf-fill { height:100%; transition:width 1s ease; }
  .cf-g { background:linear-gradient(90deg,var(--accent),#00e87a50); }
  .cf-r { background:linear-gradient(90deg,var(--accent3),#e8003d50); }
  .cf-y { background:linear-gradient(90deg,var(--accent4),#e8a80050); }
  .conf-lbl { font-size:8px; color:var(--text3); margin-top:4px; letter-spacing:1px; font-family:'DM Sans',sans-serif; }

  .load-block { padding:20px 14px; display:flex; flex-direction:column; gap:12px; }
  .load-top { display:flex; align-items:center; gap:10px; }
  .spinner { width:14px; height:14px; border:1.5px solid var(--border2); border-top-color:var(--accent2); border-radius:50%; animation:spin 0.8s linear infinite; flex-shrink:0; }
  @keyframes spin { to{transform:rotate(360deg)} }
  .load-txt { font-size:10px; color:var(--text3); letter-spacing:1px; }
  .prog-track { width:100%; background:var(--border2); height:3px; border-radius:2px; overflow:hidden; }
  .prog-fill { height:100%; border-radius:2px; transition:width 0.4s ease; background:linear-gradient(90deg,var(--accent),var(--accent2)); box-shadow:0 0 8px #00ff9d80; }
  .prog-lbl { font-size:9px; color:var(--text3); letter-spacing:1px; }

  .empty { padding:40px 20px; text-align:center; color:var(--text3); font-size:10px; letter-spacing:2px; line-height:2.4; }
  .empty-icon { font-size:22px; margin-bottom:12px; opacity:0.25; letter-spacing:4px; }

  .sammy { position:fixed; bottom:10px; right:12px; font-family:'Orbitron',sans-serif; font-size:7px; letter-spacing:3px; color:var(--text3); padding:2px 8px; background:transparent; z-index:50; pointer-events:none; white-space:nowrap; opacity:0.4; }
  .sammy span { color:var(--accent); text-shadow:var(--glow); }

  .matrix { position:fixed; bottom:0; right:0; width:45px; height:80px; pointer-events:none; opacity:0.05; font-size:9px; color:var(--accent); overflow:hidden; z-index:50; }
</style>
</head>
<body>

<header class="header">
  <div class="header-left">
    <button class="back-btn" id="backBtn" onclick="goHome()">← BACK</button>
    <div class="logo">
      <div class="logo-hex">◈</div>
      <div class="logo-text">CIPHER</div>
    </div>
  </div>
  <div class="header-right">
    <div class="dot-pill"><div class="dot green"></div>LIVE</div>
    <div class="dot-pill"><div class="dot blue"></div>AI</div>
    <button onclick="showScannerPage()" id="scanNavBtn" style="background:none;border:1px solid var(--border2);color:var(--text2);font-family:'DM Sans',sans-serif;font-size:10px;font-weight:600;padding:4px 10px;cursor:pointer;letter-spacing:1px;text-transform:uppercase;transition:all 0.2s;" onmouseover="this.style.color='var(--accent)';this.style.borderColor='var(--accent)'" onmouseout="this.style.color='var(--text2)';this.style.borderColor='var(--border2)'">SCAN</button>
    <button onclick="window.location.href='cipher_settings.html'" style="background:none;border:1px solid var(--border2);color:var(--text2);font-size:14px;width:30px;height:30px;cursor:pointer;transition:all 0.2s;display:flex;align-items:center;justify-content:center;" onmouseover="this.style.color='var(--accent2)';this.style.borderColor='var(--accent2)'" onmouseout="this.style.color='var(--text2)';this.style.borderColor='var(--border2)'" title="Settings">⚙</button>
  </div>
</header>

<div class="app">

  <!-- HOME PAGE -->
  <div class="page visible" id="homePage">
    <div class="home-bar">
      <div class="mkt-count">// <b id="mktCount">LOADING...</b></div>
      <button onclick="fetchPrices()" id="refreshPriceBtn" style="background:none;border:1px solid var(--border2);color:var(--accent2);font-family:'Share Tech Mono',monospace;font-size:11px;padding:5px 10px;cursor:pointer;letter-spacing:1px;flex-shrink:0;" title="Refresh prices">REFRESH</button>
      <div class="search-box">
        <span>🔍</span>
        <input type="text" id="searchInput" placeholder="SEARCH..." autocomplete="off" oninput="handleSearch(this.value)">
      </div>
    </div>

    <!-- MEXC TICKER SEARCH -->
    <div style="padding:8px 10px;border-bottom:1px solid var(--border);background:var(--bg2);">
      <div style="font-size:8px;color:var(--text3);letter-spacing:2px;margin-bottom:6px;">// MEXC TICKER SEARCH</div>
      <div style="display:flex;gap:6px;">
        <input type="text" id="mexcTickerInput"
          placeholder="e.g. BONK, PEPE, WIF..."
          autocomplete="off"
          style="flex:1;background:#020408;border:1px solid var(--border2);color:var(--text);font-family:'Share Tech Mono',monospace;font-size:12px;padding:8px 10px;outline:none;letter-spacing:1px;"
          onkeydown="if(event.key==='Enter') fetchMexcTicker()"
        >
        <button onclick="fetchMexcTicker()" id="mexcFetchBtn"
          style="background:#00ff9d15;border:1px solid #00ff9d40;color:var(--accent);font-family:'Share Tech Mono',monospace;font-size:10px;padding:8px 14px;cursor:pointer;letter-spacing:1px;white-space:nowrap;">
          FETCH
        </button>
      </div>
      <div id="mexcFetchStatus" style="font-size:9px;color:var(--text3);margin-top:5px;letter-spacing:1px;display:none;"></div>
    </div>

    <div class="token-list" id="tokenList">
      <div class="empty">
        <div class="empty-icon">◈</div>
        LOADING MARKETS...
      </div>
    </div>
  </div>

  <!-- DETAIL PAGE -->
  <div class="page hidden-right" id="detailPage">
    <div class="detail-tabs">
      <button class="dtab active" onclick="showTab('chart')" id="dtab-chart">CHART</button>
      <button class="dtab" onclick="showTab('ai')" id="dtab-ai">ANALYSIS</button>
      <button class="dtab" onclick="showTab('history')" id="dtab-history">LOG HISTORY</button>
    </div>

    <!-- CHART TAB -->
    <div class="dcontent active" id="dc-chart">
      <div class="chart-topbar">
        <div class="c-info">
          <div class="c-sym" id="cSym">BTC</div>
          <div class="c-price" id="cPrice">$—</div>
          <div class="c-chg up" id="cChg">+0.00%</div>
        </div>
        <div class="tf-row">
          <div class="tf-btns">
            <button class="tf-btn" data-tf="5M">5M</button>
            <button class="tf-btn" data-tf="15M">15M</button>
            <button class="tf-btn active" data-tf="1H">1H</button>
            <button class="tf-btn" data-tf="4H">4H</button>
            <button class="tf-btn" data-tf="1D">1D</button>
            <button class="tf-btn" data-tf="1W">1W</button>
          </div>
          <button onclick="refreshChart()" id="refreshChartBtn" style="background:none;border:1px solid var(--border2);color:var(--text3);font-family:'Share Tech Mono',monospace;font-size:9px;padding:4px 7px;cursor:pointer;transition:all 0.2s;flex-shrink:0;" title="Refresh">↺</button>
        </div>
      </div>
      <div id="chartStatus" style="display:none;padding:4px 12px;font-size:8px;letter-spacing:1px;text-align:center;"></div>
      <div class="chart-area">
        <canvas id="chartCanvas"></canvas>
        <div class="chart-tags">
          <div class="ctag ema">EMA 20/50</div>
          <div class="ctag bb">BOLL BANDS</div>
        </div>
        <!-- Zoom buttons -->
        <div style="position:absolute;bottom:8px;right:8px;display:flex;gap:4px;z-index:5;">
          <button onclick="zoomChart(-1)" style="background:var(--bg3);border:1px solid var(--border2);color:var(--accent);font-family:'Share Tech Mono',monospace;font-size:14px;width:28px;height:28px;cursor:pointer;display:flex;align-items:center;justify-content:center;">−</button>
          <button onclick="zoomChart(1)" style="background:var(--bg3);border:1px solid var(--border2);color:var(--accent);font-family:'Share Tech Mono',monospace;font-size:14px;width:28px;height:28px;cursor:pointer;display:flex;align-items:center;justify-content:center;">+</button>
        </div>
        <!-- Candle tooltip -->
        <div id="candleTooltip" style="display:none;position:absolute;top:8px;right:8px;background:#020408dd;border:1px solid var(--border2);padding:8px 10px;font-size:9px;color:var(--text2);letter-spacing:1px;line-height:1.8;pointer-events:none;z-index:5;min-width:110px;"></div>
      </div>
      <div class="ind-row">
        <div class="ind-cell">
          <div class="ind-lbl">// RSI (14)</div>
          <div class="ind-val neutral" id="rsiVal">—</div>
          <div class="ind-bar"><div class="ind-fill" id="rsiFill" style="width:0%;background:var(--accent4)"></div></div>
        </div>
        <div class="ind-cell">
          <div class="ind-lbl">// MACD</div>
          <div class="ind-val bullish" id="macdVal">—</div>
          <div class="ind-bar"><div class="ind-fill" id="macdFill" style="width:50%;background:var(--accent)"></div></div>
        </div>
      </div>
    </div>

    <!-- AI TAB -->
    <div class="dcontent" id="dc-ai">
      <div class="ai-wrap">
        <div class="ai-top">
          <div class="ai-title">AI AGENT</div>
          <div style="display:flex;align-items:center;gap:8px;">
            <div class="ai-badge">CLAUDE</div>
            <!-- MODE TOGGLE -->
            <div id="modeToggle" onclick="toggleMode()" style="display:flex;align-items:center;gap:0;cursor:pointer;border:1px solid var(--border2);overflow:hidden;font-family:'DM Sans',sans-serif;font-size:9px;font-weight:700;letter-spacing:1px;">
              <div id="modeToggleSafe" style="padding:3px 8px;background:var(--accent);color:#020408;transition:all 0.2s;">SAFE</div>
              <div id="modeToggleDegen" style="padding:3px 8px;background:transparent;color:var(--text3);transition:all 0.2s;">DEGEN</div>
            </div>
          </div>
        </div>
        <div class="pw-wrap">
          <div class="pw-lbl">// ACCESS PASSWORD</div>
          <input type="text" class="pw-input" id="pwInput" placeholder="••••••••"
            autocomplete="off" autocorrect="off" spellcheck="false"
            onkeydown="if(event.key==='Enter')runAnalysis()">
        </div>
        <!-- TOKEN GRADE PANEL -->
        <div id="gradePanel" style="display:none;margin:10px 14px 0;border:1px solid var(--border2);background:var(--bg3);">
          <div style="display:flex;align-items:center;justify-content:space-between;padding:8px 12px;border-bottom:1px solid var(--border);">
            <div style="font-size:8px;color:var(--text3);letter-spacing:2px;">CIPHER GRADE</div>
            <div id="gradeLetter" style="font-family:'Orbitron',sans-serif;font-size:20px;font-weight:900;">—</div>
          </div>
          <div id="gradeRows" style="padding:8px 12px;display:flex;flex-direction:column;gap:5px;"></div>
        </div>
        <div class="stats-g" id="statsGrid" style="display:none">
          <div class="stat-c"><div class="stat-l">24H HIGH</div><div class="stat-v" id="s24h">—</div></div>
          <div class="stat-c"><div class="stat-l">24H LOW</div><div class="stat-v" id="sLow">—</div></div>
          <div class="stat-c"><div class="stat-l">SUPPORT</div><div class="stat-v" id="sSup">—</div></div>
          <div class="stat-c"><div class="stat-l">RESISTANCE</div><div class="stat-v" id="sRes">—</div></div>
        </div>
        <button class="run-btn" id="runBtn" onclick="runAnalysis()">RUN ANALYSIS</button>
        <button class="run-btn" id="scalp-btn" onclick="runScalpMode()" style="margin-top:0;margin-bottom:0;border-color:var(--accent4);color:var(--accent4);background:#e8a80008;letter-spacing:3px;">⚡ SCALP — 5M</button>
        <button class="run-btn" id="manip-btn" onclick="runManipMode()" style="margin-top:4px;margin-bottom:10px;border-color:#a855f7;color:#a855f7;background:#a855f708;letter-spacing:3px;">⚡ MANIPULATION — 5M</button>
        <div class="out-area" id="outArea">
          <div class="empty">
            <div class="empty-icon">◈ ◈ ◈</div>
            RUN ANALYSIS TO BEGIN
          </div>
        </div>
      </div>
    </div>

    <!-- HISTORY TAB -->
    <div class="dcontent" id="dc-history">
      <div style="display:flex;align-items:center;justify-content:space-between;padding:10px 14px;border-bottom:1px solid var(--border);flex-shrink:0;">
        <div style="font-size:9px;letter-spacing:2px;color:var(--text3);">// ANALYSIS HISTORY</div>
        <button onclick="clearHistory()" style="background:none;border:1px solid #ff3c6e40;color:var(--accent3);font-family:'Share Tech Mono',monospace;font-size:8px;padding:4px 8px;cursor:pointer;letter-spacing:1px;">CLEAR ALL</button>
      </div>
      <div id="historyList" style="overflow-y:auto;flex:1;">
        <div class="empty" id="historyEmpty">
          <div class="empty-icon">LOG</div>
          No analysis history yet.<br>Run analysis to start tracking.
        </div>
      </div>
    </div>
  </div>

  <!-- SCANNER PAGE -->
  <div class="page hidden-right" id="scannerPage">
    <!-- Scan button + status -->
    <div style="padding:10px 14px;border-bottom:1px solid var(--border);background:var(--bg3);flex-shrink:0;display:flex;align-items:center;gap:10px;">
      <button onclick="runMexcScan()" id="scanBtn" style="background:var(--accent);color:#020408;border:none;font-family:'Orbitron',monospace;font-size:10px;font-weight:700;padding:8px 16px;cursor:pointer;letter-spacing:2px;flex-shrink:0;">SCAN NOW</button>
      <div id="scanStatus" style="font-size:9px;color:var(--text3);letter-spacing:1px;">Tap SCAN NOW to find top opportunities on MEXC</div>
    </div>

    <!-- Results — sectioned -->
    <div id="scanResults" style="overflow-y:auto;flex:1;">
      <div class="empty" id="scanEmpty">
        <div class="empty-icon">⚡</div>
        Tap SCAN NOW to find<br>top trading opportunities
      </div>
    </div>
  </div>

</div>

<div class="sammy">made by <span>SAMMY</span></div>
<div class="matrix" id="matrix"></div>

<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script>
const SERVER = 'https://back-end-1-928p.onrender.com';
const SUPABASE_URL = 'https://zttdlnavawepvhbtldgq.supabase.co';
const SUPABASE_KEY = 'sb_publishable_PiRo_l11XVyrqnhmn5NldQ_Ju0ItrBV';
const NOTIFY_BOT_TOKEN = '8685607507:AAHSQ-8hz9ivTNaNmYTKy8Gl-l-ZQaNO9YQ';
const NOTIFY_BOT_URL   = 'https://cipher-notification-bot.onrender.com';
const { createClient } = supabase;
const sb = createClient(SUPABASE_URL, SUPABASE_KEY);

let TOKENS = [];
let activeToken = null;
let activeTimeframe = '1H';
let chartData = [];
let searchQuery = '';
let zoomLevel = 1;
let degenMode = false;
let currentUser = null;
let userProfile = null;
let analysisHistory = JSON.parse(localStorage.getItem('cipherHistory') || '[]');

// ============================================================
// AUTH — check login on load
// ============================================================
async function initAuth() {
  const { data: { session } } = await sb.auth.getSession();
  if (!session) {
    window.location.href = 'cipher_auth.html';
    return false;
  }
  currentUser = session.user;
  // Load profile (telegram chat_id + prefs)
  const { data } = await sb.from('profiles').select('*').eq('user_id', currentUser.id).single();
  userProfile = data || null;
  return true;
}

// Send notification to user's personal Telegram
async function sendPersonalNotification(text, type='general') {
  if (!userProfile?.telegram_verified || !userProfile?.telegram_chat_id) return;
  const prefs = userProfile?.notification_prefs || {};
  const prefMap = { analysis:'analysis', entry:'entry', dead:'dead', expired:'expired', feargreed:'feargreed' };
  const key = prefMap[type];
  if (key && prefs[key] === false) return; // muted
  try {
    await fetch(`https://api.telegram.org/bot${NOTIFY_BOT_TOKEN}/sendMessage`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ chat_id: userProfile.telegram_chat_id, text, parse_mode: 'HTML' })
    });
  } catch(e) { console.error('Notify error:', e); }
}

// NAVIGATION
function goHome() {
  document.getElementById('homePage').className = 'page visible';
  document.getElementById('detailPage').className = 'page hidden-right';
  document.getElementById('scannerPage').className = 'page hidden-right';
  document.getElementById('backBtn').classList.remove('show');
  const gp = document.getElementById('gradePanel');
  if (gp) gp.style.display = 'none';
  const btn = document.getElementById('scanNavBtn');
  if (btn) { btn.textContent = 'SCAN'; btn.onclick = showScannerPage; }
  sessionStorage.removeItem('cipher_active_token');
}

async function goDetail(id) {
  activeToken = TOKENS.find(t => t.id === id);
  if (!activeToken) return;
  zoomLevel = 1;
  tooltipCandle = null;
  document.getElementById('homePage').className = 'page hidden-left';
  document.getElementById('detailPage').className = 'page visible';
  document.getElementById('backBtn').classList.add('show');
  updateChartHeader();
  showTab('chart');
  document.getElementById('statsGrid').style.display = 'none';

  // Disable analysis buttons until chart is ready
  const runBtn   = document.getElementById('runBtn');
  const scalpBtn = document.getElementById('scalp-btn');
  const manipBtn = document.getElementById('manip-btn');
  if (runBtn)   { runBtn.disabled = true;   runBtn.textContent = 'LOADING CHART...'; }
  if (scalpBtn) { scalpBtn.disabled = true; scalpBtn.textContent = 'LOADING...'; }
  if (manipBtn) { manipBtn.disabled = true; manipBtn.textContent = 'LOADING...'; }

  document.getElementById('outArea').innerHTML = `
    <div class="empty">
      <div class="empty-icon">◈</div>
      LOADING CHART DATA...<br>
      <span style="font-size:9px;color:var(--text3);">Please wait before running analysis</span>
    </div>`;

  await generateChartData();
  drawChart();
  updateIndicators();
  gradeToken();
  savePageState();
  const isSimulated = !chartData.length || chartData[0]?.vol === 0;
  if (runBtn) {
    runBtn.disabled = false;
    runBtn.textContent = isSimulated ? 'RUN ANALYSIS (simulated data)' : 'RUN ANALYSIS';
  }
  if (scalpBtn) {
    scalpBtn.disabled = false;
    scalpBtn.textContent = '⚡ SCALP — 5M';
  }
  if (manipBtn) {
    manipBtn.disabled = false;
    manipBtn.textContent = '⚡ MANIPULATION — 5M';
  }

  document.getElementById('outArea').innerHTML = `
    <div class="empty">
      <div class="empty-icon">◈</div>
      READY — ${activeToken.symbol}<br>
      <span style="font-size:9px;color:var(--text3);">${chartData.length} candles loaded</span>
    </div>`;
}

function showChartStatus(msg, color='var(--text3)') {
  const el = document.getElementById('chartStatus');
  if (!el) return;
  if (!msg) { el.style.display='none'; return; }
  el.style.display='block';
  el.style.color=color;
  el.style.background=color==='var(--accent3)'?'#ff3c6e10':'#00c9ff08';
  el.textContent=msg;
}

async function refreshChart() {
  const btn = document.getElementById('refreshChartBtn');
  if (btn) { btn.textContent='⟳'; btn.style.opacity='0.5'; btn.disabled=true; }
  await generateChartData();
  drawChart();
  updateIndicators();
  if (btn) { btn.textContent='REFRESH'; btn.style.opacity='1'; btn.disabled=false; }
}

function showTab(tab) {
  document.querySelectorAll('.dcontent').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.dtab').forEach(t => t.classList.remove('active'));
  document.getElementById('dtab-' + tab).classList.add('active');
  document.getElementById('dc-' + tab).classList.add('active');
  if (tab === 'chart' && chartData.length) setTimeout(drawChart, 50);
  if (tab === 'history') renderHistory();
}

function zoomChart(dir) {
  zoomLevel = Math.max(0.2, Math.min(1, zoomLevel - dir * 0.15));
  drawChart();
}

// CANDLE TOOLTIP on tap/click
function handleChartTap(e) {
  if (!chartData.length) return;
  const canvas = document.getElementById('chartCanvas');
  const rect = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  const clientX = e.touches ? e.touches[0].clientX : e.clientX;
  const x = (clientX - rect.left);
  const W = rect.width;

  const visibleCount = Math.floor(chartData.length * zoomLevel);
  const startIdx = chartData.length - visibleCount;
  const cw = (W - 40) / visibleCount;
  const idx = Math.floor((x - 20) / cw) + startIdx;

  if (idx < 0 || idx >= chartData.length) {
    document.getElementById('candleTooltip').style.display = 'none';
    return;
  }

  const c = chartData[idx];
  const isUp = c.close >= c.open;
  const tooltip = document.getElementById('candleTooltip');
  tooltip.style.display = 'block';
  tooltip.style.borderColor = isUp ? '#00ff9d40' : '#ff3c6e40';
  tooltip.innerHTML = `
    <div style="color:${isUp?'var(--accent)':'var(--accent3)'};font-family:'Orbitron',sans-serif;font-size:8px;margin-bottom:4px;">${isUp?'▲ BULLISH':'▼ BEARISH'}</div>
    <div>O: <span style="color:var(--text)">${fmt(c.open)}</span></div>
    <div>H: <span style="color:var(--accent)">${fmt(c.high)}</span></div>
    <div>L: <span style="color:var(--accent3)">${fmt(c.low)}</span></div>
    <div>C: <span style="color:var(--text)">${fmt(c.close)}</span></div>`;

  // Hide tooltip after 3 seconds
  clearTimeout(tooltip._timer);
  tooltip._timer = setTimeout(() => { tooltip.style.display = 'none'; }, 3000);
}

// FETCH PRICES — from all exchanges simultaneously
async function fetchPrices() {
  const btn = document.getElementById('refreshPriceBtn');
  if (btn) { btn.textContent='⟳'; btn.style.opacity='0.5'; btn.disabled=true; }
  // Show waking up message after 3 seconds
  const wakeTimer = setTimeout(() => {
    document.getElementById('mktCount').textContent = 'WAKING SERVER...';
  }, 3000);
  try {
    document.getElementById('mktCount').textContent = 'LOADING...';

    // Run ALL fetches simultaneously — server proxy first for prices
    const fetchWithTimeout = (url, opts={}, ms=8000) => {
      const ctrl = new AbortController();
      const timer = setTimeout(()=>ctrl.abort(), ms);
      return fetch(url, {...opts, signal:ctrl.signal}).finally(()=>clearTimeout(timer));
    };

    const [cgRes, tickerRes, binanceRes, bybitRes, okxRes, hlRes, mexcRes] = await Promise.allSettled([
      // CoinGecko — metadata
      fetchWithTimeout('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&price_change_percentage=24h').then(r=>r.json()),
      // Server ticker proxy (no CORS)
      fetchWithTimeout(`${SERVER}/tickers`, {}, 12000).then(r=>r.json()),
      // Binance direct
      fetchWithTimeout('https://api.binance.com/api/v3/ticker/24hr').then(r=>r.json()),
      // Bybit direct
      fetchWithTimeout('https://api.bybit.com/v5/market/tickers?category=spot').then(r=>r.json()),
      // OKX direct
      fetchWithTimeout('https://www.okx.com/api/v5/market/tickers?instType=SPOT').then(r=>r.json()),
      // Hyperliquid direct
      fetchWithTimeout('https://api.hyperliquid.xyz/info', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'spotMetaAndAssetCtxs'})}).then(r=>r.json()),
      // MEXC direct
      fetchWithTimeout('https://www.mexc.com/open/api/v2/market/ticker').then(r=>r.json()),
    ]);

    // Parse CoinGecko
    let cgCoins = [];
    if (cgRes.status === 'fulfilled' && Array.isArray(cgRes.value)) {
      cgCoins = cgRes.value.filter(c => c && c.id);
    }

    // Parse server ticker proxy (most reliable — no CORS)
    let serverPrices = {};
    if (tickerRes.status === 'fulfilled' && typeof tickerRes.value === 'object') {
      serverPrices = tickerRes.value;
    }

    // Parse Binance direct
    let binancePrices = {};
    if (binanceRes.status === 'fulfilled' && Array.isArray(binanceRes.value)) {
      binanceRes.value.forEach(t => {
        if (t.symbol?.endsWith('USDT')) {
          const sym = t.symbol.replace('USDT','');
          binancePrices[sym] = { price: parseFloat(t.lastPrice), change: parseFloat(t.priceChangePercent), high: parseFloat(t.highPrice), low: parseFloat(t.lowPrice) };
        }
      });
    }

    // Parse Bybit direct
    let bybitPrices = {};
    if (bybitRes.status === 'fulfilled') {
      (bybitRes.value?.result?.list || []).forEach(t => {
        if (t.symbol?.endsWith('USDT')) {
          const sym = t.symbol.replace('USDT','');
          bybitPrices[sym] = { price: parseFloat(t.lastPrice), change: parseFloat(t.price24hPcnt)*100, high: parseFloat(t.highPrice24h), low: parseFloat(t.lowPrice24h) };
        }
      });
    }

    // Parse OKX direct
    let okxPrices = {};
    if (okxRes.status === 'fulfilled') {
      (okxRes.value?.data || []).forEach(t => {
        if (t.instId?.endsWith('-USDT')) {
          const sym = t.instId.replace('-USDT','');
          okxPrices[sym] = { price: parseFloat(t.last), change: ((parseFloat(t.last)-parseFloat(t.open24h))/parseFloat(t.open24h))*100, high: parseFloat(t.high24h), low: parseFloat(t.low24h) };
        }
      });
    }

    // Parse Hyperliquid direct
    let hlPrices = {};
    if (hlRes.status === 'fulfilled') {
      const tokens = hlRes.value?.[0]?.tokens || [];
      const ctxs = hlRes.value?.[1] || [];
      tokens.forEach((t,i) => {
        const ctx = ctxs[i];
        if (ctx?.midPrice) {
          const sym = t.name.toUpperCase();
          hlPrices[sym] = { price: parseFloat(ctx.midPrice), change: 0, high: parseFloat(ctx.midPrice)*1.01, low: parseFloat(ctx.midPrice)*0.99 };
        }
      });
    }

    // Parse MEXC direct
    let mexcPrices = {};
    if (mexcRes.status === 'fulfilled') {
      (mexcRes.value?.data || []).forEach(t => {
        if (t.symbol?.endsWith('_USDT')) {
          const sym = t.symbol.replace('_USDT','');
          mexcPrices[sym] = { price: parseFloat(t.last), change: parseFloat(t.priceChangePercent)||0, high: parseFloat(t.high), low: parseFloat(t.low) };
        }
      });
    }

    // Build token list — server prices take priority
    if (cgCoins.length) {
      TOKENS = cgCoins.map(c => {
        const sym = c.symbol.toUpperCase();
        // Server proxy prices take priority, then direct exchange prices
        let price, change, high, low, source;
        if (serverPrices[sym] && serverPrices[sym].price > 0) {
          const sp = serverPrices[sym];
          price = sp.price; change = sp.change; high = sp.high; low = sp.low;
          source = `server (${sp.sources} exchanges)`;
        } else {
          const prices = [binancePrices[sym], bybitPrices[sym], okxPrices[sym], hlPrices[sym], mexcPrices[sym]].filter(p => p && p.price > 0);
          if (prices.length > 0) {
            price  = prices.reduce((s,p)=>s+p.price,0)/prices.length;
            change = prices.filter(p=>p.change!==0).reduce((s,p,_,a)=>s+p.change/a.length,0) || c.price_change_percentage_24h || 0;
            high   = Math.max(...prices.map(p=>p.high));
            low    = Math.min(...prices.map(p=>p.low));
            source = `${prices.length} exchange${prices.length>1?'s':''}`;
          } else {
            price=c.current_price||0; change=c.price_change_percentage_24h||0;
            high=c.high_24h||0; low=c.low_24h||0; source='coingecko';
          }
        }
        return { id:c.id, symbol:sym, name:c.name, price, change, high, low, rank:c.market_cap_rank||999, priceSource:source };
      });
    } else if (Object.keys(serverPrices).length) {
      // No CoinGecko — build from server prices
      TOKENS = Object.entries(serverPrices).slice(0,100).map(([sym,p],i) => ({
        id:sym.toLowerCase(), symbol:sym, name:sym,
        price:p.price, change:p.change, high:p.high, low:p.low,
        rank:i+1, priceSource:'server',
      }));
    } else if (Object.keys(binancePrices).length) {
      TOKENS = Object.entries(binancePrices).map(([sym,p],i) => ({
        id:sym.toLowerCase(), symbol:sym, name:sym,
        price:p.price, change:p.change, high:p.high, low:p.low,
        rank:i+1, priceSource:'binance',
      })).sort((a,b)=>b.price-a.price).slice(0,100);
    } else {
      throw new Error('All price sources failed — check your connection');
    }

    const hasServer = Object.keys(serverPrices).length > 0;
    const activeSources = [
      hasServer ? 'SERVER' : null,
      Object.keys(binancePrices).length ? 'BINANCE' : null,
      Object.keys(bybitPrices).length ? 'BYBIT' : null,
      Object.keys(okxPrices).length ? 'OKX' : null,
    ].filter(Boolean);
    const sourceSummary = hasServer ? 'SERVER PROXY' : activeSources.length >= 2 ? `${activeSources.length}-EXCHANGE AVG` : activeSources.join('+') || 'COINGECKO';

    document.getElementById('mktCount').textContent = `${TOKENS.length} MARKETS · ${sourceSummary}`;
    clearTimeout(wakeTimer);
    if (btn) { btn.textContent='REFRESH'; btn.style.opacity='1'; btn.disabled=false; }
    if (activeToken) {
      const updated = TOKENS.find(t => t.id === activeToken.id);
      if (updated) { activeToken = updated; updateChartHeader(); }
    }
    renderList();
  } catch(e) {
    clearTimeout(wakeTimer);
    if (btn) { btn.textContent='REFRESH'; btn.style.opacity='1'; btn.disabled=false; }
    document.getElementById('mktCount').textContent = 'ERROR';
    document.getElementById('tokenList').innerHTML = `
      <div class="empty">
        <div class="empty-icon">⚠</div>
        <div style="color:var(--accent3);margin-bottom:8px;">LOAD FAILED</div>
        <div style="font-size:9px;color:var(--text3);margin-bottom:14px;">${e.message}</div>
        <span onclick="fetchPrices()" style="color:var(--accent);cursor:pointer;border:1px solid var(--accent);padding:6px 14px;display:inline-block;">REFRESH RETRY NOW</span>
      </div>`;
  }
}

// RENDER LIST
function renderList() {
  const list = document.getElementById('tokenList');
  if (!TOKENS.length) return;
  const q = searchQuery.toUpperCase();
  const items = q
    ? TOKENS.filter(t => t.symbol.includes(q) || t.name.toUpperCase().includes(q))
        .sort((a,b) => {
          const aS = a.symbol.startsWith(q) || a.name.toUpperCase().startsWith(q);
          const bS = b.symbol.startsWith(q) || b.name.toUpperCase().startsWith(q);
          return aS === bS ? a.symbol.localeCompare(b.symbol) : aS ? -1 : 1;
        }).slice(0, 100)
    : TOKENS;

  if (!items.length) {
    list.innerHTML = `<div class="empty"><div class="empty-icon">◈</div>NO RESULTS FOR "${q}"</div>`;
    return;
  }

  list.innerHTML = items.map(t => `
    <div class="token-row" onclick="goDetail('${t.id}')">
      <div class="t-rank">#${t.rank}</div>
      <div class="t-icon">${t.symbol.slice(0,3)}</div>
      <div class="t-info">
        <div class="t-sym">${t.symbol}</div>
        <div class="t-name">${t.name}</div>
      </div>
      <div class="t-right">
        <div class="t-price">${fmt(t.price)}</div>
        <div class="t-chg ${t.change >= 0 ? 'up':'down'}">${t.change >= 0?'+':''}${t.change.toFixed(2)}%</div>
      </div>
      <div class="t-arrow"></div>
    </div>`).join('');
}

function handleSearch(v) { searchQuery = v; renderList(); }

// ============================================================
// MEXC TICKER SEARCH — fetch any token directly from MEXC
// ============================================================
async function fetchMexcTicker() {
  const input = document.getElementById('mexcTickerInput');
  const btn   = document.getElementById('mexcFetchBtn');

  let ticker = input.value.trim().toUpperCase().replace('$','').replace('USDT','').replace('_USDT','');
  if (!ticker) { showMexcStatus('Enter a ticker symbol', 'var(--accent3)'); return; }

  btn.textContent = '...'; btn.disabled = true;
  showMexcStatus(`Fetching ${ticker}...`, 'var(--text2)');

  try {
    const timeout = (ms) => new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), ms));

    // Fetch ticker only first — fast, 6s timeout
    let price = 0, change = 0, high = 0, low = 0, src = '';
    try {
      const d = await Promise.race([
        fetch(`${SERVER}/ticker?symbol=${ticker}`).then(r => r.json()),
        timeout(6000)
      ]);
      if (d && d.price > 0) {
        price = d.price; change = d.change; high = d.high; low = d.low; src = d.source;
      }
    } catch(e) {}

    // Fallback — check scan data
    if (!price) {
      const scanToken = scanData.find(t => t.sym === ticker);
      if (scanToken) {
        price = scanToken.price; change = scanToken.change;
        high = scanToken.high; low = scanToken.low; src = 'MEXC';
      }
    }

    if (!price) {
      showMexcStatus(`❌ ${ticker} not found`, 'var(--accent3)');
      btn.textContent = 'FETCH'; btn.disabled = false;
      return;
    }

    // Build token and open immediately — don't wait for candles
    const token = {
      id: ticker.toLowerCase(), symbol: ticker, name: ticker,
      price, change, high, low, rank: 999, priceSource: src || 'MEXC',
    };
    const exists = TOKENS.findIndex(t => t.symbol === ticker);
    if (exists >= 0) TOKENS[exists] = token; else TOKENS.unshift(token);

    renderList();
    showMexcStatus(`✓ ${ticker} — ${fmt(price)} (${change >= 0?'+':''}${change.toFixed(2)}%)`, 'var(--accent)');
    input.value = '';
    btn.textContent = 'FETCH'; btn.disabled = false;

    // Open chart — candles load inside goDetail
    await goDetail(token.id);

  } catch(e) {
    showMexcStatus(`❌ Error: ${e.message}`, 'var(--accent3)');
    btn.textContent = 'FETCH'; btn.disabled = false;
  }
}

function showMexcStatus(msg, color='var(--text3)') {
  const el = document.getElementById('mexcFetchStatus');
  if (!el) return;
  el.textContent = msg;
  el.style.color = color;
  el.style.display = 'block';
  setTimeout(() => { el.style.display = 'none'; }, 5000);
}

// ============================================================
// ANALYSIS HISTORY
// ============================================================
function saveToHistory(a, token, timeframe) {
  // Fallback for missing stop/target using ATR estimate
  const entryPrice = parseFloat(a.entry?.toString().replace(/[^0-9.]/g,'')) || token.price;
  const atrEst = entryPrice * 0.015; // 1.5% estimate if ATR unavailable
  const isBuy = a.signal === 'LONG';
  const stop   = a.stop   || (isBuy ? (entryPrice - atrEst).toFixed(6) : (entryPrice + atrEst).toFixed(6));
  const target = a.target || (isBuy ? (entryPrice + atrEst*2).toFixed(6) : (entryPrice - atrEst*2).toFixed(6));

  const entry = {
    id: Date.now(),
    symbol: token.symbol,
    name: token.name,
    timeframe,
    signal: a.signal,
    confidence: a.confidence,
    entry: a.entry || entryPrice,
    target,
    stop,
    rr: a.rr_ratio || '1:2',
    bias: a.bias || '',
    reasoning: a.reasoning || '',
    price: token.price,
    timestamp: new Date().toISOString(),
    status: 'active',
  };
  analysisHistory.unshift(entry);
  if (analysisHistory.length > 50) analysisHistory = analysisHistory.slice(0, 50);
  localStorage.setItem('cipherHistory', JSON.stringify(analysisHistory));
  renderHistory();
}

function showHistoryPage() {}

// ============================================================
// TOKEN GRADING SYSTEM
// ============================================================
function gradeToken() {
  if (!activeToken || !chartData.length) return;

  const price   = activeToken.price || 0;
  const change  = activeToken.change || 0;
  const high24  = activeToken.high || price;
  const low24   = activeToken.low  || price;
  const vol24   = activeToken.vol  || 0;

  const closes  = chartData.map(c => c.close);
  const highs   = chartData.map(c => c.high);
  const lows    = chartData.map(c => c.low);
  const vols    = chartData.map(c => c.vol);
  const n       = closes.length;
  if (n < 10) return;

  const rangePct  = low24 > 0 ? ((high24 - low24) / low24) * 100 : 0;
  const avgVol    = vols.slice(-20).reduce((a,b)=>a+b,0) / Math.min(20,n);
  const lastVol   = vols[n-1];

  // ATR
  let atr = 0;
  for (let i = Math.max(1,n-14); i < n; i++) {
    atr += Math.max(highs[i]-lows[i], Math.abs(highs[i]-closes[i-1]), Math.abs(lows[i]-closes[i-1]));
  }
  atr /= Math.min(14, n-1);
  const atrPct = price > 0 ? (atr / price) * 100 : 0;

  // EMA trend
  const emaCalc = (d, p) => { const k=2/(p+1); let e=d[0]; for(let i=1;i<d.length;i++) e=d[i]*k+e*(1-k); return e; };
  const ema20 = emaCalc(closes, 20);
  const ema50 = emaCalc(closes.slice(-60), 50);
  const emaBullish = price > ema20 && ema20 > ema50;
  const emaBearish = price < ema20 && ema20 < ema50;

  // RSI — proper Wilder smoothing
  let rsi = 50;
  if (n >= 15) {
    let avgGain = 0, avgLoss = 0;
    for (let i = 1; i <= 14; i++) {
      const d = closes[i] - closes[i-1];
      if (d > 0) avgGain += d; else avgLoss -= d;
    }
    avgGain /= 14; avgLoss /= 14;
    for (let i = 15; i < n; i++) {
      const d = closes[i] - closes[i-1];
      avgGain = (avgGain * 13 + (d > 0 ? d : 0)) / 14;
      avgLoss = (avgLoss * 13 + (d < 0 ? -d : 0)) / 14;
    }
    rsi = avgLoss === 0 ? 100 : Math.round(100 - (100 / (1 + avgGain / avgLoss)));
    rsi = Math.max(0, Math.min(100, rsi));
  }

  // ── SCORE EACH DIMENSION (0-10) ──
  const scores = {};

  // 1. LIQUIDITY — price range + volume
  let liqScore = 5;
  if (price > 1)      liqScore += 2;
  if (price > 10)     liqScore += 1;
  if (price < 0.001)  liqScore -= 3;
  if (price < 0.0001) liqScore -= 2;
  if (lastVol > avgVol * 1.5) liqScore += 1;
  if (lastVol < avgVol * 0.3) liqScore -= 2;
  scores.liquidity = Math.max(0, Math.min(10, liqScore));

  // 2. VOLATILITY — lower range = more predictable = higher score
  let volScore = 8;
  if (rangePct > 100) volScore = 0;
  else if (rangePct > 50) volScore = 2;
  else if (rangePct > 30) volScore = 4;
  else if (rangePct > 15) volScore = 6;
  else if (rangePct > 8)  volScore = 8;
  else volScore = 10;
  if (atrPct > 15) volScore = Math.min(volScore, 1);
  if (atrPct > 10) volScore = Math.min(volScore, 3);
  scores.volatility = volScore;

  // 3. TREND STRENGTH — clear trend = higher score
  let trendScore = 5;
  if (emaBullish || emaBearish) trendScore += 3;
  if (Math.abs(change) > 5 && Math.abs(change) < 30) trendScore += 2;
  if (Math.abs(change) > 50) trendScore -= 3;
  scores.trend = Math.max(0, Math.min(10, trendScore));

  // 4. VOLUME QUALITY
  let volQScore = 5;
  if (lastVol > avgVol * 2)   volQScore = 9;
  else if (lastVol > avgVol)  volQScore = 7;
  else if (lastVol < avgVol * 0.5) volQScore = 3;
  scores.volume = volQScore;

  // 5. MOMENTUM — RSI in healthy range
  let momScore = 5;
  if (rsi >= 40 && rsi <= 60) momScore = 6;
  if (rsi >= 50 && rsi <= 70) momScore = 8; // bullish but not overbought
  if (rsi >= 30 && rsi <= 45) momScore = 7; // oversold bounce potential
  if (rsi > 80 || rsi < 20)   momScore = 3; // extreme
  scores.momentum = momScore;

  // ── OVERALL SCORE ──
  const weights = { liquidity:0.25, volatility:0.30, trend:0.20, volume:0.15, momentum:0.10 };
  const overall = Object.entries(weights).reduce((sum,[k,w]) => sum + scores[k]*w, 0);

  // ── GRADE ──
  let grade, gradeColor;
  if (overall >= 8.5)      { grade = 'A+'; gradeColor = '#00e87a'; }
  else if (overall >= 7.5) { grade = 'A';  gradeColor = '#00e87a'; }
  else if (overall >= 6.5) { grade = 'B+'; gradeColor = '#00b8e6'; }
  else if (overall >= 5.5) { grade = 'B';  gradeColor = '#00b8e6'; }
  else if (overall >= 4.5) { grade = 'C+'; gradeColor = '#e8a800'; }
  else if (overall >= 3.5) { grade = 'C';  gradeColor = '#e8a800'; }
  else if (overall >= 2.5) { grade = 'D';  gradeColor = '#e8003d'; }
  else                     { grade = 'F';  gradeColor = '#e8003d'; }

  // ── VERDICT ──
  const verdicts = {
    'A+': 'IDEAL SETUP — High quality token, strong signals',
    'A':  'GOOD TOKEN — Clean setup, tradeable with normal size',
    'B+': 'ABOVE AVERAGE — Solid setup with minor cautions',
    'B':  'TRADEABLE — Some risk factors, reduce size slightly',
    'C+': 'CAUTION — Notable risk, use smaller position',
    'C':  'HIGH RISK — Significant volatility, max 3% size',
    'D':  'DANGEROUS — Very high risk, consider skipping',
    'F':  'DO NOT TRADE — Extreme risk, likely manipulation',
  };

  // ── RENDER ──
  const panel = document.getElementById('gradePanel');
  const letter = document.getElementById('gradeLetter');
  const rows = document.getElementById('gradeRows');
  if (!panel || !letter || !rows) return;

  letter.textContent = grade;
  letter.style.color = gradeColor;

  const dims = [
    { label: 'LIQUIDITY',  score: scores.liquidity,  icon: '💧' },
    { label: 'VOLATILITY', score: scores.volatility, icon: '⚡' },
    { label: 'TREND',      score: scores.trend,       icon: '📈' },
    { label: 'VOLUME',     score: scores.volume,      icon: '📊' },
    { label: 'MOMENTUM',   score: scores.momentum,    icon: '🔥' },
  ];

  rows.innerHTML = dims.map(d => {
    const barColor = d.score >= 7 ? 'var(--accent)' : d.score >= 5 ? 'var(--accent4)' : 'var(--accent3)';
    return `
      <div style="display:flex;align-items:center;gap:8px;">
        <div style="font-size:8px;color:var(--text3);letter-spacing:1px;width:70px;flex-shrink:0;">${d.label}</div>
        <div style="flex:1;background:var(--border2);height:4px;border-radius:2px;overflow:hidden;">
          <div style="width:${d.score*10}%;height:100%;background:${barColor};border-radius:2px;transition:width 0.6s cubic-bezier(0.32,0.72,0,1);"></div>
        </div>
        <div style="font-size:9px;color:${barColor};width:20px;text-align:right;font-family:'Orbitron',sans-serif;">${d.score}</div>
      </div>`;
  }).join('') + `
    <div style="margin-top:6px;padding-top:6px;border-top:1px solid var(--border);font-size:9px;color:${gradeColor};font-family:'DM Sans',sans-serif;">${verdicts[grade]}</div>
  `;

  panel.style.display = 'block';
}

function toggleMode() {
  degenMode = !degenMode;
  const safe  = document.getElementById('modeToggleSafe');
  const degen = document.getElementById('modeToggleDegen');
  const runBtn = document.getElementById('runBtn');
  const scalpBtn = document.getElementById('scalp-btn');

  if (degenMode) {
    safe.style.background  = 'transparent';
    safe.style.color       = 'var(--text3)';
    degen.style.background = 'var(--accent3)';
    degen.style.color      = '#fff';
    if (runBtn)   { runBtn.style.borderColor = 'var(--accent3)'; runBtn.style.color = 'var(--accent3)'; runBtn.style.background = '#e8003d08'; }
    if (scalpBtn) { scalpBtn.style.borderColor = 'var(--accent3)'; }
    showChartStatus('DEGEN MODE — High risk signals enabled', 'var(--accent3)');
    setTimeout(() => showChartStatus(''), 3000);
  } else {
    safe.style.background  = 'var(--accent)';
    safe.style.color       = '#020408';
    degen.style.background = 'transparent';
    degen.style.color      = 'var(--text3)';
    if (runBtn)   { runBtn.style.borderColor = 'var(--accent)'; runBtn.style.color = 'var(--accent)'; runBtn.style.background = '#00e87a08'; }
    if (scalpBtn) { scalpBtn.style.borderColor = 'var(--accent4)'; }
    showChartStatus('SAFE MODE — Conservative signals enabled', 'var(--accent)');
    setTimeout(() => showChartStatus(''), 3000);
  }
}

// ============================================================
// MEXC SCANNER — Sectioned by method
// ============================================================
let scanData = [];

function showScannerPage() {
  document.getElementById('homePage').className = 'page hidden-left';
  document.getElementById('detailPage').className = 'page hidden-right';
  document.getElementById('scannerPage').className = 'page visible';
  document.getElementById('backBtn').classList.add('show');
  document.getElementById('backBtn').onclick = goHome;
  const btn = document.getElementById('scanNavBtn');
  if (btn) { btn.textContent = 'CLOSE'; btn.onclick = goHome; }
}

const SECTORS = {
  'Layer 1':  ['BTC','ETH','SOL','AVAX','ADA','DOT','ATOM','NEAR','FTM','ONE','ALGO','EGLD','HBAR','SUI','APT','SEI','INJ','TIA','DYMENSION'],
  'Layer 2':  ['MATIC','ARB','OP','IMX','LRC','METIS','BOBA','SKL','STRK','MANTA','BLAST'],
  'DeFi':     ['UNI','AAVE','COMP','MKR','SNX','CRV','BAL','SUSHI','1INCH','GMX','DYDX','PENDLE','JUP','RAY','ORCA'],
  'Meme':     ['DOGE','SHIB','PEPE','BONK','WIF','FLOKI','BABYDOGE','MEME','BRETT','POPCAT','MOG'],
  'AI':       ['FET','AGIX','OCEAN','RLC','NMR','GRT','RNDR','TAO','WLD','ARKM','AIXBT'],
  'Gaming':   ['AXS','SAND','MANA','ENJ','GALA','ILV','MAGIC','BEAM','RON','PIXEL'],
  'Exchange': ['BNB','OKB','CRO','KCS','HT','MX'],
  'RWA':      ['ONDO','CFG','RIO','POLYX','CPOOL'],
};
const STABLES = ['USDT','USDC','BUSD','DAI','TUSD','USDP','FRAX','FDUSD','PYUSD','USDD'];

async function runMexcScan() {
  const btn = document.getElementById('scanBtn');
  const status = document.getElementById('scanStatus');
  const empty = document.getElementById('scanEmpty');
  const results = document.getElementById('scanResults');

  btn.textContent = 'SCANNING...'; btn.disabled = true;
  status.textContent = 'Fetching MEXC markets...';
  status.style.color = 'var(--accent2)';
  results.innerHTML = '';
  empty.style.display = 'none';

  try {
    // Fetch ALL MEXC futures tickers directly via server proxy
    status.textContent = 'Fetching all MEXC futures...';
    const r = await fetch(`${SERVER}/mexc-scan`);
    const allTickers = await r.json();
    if (!allTickers || !Object.keys(allTickers).length) throw new Error('No data from server');

    status.textContent = `Processing ${Object.keys(allTickers).length} tokens...`;

    const tokens = [];
    for (const [sym, d] of Object.entries(allTickers)) {
      if (!d.price || d.price <= 0) continue;
      if (STABLES.includes(sym)) continue;
      if (d.price < 0.0000001) continue;

      const rangePercent = d.high && d.low ? ((d.high - d.low) / d.low) * 100 : 0;
      const sector = getTokenSector(sym);

      tokens.push({
        sym, price: d.price,
        change: d.change || 0,
        high: d.high || d.price,
        low: d.low || d.price,
        rangePercent,
        sources: d.sources || 1,
        sector,
      });
    }

    // ── METHOD 1: Volume Spikes (high range = unusual activity)
    const volumeSpikes = [...tokens]
      .filter(t => t.rangePercent > 8)
      .sort((a,b) => b.rangePercent - a.rangePercent)
      .slice(0, 10);

    // ── METHOD 2: Momentum — biggest movers up
    const topGainers = [...tokens]
      .filter(t => t.change > 3)
      .sort((a,b) => b.change - a.change)
      .slice(0, 10);

    // ── METHOD 3: Potential reversals — biggest losers (oversold bounce)
    const potentialReversals = [...tokens]
      .filter(t => t.change < -8)
      .sort((a,b) => a.change - b.change)
      .slice(0, 10);

    // ── METHOD 4: BTC Laggards — tokens that haven't moved yet
    // BTC's 24H change as benchmark
    const btcChange = tokens.find(t => t.sym === 'BTC')?.change || 0;
    const btcLaggards = [...tokens]
      .filter(t => btcChange > 2 && t.change < btcChange * 0.3 && t.change > -2)
      .sort((a,b) => a.change - b.change)
      .slice(0, 10);

    // ── METHOD 5: Sector leaders — top performer per sector
    const sectorLeaders = [];
    for (const [sector, syms] of Object.entries(SECTORS)) {
      const sectorTokens = tokens.filter(t => syms.includes(t.sym)).sort((a,b) => b.change - a.change);
      if (sectorTokens.length) sectorLeaders.push({ ...sectorTokens[0], sectorLabel: sector });
    }
    sectorLeaders.sort((a,b) => b.change - a.change);

    // ── METHOD 6: Near 24H High (breakout candidates)
    const breakouts = [...tokens]
      .filter(t => t.high > 0 && (t.price / t.high) > 0.92 && t.change > 2)
      .sort((a,b) => (b.price/b.high) - (a.price/a.high))
      .slice(0, 10);

    // ── METHOD 7: Near 24H Low (bounce candidates)
    const bounceCandidates = [...tokens]
      .filter(t => t.low > 0 && (t.price / t.low) < 1.05 && t.change < -5)
      .sort((a,b) => (a.price/a.low) - (b.price/b.low))
      .slice(0, 10);

    scanData = tokens;
    status.textContent = `Scan complete — ${tokens.length} tokens analysed`;
    status.style.color = 'var(--accent)';

    // Render all sections
    results.innerHTML = [
      renderScanSection('VOLUME SPIKES', 'Unusual activity — 3x+ normal range', volumeSpikes, '#00c9ff'),
      renderScanSection('TOP GAINERS', 'Strong momentum — potential continuation', topGainers, '#00ff9d'),
      renderScanSection('REVERSAL WATCH', 'Oversold — potential bounce incoming', potentialReversals, '#ff6b6b'),
      btcLaggards.length ? renderScanSection('BTC LAGGARDS', `BTC up ${btcChange.toFixed(1)}% but these haven't moved yet`, btcLaggards, '#fbbf24') : '',
      renderScanSection('BREAKOUT CANDIDATES', 'Price near 24H high — potential breakout', breakouts, '#a78bfa'),
      renderScanSection('BOUNCE CANDIDATES', 'Price near 24H low — potential reversal', bounceCandidates, '#f97316'),
      renderScanSection('SECTOR LEADERS', 'Top performer in each sector', sectorLeaders, '#60a5fa'),
    ].join('');

  } catch(e) {
    status.textContent = `❌ Scan failed: ${e.message}`;
    status.style.color = 'var(--accent3)';
    empty.style.display = 'block';
  }

  btn.textContent = 'SCAN NOW'; btn.disabled = false;
}

function getTokenSector(sym) {
  for (const [sector, syms] of Object.entries(SECTORS)) {
    if (syms.includes(sym)) return sector;
  }
  return 'Other';
}

function renderScanSection(title, subtitle, tokens, color) {
  if (!tokens.length) return '';
  const rows = tokens.map(t => {
    const changeColor = t.change >= 0 ? 'var(--accent)' : 'var(--accent3)';
    const changeSign  = t.change >= 0 ? '+' : '';
    const sectorLabel = t.sectorLabel || t.sector || '';
    return `
      <div onclick="loadScanToken('${t.sym}')" style="padding:10px 14px;border-bottom:1px solid var(--border);cursor:pointer;display:flex;align-items:center;gap:10px;" onmouseover="this.style.background='#ffffff08'" onmouseout="this.style.background='transparent'">
        <div style="flex:1;min-width:0;">
          <div style="display:flex;align-items:center;gap:6px;margin-bottom:2px;">
            <span style="font-family:'Orbitron',sans-serif;font-size:13px;color:var(--text);font-weight:700;">${t.sym}</span>
            ${sectorLabel ? `<span style="font-size:7px;padding:1px 5px;border:1px solid ${color}40;color:${color};letter-spacing:1px;">${sectorLabel}</span>` : ''}
          </div>
          <div style="font-size:10px;color:var(--text2);">${fmt(t.price)}</div>
        </div>
        <div style="text-align:right;flex-shrink:0;">
          <div style="font-size:13px;font-weight:700;color:${changeColor};">${changeSign}${t.change.toFixed(2)}%</div>
          <div style="font-size:8px;color:var(--text3);">Range ${t.rangePercent.toFixed(1)}%</div>
        </div>
        <div style="font-size:12px;color:var(--text3);"></div>
      </div>
    `;
  }).join('');

  return `
    <div style="border-left:3px solid ${color};margin:8px 0 0 0;">
      <div style="padding:10px 14px;background:${color}10;border-bottom:1px solid ${color}20;">
        <div style="font-size:11px;color:${color};letter-spacing:2px;font-weight:700;margin-bottom:2px;">${title}</div>
        <div style="font-size:8px;color:var(--text3);letter-spacing:1px;">${subtitle}</div>
      </div>
      ${rows}
    </div>
  `;
}

async function loadScanToken(sym) {
  // Check if already in token list
  const existing = TOKENS.find(t => t.symbol === sym);
  if (existing) { goHome(); await goDetail(existing.id); return; }

  // Try fetching from server ticker endpoint
  try {
    const r = await fetch(`${SERVER}/ticker?symbol=${sym}`);
    const d = await r.json();
    if (d.price && d.price > 0) {
      const token = { id: sym.toLowerCase(), symbol: sym, name: sym, price: d.price, change: d.change || 0, high: d.high || d.price, low: d.low || d.price, rank: 999, priceSource: d.source || 'MEXC' };
      TOKENS.unshift(token);
      goHome();
      await goDetail(token.id);
      return;
    }
  } catch(e) { console.error('loadScanToken ticker error:', e); }

  // Fallback — use scan data if available
  const scanToken = scanData.find(t => t.sym === sym);
  if (scanToken) {
    const token = { id: sym.toLowerCase(), symbol: sym, name: sym, price: scanToken.price, change: scanToken.change, high: scanToken.high, low: scanToken.low, rank: 999, priceSource: 'MEXC' };
    TOKENS.unshift(token);
    goHome();
    await goDetail(token.id);
    return;
  }

  alert(`❌ Could not load ${sym} — try searching it in the MEXC ticker search box`);
}

function openHistory() {
  // If on detail page — just switch to history tab
  const detailPage = document.getElementById('detailPage');
  if (detailPage && detailPage.className.includes('visible')) {
    showTab('history');
    return;
  }
  // If on home page — go to first token's detail and show history tab
  if (TOKENS.length) {
    goDetail(TOKENS[0].id).then(() => showTab('history'));
  }
}

function renderHistoryInContainer(listId, emptyId) {
  const list = document.getElementById(listId);
  const empty = document.getElementById(emptyId);
  if (!list) return;

  if (!analysisHistory.length) {
    list.innerHTML = '';
    if (empty) empty.style.display = 'block';
    return;
  }
  if (empty) empty.style.display = 'none';

  list.innerHTML = analysisHistory.map(h => {
    const emoji = h.signal === 'LONG' ? '▲' : h.signal === 'SHORT' ? '▼' : '—';
    const statusColor = h.status === 'dead' ? 'var(--accent3)' : h.status === 'expired' ? 'var(--accent4)' : 'var(--accent)';
    const statusLabel = h.status === 'dead' ? 'DEAD' : h.status === 'expired' ? 'EXPIRED' : 'ACTIVE';
    const date = new Date(h.timestamp);
    const dateStr = date.toLocaleDateString('en-US', {month:'short', day:'numeric'}) + ' ' +
      date.toLocaleTimeString('en-US', {hour:'2-digit', minute:'2-digit'});

    return `
      <div id="${listId}-item-${h.id}" style="padding:12px 14px;border-bottom:1px solid var(--border);animation:fadeUp 0.3s ease;">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">
          <div style="display:flex;align-items:center;gap:8px;">
            <span style="font-size:13px;">${emoji}</span>
            <span style="font-family:'Orbitron',sans-serif;font-size:13px;color:var(--text);font-weight:700;">${h.symbol}</span>
            <span style="font-size:8px;color:var(--text3);letter-spacing:1px;">${h.timeframe}</span>
          </div>
          <div style="display:flex;align-items:center;gap:8px;">
            <span style="font-size:8px;color:${statusColor};letter-spacing:1px;">${statusLabel}</span>
            <button onclick="deleteHistoryItem(${h.id})" style="background:none;border:1px solid #ff3c6e30;color:#ff3c6e80;font-size:9px;padding:2px 6px;cursor:pointer;font-family:'Share Tech Mono',monospace;">✕</button>
          </div>
        </div>
        <div style="display:flex;gap:16px;margin-bottom:5px;">
          <div style="font-size:9px;color:var(--text2);">Signal: <b style="color:${h.signal==='LONG'?'var(--accent)':h.signal==='SHORT'?'var(--accent3)':'var(--accent4)'}">${h.signal}</b> (${h.confidence}%)</div>
          <div style="font-size:9px;color:var(--text2);">Price: <b>${fmt(h.price)}</b></div>
        </div>
        <div style="display:flex;gap:12px;margin-bottom:5px;">
          <div style="font-size:8px;color:var(--text3);">🎯 ${h.entry || '—'}</div>
          <div style="font-size:8px;color:var(--accent);">✅ ${h.target || '—'}</div>
          <div style="font-size:8px;color:var(--accent3);">🛑 ${h.stop || '—'}</div>
          <div style="font-size:8px;color:var(--text3);">⚖️ ${h.rr || '1:2'}</div>
        </div>
        ${h.bias ? `<div style="font-size:8px;color:var(--text3);font-style:italic;letter-spacing:1px;">${h.bias}</div>` : ''}
        <div style="font-size:7px;color:var(--text3);margin-top:4px;letter-spacing:1px;">${dateStr}</div>
      </div>
    `;
  }).join('');
}

function renderHistory() {
  renderHistoryInContainer('historyList', 'historyEmpty');
}

function deleteHistoryItem(id) {
  analysisHistory = analysisHistory.filter(h => h.id !== id);
  localStorage.setItem('cipherHistory', JSON.stringify(analysisHistory));
  document.querySelectorAll(`[id$="-item-${id}"]`).forEach(el => el.remove());
  if (!analysisHistory.length) {
    const empty = document.getElementById('historyEmpty');
    if (empty) empty.style.display = 'block';
  }
}

function clearHistory(fromPage = false) {
  if (!confirm('Clear all analysis history?')) return;
  analysisHistory = [];
  localStorage.setItem('cipherHistory', JSON.stringify([]));
  renderHistory();
}

function updateHistoryStatus(status) {
  if (!analysisHistory.length) return;
  analysisHistory[0].status = status;
  localStorage.setItem('cipherHistory', JSON.stringify(analysisHistory));
  renderHistory();
}

function fmt(p) {
  if (!p) return '$—';
  if (p >= 1000) return '$' + p.toLocaleString('en-US', {maximumFractionDigits:0});
  if (p >= 1) return '$' + p.toFixed(2);
  if (p >= 0.01) return '$' + p.toFixed(4);
  return '$' + p.toFixed(6);
}

// CHART
function updateChartHeader() {
  if (!activeToken) return;
  document.getElementById('cSym').textContent = activeToken.symbol;
  document.getElementById('cPrice').textContent = fmt(activeToken.price);
  const el = document.getElementById('cChg');
  el.textContent = (activeToken.change >= 0 ? '+':'') + activeToken.change.toFixed(2) + '%';
  el.className = 'c-chg ' + (activeToken.change >= 0 ? 'up':'down');
  // Refresh live price from server in background
  refreshLivePrice();
}

async function refreshLivePrice() {
  if (!activeToken) return;
  try {
    const r = await fetch(`${SERVER}/ticker?symbol=${activeToken.symbol}`, {signal: AbortSignal.timeout(6000)});
    if (!r.ok) return;
    const d = await r.json();
    if (!d.price || d.price <= 0) return;
    // Update token with fresh data
    activeToken.price  = d.price;
    activeToken.change = d.change || activeToken.change;
    activeToken.high   = d.high   || activeToken.high;
    activeToken.low    = d.low    || activeToken.low;
    // Update UI
    document.getElementById('cPrice').textContent = fmt(d.price);
    const el = document.getElementById('cChg');
    const chg = d.change || activeToken.change;
    el.textContent = (chg >= 0 ? '+':'') + chg.toFixed(2) + '%';
    el.className = 'c-chg ' + (chg >= 0 ? 'up':'down');
    // Update 24H stats if visible
    if (d.high) document.getElementById('s24h').textContent = fmt(d.high);
    if (d.low)  document.getElementById('sLow').textContent = fmt(d.low);
  } catch(e) {}
}

// REAL CHART DATA FROM BINANCE
async function generateChartData() {
  chartData = [];
  if (!activeToken) return;

  // Clear canvas immediately
  const cv = document.getElementById('chartCanvas');
  if (cv) {
    const ctx = cv.getContext('2d');
    ctx.clearRect(0, 0, cv.width, cv.height);
  }

  const intervalMap = {'5M':'5m','15M':'15m','1H':'1h','4H':'4h','1D':'1d','1W':'1w'};
  const interval = intervalMap[activeTimeframe] || '1h';
  const limits = {'5M':100,'15M':80,'1H':80,'4H':90,'1D':60,'1W':52};
  const limit = limits[activeTimeframe] || 80;
  const symbol = activeToken.symbol + 'USDT';

  // Remove any existing loader first
  const existing = document.getElementById('chartLoader');
  if (existing) existing.remove();

  // Show loading overlay on chart
  const chartArea = document.querySelector('.chart-area');
  const overlay = document.createElement('div');
  overlay.id = 'chartLoader';
  overlay.style.cssText = `position:absolute;inset:0;background:#020408ee;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;z-index:10;`;
  overlay.innerHTML = `
    <div style="font-family:'Orbitron',sans-serif;font-size:10px;color:var(--accent2);letter-spacing:3px;" id="chartLoadMsg">FETCHING CANDLES...</div>
    <div style="width:160px;background:var(--border2);height:3px;border-radius:2px;overflow:hidden;">
      <div id="chartLoadBar" style="height:100%;width:0%;background:linear-gradient(90deg,var(--accent),var(--accent2));border-radius:2px;transition:width 0.3s ease;box-shadow:0 0 8px #00ff9d80;"></div>
    </div>
    <div id="chartLoadPct" style="font-size:9px;color:var(--text3);letter-spacing:1px;">0%</div>`;
  chartArea.appendChild(overlay);

  const setLoad = (pct, msg) => {
    const bar = document.getElementById('chartLoadBar');
    const lbl = document.getElementById('chartLoadPct');
    const txt = document.getElementById('chartLoadMsg');
    if (bar) bar.style.width = pct + '%';
    if (lbl) lbl.textContent = pct + '%';
    if (txt && msg) txt.textContent = msg;
  };

  let fakeTimer = null;
  try {
    setLoad(10, 'CONNECTING TO BINANCE...');
    let fakePct = 10;
    fakeTimer = setInterval(() => {
      if (fakePct < 75) { fakePct += 3; setLoad(fakePct); }
    }, 200);

    let raw = null;
    let dataFrom = '';

    // Helper: fetch with timeout
    const fetchT = (url, opts={}, ms=8000) => {
      const ctrl = new AbortController();
      const timer = setTimeout(() => ctrl.abort(), ms);
      return fetch(url, {...opts, signal: ctrl.signal}).finally(() => clearTimeout(timer));
    };

    // Fetch candles via Render server proxy (no CORS issues)
    // Try up to 2 times in case server is waking up
    for (let attempt = 1; attempt <= 2; attempt++) {
      try {
        setLoad(20, attempt === 1 ? 'FETCHING FROM SERVER...' : 'RETRYING SERVER...');
        const res = await fetchT(`${SERVER}/candles?symbol=${activeToken.symbol}&interval=${interval}&limit=${limit}`, {}, 10000);
        if (res.ok) {
          const data = await res.json();
          if (data.candles && data.candles.length) {
            raw = data.candles.map(c => [null, c.o, c.h, c.l, c.c, c.v]);
            dataFrom = data.source;
            if (data.warning) {
              showChartStatus(`⚠ ${data.warning} — treat analysis with caution`, 'var(--accent4)');
            }
            break;
          }
        }
      } catch(e) {
        if (attempt === 1) await new Promise(r => setTimeout(r, 1000)); // wait 1s before retry
      }
    }

    // Fallback: try direct exchanges (works on some networks)
    if (!raw) {
      try {
        setLoad(45, 'TRYING BINANCE DIRECT...');
        const res = await fetchT(`https://api.binance.com/api/v3/klines?symbol=${symbol}&interval=${interval}&limit=${limit}`);
        if (res.ok) {
          const data = await res.json();
          if (Array.isArray(data) && data.length) { raw = data; dataFrom = 'BINANCE'; }
        }
      } catch(e) {}
    }

    if (!raw) {
      try {
        setLoad(65, 'TRYING BYBIT DIRECT...');
        const bybitInterval = {'5m':'5','15m':'15','1h':'60','4h':'240','1d':'D','1w':'W'}[interval]||'60';
        const res = await fetchT(`https://api.bybit.com/v5/market/kline?category=spot&symbol=${symbol}&interval=${bybitInterval}&limit=${limit}`);
        if (res.ok) {
          const data = await res.json();
          const list = data?.result?.list;
          if (Array.isArray(list) && list.length) {
            raw = list.reverse().map(c => [null,c[1],c[2],c[3],c[4],c[5]]);
            dataFrom = 'BYBIT';
          }
        }
      } catch(e) {}
    }

    clearInterval(fakeTimer);

    if (raw) {
      setLoad(90, 'RENDERING...');
      chartData = raw.map(c => ({
        open:  parseFloat(c[1]),
        high:  parseFloat(c[2]),
        low:   parseFloat(c[3]),
        close: parseFloat(c[4]),
        vol:   parseFloat(c[5]),
      }));
      setLoad(100, 'DONE!');
      showChartStatus(` ${dataFrom} LIVE DATA`, 'var(--accent2)');
      setTimeout(()=>showChartStatus(''), 3000);
    } else {
      throw new Error('All sources failed');
    }
  } catch(e) {
    if (fakeTimer) clearInterval(fakeTimer);
    setLoad(100, 'USING SIMULATED DATA');
    showChartStatus('ALL SOURCES UNAVAILABLE — Showing simulated data', 'var(--accent3)');
    const base = activeToken.price || 1, vol = base * 0.012;
    let price = base * (0.92 + Math.random() * 0.06);
    for (let i = 0; i < limit; i++) {
      const open = price, close = open + (Math.random()-0.485)*vol;
      const wick = vol*(0.3+Math.random()*0.7);
      chartData.push({open,close,high:Math.max(open,close)+wick*0.5,low:Math.min(open,close)-wick*0.5,vol:0.3+Math.random()*0.7});
      price = close;
    }
    const scale = activeToken.price / chartData[chartData.length-1].close;
    chartData.forEach(c => {c.open*=scale;c.close*=scale;c.high*=scale;c.low*=scale;});
  } finally {
    const el = document.getElementById('chartLoader');
    if (el) el.remove();
  }
}

function ema(data, p) {
  const k=2/(p+1); let prev=data[0];
  return data.map(v => { const e=v*k+prev*(1-k); prev=e; return e; });
}

function drawChart() {
  const cv = document.getElementById('chartCanvas');
  if (!cv || !chartData.length) return;
  const dpr = window.devicePixelRatio||1;
  const r = cv.parentElement.getBoundingClientRect();
  if (!r.width||!r.height) return;
  cv.width = r.width*dpr; cv.height = r.height*dpr;
  const ctx = cv.getContext('2d'); ctx.scale(dpr,dpr);
  const W=r.width, H=r.height;
  ctx.clearRect(0,0,W,H);

  ctx.strokeStyle='#0d2035'; ctx.lineWidth=0.5;
  for(let i=1;i<6;i++){const y=H*0.06+(H*0.68)*(i/6);ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();}
  for(let i=0;i<8;i++){const x=W*i/8;ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke();}

  const visibleCount = Math.floor(chartData.length * zoomLevel);
  const startIdx = chartData.length - visibleCount;
  const visible = chartData.slice(startIdx);
  const n = visible.length;
  const closes = visible.map(c=>c.close);
  const allP = visible.flatMap(c=>[c.high,c.low]);
  const minP=Math.min(...allP),maxP=Math.max(...allP),rng=maxP-minP||1;
  const cTop=H*0.04,cH=H*0.63,vTop=H*0.71,vH=H*0.17;
  const cw=(W-40)/n;
  const py=p=>cTop+cH-((p-minP)/rng)*cH;
  const cx=i=>20+i*cw+cw*0.5;

  for(const side of['upper','lower']){
    ctx.strokeStyle='#ffbe0012';ctx.lineWidth=1;ctx.beginPath();
    for(let i=20;i<n;i++){
      const sl=closes.slice(i-20,i),mean=sl.reduce((a,b)=>a+b)/20;
      const std=Math.sqrt(sl.reduce((a,b)=>a+(b-mean)**2,0)/20);
      const v=side==='upper'?mean+2*std:mean-2*std;
      i===20?ctx.moveTo(cx(i),py(v)):ctx.lineTo(cx(i),py(v));
    }
    ctx.stroke();
  }

  [[ema(closes,20),'rgba(0,201,255,0.5)'],[ema(closes,50),'rgba(255,190,0,0.4)']].forEach(([e,color])=>{
    ctx.strokeStyle=color;ctx.lineWidth=1.2;ctx.beginPath();
    e.forEach((v,i)=>i===0?ctx.moveTo(cx(i),py(v)):ctx.lineTo(cx(i),py(v)));ctx.stroke();
  });

  visible.forEach((c,i)=>{
    const up=c.close>=c.open,color=up?'#00ff9d':'#ff3c6e',x=cx(i);
    const oY=py(c.open),cY=py(c.close),w=Math.max(cw*0.7,2);
    ctx.strokeStyle=color;ctx.lineWidth=1;
    ctx.beginPath();ctx.moveTo(x,py(c.high));ctx.lineTo(x,py(c.low));ctx.stroke();
    ctx.fillStyle=up?'#00ff9d60':'#ff3c6e60';
    const bt=Math.min(oY,cY),bh=Math.abs(oY-cY)||1;
    ctx.fillRect(x-w/2,bt,w,bh);ctx.strokeRect(x-w/2,bt,w,bh);
  });

  const mv=Math.max(...visible.map(c=>c.vol));
  visible.forEach((c,i)=>{
    ctx.fillStyle=c.close>=c.open?'rgba(0,255,157,0.35)':'rgba(255,60,110,0.35)';
    const bh=(c.vol/mv)*vH;ctx.fillRect(cx(i)-cw*0.35,vTop+vH-bh,cw*0.7,bh);
  });

  const lp=closes[n-1],ly=py(lp);
  ctx.setLineDash([4,4]);ctx.strokeStyle='rgba(0,255,157,0.35)';ctx.lineWidth=1;
  ctx.beginPath();ctx.moveTo(0,ly);ctx.lineTo(W,ly);ctx.stroke();ctx.setLineDash([]);
  ctx.fillStyle='#001a10';ctx.strokeStyle='#00ff9d';ctx.lineWidth=1;
  ctx.fillRect(W-66,ly-8,61,16);ctx.strokeRect(W-66,ly-8,61,16);
  ctx.fillStyle='#00ff9d';ctx.font='9px "Share Tech Mono"';
  ctx.textAlign='right';ctx.fillText(fmt(lp),W-7,ly+4);ctx.textAlign='left';
}

function updateIndicators() {
  if (!chartData.length||!activeToken) return;
  const closes=chartData.map(c=>c.close);
  const highs=chartData.map(c=>c.high);
  const lows=chartData.map(c=>c.low);
  const vols=chartData.map(c=>c.vol);
  const n=closes.length;

  // RSI (14) — proper Wilder smoothing
  let rsi = 50;
  if (n >= 15) {
    let avgG = 0, avgL = 0;
    for (let i = 1; i <= 14; i++) { const d=closes[i]-closes[i-1]; d>0?avgG+=d:avgL-=d; }
    avgG/=14; avgL/=14;
    for (let i = 15; i < n; i++) {
      const d=closes[i]-closes[i-1];
      avgG=(avgG*13+(d>0?d:0))/14;
      avgL=(avgL*13+(d<0?-d:0))/14;
    }
    rsi = avgL===0 ? 100 : Math.round(100-(100/(1+avgG/avgL)));
    rsi = Math.max(0, Math.min(100, rsi));
  }
  const rEl=document.getElementById('rsiVal');
  rEl.textContent=rsi;rEl.className='ind-val '+(rsi>70?'bearish':rsi<30?'bullish':'neutral');
  const rf=document.getElementById('rsiFill');
  rf.style.width=rsi+'%';rf.style.background=rsi>70?'var(--accent3)':rsi<30?'var(--accent)':'var(--accent4)';

  // MACD
  const m12=ema(closes,12),m26=ema(closes,26),ml=m12.map((v,i)=>v-m26[i]),sig=ema(ml,9);
  const macd=ml[n-1]-sig[n-1];
  const mEl=document.getElementById('macdVal');
  // Dynamic decimals based on magnitude
  // MACD — show as % of price so it's meaningful for all token prices
  const macdPct = (macd / closes[n-1]) * 100;
  const macdDisplay = (macdPct >= 0 ? '+' : '') + macdPct.toFixed(2) + '%';
  mEl.textContent = macdDisplay;
  mEl.className='ind-val '+(macd>0?'bullish':'bearish');
  const mf=document.getElementById('macdFill');
  mf.style.width=Math.min(100, Math.abs(macdPct) * 20)+'%';
  mf.style.background=macd>0?'var(--accent)':'var(--accent3)';

  // Stochastic RSI
  const rsiArr=[];
  for(let i=14;i<n;i++){
    let gg=0,ll=0;
    for(let j=i-13;j<=i;j++){const d=closes[j]-closes[j-1];d>0?gg+=d:ll-=d;}
    rsiArr.push(100-(100/(1+(ll===0?100:gg/ll))));
  }
  const rsiMin=Math.min(...rsiArr.slice(-14));
  const rsiMax=Math.max(...rsiArr.slice(-14));
  const stochRsi=rsiMax===rsiMin?50:Math.round(((rsiArr[rsiArr.length-1]-rsiMin)/(rsiMax-rsiMin))*100);

  // ATR (14) — Average True Range
  let atrSum=0;
  for(let i=n-14;i<n;i++){
    const tr=Math.max(highs[i]-lows[i], Math.abs(highs[i]-closes[i-1]), Math.abs(lows[i]-closes[i-1]));
    atrSum+=tr;
  }
  const atr=atrSum/14;

  // VWAP
  let cumTPV=0,cumVol=0;
  for(let i=0;i<n;i++){
    const tp=(highs[i]+lows[i]+closes[i])/3;
    cumTPV+=tp*vols[i];
    cumVol+=vols[i];
  }
  const vwap=cumTPV/cumVol;

  // ADX (14) — Trend Strength
  let adx = 0;
  try {
    const trueRanges=[], plusDM=[], minusDM=[];
    for(let i=1;i<n;i++){
      const tr=Math.max(highs[i]-lows[i],Math.abs(highs[i]-closes[i-1]),Math.abs(lows[i]-closes[i-1]));
      const upMove=highs[i]-highs[i-1];
      const downMove=lows[i-1]-lows[i];
      trueRanges.push(tr);
      plusDM.push(upMove>downMove&&upMove>0?upMove:0);
      minusDM.push(downMove>upMove&&downMove>0?downMove:0);
    }
    const period=14;
    let atr14=trueRanges.slice(0,period).reduce((a,b)=>a+b,0);
    let pDM14=plusDM.slice(0,period).reduce((a,b)=>a+b,0);
    let mDM14=minusDM.slice(0,period).reduce((a,b)=>a+b,0);
    const dxArr=[];
    for(let i=period;i<trueRanges.length;i++){
      atr14=atr14-atr14/period+trueRanges[i];
      pDM14=pDM14-pDM14/period+plusDM[i];
      mDM14=mDM14-mDM14/period+minusDM[i];
      const pDI=100*pDM14/atr14;
      const mDI=100*mDM14/atr14;
      const dx=100*Math.abs(pDI-mDI)/(pDI+mDI||1);
      dxArr.push(dx);
    }
    adx=Math.round(dxArr.slice(-14).reduce((a,b)=>a+b,0)/Math.min(14,dxArr.length));
  } catch(e){}

  // Volume Confirmation
  const avgVol = vols.slice(-20).reduce((a,b)=>a+b,0)/20;
  const lastVol = vols[n-1];
  const volumeStrength = lastVol>avgVol*1.5?'HIGH (strong confirmation)':lastVol>avgVol?'ABOVE AVERAGE':lastVol<avgVol*0.5?'LOW (weak signal)':'AVERAGE';

  // Support & Resistance (swing highs/lows)
  const sup=Math.min(...lows.slice(-20));
  const res=Math.max(...highs.slice(-20));
  const swingHigh=Math.max(...highs.slice(-50));
  const swingLow=Math.min(...lows.slice(-50));

  // 24H stats — use token's actual 24H high/low from ticker, not candle derived
  const high24 = activeToken.high > 0 ? activeToken.high : Math.max(...highs);
  const low24  = activeToken.low  > 0 ? activeToken.low  : Math.min(...lows);
  document.getElementById('s24h').textContent=fmt(high24);
  document.getElementById('sLow').textContent=fmt(low24);
  document.getElementById('sSup').textContent=fmt(sup);
  document.getElementById('sRes').textContent=fmt(res);
  document.getElementById('statsGrid').style.display='grid';

  return {rsi, macd, atr, vwap, sup, res, swingHigh, swingLow, adx, volumeStrength};
}

// AI ANALYSIS
// ============================================================
// SCALP MODE — fast 5M analysis
// ============================================================
// ============================================================
// MANIPULATION MODE — detects stop hunts & fake breakouts on 5M
// ============================================================
async function runManipMode() {
  if (!currentUser) { window.location.href = 'cipher_auth.html'; return; }
  if (!activeToken) { alert('Select a token first'); return; }
  if (!chartData.length) { alert('Chart still loading — please wait'); return; }

  const btn    = document.getElementById('manip-btn');
  const runBtn = document.getElementById('runBtn');
  const scalpBtn = document.getElementById('scalp-btn');
  const out    = document.getElementById('outArea');

  btn.disabled = true; btn.textContent = 'SCANNING...';
  runBtn.disabled = true; scalpBtn.disabled = true;

  out.innerHTML = `
    <div class="load-block">
      <div class="load-top"><div class="spinner"></div><div class="load-txt" id="lMsg">LOADING 5M DATA...</div></div>
      <div class="prog-track"><div class="prog-fill" id="pBar" style="width:0%"></div></div>
      <div class="prog-lbl" id="pLbl">0%</div>
    </div>`;

  const setLoad = (pct, msg) => {
    const b = document.getElementById('pBar');
    const l = document.getElementById('pLbl');
    const m = document.getElementById('lMsg');
    if (b) b.style.width = pct + '%';
    if (l) l.textContent = pct + '%';
    if (m) m.textContent = msg;
  };

  try {
    setLoad(15, 'FETCHING 5M CANDLES...');
    const r = await fetch(`${SERVER}/candles?symbol=${activeToken.symbol}&interval=5m&limit=100`);
    if (!r.ok) throw new Error('Server error');
    const candleData = await r.json();
    const candles = candleData.candles;
    if (!candles || candles.length < 20) throw new Error('Not enough 5M data');

    setLoad(40, 'DETECTING MANIPULATION PATTERNS...');

    const closes = candles.map(c => c.c);
    const highs  = candles.map(c => c.h);
    const lows   = candles.map(c => c.l);
    const opens  = candles.map(c => c.o);
    const vols   = candles.map(c => c.v);
    const n = closes.length;
    const cp = closes[n - 1];

    // ── MANIPULATION PATTERN DETECTION ──

    const patterns = [];

    // ATR for context
    const trs = [];
    for (let i = 1; i < n; i++) {
      trs.push(Math.max(highs[i]-lows[i], Math.abs(highs[i]-closes[i-1]), Math.abs(lows[i]-closes[i-1])));
    }
    const atr = trs.slice(-14).reduce((a,b) => a+b, 0) / 14;
    const atrPct = (atr / cp) * 100;

    // Volume average
    const avgVol = vols.slice(-20).reduce((a,b) => a+b, 0) / 20;

    // Support & Resistance (last 30 candles)
    const recentHighs = highs.slice(-30);
    const recentLows  = lows.slice(-30);
    const resistance  = Math.max(...recentHighs.slice(0, -3)); // exclude last 3
    const support     = Math.min(...recentLows.slice(0, -3));

    // ── 1. STOP HUNT DETECTION ──
    // Wick below support then snapped back
    const last  = candles[n-1];
    const prev  = candles[n-2];
    const prev2 = candles[n-3];

    const lastWickLow  = Math.min(last.o, last.c) - last.l;
    const lastWickHigh = last.h - Math.max(last.o, last.c);
    const lastBody     = Math.abs(last.c - last.o);
    const prevBody     = Math.abs(prev.c - prev.o);

    let manipType = 'NONE';
    let manipSignal = 'NEUTRAL';
    let manipStrength = 0;

    // Stop hunt low — wick below support, close back above
    if (last.l < support && last.c > support && lastWickLow > lastBody * 1.5) {
      manipType = 'STOP HUNT LOW';
      manipSignal = 'LONG';
      manipStrength = 85;
      patterns.push(`🔻 Stop hunt below support $${fmt(support)} — wick ${((lastWickLow/cp)*100).toFixed(2)}% — snap back LONG`);
    }

    // Stop hunt high — wick above resistance, close back below
    if (last.h > resistance && last.c < resistance && lastWickHigh > lastBody * 1.5) {
      manipType = 'STOP HUNT HIGH';
      manipSignal = 'SHORT';
      manipStrength = 85;
      patterns.push(`🔺 Stop hunt above resistance $${fmt(resistance)} — wick ${((lastWickHigh/cp)*100).toFixed(2)}% — snap back SHORT`);
    }

    // ── 2. FAKE BREAKOUT ──
    // Previous candle broke level but this candle closed back inside
    if (prev.h > resistance && last.c < resistance && last.c < prev.c) {
      manipType = 'FAKE BREAKOUT HIGH';
      manipSignal = 'SHORT';
      manipStrength = 80;
      patterns.push(`🚫 Fake breakout above $${fmt(resistance)} — failed close — SHORT`);
    }

    if (prev.l < support && last.c > support && last.c > prev.c) {
      manipType = 'FAKE BREAKOUT LOW';
      manipSignal = 'LONG';
      manipStrength = 80;
      patterns.push(`🚫 Fake breakdown below $${fmt(support)} — failed close — LONG`);
    }

    // ── 3. VOLUME SPIKE REVERSAL ──
    // Huge volume candle in one direction, next candle reverses
    if (vols[n-2] > avgVol * 3 && Math.sign(closes[n-1] - opens[n-1]) !== Math.sign(closes[n-2] - opens[n-2])) {
      const dir = closes[n-1] > opens[n-1] ? 'LONG' : 'SHORT';
      if (manipType === 'NONE') {
        manipType = 'VOLUME SPIKE REVERSAL';
        manipSignal = dir;
        manipStrength = 75;
      }
      patterns.push(`📊 Volume spike ${(vols[n-2]/avgVol).toFixed(1)}x avg — reversal candle forming`);
    }

    // ── 4. SLOW BLEED EXHAUSTION ──
    // 5+ red candles in a row, volume dying, RSI < 30
    const last5 = candles.slice(-5);
    const allRed = last5.every(c => c.c < c.o);
    const volDrying = vols[n-1] < avgVol * 0.4;
    let rsi = 50;
    try {
      let g = 0, l = 0;
      for (let i = n-9; i < n; i++) { const d = closes[i]-closes[i-1]; d>0?g+=d:l-=d; }
      rsi = Math.round(100-(100/(1+(l===0?100:g/l))));
    } catch(e) {}

    if (allRed && volDrying && rsi < 35) {
      if (manipType === 'NONE') {
        manipType = 'SLOW BLEED EXHAUSTION';
        manipSignal = 'LONG';
        manipStrength = 70;
      }
      patterns.push(`😮‍💨 5 consecutive red candles + volume drying + RSI ${rsi} — seller exhaustion LONG`);
    }

    // ── 5. PUMP EXHAUSTION ──
    const last5Green = candles.slice(-5).every(c => c.c > c.o);
    const volDyingGreen = vols[n-1] < vols[n-3] * 0.5;
    if (last5Green && volDyingGreen && rsi > 75) {
      if (manipType === 'NONE') {
        manipType = 'PUMP EXHAUSTION';
        manipSignal = 'SHORT';
        manipStrength = 70;
      }
      patterns.push(`🎈 5 consecutive green candles + volume fading + RSI ${rsi} — pump exhaustion SHORT`);
    }

    setLoad(70, 'ASKING AI...');

    // Entry/TP/SL based on ATR
    const isLong = manipSignal === 'LONG';
    const entry  = cp;
    const tp     = isLong ? cp + atr * 1.5 : cp - atr * 1.5;
    const sl     = isLong ? cp - atr * 0.8 : cp + atr * 0.8;
    const tpPct  = Math.abs((tp - entry) / entry * 100).toFixed(2);
    const slPct  = Math.abs((sl - entry) / entry * 100).toFixed(2);

    // Ask AI to validate and add context
    const manipPrompt = `You are CIPHER in MANIPULATION MODE. Validate this manipulation pattern for ${activeToken.symbol} 5M chart.

DETECTED PATTERN: ${manipType}
SIGNAL: ${manipSignal}
STRENGTH: ${manipStrength}%
Current Price: $${fmt(cp)}
ATR(14): $${fmt(atr)} (${atrPct.toFixed(2)}% of price)
RSI(9): ${rsi}
Support: $${fmt(support)} | Resistance: $${fmt(resistance)}
Volume vs avg: ${(vols[n-1]/avgVol).toFixed(1)}x

DETECTED SIGNALS:
${patterns.join('\n')}

${manipType === 'NONE' ? 'NO CLEAR MANIPULATION PATTERN DETECTED. Advise the trader to wait.' : `Validate the ${manipType} pattern and give entry guidance.`}

Rules:
- Window: 5-15 mins MAX for manipulation trades
- SL must be TIGHT — behind the manipulation wick
- Entry AT MARKET — manipulation trades need immediate entry
- If pattern is NONE — say WAIT clearly

Respond ONLY in JSON:
{"valid":true or false,"signal":"${manipSignal}","confidence":${manipStrength},"entry":"${fmt(entry)}","target":"${fmt(tp)}","stop":"${fmt(sl)}","tp_pct":"${tpPct}%","sl_pct":"${slPct}%","window":"5-15 mins","reasoning":"2 sentences validating the pattern","action":"ENTER NOW or WAIT","warning":"one risk warning or empty"}`;

    const aiRes = await fetch(`${SERVER}/analyze`, {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({prompt: manipPrompt})
    });
    if (!aiRes.ok) throw new Error('AI error');
    const aiData = await aiRes.json();
    let raw = aiData.content[0].text.trim().replace(/```json|```/g,'').trim();
    const s = JSON.parse(raw);

    setLoad(100, 'DONE!');
    await new Promise(res => setTimeout(res, 200));

    // Render result
    const sigColor  = s.signal === 'LONG' ? 'var(--accent)' : s.signal === 'SHORT' ? 'var(--accent3)' : 'var(--accent4)';
    const typeColor = '#a855f7';
    const isWait    = !s.valid || s.action === 'WAIT' || manipType === 'NONE';

    out.innerHTML = `
      <div class="out-block" style="border-left:2px solid #a855f7;">
        <div class="out-meta">
          <div class="out-tag" style="background:#a855f708;border-color:#a855f730;color:#a855f7;">MANIPULATION — 5M</div>
          <div class="out-time">${new Date().toLocaleTimeString('en-US',{hour:'2-digit',minute:'2-digit'})}</div>
        </div>

        <!-- Pattern type -->
        <div style="padding:8px 10px;background:#a855f710;border:1px solid #a855f730;margin-bottom:10px;">
          <div style="font-size:8px;color:#a855f7;letter-spacing:2px;margin-bottom:3px;">PATTERN DETECTED</div>
          <div style="font-size:12px;font-family:'Orbitron',sans-serif;color:${isWait?'var(--accent4)':'#fff'};font-weight:700;">${isWait ? 'NO CLEAR PATTERN — WAIT' : manipType}</div>
        </div>

        ${!isWait ? `
        <!-- Signal + Action -->
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
          <div>
            <div style="font-size:8px;color:var(--text3);letter-spacing:2px;margin-bottom:4px;">DIRECTION</div>
            <div style="font-family:'Orbitron',sans-serif;font-size:20px;font-weight:900;color:${sigColor};">${s.signal}</div>
          </div>
          <div style="text-align:right;">
            <div style="font-size:8px;color:var(--text3);letter-spacing:2px;margin-bottom:4px;">ACTION</div>
            <div style="font-size:12px;font-weight:700;color:${s.action==='ENTER NOW'?'var(--accent)':'var(--accent4)'};letter-spacing:1px;">${s.action}</div>
            <div style="font-size:9px;color:var(--text3);margin-top:2px;">${s.confidence}% confidence</div>
          </div>
        </div>

        <!-- Entry/TP/SL -->
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1px;background:var(--border);margin-bottom:10px;">
          <div style="background:var(--bg3);padding:8px 10px;">
            <div style="font-size:7px;color:var(--text3);letter-spacing:1px;margin-bottom:3px;">MARKET ENTRY</div>
            <div style="font-size:13px;font-family:'Rajdhani',sans-serif;font-weight:700;color:var(--text);">${fmt(parseFloat(s.entry))}</div>
          </div>
          <div style="background:var(--bg3);padding:8px 10px;">
            <div style="font-size:7px;color:var(--accent);letter-spacing:1px;margin-bottom:3px;">TAKE PROFIT</div>
            <div style="font-size:13px;font-family:'Rajdhani',sans-serif;font-weight:700;color:var(--accent);">${fmt(parseFloat(s.target))}</div>
            <div style="font-size:8px;color:var(--accent);margin-top:1px;">+${s.tp_pct}</div>
          </div>
          <div style="background:var(--bg3);padding:8px 10px;">
            <div style="font-size:7px;color:var(--accent3);letter-spacing:1px;margin-bottom:3px;">STOP LOSS</div>
            <div style="font-size:13px;font-family:'Rajdhani',sans-serif;font-weight:700;color:var(--accent3);">${fmt(parseFloat(s.stop))}</div>
            <div style="font-size:8px;color:var(--accent3);margin-top:1px;">-${s.sl_pct}</div>
          </div>
        </div>

        <!-- Window -->
        <div style="padding:6px 10px;background:#a855f708;border:1px solid #a855f720;margin-bottom:10px;display:flex;justify-content:space-between;align-items:center;">
          <div style="font-size:9px;color:#a855f7;letter-spacing:1px;">TIME WINDOW</div>
          <div style="font-size:11px;font-weight:700;color:#fff;">${s.window}</div>
        </div>` : ''}

        <!-- Detected patterns list -->
        ${patterns.length ? `
        <div style="margin-bottom:10px;">
          <div style="font-size:8px;color:var(--text3);letter-spacing:2px;margin-bottom:6px;">SIGNALS FOUND</div>
          ${patterns.map(p => `<div style="font-size:10px;color:var(--text2);padding:4px 0;border-bottom:1px solid var(--border);font-family:'DM Sans',sans-serif;">${p}</div>`).join('')}
        </div>` : ''}

        <!-- Reasoning -->
        <div style="font-size:11px;color:var(--text2);line-height:1.7;font-family:'DM Sans',sans-serif;margin-bottom:${s.warning?'8px':'0'}">${s.reasoning}</div>
        ${s.warning ? `<div style="font-size:10px;color:var(--accent4);margin-top:4px;font-family:'DM Sans',sans-serif;">⚠ ${s.warning}</div>` : ''}

        <div style="display:flex;gap:8px;margin-top:10px;padding-top:10px;border-top:1px solid var(--border);">
          <div style="font-size:8px;color:var(--text3);">ATR ${atrPct.toFixed(2)}%</div>
          <div style="font-size:8px;color:var(--text3);">RSI ${rsi}</div>
          <div style="font-size:8px;color:var(--text3);">VOL ${(vols[n-1]/avgVol).toFixed(1)}x avg</div>
        </div>
      </div>
    `;

    // Send to Telegram if signal found and linked
    if (!isWait && userProfile?.telegram_verified) {
      sendPersonalNotification(
        `MANIPULATION ALERT — ${activeToken.symbol} 5M\n\n` +
        `Pattern: ${manipType}\n` +
        `Signal: ${s.signal} (${s.confidence}%)\n` +
        `Action: ${s.action}\n\n` +
        `Entry: ${s.entry}\n` +
        `TP: ${s.target} (+${s.tp_pct})\n` +
        `SL: ${s.stop} (-${s.sl_pct})\n` +
        `Window: ${s.window}\n\n` +
        `${s.reasoning}\n\n` +
        `NOT FINANCIAL ADVICE`,
        'analysis'
      );
    }

  } catch(e) {
    out.innerHTML = `<div class="out-block" style="border-left:2px solid var(--accent3)">
      <div class="out-txt" style="color:var(--accent3)">MANIP ERROR: ${e.message}</div>
    </div>`;
  }

  btn.disabled = false; btn.textContent = '⚡ MANIPULATION — 5M';
  runBtn.disabled = false; scalpBtn.disabled = false;
}

async function runScalpMode() {
  if (!currentUser) { window.location.href = 'cipher_auth.html'; return; }
  if (!activeToken) { alert('Select a token first'); return; }
  if (!chartData.length) {
    alert('Chart still loading — please wait a moment before running scalp analysis');
    return;
  }

  const btn = document.getElementById('scalp-btn');
  const runBtn = document.getElementById('runBtn');
  const out = document.getElementById('outArea');

  btn.disabled = true; btn.textContent = 'SCANNING...';
  runBtn.disabled = true;

  // Switch to 5M for scalp
  const prevTf = activeTimeframe;
  activeTimeframe = '5M';
  document.querySelectorAll('.tf-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.tf === '5M');
  });

  out.innerHTML = `
    <div class="load-block">
      <div class="load-top"><div class="spinner"></div><div class="load-txt" id="lMsg">LOADING 5M CANDLES...</div></div>
      <div class="prog-track"><div class="prog-fill" id="pBar" style="width:0%"></div></div>
      <div class="prog-lbl" id="pLbl">0%</div>
    </div>`;

  const setLoad = (pct, msg) => {
    const b = document.getElementById('pBar');
    const l = document.getElementById('pLbl');
    const m = document.getElementById('lMsg');
    if (b) b.style.width = pct + '%';
    if (l) l.textContent = pct + '%';
    if (m) m.textContent = msg;
  };

  try {
    // Fetch 5M candles
    setLoad(15, 'FETCHING 5M CANDLES...');
    const r = await fetch(`${SERVER}/candles?symbol=${activeToken.symbol}&interval=5m&limit=100`);
    if (!r.ok) throw new Error('Server error');
    const candleData = await r.json();
    const candles = candleData.candles;
    if (!candles || candles.length < 20) throw new Error('Not enough 5M candle data');

    setLoad(35, 'FETCHING 15M TREND...');
    // Fetch 15M for trend confirmation
    let htfTrend = 'UNKNOWN';
    try {
      const r15 = await fetch(`${SERVER}/candles?symbol=${activeToken.symbol}&interval=15m&limit=50`);
      if (r15.ok) {
        const d15 = await r15.json();
        if (d15.candles && d15.candles.length >= 20) {
          const c15 = d15.candles;
          const n = c15.length;
          const closes15 = c15.map(c => c.c);
          const ema20 = closes15.slice(-20).reduce((a, b) => a + b, 0) / 20;
          const ema50 = closes15.length >= 50 ? closes15.slice(-50).reduce((a, b) => a + b, 0) / 50 : ema20;
          const last = closes15[n - 1];
          htfTrend = last > ema20 && ema20 > ema50 ? 'BULLISH' : last < ema20 && ema20 < ema50 ? 'BEARISH' : 'MIXED';
        }
      }
    } catch(e) {}

    setLoad(55, 'CALCULATING SCALP INDICATORS...');

    // Calculate indicators on 5M data
    const closes = candles.map(c => c.c);
    const highs  = candles.map(c => c.h);
    const lows   = candles.map(c => c.l);
    const vols   = candles.map(c => c.v);
    const n = closes.length;
    const cp = closes[n - 1];

    // RSI (9 period for scalping — more sensitive)
    let rsi = 50;
    try {
      let g = 0, l = 0;
      for (let i = n - 9; i < n; i++) {
        const d = closes[i] - closes[i - 1];
        if (d > 0) g += d; else l -= d;
      }
      rsi = Math.round(100 - (100 / (1 + (l === 0 ? 100 : g / l))));
    } catch(e) {}

    // EMA 9 and EMA 21 (scalp EMAs)
    const emaCalc = (data, p) => {
      const k = 2 / (p + 1); let e = data[0];
      for (let i = 1; i < data.length; i++) e = data[i] * k + e * (1 - k);
      return e;
    };
    const ema9  = emaCalc(closes.slice(-30), 9);
    const ema21 = emaCalc(closes.slice(-30), 21);

    // ATR (7 period for scalping)
    let atr = 0;
    try {
      const trs = [];
      for (let i = n - 7; i < n; i++) {
        trs.push(Math.max(highs[i] - lows[i], Math.abs(highs[i] - closes[i-1]), Math.abs(lows[i] - closes[i-1])));
      }
      atr = trs.reduce((a, b) => a + b, 0) / trs.length;
    } catch(e) {}

    // Volume spike (last candle vs 10 avg)
    const avgVol = vols.slice(-10).reduce((a, b) => a + b, 0) / 10;
    const volSpike = vols[n - 1] > avgVol * 1.5;
    const volStr = vols[n - 1] > avgVol * 2 ? 'STRONG SPIKE' : vols[n - 1] > avgVol * 1.5 ? 'ABOVE AVERAGE' : 'NORMAL';

    // Momentum — last 3 candles direction
    const last3Green = closes[n-1] > closes[n-2] && closes[n-2] > closes[n-3];
    const last3Red   = closes[n-1] < closes[n-2] && closes[n-2] < closes[n-3];
    const momentum = last3Green ? 'BULLISH MOMENTUM' : last3Red ? 'BEARISH MOMENTUM' : 'MIXED';

    // Support/Resistance (recent 20 candles)
    const recentHigh = Math.max(...highs.slice(-20));
    const recentLow  = Math.min(...lows.slice(-20));

    setLoad(75, 'ASKING AI...');

    const scalpPrompt = `You are CIPHER in SCALP MODE${degenMode ? ' — DEGEN' : ''}. Give an ultra-fast scalp setup for ${activeToken.symbol}.

TIMEFRAME: 5M (scalp) | 15M TREND: ${htfTrend}
Current Price: $${fmt(cp)}
EMA9: $${fmt(ema9)} | EMA21: $${fmt(ema21)}
RSI(9): ${rsi} ${rsi > 70 ? '(OVERBOUGHT)' : rsi < 30 ? '(OVERSOLD)' : '(NEUTRAL)'}
ATR(7): $${fmt(atr)} (${((atr/cp)*100).toFixed(3)}% of price)
Volume: ${volStr}
Momentum: ${momentum}
Recent High: $${fmt(recentHigh)} | Recent Low: $${fmt(recentLow)}

SCALP RULES:
${degenMode ? `
- DEGEN MODE: Always give LONG or SHORT. Never SKIP.
- Trade against the trend if momentum is strong enough — contrarian scalps are valid.
- Entry AT market is acceptable if momentum is explosive.
- SL = 0.8x ATR (ultra tight — take the loss fast and re-enter)
- TP = 2x ATR (ride the momentum further)
- Time in trade: 2-10 minutes MAX
- Position size up to 10% — degen scalps hit hard.
- Chase if needed — missing the move is worse than a bad entry.
` : `
- Only trade WITH the 15M trend direction.
- Entry must be at EMA9 bounce, recent support/resistance, or momentum breakout.
- SL = 1x ATR (tight — scalps need tight stops)
- TP = 1.5x ATR (quick profit — don't be greedy)
- Time in trade: 5-20 minutes MAX
- SKIP only when 15M trend directly contradicts 5M with no resolution.
- Position size MAX 5% of capital.
`}

Respond ONLY in JSON:
{"signal":"LONG or SHORT${degenMode ? '' : ' or SKIP'}","confidence":${degenMode ? '60-95' : '50-90'},"entry":"price","target":"price","stop":"price","tp_pct":"expected % gain","sl_pct":"expected % loss","rr":"risk reward e.g 1:1.5","window":"time window e.g 10-15 mins","reasoning":"2 sentences max — be direct","caution":"${degenMode ? 'one word max risk flag' : 'one caution flag or empty string'}","chase":"true or false"}`;

    const aiRes = await fetch(`${SERVER}/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: scalpPrompt })
    });
    if (!aiRes.ok) throw new Error('AI error');
    const aiData = await aiRes.json();
    let raw = aiData.content[0].text.trim().replace(/```json|```/g, '').trim();
    const s = JSON.parse(raw);

    setLoad(100, 'DONE!');
    await new Promise(res => setTimeout(res, 200));

    // Render scalp result
    const isLong  = s.signal === 'LONG';
    const isShort = s.signal === 'SHORT';
    const isSkip  = s.signal === 'SKIP';
    const sigColor = isLong ? 'var(--accent)' : isShort ? 'var(--accent3)' : 'var(--accent4)';
    const trendColor = htfTrend === 'BULLISH' ? 'var(--accent)' : htfTrend === 'BEARISH' ? 'var(--accent3)' : 'var(--accent4)';

    out.innerHTML = `
      <div class="out-block" style="border-left:2px solid var(--accent4);">
        <div class="out-meta">
          <div class="out-tag" style="background:#e8a80010;border-color:#e8a80030;color:var(--accent4);">SCALP MODE — 5M</div>
          <div class="out-time">${new Date().toLocaleTimeString('en-US',{hour:'2-digit',minute:'2-digit'})}</div>
        </div>

        <!-- Signal -->
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
          <div>
            <div style="font-size:8px;color:var(--text3);letter-spacing:2px;margin-bottom:4px;">DIRECTION</div>
            <div style="font-family:'Orbitron',sans-serif;font-size:22px;font-weight:900;color:${sigColor};letter-spacing:3px;">${s.signal}</div>
          </div>
          <div style="text-align:right;">
            <div style="font-size:8px;color:var(--text3);letter-spacing:2px;margin-bottom:4px;">15M TREND</div>
            <div style="font-size:11px;color:${trendColor};font-weight:700;letter-spacing:1px;">${htfTrend}</div>
            <div style="font-size:9px;color:var(--text3);margin-top:2px;">${s.confidence}% confidence</div>
          </div>
        </div>

        ${isSkip ? `
        <div style="padding:12px;background:#e8a80010;border:1px solid #e8a80030;margin-bottom:10px;">
          <div style="font-size:10px;color:var(--accent4);letter-spacing:2px;margin-bottom:4px;">NO SETUP — STAY OUT</div>
          <div style="font-size:11px;color:var(--text2);font-family:'DM Sans',sans-serif;">${s.reasoning}</div>
        </div>` : `

        <!-- Entry / TP / SL -->
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1px;background:var(--border);margin-bottom:10px;">
          <div style="background:var(--bg3);padding:8px 10px;">
            <div style="font-size:7px;color:var(--text3);letter-spacing:1px;margin-bottom:3px;">${s.chase === 'true' ? 'CHASE ENTRY' : 'LIMIT ENTRY'}</div>
            <div style="font-size:13px;font-family:'Rajdhani',sans-serif;font-weight:700;color:var(--text);">${fmt(parseFloat(s.entry))}</div>
          </div>
          <div style="background:var(--bg3);padding:8px 10px;">
            <div style="font-size:7px;color:var(--accent);letter-spacing:1px;margin-bottom:3px;">TAKE PROFIT</div>
            <div style="font-size:13px;font-family:'Rajdhani',sans-serif;font-weight:700;color:var(--accent);">${fmt(parseFloat(s.target))}</div>
            <div style="font-size:8px;color:var(--accent);margin-top:1px;">+${s.tp_pct}</div>
          </div>
          <div style="background:var(--bg3);padding:8px 10px;">
            <div style="font-size:7px;color:var(--accent3);letter-spacing:1px;margin-bottom:3px;">STOP LOSS</div>
            <div style="font-size:13px;font-family:'Rajdhani',sans-serif;font-weight:700;color:var(--accent3);">${fmt(parseFloat(s.stop))}</div>
            <div style="font-size:8px;color:var(--accent3);margin-top:1px;">-${s.sl_pct}</div>
          </div>
        </div>

        <!-- Stats row -->
        <div style="display:flex;gap:8px;margin-bottom:10px;">
          <div style="flex:1;background:var(--bg3);border:1px solid var(--border2);padding:7px 10px;">
            <div style="font-size:7px;color:var(--text3);letter-spacing:1px;margin-bottom:2px;">R/R</div>
            <div style="font-size:12px;font-family:'Orbitron',sans-serif;color:var(--accent2);">${s.rr}</div>
          </div>
          <div style="flex:1;background:var(--bg3);border:1px solid var(--border2);padding:7px 10px;">
            <div style="font-size:7px;color:var(--text3);letter-spacing:1px;margin-bottom:2px;">WINDOW</div>
            <div style="font-size:12px;font-family:'Orbitron',sans-serif;color:var(--accent4);">${s.window}</div>
          </div>
          <div style="flex:1;background:var(--bg3);border:1px solid var(--border2);padding:7px 10px;">
            <div style="font-size:7px;color:var(--text3);letter-spacing:1px;margin-bottom:2px;">SIZE</div>
            <div style="font-size:12px;font-family:'Orbitron',sans-serif;color:var(--text);">MAX 5%</div>
          </div>
        </div>

        <!-- Entry type badge -->
        <div style="padding:6px 10px;background:${s.chase==='true'?'#e8003d10':'#00e87a08'};border:1px solid ${s.chase==='true'?'#e8003d30':'#00e87a20'};margin-bottom:10px;">
          <div style="font-size:9px;color:${s.chase==='true'?'var(--accent3)':'var(--accent)'};letter-spacing:1px;">
            ${s.chase==='true' ? 'MARKET ORDER — Price moving fast, enter at market' : 'LIMIT ORDER — Wait for price to pull back to entry'}
          </div>
        </div>`}

        <!-- Reasoning -->
        <div style="font-size:11px;color:var(--text2);line-height:1.7;font-family:'DM Sans',sans-serif;margin-bottom:${s.caution?'8px':'0'}">${s.reasoning}</div>
        ${s.caution ? `<div style="font-size:10px;color:var(--accent4);margin-top:4px;font-family:'DM Sans',sans-serif;">Note: ${s.caution}</div>` : ''}

        <!-- Volume indicator -->
        <div style="display:flex;align-items:center;gap:8px;margin-top:10px;padding-top:10px;border-top:1px solid var(--border);">
          <div style="font-size:8px;color:var(--text3);letter-spacing:1px;">5M VOL</div>
          <div style="font-size:9px;color:${volSpike?'var(--accent)':'var(--text2)'};">${volStr}</div>
          <div style="font-size:8px;color:var(--text3);margin-left:auto;">RSI(9): <span style="color:${rsi>70?'var(--accent3)':rsi<30?'var(--accent)':'var(--text2)'}">${rsi}</span></div>
        </div>
      </div>
    `;

    // Send to Telegram if linked
    if (!isSkip && userProfile?.telegram_verified) {
      sendPersonalNotification(
        `SCALP SETUP — ${activeToken.symbol} 5M\n\n` +
        `Direction: ${s.signal} (${s.confidence}%)\n` +
        `15M Trend: ${htfTrend}\n\n` +
        `Entry: ${s.entry} ${s.chase==='true'?'(MARKET)':'(LIMIT)'}\n` +
        `TP: ${s.target} (+${s.tp_pct})\n` +
        `SL: ${s.stop} (-${s.sl_pct})\n` +
        `R/R: ${s.rr} | Window: ${s.window}\n\n` +
        `${s.reasoning}\n\n` +
        `MAX 5% position size\n` +
        `NOT FINANCIAL ADVICE`,
        'analysis'
      );
    }

  } catch(e) {
    out.innerHTML = `<div class="out-block" style="border-left:2px solid var(--accent3)">
      <div class="out-txt" style="color:var(--accent3)">SCALP ERROR: ${e.message}</div>
    </div>`;
  }

  btn.disabled = false; btn.textContent = 'SCALP MODE — 5M';
  runBtn.disabled = false;
}

async function runAnalysis() {
  if (!currentUser) { window.location.href='cipher_auth.html'; return; }
  if (!activeToken) { alert('Select a token first'); return; }
  if (!chartData.length) {
    alert('Chart still loading — please wait a moment before running analysis');
    return;
  }

  const btn=document.getElementById('runBtn');
  btn.disabled=true;btn.textContent='ANALYZING...';
  const out=document.getElementById('outArea');

  out.innerHTML=`
    <div class="load-block">
      <div class="load-top"><div class="spinner"></div><div class="load-txt" id="lMsg">CONNECTING TO AI</div></div>
      <div class="prog-track"><div class="prog-fill" id="pBar" style="width:0%"></div></div>
      <div class="prog-lbl" id="pLbl">0%</div>
    </div>`;

  const steps=[[5,'FETCHING FRESH CANDLES'],[20,'CALCULATING INDICATORS'],[40,'FETCHING MARKET DATA'],[60,'RUNNING TA ENGINE'],[80,'GENERATING SIGNAL'],[92,'FINALIZING ANALYSIS']];
  let si=0;
  const tick=setInterval(()=>{
    if(si<steps.length){
      const[p,m]=steps[si];
      const bar=document.getElementById('pBar'),lbl=document.getElementById('pLbl'),msg=document.getElementById('lMsg');
      if(bar)bar.style.width=p+'%';if(lbl)lbl.textContent=p+'%';if(msg)msg.textContent=m;si++;
    }
  },1800);

  // Fetch FRESH candles via server proxy for analysis
  let analysisChartData = chartData;
  let usingSimulated = false;
  let lowCandleWarning = '';
  let dataSource = 'SERVER PROXY';
  try {
    const intervalMap = {'5M':'5m','15M':'15m','1H':'1h','4H':'4h','1D':'1d','1W':'1w'};
    const interval = intervalMap[activeTimeframe] || '1h';
    const limit = {'5M':100,'15M':80,'1H':80,'4H':90,'1D':60,'1W':52}[activeTimeframe] || 80;

    let freshRaw = null;

    // Primary: use server proxy (no CORS)
    try {
      const r = await fetch(`${SERVER}/candles?symbol=${activeToken.symbol}&interval=${interval}&limit=${limit}`);
      if (r.ok) {
        const d = await r.json();
        if (d.candles && d.candles.length) {
          freshRaw = d.candles.map(c => [null, c.o, c.h, c.l, c.c, c.v]);
          dataSource = `${d.source} (FRESH via server)`;
          if (d.warning) lowCandleWarning = d.warning;
          if (d.candles.length < 50) lowCandleWarning = `Only ${d.candles.length} candles — indicators may be inaccurate`;
        }
      }
    } catch(e) {}

    // Fallback: try direct exchanges
    if (!freshRaw) {
      try {
        const symbol = activeToken.symbol + 'USDT';
        const r = await fetch(`https://api.binance.com/api/v3/klines?symbol=${symbol}&interval=${interval}&limit=${limit}`);
        if (r.ok) { const d = await r.json(); if (Array.isArray(d)&&d.length) { freshRaw=d; dataSource='BINANCE (FRESH)'; } }
      } catch(e) {}
    }

    if (freshRaw) {
      analysisChartData = freshRaw.map(c => ({
        open: parseFloat(c[1]), high: parseFloat(c[2]),
        low: parseFloat(c[3]), close: parseFloat(c[4]),
        vol: parseFloat(c[5]),
      }));
    } else {
      dataSource = usingSimulated ? 'SIMULATED (all sources failed)' : 'CHART DATA (cached)';
    }
  } catch(e) {
    dataSource = 'CHART DATA (cached)';
  }

  // Use fresh data for all calculations
  const closes = analysisChartData.map(c=>c.close);
  const n = closes.length;

  // Recalculate ALL indicators from fresh data — do NOT use updateIndicators() for analysis
  const freshHighs = analysisChartData.map(c=>c.high);
  const freshLows  = analysisChartData.map(c=>c.low);
  const freshVols  = analysisChartData.map(c=>c.vol);

  // ── RSI(14) — proper Wilder smoothing over full history ──
  let freshRsi = 50;
  try {
    if (n >= 15) {
      // First avg gain/loss over first 14 periods
      let avgGain = 0, avgLoss = 0;
      for (let i = 1; i <= 14; i++) {
        const d = closes[i] - closes[i-1];
        if (d > 0) avgGain += d; else avgLoss -= d;
      }
      avgGain /= 14; avgLoss /= 14;
      // Wilder smooth over remaining candles
      for (let i = 15; i < n; i++) {
        const d = closes[i] - closes[i-1];
        const gain = d > 0 ? d : 0;
        const loss = d < 0 ? -d : 0;
        avgGain = (avgGain * 13 + gain) / 14;
        avgLoss = (avgLoss * 13 + loss) / 14;
      }
      freshRsi = avgLoss === 0 ? 100 : Math.round(100 - (100 / (1 + avgGain / avgLoss)));
      freshRsi = Math.max(0, Math.min(100, freshRsi));
    }
  } catch(e) {}

  // ── MACD (12,26,9) ──
  const fm12 = ema(closes, 12);
  const fm26 = ema(closes, 26);
  const fml  = fm12.map((v,i) => v - fm26[i]);
  const fsig = ema(fml, 9);
  const freshMacd = fml[n-1] - fsig[n-1];

  // ── ATR(14) — using correct high/low/close arrays ──
  let freshAtr = 0;
  try {
    let fatrSum = 0;
    const atrStart = Math.max(1, n-14);
    for (let i = atrStart; i < n; i++) {
      const tr = Math.max(
        freshHighs[i] - freshLows[i],
        Math.abs(freshHighs[i] - closes[i-1]),
        Math.abs(freshLows[i] - closes[i-1])
      );
      fatrSum += tr;
    }
    freshAtr = fatrSum / (n - atrStart);
  } catch(e) {}

  // ── VWAP (from fresh candles) ──
  let freshVwap = closes[n-1];
  try {
    let cumTPV = 0, cumVol = 0;
    for (let i = 0; i < n; i++) {
      const tp = (freshHighs[i] + freshLows[i] + closes[i]) / 3;
      cumTPV += tp * freshVols[i];
      cumVol += freshVols[i];
    }
    if (cumVol > 0) freshVwap = cumTPV / cumVol;
  } catch(e) {}

  // ── EMA 20/50 — with edge case handling ──
  const e20 = n >= 20 ? ema(closes, 20) : ema(closes, n);
  const e50 = n >= 50 ? ema(closes, 50) : ema(closes, n);
  const cp  = closes[n-1];

  // ── ADX(14) ──
  let freshAdx = 0;
  try {
    const trueRanges = [], plusDM = [], minusDM = [];
    for (let i = 1; i < n; i++) {
      const tr = Math.max(freshHighs[i]-freshLows[i], Math.abs(freshHighs[i]-closes[i-1]), Math.abs(freshLows[i]-closes[i-1]));
      const up = freshHighs[i] - freshHighs[i-1];
      const dn = freshLows[i-1] - freshLows[i];
      trueRanges.push(tr);
      plusDM.push(up > dn && up > 0 ? up : 0);
      minusDM.push(dn > up && dn > 0 ? dn : 0);
    }
    const p = 14;
    let atr14 = trueRanges.slice(0,p).reduce((a,b)=>a+b,0);
    let pDM   = plusDM.slice(0,p).reduce((a,b)=>a+b,0);
    let mDM   = minusDM.slice(0,p).reduce((a,b)=>a+b,0);
    const dxArr = [];
    for (let i = p; i < trueRanges.length; i++) {
      atr14 = atr14 - atr14/p + trueRanges[i];
      pDM   = pDM   - pDM/p   + plusDM[i];
      mDM   = mDM   - mDM/p   + minusDM[i];
      const pDI = 100 * pDM / atr14;
      const mDI = 100 * mDM / atr14;
      dxArr.push(100 * Math.abs(pDI - mDI) / ((pDI + mDI) || 1));
    }
    freshAdx = Math.round(dxArr.slice(-14).reduce((a,b)=>a+b,0) / Math.min(14, dxArr.length));
  } catch(e) {}

  // ── Bollinger Bands(20) ──
  const bbPeriod = Math.min(20, n);
  const bs  = closes.slice(-bbPeriod);
  const bm  = bs.reduce((a,b)=>a+b,0) / bbPeriod;
  const bstd = Math.sqrt(bs.reduce((a,b)=>a+(b-bm)**2,0) / bbPeriod);

  // ── Support / Resistance ──
  const sup       = Math.min(...freshLows.slice(-20));
  const res       = Math.max(...freshHighs.slice(-20));
  const swingHigh = Math.max(...freshHighs.slice(-Math.min(50,n)));
  const swingLow  = Math.min(...freshLows.slice(-Math.min(50,n)));

  // ── Volume Strength ──
  const avgVol2 = freshVols.slice(-20).reduce((a,b)=>a+b,0) / Math.min(20, n);
  const lastVol2 = freshVols[n-1];
  const volumeStrength = lastVol2 > avgVol2*1.5 ? 'HIGH (strong confirmation)' :
                         lastVol2 > avgVol2      ? 'ABOVE AVERAGE' :
                         lastVol2 < avgVol2*0.5  ? 'LOW (weak signal)' : 'AVERAGE';

  // Use calculated values
  const rsi  = freshRsi;
  const macd = freshMacd;
  const atr  = freshAtr;
  const vwap = freshVwap;
  const adx  = freshAdx;


  // Fetch Funding Rate from Binance futures
  let fundingRate = 'N/A';
  try {
    const symbol = activeToken.symbol + 'USDT';
    const frRes = await fetch(`https://fapi.binance.com/fapi/v1/fundingRate?symbol=${symbol}&limit=1`).then(r=>r.json());
    if (Array.isArray(frRes) && frRes[0]) {
      const fr = parseFloat(frRes[0].fundingRate) * 100;
      fundingRate = `${fr.toFixed(4)}% ${fr > 0.1 ? '(OVERLEVERAGED LONG — short squeeze risk)' : fr < -0.1 ? '(OVERLEVERAGED SHORT — long squeeze risk)' : '(NEUTRAL)'}`;
    }
  } catch(e) {}

  // Previous Day High/Low/Close (institutional levels)
  let pdLevels = 'N/A';
  try {
    const symbol = activeToken.symbol + 'USDT';
    const daily = await fetch(`https://api.binance.com/api/v3/klines?symbol=${symbol}&interval=1d&limit=2`).then(r=>r.json());
    if (Array.isArray(daily) && daily.length >= 2) {
      const yesterday = daily[daily.length - 2];
      const pdh = parseFloat(yesterday[2]);
      const pdl = parseFloat(yesterday[3]);
      const pdc = parseFloat(yesterday[4]);
      const aboveClose = cp > pdc ? 'ABOVE prev close (bullish)' : 'BELOW prev close (bearish)';
      pdLevels = `PDH: ${fmt(pdh)} | PDL: ${fmt(pdl)} | PDC: ${fmt(pdc)} — Price ${aboveClose}`;
    }
  } catch(e) {}

  // Fear & Greed Index
  let fearGreed = 'UNKNOWN';
  let fearGreedValue = '';
  try {
    const fg = await fetch('https://api.alternative.me/fng/?limit=1').then(r=>r.json());
    const val = parseInt(fg.data[0].value);
    const label = fg.data[0].value_classification.toUpperCase();
    fearGreed = `${label} (${val}/100)`;
    fearGreedValue = val;
  } catch(e) {}


  const modeInstructions = degenMode ? `
ANALYSIS MODE: DEGEN 🔥
- NEVER say NEUTRAL. Always give LONG or SHORT — even if signals conflict.
- Minimum confidence: 60%. Max: 95%.
- Volatile tokens are OPPORTUNITIES not warnings. High ATR = high reward potential.
- Ignore "too volatile" — the user knows the risk and wants the signal.
- Give aggressive entries — at or near current price if momentum is strong.
- Position size: up to 15% of capital on high conviction, 5-10% on medium.
- SL can be wider — up to 20% from entry for high volatility tokens.
- Focus on MOMENTUM and TREND — ignore ranging/neutral conditions.
- If RSI > 70 and trending — still give LONG. If RSI < 30 and trending down — still give SHORT.
- Caution field should be SHORT — just flag the key risk, don't lecture.
- The user is an experienced trader. Be direct. No hand-holding.
` : `
ANALYSIS MODE: SAFE
- Only give HIGH confidence (80%+) when trend, momentum AND volume all agree.
- NEUTRAL should be RARE — only use when LONG and SHORT are perfectly balanced.
- When ADX < 20 (ranging): give LOW confidence (55-65%) directional signal instead of NEUTRAL.
- If data is limited (few candles), give directional signal with lower confidence 55-65%.
- Position size: max 20% on high conviction, 5-10% on medium.
- SL must be realistic — never more than 15% from entry for altcoins.
- If ATR > 10% of price — flag HIGH risk, reduce size to 1-3%.
`;

  const prompt=`You are CIPHER, elite AI crypto technical analyst. Analyze ${activeToken.symbol} using the provided data and give sharp actionable predictions.
${usingSimulated ? '\nWARNING: Chart data unavailable. Analysis based on SIMULATED data — lower confidence recommended.\n' : ''}
${lowCandleWarning ? `\nWARNING: ${lowCandleWarning} — keep confidence below 70% and widen SL.\n` : ''}
${modeInstructions}
TOKEN: ${activeToken.symbol} (${activeToken.name})
TIMEFRAME: ${activeTimeframe}
CURRENT PRICE: ${fmt(cp)}
24H CHANGE: ${activeToken.change>=0?'+':''}${activeToken.change.toFixed(2)}%
DATA SOURCE: ${dataSource}

MARKET SENTIMENT:
- Fear & Greed Index: ${fearGreed}${fearGreedValue !== '' ? (fearGreedValue < 25 ? ' ← Extreme fear, potential buy zone' : fearGreedValue > 75 ? ' ← Extreme greed, potential sell zone' : '') : ''}
- Funding Rate: ${fundingRate}
- Previous Day Levels: ${pdLevels}

TREND:
- EMA20: ${fmt(e20[n-1])} — price ${cp>e20[n-1]?'ABOVE (bullish)':'BELOW (bearish)'}
- EMA50: ${fmt(e50[n-1])} — price ${cp>e50[n-1]?'ABOVE (bullish)':'BELOW (bearish)'}
- VWAP: ${fmt(vwap)} — price ${cp>vwap?'ABOVE (bullish)':'BELOW (bearish)'}
- ADX(14): ${adx} ${adx>25?'(STRONG TREND — trade it)':adx>20?'(DEVELOPING TREND)':'(WEAK/RANGING — avoid breakouts)'}

MOMENTUM:
- RSI(14): ${rsi} ${rsi>70?'(OVERBOUGHT — caution longs)':rsi<30?'(OVERSOLD — potential bounce)':'(NEUTRAL)'}
- MACD: ${macd>0?'BULLISH':'BEARISH'} (${((macd/closes[n-1])*100).toFixed(3)}% of price${Math.abs((macd/closes[n-1])*100) > 1 ? ' — STRONG momentum' : Math.abs((macd/closes[n-1])*100) > 0.3 ? ' — moderate momentum' : ' — weak momentum'})

VOLATILITY:
- ATR(14): ${fmt(atr)} (${((atr/cp)*100).toFixed(2)}% of price)
- Bollinger Upper: ${fmt(bm+2*bstd)} | Lower: ${fmt(bm-2*bstd)} | Mid: ${fmt(bm)}
- Price position: ${cp > bm+2*bstd ? 'ABOVE UPPER BAND (overbought)' : cp < bm-2*bstd ? 'BELOW LOWER BAND (oversold)' : cp > bm ? 'ABOVE MID (bullish)' : 'BELOW MID (bearish)'}

VOLUME:
- Strength: ${volumeStrength}

${(() => {
  const rangePct = ((activeToken.high - activeToken.low) / activeToken.low * 100);
  const atrPct   = (atr / cp * 100);
  const price    = activeToken?.price || cp;
  const warnings = [];

  // HARD BLOCK — never short a micro-cap pump
  const isMicroCap = price < 0.01;
  const isPumping  = activeToken.change > 20;
  const isExtreme  = rangePct > 80;

  if (isMicroCap && isPumping) {
    warnings.push(`🚨 HARD BLOCK: Micro-cap token (${fmt(price)}) with +${activeToken.change.toFixed(0)}% pump. DO NOT SHORT. Signal MUST be NEUTRAL or LONG only. Shorting a pumping micro-cap risks liquidation.`);
  }
  if (isMicroCap && isExtreme) {
    warnings.push(`🚨 HARD BLOCK: Micro-cap with ${rangePct.toFixed(0)}% range. Extremely dangerous to short. NEUTRAL signal only.`);
  }
  if (!degenMode) {
    if (rangePct > 100) warnings.push(`EXTREME PUMP: 24H range ${rangePct.toFixed(0)}% — crime pump risk. Signal NEUTRAL — DO NOT SHORT.`);
    else if (rangePct > 50) warnings.push(`HIGH VOLATILITY: 24H range ${rangePct.toFixed(0)}% — reduce confidence and size.`);
    if (atrPct > 10) warnings.push(`ATR is ${atrPct.toFixed(1)}% of price — extremely volatile. Max 2% position size.`);
    if (atrPct > 15) warnings.push(`ATR > 15% of price — DO NOT TRADE. Signal NEUTRAL.`);
  } else {
    if (isMicroCap && isPumping) warnings.push(`DEGEN WARNING: Micro-cap pump in progress — if you short, use MAX 1% size and very tight SL.`);
    else if (rangePct > 100) warnings.push(`24H range ${rangePct.toFixed(0)}% — crime pump possible. Factor into SL placement.`);
  }
  return warnings.length ? `⚠ WARNINGS — READ BEFORE GENERATING SIGNAL:\n${warnings.map(w => `- ${w}`).join('\n')}` : '';
})()}

KEY LEVELS:
- Support: ${fmt(sup)} | Resistance: ${fmt(res)}
- Swing High: ${fmt(swingHigh)} | Swing Low: ${fmt(swingLow)}

ENTRY PRICE RULES — CRITICAL, FOLLOW EXACTLY:
- LONG entry = slightly BELOW current price at nearest support or EMA — so limit order gets filled on dip
- SHORT entry = slightly ABOVE current price at nearest resistance or EMA rejection — so limit order gets filled on bounce
- CURRENT LIVE PRICE is ${fmt(activeToken?.price || cp)} — ALL entries must be relative to THIS price
- For SHORT: entry MUST be >= ${fmt(activeToken?.price || cp)} (above or at current price). A SHORT entry BELOW current price will NEVER fill — it is wrong.
- For LONG: entry MUST be <= ${fmt(activeToken?.price || cp)} (below or at current price). A LONG entry ABOVE current price will NEVER fill — it is wrong.
- If price is already at a good level — use current price as entry (market order)
- SL for LONG = below entry. SL for SHORT = above entry. NEVER the other way around.
- TP for LONG = above entry. TP for SHORT = below entry. NEVER the other way around.
${degenMode ? '- DEGEN: If momentum is strong, entry AT market is acceptable. Chase if needed.' : `- SAFE: Assess whether to wait or chase:
  * If price is within 1x ATR of key level → LIMIT entry, wait for pullback
  * If momentum is explosive (volume spike + 3 consecutive candles in direction) → MARKET entry, chase now
  * If price already moved 2x ATR past key level → DO NOT CHASE — set entry at next support/resistance
  * Always specify in entry field: "LIMIT — wait for pullback" OR "MARKET — chase now" OR "WAIT — move extended, next entry at X"
`}

Respond ONLY with JSON (no markdown):
{"signal":"LONG or SHORT${degenMode ? '' : ' or NEUTRAL'}","confidence":${degenMode ? '60-95' : '55-95'},"accuracy":55-92,"bias":"punchy uppercase one-liner${degenMode ? ' — aggressive' : ''}","reasoning":"3-4 sentences covering trend, momentum, volume, and key levels","caution":"${degenMode ? '1 sentence max — key risk only' : '1-2 sentences on specific caution flags'}","confirmation":"what needs to happen to confirm the signal","alternative":"what to do if signal fails","entry":"best entry price","target":"take profit price (${degenMode ? '2x' : '3x'} ATR from entry)","stop":"stop loss price (${degenMode ? '1x' : '1.5x'} ATR from entry)","rr_ratio":"risk reward ratio e.g. 1:2","roi":"expected ROI %","position_size":"recommended % of capital${degenMode ? ' — up to 15% on high conviction' : ''}","risk":"LOW or MEDIUM or HIGH","risk_reason":"one sentence explaining risk","sentiment_impact":"one sentence on Fear & Greed and funding rate impact"}`;

  try {
    const r=await fetch(`${SERVER}/analyze`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({prompt})});
    if(!r.ok){const e=await r.json();throw new Error(e.error||'Server Error');}
    const data=await r.json();
    let raw=data.content[0].text.trim().replace(/```json|```/g,'').trim();
    const a=JSON.parse(raw);

    // Fix ROI — recalculate correctly based on signal direction
    // Also auto-correct wrong direction entries
    try {
      const entryP  = parseFloat(a.entry?.toString().replace(/[^0-9.]/g,'')) || 0;
      const targetP = parseFloat(a.target?.toString().replace(/[^0-9.]/g,'')) || 0;
      const stopP   = parseFloat(a.stop?.toString().replace(/[^0-9.]/g,'')) || 0;
      const curP = activeToken?.price || cp; // use live price not last candle close

      // Auto-correct wrong direction entries
      if (entryP > 0 && curP > 0) {
        if (a.signal === 'SHORT' && entryP < curP * 0.99) {
          // SHORT entry below current price — wrong, use current price
          a.entry = fmt(curP) + ' (MARKET)';
          a.caution = 'Entry corrected — SHORT entry must be at or above current price. ' + (a.caution || '');
        }
        if (a.signal === 'LONG' && entryP > curP * 1.01) {
          // LONG entry above current price — wrong, use current price
          a.entry = fmt(curP) + ' (MARKET)';
          a.caution = 'Entry corrected — LONG entry must be at or below current price. ' + (a.caution || '');
        }
      }

      const finalEntryP = parseFloat(a.entry?.toString().replace(/[^0-9.]/g,'')) || entryP;
      if (finalEntryP > 0 && targetP > 0) {
        let roi, rr;
        if (a.signal === 'LONG') {
          roi = ((targetP - finalEntryP) / finalEntryP * 100).toFixed(1);
          const reward = targetP - finalEntryP;
          const risk   = stopP > 0 ? finalEntryP - stopP : reward / 2;
          rr = risk > 0 ? `1:${(reward/risk).toFixed(2)}` : a.rr_ratio;
        } else if (a.signal === 'SHORT') {
          roi = ((finalEntryP - targetP) / finalEntryP * 100).toFixed(1);
          const reward = finalEntryP - targetP;
          const risk   = stopP > 0 ? stopP - finalEntryP : reward / 2;
          rr = risk > 0 ? `1:${(reward/risk).toFixed(2)}` : a.rr_ratio;
        }
        if (roi !== undefined && parseFloat(roi) > 0) {
          a.roi = `+${roi}%`;
          a.rr_ratio = rr || a.rr_ratio;
        }
      }
    } catch(e) {}
    clearInterval(tick);
    const bar=document.getElementById('pBar'),lbl=document.getElementById('pLbl');
    if(bar)bar.style.width='100%';if(lbl)lbl.textContent='100%';
    setTimeout(()=>renderResult(a, usingSimulated, dataSource),300);
  } catch(e) {
    clearInterval(tick);
    out.innerHTML=`
      <div class="out-block" style="border-left:2px solid var(--accent3)">
        <div class="out-txt" style="color:var(--accent3)">ERROR: ${e.message}</div>
        <div class="out-txt" style="margin-top:6px;color:var(--text3)">Make sure Render server is running.</div>
      </div>`;
  }
  btn.disabled=false;btn.textContent='RUN ANALYSIS';
}

function renderResult(a, isSimulated=false, dataSource='BINANCE') {
  const time=new Date().toLocaleTimeString('en-US',{hour12:false});
  const sc=a.signal==='LONG'?'sig-long':a.signal==='SHORT'?'sig-short':'sig-neut';
  const cc=a.signal==='LONG'?'cf-g':a.signal==='SHORT'?'cf-r':'cf-y';
  document.getElementById('outArea').innerHTML=`
    <div class="out-block">
      <div class="out-meta"><div class="out-tag">${activeToken.symbol}</div><div class="out-time">${time} UTC</div></div>
      ${isSimulated ? `
      <div style="background:#ff3c6e15;border:1px solid #ff3c6e40;padding:8px 10px;margin-bottom:10px;border-radius:2px;">
        <div style="font-size:9px;color:var(--accent3);letter-spacing:1px;">SIMULATED DATA — Binance unavailable</div>
        <div style="font-size:8px;color:var(--text3);margin-top:3px;">Analysis accuracy is lower. Do not trade on this signal.</div>
      </div>` : `
      <div style="font-size:8px;color:var(--text3);letter-spacing:1px;margin-bottom:8px;"> ${dataSource}</div>`}
      <div class="sig-block">
        <div class="sig-lbl">// SIGNAL</div>
        <div class="sig-val ${sc}">${a.signal}</div>
        <div class="conf-bar"><div class="conf-fill ${cc}" style="width:${a.confidence}%"></div></div>
        <div class="conf-lbl">CONFIDENCE: ${a.confidence}%</div>
        <div style="margin-top:8px;height:3px;background:var(--border2);border-radius:1px;overflow:hidden;">
          <div style="height:100%;width:${a.accuracy||70}%;background:linear-gradient(90deg,var(--accent4),#ffbe0030);border-radius:1px;transition:width 1s ease;"></div>
        </div>
        <div class="conf-lbl">ACCURACY ESTIMATE: ${a.accuracy||70}%</div>
      </div>
      <div style="margin-top:10px;padding:8px 0;border-top:1px solid var(--border)">
        <div style="font-size:8px;color:var(--text3);letter-spacing:2px;margin-bottom:4px">// BIAS</div>
        <div style="font-size:11px;color:var(--accent2);line-height:1.5;letter-spacing:1px">${a.bias}</div>
      </div>
      ${a.sentiment_impact ? `
      <div style="margin-top:10px;padding:8px 0;border-top:1px solid var(--border)">
        <div style="font-size:8px;color:var(--text3);letter-spacing:2px;margin-bottom:4px">// MARKET SENTIMENT</div>
        <div style="font-size:11px;color:var(--accent4);line-height:1.5;">${a.sentiment_impact}</div>
      </div>` : ''}
      <div style="margin-top:10px;padding:8px 0;border-top:1px solid var(--border)">
        <div style="font-size:8px;color:var(--text3);letter-spacing:2px;margin-bottom:6px">// ANALYSIS</div>
        <div class="out-txt">${a.reasoning}</div>
      </div>
      ${a.caution ? `
      <div style="margin-top:10px;padding:8px 0;border-top:1px solid var(--border)">
        <div style="font-size:8px;color:var(--accent3);letter-spacing:2px;margin-bottom:4px">CAUTION FLAGS</div>
        <div class="out-txt" style="color:var(--accent3)">${a.caution}</div>
      </div>` : ''}
      ${a.confirmation ? `
      <div style="margin-top:10px;padding:8px 0;border-top:1px solid var(--border)">
        <div style="font-size:8px;color:var(--accent);letter-spacing:2px;margin-bottom:4px">✓ CONFIRMATION</div>
        <div class="out-txt" style="color:var(--accent)">${a.confirmation}</div>
      </div>` : ''}
      ${a.alternative ? `
      <div style="margin-top:10px;padding:8px 0;border-top:1px solid var(--border)">
        <div style="font-size:8px;color:var(--accent2);letter-spacing:2px;margin-bottom:4px">REFRESH IF SIGNAL FAILS</div>
        <div class="out-txt" style="color:var(--accent2)">${a.alternative}</div>
      </div>` : ''}
      <div style="margin-top:10px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:1px;background:var(--border)">
        ${(()=>{
          const entryP = parseFloat(a.entry?.toString().replace(/[^0-9.]/g,''));
          const currP = activeToken?.price || 0;
          const isBuy = a.signal === 'LONG';
          let entryLabel = 'ENTRY';
          let entryColor = 'var(--text3)';
          let entryTag = '';
          if (entryP && currP) {
            const diff = Math.abs(currP - entryP) / entryP;
            if (diff <= 0.005) {
              entryTag = '● CMP';
              entryColor = 'var(--accent)';
            } else if (isBuy && currP > entryP) {
              entryTag = '⏳ LIMIT — wait for pullback';
              entryColor = 'var(--accent4)';
            } else if (!isBuy && currP < entryP) {
              entryTag = '⏳ LIMIT — wait for bounce';
              entryColor = 'var(--accent4)';
            } else if (isBuy && currP < entryP * 0.98) {
              entryTag = '❌ MISSED — wait for next setup';
              entryColor = 'var(--accent3)';
            } else if (!isBuy && currP > entryP * 1.02) {
              entryTag = '❌ MISSED — wait for next setup';
              entryColor = 'var(--accent3)';
            } else {
              entryTag = '🎯 NEAR ENTRY';
              entryColor = 'var(--accent2)';
            }
          }
          return `
          <div style="background:var(--bg3);padding:8px 6px;grid-column:span 3;">
            <div style="font-size:7px;letter-spacing:1px;margin-bottom:3px;color:${entryColor}">${entryTag || 'ENTRY'}</div>
            <div style="font-size:13px;color:var(--text);font-family:'Rajdhani',sans-serif;font-weight:700">${a.entry}</div>
          </div>
          <div style="background:var(--bg3);padding:8px 6px">
            <div style="font-size:7px;color:var(--accent);letter-spacing:1px;margin-bottom:3px">TAKE PROFIT</div>
            <div style="font-size:10px;color:var(--accent);font-family:'Rajdhani',sans-serif;font-weight:600">${a.target}</div>
          </div>
          <div style="background:var(--bg3);padding:8px 6px">
            <div style="font-size:7px;color:var(--accent3);letter-spacing:1px;margin-bottom:3px">STOP LOSS</div>
            <div style="font-size:10px;color:var(--accent3);font-family:'Rajdhani',sans-serif;font-weight:600">${a.stop}</div>
          </div>
          `;
        })()}
      </div>
      <div style="margin-top:1px;display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--border)">
        <div style="background:var(--bg3);padding:8px 6px">
          <div style="font-size:7px;color:var(--text3);letter-spacing:1px;margin-bottom:3px">RISK/REWARD</div>
          <div style="font-size:13px;color:var(--accent2);font-family:'Rajdhani',sans-serif;font-weight:700">${a.rr_ratio||'1:2'}</div>
        </div>
        <div style="background:var(--bg3);padding:8px 6px">
          <div style="font-size:7px;color:var(--text3);letter-spacing:1px;margin-bottom:3px">EXPECTED ROI</div>
          <div style="font-size:13px;font-family:'Rajdhani',sans-serif;font-weight:700;color:var(--accent)">${a.roi||'—'}</div>
        </div>
      </div>
      ${a.position_size ? `
      <div style="margin-top:1px;background:var(--bg3);padding:10px 10px;border:1px solid #00ff9d25;">
        <div style="font-size:7px;color:var(--text3);letter-spacing:1px;margin-bottom:4px">💰 RECOMMENDED POSITION SIZE</div>
        <div style="font-size:16px;color:var(--accent);font-family:'Orbitron',sans-serif;font-weight:700;text-shadow:var(--glow)">${a.position_size}</div>
        <div style="font-size:8px;color:var(--text3);margin-top:3px;letter-spacing:1px;">Based on ${a.confidence}% confidence + ${a.risk} risk</div>
      </div>` : ''}
      <div style="margin-top:8px;display:flex;align-items:center;justify-content:space-between">
        <div style="font-size:8px;color:var(--text3);letter-spacing:1px">RISK</div>
        <div style="font-size:9px;padding:2px 10px;border:1px solid;letter-spacing:1px;
          ${a.risk==='LOW'?'border-color:#00ff9d40;color:var(--accent);background:#00ff9d10':
            a.risk==='HIGH'?'border-color:#ff3c6e40;color:var(--accent3);background:#ff3c6e10':
            'border-color:#ffbe0040;color:var(--accent4);background:#ffbe0010'}">${a.risk}</div>
      </div>
      ${a.risk_reason ? `<div style="margin-top:5px;font-size:9px;color:var(--text3);letter-spacing:1px;">${a.risk_reason}</div>` : ''}

      <!-- SIGNAL TIMER -->
      <div style="margin-top:10px;padding:10px;border:1px solid var(--border2);background:var(--bg3);">
        <div style="font-size:8px;color:var(--text3);letter-spacing:2px;margin-bottom:6px;">⏱ SIGNAL VALIDITY TIMER</div>
        <div id="timerDisplay" style="font-size:18px;color:var(--text3);font-family:'Orbitron',sans-serif;font-weight:700;">--:--</div>
        <div id="timerStatus" style="font-size:8px;color:var(--text3);margin-top:3px;letter-spacing:1px;">Tap below to start tracking this setup</div>
        <button id="setTimerBtn" onclick="activateTimer()" style="margin-top:8px;width:100%;background:#00ff9d10;border:1px solid #00ff9d40;color:var(--accent);font-family:'Share Tech Mono',monospace;font-size:10px;padding:7px;cursor:pointer;letter-spacing:2px;">
          ⏱ SET TIMER
        </button>
      </div>

      <div style="margin-top:10px;padding-top:8px;border-top:1px solid var(--border);font-size:8px;color:var(--text3);letter-spacing:1px;line-height:1.8">
        NOT FINANCIAL ADVICE. AI-GENERATED ONLY.
      </div>
    </div>`;

  // Store signal for manual timer activation
  activeSignal = a;
  timerActive = false;

  // Check for signal reversal against last history entry for this token
  checkSignalReversal(a, activeToken, activeTimeframe);

  // Save to history
  saveToHistory(a, activeToken, activeTimeframe);

  // Register with notification bot for 24/7 monitoring
  registerSignalForMonitoring(a, activeToken, activeTimeframe);

  // Auto send analysis to Telegram
  sendToTelegram();
}

// ============================================================
// SIGNAL REVERSAL DETECTION
// ============================================================
function checkSignalReversal(newSignal, token, timeframe) {
  if (!token || newSignal.signal === 'NEUTRAL') return;

  // Find last analysis for this token + timeframe
  const last = analysisHistory.find(h =>
    h.symbol === token.symbol &&
    h.timeframe === timeframe &&
    h.signal !== 'NEUTRAL' &&
    h.status === 'active'
  );

  if (!last) return;
  if (last.signal === newSignal.signal) return; // Same direction — no reversal

  // REVERSAL DETECTED!
  const prevEmoji = last.signal === 'LONG' ? '▲' : '▼';
  const newEmoji  = newSignal.signal === 'LONG' ? '▲' : '▼';

  // Show reversal banner in AI tab
  const outArea = document.getElementById('outArea');
  if (outArea) {
    const banner = document.createElement('div');
    banner.style.cssText = 'padding:10px 14px;background:#ff3c6e15;border:1px solid #ff3c6e40;border-left:3px solid var(--accent3);margin-bottom:4px;animation:fadeUp 0.3s ease;';
    banner.innerHTML = `
      <div style="font-size:9px;color:var(--accent3);letter-spacing:2px;margin-bottom:4px;">SIGNAL REVERSAL DETECTED</div>
      <div style="font-size:10px;color:var(--text2);line-height:1.6;">
        Previous: ${prevEmoji} <b style="color:var(--text)">${last.signal}</b> from ${new Date(last.timestamp).toLocaleTimeString('en-US',{hour:'2-digit',minute:'2-digit'})}<br>
        New: ${newEmoji} <b style="color:var(--text)">${newSignal.signal}</b> (${newSignal.confidence}% confidence)
      </div>
      <div style="font-size:9px;color:var(--accent4);margin-top:6px;">⚠️ Consider closing your ${last.signal} and reviewing the new setup.</div>
    `;
    outArea.prepend(banner);
  }

  // Mark old entry as dead
  const oldIdx = analysisHistory.findIndex(h => h.id === last.id);
  if (oldIdx >= 0) {
    analysisHistory[oldIdx].status = 'dead';
    localStorage.setItem('cipherHistory', JSON.stringify(analysisHistory));
  }

  // Send Telegram notification
  sendTelegramMessage(
    `🔄 <b>SIGNAL REVERSAL — ${token.symbol}</b>\n\n` +
    `Previous: ${prevEmoji} <b>${last.signal}</b> (from ${new Date(last.timestamp).toLocaleTimeString('en-US',{hour:'2-digit',minute:'2-digit'})})\n` +
    `New: ${newEmoji} <b>${newSignal.signal}</b> (${newSignal.confidence}% confidence)\n\n` +
    `📝 ${newSignal.reasoning || ''}\n\n` +
    `🎯 New Entry: <b>${newSignal.entry}</b>\n` +
    `✅ New TP: <b>${newSignal.target}</b>\n` +
    `🛑 New SL: <b>${newSignal.stop}</b>\n\n` +
    `⚠️ Consider closing your ${last.signal} position and reviewing the new setup.\n\n` +
    `⚠️ NOT FINANCIAL ADVICE`,
    'analysis'
  );
}

// ============================================================
// TELEGRAM NOTIFICATION CONFIG
// ============================================================
async function sendTelegramMessage(text, type='general') {
  // Use personal notification if user has linked Telegram
  await sendPersonalNotification(text, type);
}

async function registerSignalForMonitoring(a, token, timeframe) {
  if (!currentUser || !a || !token) return;
  if (!userProfile?.telegram_verified) return;
  try {
    const tfMap = {'5M':'5m','15M':'15m','1H':'1h','4H':'4h','1D':'1d','1W':'1w'};
    await fetch(`${NOTIFY_BOT_URL}/register-signal`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        user_id:   currentUser.id,
        symbol:    token.symbol,
        signal:    a.signal,
        entry:     a.entry,
        target:    a.target,
        stop:      a.stop,
        timeframe: tfMap[timeframe] || '1h',
        price:     token.price,
      })
    });
    console.log(`Signal registered: ${token.symbol} ${a.signal}`);
  } catch(e) {
    console.error('Register signal error:', e);
  }
}

async function sendToTelegram() {
  const btn = document.getElementById('tgBtn');
  if (!activeSignal || !activeToken) return;
  if (!userProfile?.telegram_verified) {
    alert('Link your Telegram in Settings first!');
    return;
  }
  if (btn) { btn.textContent = '⏳ SENDING...'; btn.disabled = true; }
  const a = activeSignal;
  const emoji = a.signal==='LONG' ? '▲' : a.signal==='SHORT' ? '▼' : '—';
  const msg = (
    `${emoji} <b>CIPHER SIGNAL — ${activeToken.symbol}</b>\n\n` +
    `Signal: <b>${a.signal}</b> (${a.confidence}% confidence)\n` +
    `Timeframe: <b>${activeTimeframe}</b>\n\n` +
    `ENTRY <b>${a.entry}</b>\n` +
    `TP <b>${a.target}</b>\n` +
    `SL <b>${a.stop}</b>\n` +
    `R/R <b>${a.rr_ratio||'1:2'}</b>\n` +
    `📈 ROI: <b>${a.roi||'—'}</b>\n` +
    `💰 Position: <b>${a.position_size||'—'}</b>\n\n` +
    `📝 ${a.reasoning||''}\n` +
    `⚠️ ${a.caution||''}\n\n` +
    `⏱ Signal expires in: <b>${getTimerLabel()}</b>\n\n` +
    `⚠️ NOT FINANCIAL ADVICE`
  );
  await sendTelegramMessage(msg, 'analysis');
  if (btn) { btn.textContent = '✅ SENT'; btn.disabled = false; }
  setTimeout(() => { if (btn) btn.textContent = '📱 SEND TO TELEGRAM'; }, 3000);
}

// ============================================================
// SIGNAL EXPIRY TIMER
// ============================================================
let signalTimerInterval = null;
let signalExpiry = null;
let activeSignal = null;
let setupMonitorInterval = null;
let timerActive = false;

const EXPIRY_MINUTES = {'5M': 5, '15M': 15, '1H': 60, '4H': 240, '1D': 1440, '1W': 10080};

function getTimerLabel() {
  if (!signalExpiry) return '--:--';
  const remaining = Math.max(0, signalExpiry - Date.now());
  const mins = Math.floor(remaining / 60000);
  const secs = Math.floor((remaining % 60000) / 1000);
  if (mins >= 60) return `${Math.floor(mins/60)}h ${mins%60}m`;
  return `${mins}m ${secs.toString().padStart(2,'0')}s`;
}

function activateTimer() {
  if (!activeSignal || !activeToken) return;
  const btn = document.getElementById('setTimerBtn');
  if (btn) { btn.textContent = 'TIMER ACTIVE'; btn.disabled = true; btn.style.opacity = '0.6'; }
  startSignalTimer(activeSignal);
  startSetupMonitor(activeSignal);
  // Auto-send to Telegram when timer is set
  sendToTelegram();
}

function startSignalTimer(a) {
  timerActive = true;
  if (signalTimerInterval) clearInterval(signalTimerInterval);
  const minutes = EXPIRY_MINUTES[activeTimeframe] || 60;
  signalExpiry = Date.now() + minutes * 60 * 1000;

  signalTimerInterval = setInterval(() => {
    const remaining = Math.max(0, signalExpiry - Date.now());
    const pct = remaining / (minutes * 60 * 1000);
    const display = document.getElementById('timerDisplay');
    const status = document.getElementById('timerStatus');
    if (!display) { clearInterval(signalTimerInterval); return; }

    display.textContent = getTimerLabel();

    if (remaining === 0) {
      // Check if price is still near entry zone
      const entryPrice = parseFloat(a.entry?.toString().replace(/[^0-9.]/g,''));
      const currentPrice = activeToken?.price;
      const atr = parseFloat(a.stop) ? Math.abs(parseFloat(a.entry) - parseFloat(a.stop)) / 1.5 : 0;
      const nearEntry = entryPrice && currentPrice && atr
        ? Math.abs(currentPrice - entryPrice) < atr * 1.5
        : false;

      if (nearEntry) {
        // Timer elapsed but price still near entry — still valid!
        display.style.color = 'var(--accent4)';
        display.textContent = 'ELAPSED';
        if (status) {
          status.textContent = 'Timer elapsed but setup still valid — re-run analysis to confirm';
          status.style.color = 'var(--accent4)';
        }
        sendTelegramMessage(
          `⏱ <b>TIMER ELAPSED — ${activeToken?.symbol}</b>\n\n` +
          `Your ${activeTimeframe} ${a.signal} timer ran out BUT price is still near entry.\n\n` +
          `Current: <b>$${currentPrice}</b> | Entry: <b>${a.entry}</b>\n\n` +
          `Setup may still be valid — re-run analysis to confirm before entering.`,
          'expired'
        );
      } else {
        // Timer elapsed and price moved away — invalidated
        display.style.color = 'var(--accent3)';
        display.textContent = 'EXPIRED';
        if (status) {
          status.textContent = '❌ Signal expired — price moved away from entry';
          status.style.color = 'var(--accent3)';
        }
        sendTelegramMessage(
          `❌ <b>SIGNAL EXPIRED — ${activeToken?.symbol}</b>\n\n` +
          `Your ${activeTimeframe} ${a.signal} signal has expired and price moved away from entry.\n\n` +
          `Do not enter this trade. Re-run analysis for a fresh signal.`,
          'expired'
        );
      }
      clearInterval(signalTimerInterval);
      timerActive = false;
      updateHistoryStatus(nearEntry ? 'active' : 'expired');
    } else if (pct < 0.2) {
      display.style.color = 'var(--accent3)';
      if (status) { status.textContent = 'Expiring soon — act now or skip'; status.style.color = 'var(--accent3)'; }
    } else if (pct < 0.5) {
      display.style.color = 'var(--accent4)';
      if (status) { status.textContent = 'Signal still valid'; status.style.color = 'var(--text3)'; }
    } else {
      display.style.color = 'var(--accent)';
      if (status) { status.textContent = 'Signal fresh ✓'; status.style.color = 'var(--accent)'; }
    }
  }, 1000);
}

// ============================================================
// SETUP MONITOR — checks if price moves past entry zone
// ============================================================
function startSetupMonitor(a) {
  if (setupMonitorInterval) clearInterval(setupMonitorInterval);
  if (!a.entry || a.signal === 'NEUTRAL') return;

  const entryPrice = parseFloat(a.entry?.toString().replace(/[^0-9.]/g,''));
  const slPrice    = parseFloat(a.stop?.toString().replace(/[^0-9.]/g,''));
  const atr = slPrice ? Math.abs(entryPrice - slPrice) / 1.5 : 0;
  if (!entryPrice || !atr) return;

  let alerted = false;
  let entryAlerted = false;
  let slAlerted = false;

  setupMonitorInterval = setInterval(async () => {
    if (!activeToken || !signalExpiry || Date.now() > signalExpiry) {
      clearInterval(setupMonitorInterval);
      return;
    }

    const currentPrice = activeToken.price;
    const diff = Math.abs(currentPrice - entryPrice);
    const isBuy = a.signal === 'LONG';

    // Entry zone alert — price within 0.3% of entry
    if (!entryAlerted && diff / entryPrice < 0.003) {
      entryAlerted = true;
      sendTelegramMessage(
        `🎯 <b>ENTRY ZONE HIT — ${activeToken.symbol}</b>\n\n` +
        `Price is near your entry zone!\n` +
        `Current: <b>$${fmt(currentPrice)}</b>\n` +
        `Entry: <b>${a.entry}</b>\n\n` +
        `Signal: ${a.signal} | TP: ${a.target} | SL: ${a.stop}\n\n` +
        `⚠️ NOT FINANCIAL ADVICE`,
        'entry'
      );
    }

    // SL hit — price reached stop loss level
    if (!slAlerted && slPrice) {
      const slHit = isBuy
        ? currentPrice <= slPrice
        : currentPrice >= slPrice;

      if (slHit) {
        slAlerted = true;
        alerted = true;
        clearInterval(setupMonitorInterval);
        updateHistoryStatus('dead');

        const display = document.getElementById('timerDisplay');
        const status  = document.getElementById('timerStatus');
        if (display) { display.textContent = 'SL HIT'; display.style.color = 'var(--accent3)'; }
        if (status)  { status.textContent  = '🛑 Stop loss hit — reanalysing...'; status.style.color = 'var(--accent3)'; }

        // Notify immediately
        sendTelegramMessage(
          `🛑 <b>STOP LOSS HIT — ${activeToken.symbol}</b>\n\n` +
          `Your ${a.signal} setup hit the stop loss.\n` +
          `Current: <b>$${fmt(currentPrice)}</b> | SL was: <b>${a.stop}</b>\n\n` +
          `⏳ Running fresh analysis...`,
          'dead'
        );

        // Auto reanalysis after SL hit
        await runPostSLAnalysis(a, currentPrice);
        return;
      }
    }

    // Setup dead — price moved 1.5x ATR past entry in wrong direction
    if (!alerted) {
      const setupDead = isBuy
        ? currentPrice < entryPrice - atr * 1.5
        : currentPrice > entryPrice + atr * 1.5;

      if (setupDead) {
        alerted = true;
        clearInterval(setupMonitorInterval);
        updateHistoryStatus('dead');
        const display = document.getElementById('timerDisplay');
        const status  = document.getElementById('timerStatus');
        if (display) { display.textContent = 'DEAD'; display.style.color = 'var(--accent3)'; }
        if (status)  { status.textContent  = '❌ Setup invalidated — price moved against entry'; status.style.color = 'var(--accent3)'; }

        sendTelegramMessage(
          `❌ <b>SETUP DEAD — ${activeToken.symbol}</b>\n\n` +
          `Price moved past the entry zone.\n` +
          `Current: <b>$${fmt(currentPrice)}</b>\n` +
          `Entry was: <b>${a.entry}</b>\n\n` +
          `Signal is <b>INVALIDATED</b>. Do not enter this trade.\n` +
          `Run fresh analysis if you still want to trade ${activeToken.symbol}.`,
          'dead'
        );
      }
    }
  }, 15000);
}

// ============================================================
// POST-SL AUTO REANALYSIS
// ============================================================
async function runPostSLAnalysis(prevSignal, currentPrice) {
  if (!activeToken) return;

  const status = document.getElementById('timerStatus');
  if (status) { status.textContent = 'REANALYSING after SL hit...'; status.style.color = 'var(--accent2)'; }

  try {
    // Fetch fresh candles
    const intervalMap = {'5M':'5m','15M':'15m','1H':'1h','4H':'4h','1D':'1d','1W':'1w'};
    const interval = intervalMap[activeTimeframe] || '1h';
    const limit = {'5M':100,'15M':80,'1H':80,'4H':90,'1D':60,'1W':52}[activeTimeframe] || 80;

    let freshCandles = chartData;
    try {
      const r = await fetch(`${SERVER}/candles?symbol=${activeToken.symbol}&interval=${interval}&limit=${limit}`);
      const d = await r.json();
      if (d.candles && d.candles.length) {
        freshCandles = d.candles.map(c => ({open:c.o,high:c.h,low:c.l,close:c.c,vol:c.v}));
      }
    } catch(e) {}

    const closes = freshCandles.map(c=>c.close);
    const highs  = freshCandles.map(c=>c.high);
    const lows   = freshCandles.map(c=>c.low);
    const n = closes.length;

    // Quick RSI
    let rsi = 50, g = 0, l = 0;
    for(let i=1;i<=14&&i<n;i++){const d=closes[n-i]-closes[n-i-1];d>0?g+=d:l-=d;}
    rsi = Math.round(100-(100/(1+(l===0?100:g/l))));

    // EMA
    const k20=2/21; let e20=closes[0];
    closes.forEach(v=>{e20=v*k20+e20*(1-k20);});
    const k50=2/51; let e50=closes[0];
    closes.forEach(v=>{e50=v*k50+e50*(1-k50);});

    // ATR
    let atrSum=0;
    for(let i=Math.max(1,n-14);i<n;i++){
      atrSum+=Math.max(highs[i]-lows[i],Math.abs(highs[i]-closes[i-1]),Math.abs(lows[i]-closes[i-1]));
    }
    const atr=atrSum/Math.min(14,n-1);

    const prompt = `You are CIPHER, elite crypto analyst. A trader's ${prevSignal.signal} position on ${activeToken.symbol} just hit its stop loss at ${prevSignal.stop}. Current price is $${currentPrice}.

PREVIOUS SETUP:
- Signal: ${prevSignal.signal}
- Entry: ${prevSignal.entry}
- SL: ${prevSignal.stop} ← HIT
- TP: ${prevSignal.target}
- Timeframe: ${activeTimeframe}

FRESH MARKET DATA:
- Current Price: $${currentPrice}
- RSI(14): ${rsi}
- EMA20: $${e20.toFixed(4)} | EMA50: $${e50.toFixed(4)}
- Trend: ${currentPrice > e20 && e20 > e50 ? 'BULLISH' : currentPrice < e20 && e20 < e50 ? 'BEARISH' : 'MIXED'}
- ATR: $${atr.toFixed(4)}

Analyze the current market structure after this SL hit. Should the trader:
1. Re-enter LONG (better entry found)
2. Flip to SHORT (market reversed)  
3. Stay out (market too choppy)

Respond ONLY in JSON:
{"action":"RE_ENTRY or REVERSAL or STAY_OUT","signal":"LONG or SHORT or NEUTRAL","confidence":40-92,"reasoning":"2-3 sentences explaining what happened and what to do","entry":"price or null","target":"price or null","stop":"price or null","rr":"1:X or null","caution":"key risk"}`;

    const r = await fetch(`${SERVER}/analyze`, {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({prompt})
    });
    const data = await r.json();
    const raw = data.content?.[0]?.text?.trim().replace(/```json|```/g,'').trim();
    const result = JSON.parse(raw);

    // Action labels
    const actionEmoji = result.action === 'RE_ENTRY' ? '🔁' : result.action === 'REVERSAL' ? '🔄' : '⏸';
    const actionLabel = result.action === 'RE_ENTRY' ? 'RE-ENTRY POSSIBLE' : result.action === 'REVERSAL' ? 'REVERSAL DETECTED' : 'STAY OUT';
    const sigEmoji = result.signal === 'LONG' ? '▲' : result.signal === 'SHORT' ? '▼' : '—';

    // Update timer display
    const display = document.getElementById('timerDisplay');
    if (display) {
      display.textContent = actionLabel;
      display.style.color = result.action === 'STAY_OUT' ? 'var(--accent4)' : result.action === 'REVERSAL' ? 'var(--accent3)' : 'var(--accent)';
      display.style.fontSize = '11px';
    }
    if (status) {
      status.textContent = result.reasoning;
      status.style.color = 'var(--text2)';
    }

    // Build notification message
    let msg = `${actionEmoji} <b>${actionLabel} — ${activeToken.symbol}</b>\n\n`;
    msg += `🛑 Previous ${prevSignal.signal} hit SL at ${prevSignal.stop}\n\n`;
    msg += `${sigEmoji} New Signal: <b>${result.signal}</b> (${result.confidence}% confidence)\n`;
    msg += `📝 ${result.reasoning}\n\n`;

    if (result.action !== 'STAY_OUT' && result.entry) {
      msg += `ENTRY <b>${result.entry}</b>\n`;
      msg += `TP <b>${result.target}</b>\n`;
      msg += `SL <b>${result.stop}</b>\n`;
      msg += `R/R <b>${result.rr}</b>\n\n`;
    }

    msg += `⚠️ ${result.caution}\n\n`;
    msg += `⚠️ NOT FINANCIAL ADVICE`;

    // Send to notification bot
    await sendTelegramMessage(msg, 'dead');

    // Show in analysis tab
    const outArea = document.getElementById('outArea');
    if (outArea) {
      const div = document.createElement('div');
      div.className = 'out-block';
      div.style.borderLeft = `2px solid ${result.action === 'STAY_OUT' ? 'var(--accent4)' : result.action === 'REVERSAL' ? 'var(--accent3)' : 'var(--accent)'}`;
      div.innerHTML = `
        <div style="font-size:10px;color:var(--text3);letter-spacing:2px;margin-bottom:8px;">POST-SL REANALYSIS</div>
        <div style="font-size:14px;font-weight:700;color:${result.action==='STAY_OUT'?'var(--accent4)':result.action==='REVERSAL'?'var(--accent3)':'var(--accent)'};margin-bottom:6px;">${actionEmoji} ${actionLabel}</div>
        <div style="font-size:10px;color:var(--text2);margin-bottom:8px;">${sigEmoji} ${result.signal} — ${result.confidence}% confidence</div>
        <div style="font-size:9px;color:var(--text2);line-height:1.6;margin-bottom:8px;">${result.reasoning}</div>
        ${result.action !== 'STAY_OUT' && result.entry ? `
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;margin-bottom:8px;">
          <div style="background:var(--bg3);padding:6px;text-align:center;">
            <div style="font-size:7px;color:var(--text3);letter-spacing:1px;">ENTRY</div>
            <div style="font-size:11px;color:var(--text);">${result.entry}</div>
          </div>
          <div style="background:var(--bg3);padding:6px;text-align:center;">
            <div style="font-size:7px;color:var(--accent);letter-spacing:1px;">TP</div>
            <div style="font-size:11px;color:var(--accent);">${result.target}</div>
          </div>
          <div style="background:var(--bg3);padding:6px;text-align:center;">
            <div style="font-size:7px;color:var(--accent3);letter-spacing:1px;">SL</div>
            <div style="font-size:11px;color:var(--accent3);">${result.stop}</div>
          </div>
        </div>` : ''}
        <div style="font-size:8px;color:var(--accent4);">⚠️ ${result.caution}</div>
      `;
      outArea.prepend(div);
      // Switch to AI tab to show result
      showTab('ai');
    }

  } catch(e) {
    console.error('Post-SL reanalysis error:', e);
    if (status) { status.textContent = '❌ Reanalysis failed — run manually'; status.style.color = 'var(--accent3)'; }
    sendTelegramMessage(
      `🛑 <b>SL HIT — ${activeToken?.symbol}</b>\n\nReanalysis failed. Please run analysis manually.\n\n⚠️ NOT FINANCIAL ADVICE`,
      'dead'
    );
  }
}

// TIMEFRAME
document.querySelectorAll('.tf-btn').forEach(btn=>{
  btn.addEventListener('click', async ()=>{
    document.querySelectorAll('.tf-btn').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    activeTimeframe=btn.dataset.tf;
    zoomLevel = 1;
    await generateChartData();
    drawChart();
    updateIndicators();
    gradeToken();
    savePageState();
  });
});

// MATRIX RAIN
const chars='01◈⬡∑∇アイウ';
setInterval(()=>{
  let h='';for(let i=0;i<60;i++){h+=chars[Math.floor(Math.random()*chars.length)];if(i%5===4)h+='\n';}
  document.getElementById('matrix').textContent=h;
},120);

// ============================================================
// ZOOM & TOOLTIP
// ============================================================
let tooltipCandle = null;

function handleChartTap(e) {
  if (!chartData.length) return;
  const cv = document.getElementById('chartCanvas');
  const rect = cv.getBoundingClientRect();
  const clientX = e.touches ? e.changedTouches[0].clientX : e.clientX;
  const x = clientX - rect.left;
  const W = rect.width;

  const visibleCount = Math.floor(chartData.length * zoomLevel);
  const startIdx = chartData.length - visibleCount;
  const n = visibleCount;
  const cw = (W - 40) / n;

  const idx = Math.floor((x - 20) / cw);
  if (idx < 0 || idx >= n) { tooltipCandle = null; drawChart(); return; }

  const candle = chartData[startIdx + idx];
  tooltipCandle = candle;
  drawChart();

  // Draw tooltip
  const cv2 = document.getElementById('chartCanvas');
  const ctx = cv2.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const allP = chartData.slice(startIdx).flatMap(c=>[c.high,c.low]);
  const minP=Math.min(...allP),maxP=Math.max(...allP),rng=maxP-minP||1;
  const H = rect.height;
  const cTop=H*0.04,cH=H*0.63;
  const py=p=>cTop+cH-((p-minP)/rng)*cH;

  ctx.scale(1/dpr, 1/dpr);
  const cx2 = (20 + idx * cw + cw * 0.5) * dpr;

  const lines = [
    `O: ${fmt(candle.open)}`,
    `H: ${fmt(candle.high)}`,
    `L: ${fmt(candle.low)}`,
    `C: ${fmt(candle.close)}`,
  ];

  const boxW = 110, boxH = lines.length * 16 + 12;
  let bx = cx2/dpr + 10;
  if (bx + boxW > W) bx = cx2/dpr - boxW - 10;
  const by = cTop + 10;

  ctx.scale(dpr, dpr);
  ctx.fillStyle = '#020408ee';
  ctx.strokeStyle = '#00ff9d60';
  ctx.lineWidth = 1;
  ctx.fillRect(bx, by, boxW, boxH);
  ctx.strokeRect(bx, by, boxW, boxH);
  ctx.fillStyle = '#00ff9d';
  ctx.font = '9px "Share Tech Mono"';
  lines.forEach((l, i) => ctx.fillText(l, bx + 8, by + 14 + i * 16));
}

// PINCH ZOOM
let pinchStartDist = null;
let pinchStartZoom = 1;

document.querySelector('.chart-area').addEventListener('touchstart', e => {
  if (e.touches.length === 2) {
    pinchStartDist = Math.hypot(
      e.touches[0].clientX - e.touches[1].clientX,
      e.touches[0].clientY - e.touches[1].clientY
    );
    pinchStartZoom = zoomLevel;
  }
}, {passive: true});

document.querySelector('.chart-area').addEventListener('touchmove', e => {
  if (e.touches.length === 2 && pinchStartDist) {
    e.preventDefault();
    const dist = Math.hypot(
      e.touches[0].clientX - e.touches[1].clientX,
      e.touches[0].clientY - e.touches[1].clientY
    );
    const scale = pinchStartDist / dist; // pinch in = zoom in
    zoomLevel = Math.min(1, Math.max(0.1, pinchStartZoom * scale));
    drawChart();
  }
}, {passive: false});

document.querySelector('.chart-area').addEventListener('touchend', e => {
  if (e.touches.length < 2) pinchStartDist = null;
  // Single tap = tooltip
  if (e.changedTouches.length === 1 && !pinchStartDist) {
    handleChartTap(e);
  }
}, {passive: true});

// RESIZE
new ResizeObserver(drawChart).observe(document.querySelector('.chart-area'));

// Save active token to sessionStorage whenever it changes
function savePageState() {
  if (activeToken) {
    sessionStorage.setItem('cipher_active_token', activeToken.id);
    sessionStorage.setItem('cipher_active_tf', activeTimeframe);
  }
}

// Restore state after prices load
async function restorePageState() {
  const savedId = sessionStorage.getItem('cipher_active_token');
  const savedTf = sessionStorage.getItem('cipher_active_tf');
  if (!savedId) return;
  const token = TOKENS.find(t => t.id === savedId);
  if (!token) return;
  if (savedTf) {
    activeTimeframe = savedTf;
    document.querySelectorAll('.tf-btn').forEach(b => b.classList.toggle('active', b.dataset.tf === savedTf));
  }
  await goDetail(token.id);
}

// INIT — check auth first then load
initAuth().then(ok => {
  if (!ok) return;
  fetchPrices().then(() => restorePageState());
  setInterval(fetchPrices, 60000);
});
</script>
</body>
</html>

