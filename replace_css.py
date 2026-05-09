import re

with open('main.html', 'r') as f:
    content = f.read()

# Add font
if '<link href="https://fonts.googleapis.com/css2?family=Inter:' not in content:
    content = content.replace('<title>FreshTrack — Smart Food Expiry Tracker</title>', '<title>FreshTrack — Smart Food Expiry Tracker</title>\n<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />')

new_style = """<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg1: #ffffff;
    --bg2: #f7f7f9;
    --bg3: #f0f0f4;
    --txt1: #111827;
    --txt2: #6b7280;
    --bdr: rgba(0,0,0,0.08);
    --bdr2: rgba(0,0,0,0.15);
    --green: #10b981;
    --green-d: #059669;
    --gbg: #ecfdf5; --gtxt: #065f46; --gbdr: #a7f3d0;
    --abg: #fffbeb; --atxt: #92400e; --abdr: #fde68a;
    --rbg: #fef2f2; --rtxt: #991b1b; --rbdr: #fecaca;
    --bbg: #eff6ff; --btxt: #1e3a8a; --bbdr: #bfdbfe;
    --radius: 12px; --radius-lg: 16px; --radius-xl: 24px;
    --font: 'Inter', system-ui, -apple-system, sans-serif;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg1: #18181b; --bg2: #27272a; --bg3: #09090b;
      --txt1: #f9fafb; --txt2: #9ca3af;
      --bdr: rgba(255,255,255,0.08); --bdr2: rgba(255,255,255,0.16);
      --gbg: #064e3b; --gtxt: #6ee7b7; --gbdr: #047857;
      --abg: #78350f; --atxt: #fcd34d; --abdr: #b45309;
      --rbg: #7f1d1d; --rtxt: #fca5a5; --rbdr: #b91c1c;
      --bbg: #1e3a8a; --btxt: #93c5fd; --bbdr: #1d4ed8;
    }
  }
  body {
    font-family: var(--font);
    background: var(--bg3);
    color: var(--txt1);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    padding: 16px;
    transition: background-color 0.3s ease;
  }

  /* ── FRAME ── */
  .frame {
    width: 100%;
    max-width: 440px;
    background: var(--bg1);
    border-radius: var(--radius-xl);
    border: 1px solid var(--bdr);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: 0 10px 40px rgba(0,0,0,0.08);
    height: calc(100vh - 32px);
    transition: all 0.3s ease;
  }

  /* ── TOPBAR ── */
  .topbar {
    background: var(--bg1);
    border-bottom: 1px solid var(--bdr);
    padding: 16px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-shrink: 0;
  }
  .logo { font-size: 20px; font-weight: 700; color: var(--txt1); letter-spacing: -0.3px; display: flex; align-items: center; gap: 6px; }
  .logo span { color: var(--green); }
  .topright { display: flex; align-items: center; gap: 12px; }
  .alert-badge {
    font-size: 12px; font-weight: 600; padding: 4px 10px; border-radius: 20px;
    background: var(--rbg); color: var(--rtxt); display: none;
    border: 1px solid var(--rbdr); box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  }
  .avatar {
    width: 36px; height: 36px; border-radius: 50%;
    background: linear-gradient(135deg, var(--green), var(--green-d));
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; font-weight: 700; color: #fff;
    box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
  }

  /* ── NAV ── */
  .nav {
    background: var(--bg1);
    border-bottom: 1px solid var(--bdr);
    display: flex;
    overflow-x: auto;
    flex-shrink: 0;
  }
  .nav::-webkit-scrollbar { display: none; }
  .nav-tab {
    flex: 1; min-width: 72px;
    padding: 12px 6px;
    text-align: center; font-size: 12px; font-weight: 500;
    color: var(--txt2); cursor: pointer;
    border-bottom: 2px solid transparent;
    transition: all 0.2s ease; user-select: none; white-space: nowrap;
  }
  .nav-tab:hover { color: var(--txt1); }
  .nav-tab.active { color: var(--green); border-bottom-color: var(--green); }
  .nav-icon { font-size: 20px; display: block; margin-bottom: 4px; transition: transform 0.2s ease; }
  .nav-tab:hover .nav-icon { transform: translateY(-2px); }

  /* ── BODY ── */
  .body { padding: 20px 16px; background: var(--bg2); flex: 1; overflow-y: auto; scroll-behavior: smooth; }
  .section { display: none; animation: fadeIn 0.3s ease; }
  .section.active { display: block; }
  @keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }

  /* ── STATS ROW ── */
  .stats {
    display: grid; grid-template-columns: repeat(4, minmax(0,1fr));
    gap: 10px; margin-bottom: 24px;
  }
  .stat {
    background: var(--bg1); border-radius: var(--radius-lg);
    padding: 16px 10px; text-align: center;
    border: 1px solid var(--bdr); box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  .stat:hover { transform: translateY(-2px); box-shadow: 0 6px 12px rgba(0,0,0,0.05); }
  .stat-label { font-size: 11px; font-weight: 600; color: var(--txt2); margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px; }
  .stat-val { font-size: 24px; font-weight: 700; color: var(--txt1); }
  .stat-val.g { color: var(--green); }
  .stat-val.a { color: #d97706; }
  .stat-val.r { color: #dc2626; }

  /* ── TOOLBAR ── */
  .toolbar { display: flex; gap: 10px; margin-bottom: 16px; }
  .toolbar input {
    flex: 1; padding: 12px 16px; font-size: 14px; font-family: var(--font);
    border-radius: var(--radius); border: 1px solid var(--bdr2);
    background: var(--bg1); color: var(--txt1); outline: none;
    transition: all 0.2s; box-shadow: 0 1px 3px rgba(0,0,0,0.02);
  }
  .toolbar input:focus { border-color: var(--green); box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15); }
  .btn-add {
    padding: 12px 20px; background: var(--green); color: #fff;
    border: none; border-radius: var(--radius); font-size: 14px;
    cursor: pointer; font-weight: 600; white-space: nowrap;
    transition: all 0.2s; box-shadow: 0 2px 6px rgba(16, 185, 129, 0.25);
  }
  .btn-add:hover { background: var(--green-d); transform: translateY(-1px); box-shadow: 0 4px 10px rgba(16, 185, 129, 0.35); }
  .btn-add:active { transform: translateY(0); }

  /* ── FILTER PILLS ── */
  .pills { display: flex; gap: 8px; margin-bottom: 24px; flex-wrap: wrap; }
  .pill {
    padding: 8px 16px; border-radius: 24px; font-size: 13px; font-weight: 500;
    cursor: pointer; border: 1px solid var(--bdr); user-select: none;
    background: var(--bg1); color: var(--txt2); transition: all 0.2s;
  }
  .pill:hover { background: var(--bg3); transform: scale(1.02); }
  .pill.f-all  { background: var(--txt1); color: var(--bg1); border-color: var(--txt1); }
  .pill.f-g    { background: var(--gbg); color: var(--gtxt); border-color: var(--gbdr); }
  .pill.f-a    { background: var(--abg); color: var(--atxt); border-color: var(--abdr); }
  .pill.f-r    { background: var(--rbg); color: var(--rtxt); border-color: var(--rbdr); }

  /* ── ITEM CARD ── */
  .items { display: flex; flex-direction: column; gap: 12px; }
  .item-card {
    background: var(--bg1); border-radius: var(--radius-lg);
    border: 1px solid var(--bdr); padding: 14px 16px;
    display: flex; align-items: center; gap: 14px;
    transition: all 0.2s ease; box-shadow: 0 2px 6px rgba(0,0,0,0.01);
  }
  .item-card:hover { border-color: var(--bdr2); box-shadow: 0 6px 16px rgba(0,0,0,0.06); transform: translateY(-2px); }
  .item-icon {
    width: 46px; height: 46px; border-radius: var(--radius);
    display: flex; align-items: center; justify-content: center;
    font-size: 22px; flex-shrink: 0;
  }
  .item-icon.g { background: var(--gbg); }
  .item-icon.a { background: var(--abg); }
  .item-icon.r { background: var(--rbg); }
  .item-info { flex: 1; min-width: 0; }
  .item-name { font-size: 15px; font-weight: 600; color: var(--txt1); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 2px; }
  .item-meta { font-size: 13px; color: var(--txt2); }
  .badge {
    padding: 4px 10px; border-radius: 12px; font-size: 12px;
    font-weight: 600; flex-shrink: 0; white-space: nowrap;
  }
  .badge.g { background: var(--gbg); color: var(--gtxt); }
  .badge.a { background: var(--abg); color: var(--atxt); }
  .badge.r { background: var(--rbg); color: var(--rtxt); }

  /* ── FRIDGE TOGGLE ── */
  .fridge-toggle {
    width: 38px; height: 22px; border-radius: 11px; border: none;
    cursor: pointer; flex-shrink: 0; transition: background 0.2s ease;
    position: relative; outline: none; margin-left: 4px;
  }
  .fridge-toggle.on  { background: var(--green); }
  .fridge-toggle.off { background: var(--bdr2); }
  .fridge-toggle::after {
    content: ''; position: absolute; top: 2px;
    width: 18px; height: 18px; border-radius: 50%;
    background: #fff; transition: left 0.2s ease, transform 0.2s ease;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2);
  }
  .fridge-toggle.on::after  { left: 18px; }
  .fridge-toggle.off::after { left: 2px; }
  .fridge-toggle:active::after { width: 22px; }

  /* ── DELETE BUTTON ── */
  .btn-del {
    background: var(--bg2); border: 1px solid var(--bdr); cursor: pointer;
    width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-size: 14px; color: var(--txt2); transition: all 0.15s; margin-left: 4px; opacity: 0;
  }
  .item-card:hover .btn-del { opacity: 1; }
  .btn-del:hover { background: var(--rbg); color: var(--rtxt); border-color: var(--rbdr); }
  @media (max-width: 767px) { .btn-del { opacity: 1; background: transparent; border: none; width: auto; height: auto; } .btn-del:hover { background: transparent; } }

  /* ── FRIDGE SECTION ── */
  .fridge-hint {
    font-size: 14px; color: var(--txt2); text-align: center;
    padding: 16px; background: var(--bg1);
    border-radius: var(--radius-lg); margin-bottom: 24px;
    border: 1px solid var(--bdr); box-shadow: 0 2px 8px rgba(0,0,0,0.02); line-height: 1.5;
  }
  .fridge-hint span { color: var(--green); font-weight: 600; }
  .fridge-empty {
    text-align: center; padding: 48px 20px;
    color: var(--txt2); font-size: 15px; line-height: 1.8;
  }

  /* ── CATEGORIES SECTION ── */
  .cat-group { margin-bottom: 28px; }
  .cat-header {
    display: flex; align-items: center; gap: 12px;
    margin-bottom: 16px; padding-bottom: 12px;
    border-bottom: 1px solid var(--bdr);
  }
  .cat-icon-big { font-size: 26px; }
  .cat-name { font-size: 17px; font-weight: 600; color: var(--txt1); flex: 1; }
  .cat-count {
    font-size: 13px; font-weight: 500; padding: 4px 10px; border-radius: 12px;
    background: var(--bg1); color: var(--txt2); border: 1px solid var(--bdr);
  }

  /* ── ALERTS SECTION ── */
  .alert-card {
    background: var(--bg1); border: 1px solid var(--bdr);
    border-radius: var(--radius-lg); padding: 18px; margin-bottom: 14px;
    display: flex; gap: 16px; align-items: flex-start;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02); transition: transform 0.2s ease;
  }
  .alert-card:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(0,0,0,0.06); }
  .alert-dot {
    width: 12px; height: 12px; border-radius: 50%;
    flex-shrink: 0; margin-top: 5px; box-shadow: 0 0 0 3px var(--bg2);
  }
  .alert-dot.r { background: #dc2626; box-shadow: 0 0 0 3px var(--rbg); }
  .alert-dot.a { background: #d97706; box-shadow: 0 0 0 3px var(--abg); }
  .alert-title { font-size: 16px; font-weight: 600; color: var(--txt1); }
  .alert-sub   { font-size: 14px; color: var(--txt2); margin-top: 4px; }
  .alert-actions { display: flex; gap: 10px; margin-top: 16px; flex-wrap: wrap; }
  .btn-action {
    font-size: 13px; font-weight: 600; padding: 8px 14px; border-radius: var(--radius);
    border: 1px solid var(--bdr2); background: transparent;
    color: var(--txt1); cursor: pointer; transition: all 0.2s ease;
  }
  .btn-action:hover { background: var(--bg2); }
  .btn-action.primary { background: var(--green); color: #fff; border-color: var(--green); }
  .btn-action.primary:hover { background: var(--green-d); box-shadow: 0 2px 6px rgba(16, 185, 129, 0.2); }

  /* ── RECIPES SECTION ── */
  .recipe-card {
    background: var(--bg1); border: 1px solid var(--bdr);
    border-radius: var(--radius-lg); padding: 20px; margin-bottom: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02); transition: transform 0.2s ease;
  }
  .recipe-card:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(0,0,0,0.06); }
  .recipe-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 10px; }
  .recipe-name { font-size: 17px; font-weight: 600; color: var(--txt1); margin-bottom: 4px; }
  .recipe-time { font-size: 14px; color: var(--txt2); }
  .urgency-tag {
    font-size: 12px; font-weight: 600; padding: 6px 12px; border-radius: 12px;
    background: var(--abg); color: var(--atxt); flex-shrink: 0;
  }
  .urgency-tag.low { background: var(--gbg); color: var(--gtxt); }
  .ing-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 16px; }
  .ing-chip {
    font-size: 13px; font-weight: 500; padding: 6px 12px; border-radius: 14px;
    background: var(--bg2); color: var(--txt2); border: 1px solid var(--bdr);
  }
  .ing-chip.expiring { background: var(--abg); color: var(--atxt); border-color: var(--abdr); }
  .recipe-steps {
    margin-top: 16px; padding: 16px 20px;
    background: var(--bg2); border-radius: var(--radius);
    font-size: 14px; color: var(--txt1); line-height: 1.6; border: 1px solid var(--bdr);
  }
  .recipe-steps ol { padding-left: 20px; margin-top: 0; margin-bottom: 0; }
  .recipe-steps li { margin-bottom: 8px; }
  .recipe-steps li:last-child { margin-bottom: 0; }
  details summary {
    font-size: 14px; font-weight: 600; color: var(--green); cursor: pointer;
    margin-top: 16px; list-style: none; user-select: none; display: inline-block;
  }
  details summary::-webkit-details-marker { display: none; }
  details summary:hover { color: var(--green-d); text-decoration: underline; }

  /* ── EMPTY STATE ── */
  .empty { text-align: center; padding: 48px 20px; color: var(--txt2); font-size: 15px; background: var(--bg1); border-radius: var(--radius-lg); border: 1px dashed var(--bdr2); }

  /* ── MODAL ── */
  .modal-overlay {
    display: none; position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.6); backdrop-filter: blur(4px);
    align-items: center; justify-content: center;
    z-index: 200; padding: 20px; opacity: 0; transition: opacity 0.3s ease;
  }
  .modal-overlay.open { display: flex; opacity: 1; }
  .modal {
    background: var(--bg1); border-radius: var(--radius-xl);
    padding: 28px; width: 100%; max-width: 440px;
    border: 1px solid var(--bdr2); box-shadow: 0 24px 48px rgba(0,0,0,0.2);
    transform: translateY(20px); transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  }
  .modal-overlay.open .modal { transform: translateY(0); }
  .modal-title { font-size: 20px; font-weight: 700; color: var(--txt1); margin-bottom: 24px; }
  .form-field { margin-bottom: 20px; }
  .form-label { font-size: 14px; font-weight: 600; color: var(--txt2); margin-bottom: 8px; display: block; }
  .form-input {
    width: 100%; padding: 14px 16px; font-size: 15px; font-family: var(--font);
    border: 1px solid var(--bdr2); border-radius: var(--radius);
    background: var(--bg2); color: var(--txt1); outline: none;
    transition: all 0.2s ease;
  }
  .form-input:focus { border-color: var(--green); background: var(--bg1); box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.1); }
  .fridge-row { 
    display: flex; align-items: center; gap: 14px;
    padding: 16px; background: var(--bg2);
    border-radius: var(--radius); border: 1px solid var(--bdr);
    cursor: pointer; transition: background 0.2s ease;
  }
  .fridge-row:hover { background: var(--bg3); }
  .fridge-row input { width: 20px; height: 20px; accent-color: var(--green); cursor: pointer; }
  .fridge-row label { font-size: 15px; font-weight: 500; color: var(--txt1); cursor: pointer; flex: 1; }
  .modal-btns { display: flex; gap: 16px; margin-top: 32px; }
  .modal-btns button {
    flex: 1; padding: 14px; border-radius: var(--radius);
    font-size: 15px; cursor: pointer; font-weight: 600; font-family: var(--font); transition: all 0.2s ease;
  }
  .btn-cancel {
    background: transparent; border: 1px solid var(--bdr2);
    color: var(--txt1);
  }
  .btn-cancel:hover { background: var(--bg2); }
  .btn-save { background: var(--green); color: #fff; border: none; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2); }
  .btn-save:hover { background: var(--green-d); box-shadow: 0 6px 16px rgba(16, 185, 129, 0.3); transform: translateY(-1px); }

  /* ── SCROLLBAR ── */
  ::-webkit-scrollbar { width: 8px; height: 8px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: var(--bdr2); border-radius: 10px; }
  ::-webkit-scrollbar-thumb:hover { background: var(--txt2); }

  /* ── RESPONSIVE LAPTOP / DESKTOP LAYOUT ── */
  @media (min-width: 768px) {
    body { padding: 40px; }
    .frame {
      max-width: 1200px;
      height: calc(100vh - 80px);
      display: grid;
      grid-template-areas:
        "topbar topbar"
        "nav body";
      grid-template-columns: 260px 1fr;
      grid-template-rows: auto 1fr;
      border-radius: var(--radius-xl);
    }
    .topbar { grid-area: topbar; padding: 20px 32px; border-bottom: 1px solid var(--bdr); z-index: 10; }
    .logo { font-size: 22px; }
    .nav {
      grid-area: nav;
      flex-direction: column;
      border-bottom: none;
      border-right: 1px solid var(--bdr);
      background: var(--bg1);
      padding: 32px 16px; gap: 12px;
    }
    .nav-tab {
      flex: none;
      border-bottom: none;
      border-radius: var(--radius-lg);
      text-align: left;
      padding: 16px 24px;
      display: flex;
      align-items: center;
      gap: 16px;
      font-size: 16px; font-weight: 600;
    }
    .nav-tab.active { background: var(--gbg); color: var(--gtxt); box-shadow: 0 2px 8px rgba(0,0,0,0.02); border-left: 4px solid var(--green); border-bottom: none; }
    .nav-icon { margin-bottom: 0; font-size: 22px; }
    
    .body { grid-area: body; padding: 40px; background: var(--bg2); border-top-left-radius: 0; }
    
    .stats { gap: 20px; margin-bottom: 40px; }
    .stat { padding: 24px; border-radius: var(--radius-xl); }
    .stat-label { font-size: 13px; }
    .stat-val { font-size: 36px; }
    
    .toolbar { margin-bottom: 32px; gap: 20px; }
    .toolbar input { padding: 16px 24px; font-size: 16px; border-radius: var(--radius-lg); }
    .btn-add { padding: 16px 32px; font-size: 16px; border-radius: var(--radius-lg); }
    
    .items { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 20px; }
    #cat-body .items { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 20px; }
    #alert-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(440px, 1fr)); gap: 20px; }
    #recipe-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(440px, 1fr)); gap: 20px; }
    
    .alert-card, .recipe-card { margin-bottom: 0; height: 100%; border-radius: var(--radius-xl); padding: 24px; }
    
    .item-card { padding: 20px 24px; }
    .item-icon { width: 56px; height: 56px; font-size: 26px; }
    .item-name { font-size: 17px; }
    .item-meta { font-size: 14px; }
  }
  @media (min-width: 1024px) {
    .stats { grid-template-columns: repeat(4, 1fr); }
  }
</style>"""

content = re.sub(r'<style>.*?</style>', new_style, content, flags=re.DOTALL)

with open('main.html', 'w') as f:
    f.write(content)
