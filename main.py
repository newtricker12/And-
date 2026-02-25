from flask import Flask, render_template_string, request, redirect, url_for, session, jsonify, flash

def render_template(name, **kwargs):
    return render_template_string(TEMPLATES[name], **kwargs)

TEMPLATES = {}
TEMPLATES['login.html'] = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E2EE Automation - Login</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: "Segoe UI", sans-serif; background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .container { background: rgba(255,255,255,0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 40px; width: 100%; max-width: 420px; box-shadow: 0 20px 60px rgba(0,0,0,0.5); }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { color: #e94560; font-size: 28px; font-weight: 700; letter-spacing: 2px; }
        .logo p { color: #aaa; font-size: 13px; margin-top: 5px; }
        .tabs { display: flex; margin-bottom: 25px; background: rgba(255,255,255,0.05); border-radius: 10px; overflow: hidden; }
        .tab-btn { flex: 1; padding: 12px; background: none; border: none; color: #aaa; cursor: pointer; font-size: 14px; font-weight: 600; transition: all 0.3s; }
        .tab-btn.active { background: #e94560; color: white; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .form-group { margin-bottom: 18px; }
        .form-group label { display: block; color: #ccc; font-size: 13px; margin-bottom: 6px; }
        .form-group input { width: 100%; padding: 12px 15px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; color: white; font-size: 14px; outline: none; transition: border-color 0.3s; }
        .form-group input:focus { border-color: #e94560; }
        .btn { width: 100%; padding: 13px; background: linear-gradient(135deg, #e94560, #c23152); border: none; border-radius: 10px; color: white; font-size: 15px; font-weight: 700; cursor: pointer; letter-spacing: 1px; }
        .btn:hover { opacity: 0.9; }
        .alert { padding: 10px 15px; border-radius: 8px; margin-bottom: 15px; font-size: 13px; }
        .alert-success { background: rgba(76,175,80,0.2); color: #81c784; border: 1px solid rgba(76,175,80,0.3); }
        .alert-error { background: rgba(233,69,96,0.2); color: #ef9a9a; border: 1px solid rgba(233,69,96,0.3); }
        .alert-warning { background: rgba(255,152,0,0.2); color: #ffcc80; border: 1px solid rgba(255,152,0,0.3); }
        .alert-info { background: rgba(33,150,243,0.2); color: #90caf9; border: 1px solid rgba(33,150,243,0.3); }
    </style>
</head>
<body>
<div class="container">
    <div class="logo"><h1>âš¡ E2EE AUTO</h1><p>Facebook Messenger Automation</p></div>
    {% with messages = get_flashed_messages(with_categories=true) %}{% if messages %}{% for category, message in messages %}<div class="alert alert-{{ category }}">{{ message }}</div>{% endfor %}{% endif %}{% endwith %}
    <div class="tabs">
        <button class="tab-btn active" onclick="showTab(\'login\', this)">Login</button>
        <button class="tab-btn" onclick="showTab(\'signup\', this)">Sign Up</button>
    </div>
    <div id="login" class="tab-content active">
        <form method="POST" action="/login">
            <div class="form-group"><label>Username</label><input type="text" name="username" placeholder="Enter username" required></div>
            <div class="form-group"><label>Password</label><input type="password" name="password" placeholder="Enter password" required></div>
            <button type="submit" class="btn">LOGIN</button>
        </form>
    </div>
    <div id="signup" class="tab-content">
        <form method="POST" action="/signup">
            <div class="form-group"><label>Username</label><input type="text" name="username" placeholder="Choose username" required></div>
            <div class="form-group"><label>Password</label><input type="password" name="password" placeholder="Choose password" required></div>
            <div class="form-group"><label>Confirm Password</label><input type="password" name="confirm_password" placeholder="Confirm password" required></div>
            <button type="submit" class="btn">CREATE ACCOUNT</button>
        </form>
    </div>
</div>
<script>
function showTab(tab, btn) {
    document.querySelectorAll(".tab-content").forEach(t => t.classList.remove("active"));
    document.querySelectorAll(".tab-btn").forEach(t => t.classList.remove("active"));
    document.getElementById(tab).classList.add("active");
    btn.classList.add("active");
}
</script>
</body></html>'''

TEMPLATES['approval.html'] = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E2EE - Approval</title>
    <style>
        * { margin:0;padding:0;box-sizing:border-box; }
        body { font-family:"Segoe UI",sans-serif; background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460); min-height:100vh; display:flex; align-items:center; justify-content:center; color:white; }
        .container { background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:20px; padding:40px; max-width:480px; width:100%; text-align:center; }
        h1 { color:#e94560; font-size:24px; margin-bottom:10px; }
        p { color:#aaa; font-size:14px; margin-bottom:20px; }
        .key-box { background:rgba(233,69,96,0.1); border:1px solid #e94560; border-radius:12px; padding:20px; margin-bottom:25px; }
        .key-box label { color:#aaa; font-size:12px; display:block; margin-bottom:8px; }
        .key { color:#e94560; font-size:22px; font-weight:700; letter-spacing:3px; }
        .btn { display:inline-block; padding:13px 30px; border:none; border-radius:10px; color:white; font-size:15px; font-weight:700; cursor:pointer; text-decoration:none; width:100%; margin-bottom:10px; }
        .btn-wa { background:linear-gradient(135deg,#25d366,#128c7e); }
        .btn-primary { background:linear-gradient(135deg,#e94560,#c23152); }
        .btn-logout { display:block; margin-top:15px; color:#aaa; text-decoration:none; font-size:13px; }
        .status { padding:12px; border-radius:10px; margin-bottom:20px; font-size:13px; background:rgba(255,152,0,0.15); color:#ffcc80; border:1px solid rgba(255,152,0,0.3); }
    </style>
</head>
<body>
<div class="container">
    <h1>ðŸ”‘ Key Approval</h1>
    <p>Welcome <strong style="color:white;">{{ username }}</strong>! Admin approval required.</p>
    <div class="status">â³ Waiting for admin approval...</div>
    <div class="key-box">
        <label>Your Unique Key</label>
        <div class="key">{{ user_key }}</div>
    </div>
    <a href="https://api.whatsapp.com/send?phone=918290090930&text=Hello+Sir+Please+approve+my+key:+{{ user_key }}+Username:+{{ username }}" target="_blank" class="btn btn-wa">ðŸ“± Request via WhatsApp</a>
    <form method="POST" action="/request_approval">
        <button type="submit" class="btn btn-primary">ðŸ“¨ Submit Approval Request</button>
    </form>
    <a href="/logout" class="btn-logout">â† Logout</a>
</div>
<script>
setInterval(function(){
    fetch("/check_approval").then(r=>r.json()).then(d=>{ if(d.approved) window.location.href="/dashboard"; });
}, 5000);
</script>
</body></html>'''

TEMPLATES['dashboard.html'] = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E2EE Automation - Dashboard</title>
    <style>
        * { margin:0;padding:0;box-sizing:border-box; }
        body { font-family:"Segoe UI",sans-serif; background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460); min-height:100vh; color:white; }
        .navbar { background:rgba(0,0,0,0.3); padding:15px 30px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.1); }
        .navbar h1 { color:#e94560; font-size:20px; letter-spacing:2px; }
        .main { padding:30px; max-width:1000px; margin:0 auto; }
        .stats { display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:20px; margin-bottom:30px; }
        .stat-card { background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:15px; padding:20px; text-align:center; }
        .stat-card .value { font-size:32px; font-weight:700; color:#e94560; }
        .stat-card .label { color:#aaa; font-size:13px; margin-top:5px; }
        .badge { display:inline-block; padding:5px 15px; border-radius:20px; font-size:13px; font-weight:700; }
        .badge-running { background:rgba(76,175,80,0.2); color:#81c784; border:1px solid rgba(76,175,80,0.4); }
        .badge-stopped { background:rgba(233,69,96,0.2); color:#ef9a9a; border:1px solid rgba(233,69,96,0.4); }
        .card { background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:15px; padding:25px; margin-bottom:25px; }
        .card h2 { color:#e94560; font-size:16px; margin-bottom:20px; letter-spacing:1px; }
        .form-group { margin-bottom:15px; }
        .form-group label { display:block; color:#ccc; font-size:13px; margin-bottom:6px; }
        .form-group input, .form-group textarea { width:100%; padding:11px 14px; background:rgba(255,255,255,0.07); border:1px solid rgba(255,255,255,0.15); border-radius:10px; color:white; font-size:13px; outline:none; font-family:inherit; }
        .form-group input:focus, .form-group textarea:focus { border-color:#e94560; }
        .form-group textarea { height:100px; resize:vertical; }
        .btn { padding:11px 24px; border:none; border-radius:10px; font-size:14px; font-weight:700; cursor:pointer; letter-spacing:0.5px; }
        .btn-primary { background:linear-gradient(135deg,#e94560,#c23152); color:white; }
        .btn-success { background:linear-gradient(135deg,#4caf50,#388e3c); color:white; }
        .btn-danger { background:linear-gradient(135deg,#f44336,#c62828); color:white; }
        .btn-row { display:flex; gap:12px; flex-wrap:wrap; }
        .log-box { background:rgba(0,0,0,0.4); border:1px solid rgba(255,255,255,0.1); border-radius:10px; padding:15px; height:220px; overflow-y:auto; font-family:monospace; font-size:12px; color:#aaffaa; }
        .alert { padding:10px 15px; border-radius:8px; margin-bottom:15px; font-size:13px; }
        .alert-success { background:rgba(76,175,80,0.2); color:#81c784; }
        .alert-error { background:rgba(233,69,96,0.2); color:#ef9a9a; }
        .alert-warning { background:rgba(255,152,0,0.2); color:#ffcc80; }
        .alert-info { background:rgba(33,150,243,0.2); color:#90caf9; }
    </style>
</head>
<body>
<div class="navbar">
    <h1>âš¡ E2EE AUTO</h1>
</div>
<div class="main">
    {% with messages = get_flashed_messages(with_categories=true) %}{% if messages %}{% for category, message in messages %}<div class="alert alert-{{ category }}">{{ message }}</div>{% endfor %}{% endif %}{% endwith %}
    <div class="stats">
        <div class="stat-card"><div class="value" id="msgCount">{{ automation_state.message_count }}</div><div class="label">Messages Sent</div></div>
        <div class="stat-card">
            <div class="value">
                <span id="statusBadge" class="badge {{ \'badge-running\' if automation_state.running else \'badge-stopped\' }}">
                    {{ \'ðŸŸ¢ RUNNING\' if automation_state.running else \'ðŸ”´ STOPPED\' }}
                </span>
            </div>
            <div class="label">Status</div>
        </div>
        <div class="stat-card"><div class="value">{{ user_config.delay if user_config else 30 }}s</div><div class="label">Message Delay</div></div>
    </div>
    <div class="card">
        <h2>ðŸŽ® AUTOMATION CONTROLS</h2>
        <div class="btn-row">
            <button class="btn btn-success" onclick="startAuto()">â–¶ Start</button>
            <button class="btn btn-danger" onclick="stopAuto()">â¹ Stop</button>
        </div>
    </div>
    <div class="card">
        <h2>âš™ï¸ CONFIGURATION</h2>
        <form method="POST" action="/save_config">
            <div class="form-group"><label>Facebook Chat ID / Username</label><input type="text" name="chat_id" value="{{ user_config.chat_id if user_config else \'\' }}" placeholder="e.g. 100003995292301"></div>
            <div class="form-group"><label>Name Prefix (optional)</label><input type="text" name="name_prefix" value="{{ user_config.name_prefix if user_config else \'\' }}" placeholder="e.g. Hello"></div>
            <div class="form-group"><label>Delay (seconds)</label><input type="number" name="delay" value="{{ user_config.delay if user_config else 30 }}" min="5" max="3600"></div>
            <div class="form-group"><label>Facebook Cookies</label><textarea name="cookies" placeholder="Paste cookies here...">{{ user_config.cookies if user_config else \'\' }}</textarea></div>
            <div class="form-group"><label>Messages (one per line)</label><textarea name="messages" placeholder="Hello!&#10;How are you?">{{ user_config.messages if user_config else \'\' }}</textarea></div>
            <button type="submit" class="btn btn-primary">ðŸ’¾ Save Configuration</button>
        </form>
    </div>
    <div class="card">
        <h2>ðŸ“‹ LOGS</h2>
        <div class="log-box" id="logBox"><span style="color:#666;">Waiting for logs...</span></div>
    </div>
</div>
<script>
function startAuto(){ fetch("/start_automation",{method:"POST"}).then(r=>r.json()).then(d=>{ alert(d.message); updateStatus(); }); }
function stopAuto(){ fetch("/stop_automation",{method:"POST"}).then(r=>r.json()).then(d=>{ alert(d.message); updateStatus(); }); }
function updateStatus(){
    fetch("/get_status").then(r=>r.json()).then(d=>{
        document.getElementById("msgCount").textContent = d.message_count;
        var b = document.getElementById("statusBadge");
        b.className = "badge " + (d.running ? "badge-running" : "badge-stopped");
        b.textContent = d.running ? "ðŸŸ¢ RUNNING" : "ðŸ”´ STOPPED";
    });
}
function updateLogs(){
    fetch("/get_logs").then(r=>r.json()).then(d=>{
        if(d.logs && d.logs.length > 0){
            var lb = document.getElementById("logBox");
            lb.innerHTML = d.logs.map(l=>"<div>"+l+"</div>").join("");
            lb.scrollTop = lb.scrollHeight;
        }
    });
}
setInterval(updateStatus, 3000);
setInterval(updateLogs, 3000);
updateStatus(); updateLogs();
</script>
</body></html>'''

TEMPLATES['admin_login.html'] = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Login</title>
    <style>
        * { margin:0;padding:0;box-sizing:border-box; }
        body { font-family:"Segoe UI",sans-serif; background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460); min-height:100vh; display:flex; align-items:center; justify-content:center; }
        .container { background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:20px; padding:40px; max-width:380px; width:100%; }
        h1 { color:#e94560; text-align:center; margin-bottom:25px; font-size:22px; }
        .form-group { margin-bottom:18px; }
        .form-group label { display:block; color:#ccc; font-size:13px; margin-bottom:6px; }
        .form-group input { width:100%; padding:12px 15px; background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); border-radius:10px; color:white; font-size:14px; outline:none; }
        .form-group input:focus { border-color:#e94560; }
        .btn { width:100%; padding:13px; background:linear-gradient(135deg,#e94560,#c23152); border:none; border-radius:10px; color:white; font-size:15px; font-weight:700; cursor:pointer; }
        .alert { padding:10px 15px; border-radius:8px; margin-bottom:15px; font-size:13px; background:rgba(233,69,96,0.2); color:#ef9a9a; }
    </style>
</head>
<body>
<div class="container">
    <h1>ðŸ” Admin Panel</h1>
    {% with messages = get_flashed_messages(with_categories=true) %}{% if messages %}{% for category, message in messages %}<div class="alert">{{ message }}</div>{% endfor %}{% endif %}{% endwith %}
    <form method="POST" action="/admin">
        <div class="form-group"><label>Admin Password</label><input type="password" name="password" placeholder="Enter admin password" required></div>
        <button type="submit" class="btn">ACCESS ADMIN PANEL</button>
    </form>
</div>
</body></html>'''

TEMPLATES['admin_panel.html'] = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel</title>
    <style>
        * { margin:0;padding:0;box-sizing:border-box; }
        body { font-family:"Segoe UI",sans-serif; background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460); min-height:100vh; color:white; padding:30px; }
        h1 { color:#e94560; font-size:24px; margin-bottom:25px; }
        h2 { color:#ccc; font-size:16px; margin-bottom:15px; }
        .card { background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:15px; padding:25px; margin-bottom:25px; max-width:900px; }
        table { width:100%; border-collapse:collapse; }
        th { text-align:left; padding:10px 12px; color:#aaa; font-size:12px; text-transform:uppercase; border-bottom:1px solid rgba(255,255,255,0.1); }
        td { padding:10px 12px; font-size:13px; border-bottom:1px solid rgba(255,255,255,0.05); color:#ddd; }
        .key { font-family:monospace; color:#e94560; font-weight:700; font-size:12px; }
        .btn-approve { padding:6px 14px; background:linear-gradient(135deg,#4caf50,#388e3c); border:none; border-radius:7px; color:white; font-size:12px; font-weight:700; cursor:pointer; text-decoration:none; display:inline-block; }
        .btn-direct { padding:6px 14px; background:linear-gradient(135deg,#2196f3,#1565c0); border:none; border-radius:7px; color:white; font-size:12px; font-weight:700; cursor:pointer; text-decoration:none; display:inline-block; }
        .empty { color:#666; font-size:14px; text-align:center; padding:20px; }
        .badge-ok { display:inline-block; padding:4px 10px; background:rgba(76,175,80,0.2); color:#81c784; border-radius:12px; font-size:11px; font-weight:700; }
        .badge-pending { display:inline-block; padding:4px 10px; background:rgba(255,152,0,0.2); color:#ffcc80; border-radius:12px; font-size:11px; font-weight:700; }
        a.back { display:inline-block; margin-top:10px; color:#aaa; text-decoration:none; font-size:13px; }
        .form-row { display:flex; gap:10px; margin-top:10px; }
        .form-row input { flex:1; padding:10px 14px; background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); border-radius:8px; color:white; font-size:13px; outline:none; }
        .form-row button { padding:10px 20px; background:linear-gradient(135deg,#e94560,#c23152); border:none; border-radius:8px; color:white; font-size:13px; font-weight:700; cursor:pointer; }
        .alert { padding:10px 15px; border-radius:8px; margin-bottom:15px; font-size:13px; }
        .alert-success { background:rgba(76,175,80,0.2); color:#81c784; }
        .alert-error { background:rgba(233,69,96,0.2); color:#ef9a9a; }
        .alert-warning { background:rgba(255,152,0,0.2); color:#ffcc80; }
        .alert-info { background:rgba(33,150,243,0.2); color:#90caf9; }
    </style>
</head>
<body>
<h1>ðŸ›¡ï¸ ADMIN PANEL</h1>
{% with messages = get_flashed_messages(with_categories=true) %}{% if messages %}{% for category, message in messages %}<div class="alert alert-{{ category }}">{{ message }}</div>{% endfor %}{% endif %}{% endwith %}

<div class="card">
    <h2>ðŸ‘¥ All Registered Users ({{ all_users|length }})</h2>
    {% if all_users %}
    <table>
        <tr><th>#</th><th>Username</th><th>Registered</th><th>Status</th><th>Action</th></tr>
        {% for user in all_users %}
        {% set user_approved = approved_keys.values()|selectattr("name","equalto",user[1])|list|length > 0 %}
        <tr>
            <td>{{ user[0] }}</td>
            <td><strong>{{ user[1] }}</strong></td>
            <td>{{ user[2][:16] }}</td>
            <td>{% if user_approved %}<span class="badge-ok">âœ… APPROVED</span>{% else %}<span class="badge-pending">â³ PENDING</span>{% endif %}</td>
            <td>
                {% for key, info in pending.items() %}{% if info.name == user[1] %}<a href="/admin/approve/{{ key }}" class="btn-approve">âœ… Approve</a>{% endif %}{% endfor %}
                {% if not user_approved %}
                <form method="POST" action="/admin/approve_by_username" style="display:inline">
                    <input type="hidden" name="username" value="{{ user[1] }}">
                    <button type="submit" class="btn-direct">ðŸ”‘ Force Approve</button>
                </form>
                {% endif %}
            </td>
        </tr>
        {% endfor %}
    </table>
    {% else %}<div class="empty">No users registered yet</div>{% endif %}
</div>

<div class="card">
    <h2>â³ Pending Approval Requests ({{ pending|length }})</h2>
    {% if pending %}
    <table>
        <tr><th>Key</th><th>Username</th><th>Requested At</th><th>Action</th></tr>
        {% for key, info in pending.items() %}
        <tr><td class="key">{{ key }}</td><td>{{ info.name }}</td><td>{{ info.timestamp }}</td><td><a href="/admin/approve/{{ key }}" class="btn-approve">âœ… Approve</a></td></tr>
        {% endfor %}
    </table>
    {% else %}<div class="empty">No pending requests</div>{% endif %}
</div>

<div class="card">
    <h2>ðŸ”‘ Approve Key Directly</h2>
    <p style="color:#aaa;font-size:13px;margin-bottom:10px;">Paste user key manually to approve</p>
    <div class="form-row">
        <form method="POST" action="/admin/approve_direct" style="display:flex;gap:10px;width:100%">
            <input type="text" name="key" placeholder="Paste KEY-XXXXXXXX here" required>
            <input type="text" name="username" placeholder="Username" required>
            <button type="submit">âœ… Approve</button>
        </form>
    </div>
</div>

<div class="card">
    <h2>âœ… Approved Keys ({{ approved_keys|length }})</h2>
    {% if approved_keys %}
    <table>
        <tr><th>Key</th><th>Username</th><th>Approved At</th></tr>
        {% for key, info in approved_keys.items() %}
        <tr><td class="key">{{ key }}</td><td>{{ info.name }}</td><td>{{ info.get("timestamp","â€”") }}</td></tr>
        {% endfor %}
    </table>
    {% else %}<div class="empty">No approved keys yet</div>{% endif %}
</div>

<a href="/" class="back">â† Back to Home</a>
</body></html>'''
import time
import threading
import uuid
import hashlib
import os
import json
import urllib.parse
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import database as db
import requests

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-make-it-strong'
app.config['SESSION_TYPE'] = 'filesystem'

ADMIN_PASSWORD = "ROWEDYE2E2025"
WHATSAPP_NUMBER = "918290090930"
APPROVAL_FILE = "approved_keys.json"
PENDING_FILE = "pending_approvals.json"
ADMIN_UID = "100003995292301"

# Global automation states
automation_states = {}

class AutomationState:
    def __init__(self):
        self.running = False
        self.message_count = 0
        self.logs = []
        self.message_rotation_index = 0

def generate_user_key(username, password):
    combined = f"{username}:{password}"
    key_hash = hashlib.sha256(combined.encode()).hexdigest()[:8].upper()
    return f"KEY-{key_hash}"

def load_approved_keys():
    if os.path.exists(APPROVAL_FILE):
        try:
            with open(APPROVAL_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_approved_keys(keys):
    with open(APPROVAL_FILE, 'w') as f:
        json.dump(keys, f, indent=2)

def load_pending_approvals():
    if os.path.exists(PENDING_FILE):
        try:
            with open(PENDING_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_pending_approvals(pending):
    with open(PENDING_FILE, 'w') as f:
        json.dump(pending, f, indent=2)

def send_whatsapp_message(user_name, approval_key):
    message = f"Ã°Å¸Â©Â· HELLO ABHI JAAT SIR PLEASE Ã¢ÂÂ¤Ã¯Â¸Â\nMy name is {user_name}\nPlease approve my key:\nÃ°Å¸â€â€˜ {approval_key}"
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://api.whatsapp.com/send?phone={WHATSAPP_NUMBER}&text={encoded_message}"
    return whatsapp_url

def check_approval(key):
    # Admin key is always approved
    if key == generate_admin_key():
        return True
    approved_keys = load_approved_keys()
    return key in approved_keys

def generate_admin_key():
    combined = f"admin:{ADMIN_PASSWORD}"
    key_hash = hashlib.sha256(combined.encode()).hexdigest()[:8].upper()
    return f"KEY-{key_hash}"

def approve_key_directly(key, username):
    approved_keys = load_approved_keys()
    approved_keys[key] = {"name": username, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
    save_approved_keys(approved_keys)

def log_message(msg, automation_state=None, user_id=None):
    timestamp = time.strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
    
    if automation_state:
        automation_state.logs.append(formatted_msg)
    elif user_id and user_id in automation_states:
        automation_states[user_id].logs.append(formatted_msg)

def find_message_input(driver, process_id, automation_state=None, user_id=None):
    log_message(f'{process_id}: Finding message input...', automation_state, user_id)
    time.sleep(3)
    
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
    except Exception:
        pass
    
    try:
        page_title = driver.title
        page_url = driver.current_url
        log_message(f'{process_id}: Page Title: {page_title}', automation_state, user_id)
        log_message(f'{process_id}: Page URL: {page_url}', automation_state, user_id)
    except Exception as e:
        log_message(f'{process_id}: Could not get page info: {e}', automation_state, user_id)
    
    message_input_selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"][data-lexical-editor="true"]',
        'div[aria-label*="message" i][contenteditable="true"]',
        'div[aria-label*="Message" i][contenteditable="true"]',
        'div[contenteditable="true"][spellcheck="true"]',
        '[role="textbox"][contenteditable="true"]',
        'textarea[placeholder*="message" i]',
        'div[aria-placeholder*="message" i]',
        'div[data-placeholder*="message" i]',
        '[contenteditable="true"]',
        'textarea',
        'input[type="text"]'
    ]
    
    log_message(f'{process_id}: Trying {len(message_input_selectors)} selectors...', automation_state, user_id)
    
    for idx, selector in enumerate(message_input_selectors):
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            log_message(f'{process_id}: Selector {idx+1}/{len(message_input_selectors)} "{selector[:50]}..." found {len(elements)} elements', automation_state, user_id)
            
            for element in elements:
                try:
                    is_editable = driver.execute_script("""
                        return arguments[0].contentEditable === 'true' || 
                               arguments[0].tagName === 'TEXTAREA' || 
                               arguments[0].tagName === 'INPUT';
                    """, element)
                    
                    if is_editable:
                        log_message(f'{process_id}: Found editable element with selector #{idx+1}', automation_state, user_id)
                        
                        try:
                            element.click()
                            time.sleep(0.5)
                        except:
                            pass
                        
                        element_text = driver.execute_script("return arguments[0].placeholder || arguments[0].getAttribute('aria-label') || arguments[0].getAttribute('aria-placeholder') || '';", element).lower()
                        
                        keywords = ['message', 'write', 'type', 'send', 'chat', 'msg', 'reply', 'text', 'aa']
                        if any(keyword in element_text for keyword in keywords):
                            log_message(f'{process_id}: Ã¢Å“â€¦ Found message input with text: {element_text[:50]}', automation_state, user_id)
                            return element
                        elif idx < 10:
                            log_message(f'{process_id}: Ã¢Å“â€¦ Using primary selector editable element (#{idx+1})', automation_state, user_id)
                            return element
                        elif selector == '[contenteditable="true"]' or selector == 'textarea' or selector == 'input[type="text"]':
                            log_message(f'{process_id}: Ã¢Å“â€¦ Using fallback editable element', automation_state, user_id)
                            return element
                except Exception as e:
                    log_message(f'{process_id}: Element check failed: {str(e)[:50]}', automation_state, user_id)
                    continue
        except Exception as e:
            continue
    
    try:
        page_source = driver.page_source
        log_message(f'{process_id}: Page source length: {len(page_source)} characters', automation_state, user_id)
        if 'contenteditable' in page_source.lower():
            log_message(f'{process_id}: Page contains contenteditable elements', automation_state, user_id)
        else:
            log_message(f'{process_id}: No contenteditable elements found in page', automation_state, user_id)
    except Exception:
        pass
    
    return None

def setup_browser(automation_state=None, user_id=None):
    log_message('Setting up Chrome browser...', automation_state, user_id)
    
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
    
    chromium_paths = [
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
        '/usr/bin/google-chrome',
        '/usr/bin/chrome'
    ]
    
    for chromium_path in chromium_paths:
        if Path(chromium_path).exists():
            chrome_options.binary_location = chromium_path
            log_message(f'Found Chromium at: {chromium_path}', automation_state, user_id)
            break
    
    chromedriver_paths = [
        '/usr/bin/chromedriver',
        '/usr/local/bin/chromedriver'
    ]
    
    driver_path = None
    for driver_candidate in chromedriver_paths:
        if Path(driver_candidate).exists():
            driver_path = driver_candidate
            log_message(f'Found ChromeDriver at: {driver_path}', automation_state, user_id)
            break
    
    try:
        from selenium.webdriver.chrome.service import Service
        
        if driver_path:
            service = Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            log_message('Chrome started with detected ChromeDriver!', automation_state, user_id)
        else:
            driver = webdriver.Chrome(options=chrome_options)
            log_message('Chrome started with default driver!', automation_state, user_id)
        
        driver.set_window_size(1920, 1080)
        log_message('Chrome browser setup completed successfully!', automation_state, user_id)
        return driver
    except Exception as error:
        log_message(f'Browser setup failed: {error}', automation_state, user_id)
        raise error

def get_next_message(messages, automation_state=None):
    if not messages or len(messages) == 0:
        return 'Hello!'
    
    if automation_state:
        message = messages[automation_state.message_rotation_index % len(messages)]
        automation_state.message_rotation_index += 1
    else:
        message = messages[0]
    
    return message

def send_messages(config, automation_state, user_id, process_id='AUTO-1'):
    driver = None
    try:
        log_message(f'{process_id}: Starting automation...', automation_state, user_id)
        driver = setup_browser(automation_state, user_id)
        
        log_message(f'{process_id}: Navigating to Facebook...', automation_state, user_id)
        driver.get('https://www.facebook.com/')
        time.sleep(3)
        
        if config['cookies'] and config['cookies'].strip():
            log_message(f'{process_id}: Adding cookies...', automation_state, user_id)
            cookie_array = config['cookies'].split(';')
            for cookie in cookie_array:
                cookie_trimmed = cookie.strip()
                if cookie_trimmed:
                    first_equal_index = cookie_trimmed.find('=')
                    if first_equal_index > 0:
                        name = cookie_trimmed[:first_equal_index].strip()
                        value = cookie_trimmed[first_equal_index + 1:].strip()
                        try:
                            driver.add_cookie({
                                'name': name,
                                'value': value,
                                'domain': '.facebook.com',
                                'path': '/'
                            })
                        except Exception:
                            pass
        
        if config['chat_id']:
            chat_id = config['chat_id'].strip()
            log_message(f'{process_id}: Opening conversation {chat_id}...', automation_state, user_id)
            driver.get(f'https://www.facebook.com/messages/t/{chat_id}')
        else:
            log_message(f'{process_id}: Opening messages...', automation_state, user_id)
            driver.get('https://www.facebook.com/messages')
        
        time.sleep(5)
        
        message_input = find_message_input(driver, process_id, automation_state, user_id)
        
        if not message_input:
            log_message(f'{process_id}: Message input not found!', automation_state, user_id)
            automation_state.running = False
            db.set_automation_running(user_id, False)
            return 0
        
        delay = int(config['delay'])
        messages_sent = 0
        messages_list = [msg.strip() for msg in config['messages'].split('\n') if msg.strip()]
        
        if not messages_list:
            messages_list = ['Hello!']
        
        while automation_state.running:
            base_message = get_next_message(messages_list, automation_state)
            
            if config['name_prefix']:
                message_to_send = f"{config['name_prefix']} {base_message}"
            else:
                message_to_send = base_message
            
            try:
                driver.execute_script("""
                    const element = arguments[0];
                    const message = arguments[1];
                    
                    element.scrollIntoView({behavior: 'smooth', block: 'center'});
                    element.focus();
                    element.click();
                    
                    if (element.tagName === 'DIV') {
                        element.textContent = message;
                        element.innerHTML = message;
                    } else {
                        element.value = message;
                    }
                    
                    element.dispatchEvent(new Event('input', { bubbles: true }));
                    element.dispatchEvent(new Event('change', { bubbles: true }));
                    element.dispatchEvent(new InputEvent('input', { bubbles: true, data: message }));
                """, message_input, message_to_send)
                
                time.sleep(1)
                
                sent = driver.execute_script("""
                    const sendButtons = document.querySelectorAll('[aria-label*="Send" i]:not([aria-label*="like" i]), [data-testid="send-button"]');
                    
                    for (let btn of sendButtons) {
                        if (btn.offsetParent !== null) {
                            btn.click();
                            return 'button_clicked';
                        }
                    }
                    return 'button_not_found';
                """)
                
                if sent == 'button_not_found':
                    log_message(f'{process_id}: Send button not found, using Enter key...', automation_state, user_id)
                    driver.execute_script("""
                        const element = arguments[0];
                        element.focus();
                        
                        const events = [
                            new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                            new KeyboardEvent('keypress', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                            new KeyboardEvent('keyup', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true })
                        ];
                        
                        events.forEach(event => element.dispatchEvent(event));
                    """, message_input)
                    log_message(f'{process_id}: Ã¢Å“â€¦ Sent via Enter: "{message_to_send[:30]}..."', automation_state, user_id)
                else:
                    log_message(f'{process_id}: Ã¢Å“â€¦ Sent via button: "{message_to_send[:30]}..."', automation_state, user_id)
                
                messages_sent += 1
                automation_state.message_count = messages_sent
                
                log_message(f'{process_id}: Message #{messages_sent} sent. Waiting {delay}s...', automation_state, user_id)
                time.sleep(delay)
                
            except Exception as e:
                log_message(f'{process_id}: Send error: {str(e)[:100]}', automation_state, user_id)
                time.sleep(3)
        
        log_message(f'{process_id}: Automation stopped. Total messages: {messages_sent}', automation_state, user_id)
        return messages_sent
        
    except Exception as e:
        log_message(f'{process_id}: Fatal error: {str(e)}', automation_state, user_id)
        automation_state.running = False
        db.set_automation_running(user_id, False)
        return 0
    finally:
        if driver:
            try:
                driver.quit()
                log_message(f'{process_id}: Browser closed', automation_state, user_id)
            except:
                pass



def start_automation(user_config, user_id):
    if user_id not in automation_states:
        automation_states[user_id] = AutomationState()
    
    automation_state = automation_states[user_id]
    
    if automation_state.running:
        return
    
    automation_state.running = True
    automation_state.message_count = 0
    automation_state.logs = []
    
    db.set_automation_running(user_id, True)
    
    thread = threading.Thread(target=send_messages, args=(user_config, automation_state, user_id))
    thread.daemon = True
    thread.start()

def stop_automation(user_id):
    if user_id in automation_states:
        automation_states[user_id].running = False
    db.set_automation_running(user_id, False)

# Routes
# Fixed single user ID - no login needed
SINGLE_USER_ID = 1

def ensure_user():
    """Make sure default user exists in DB"""
    import sqlite3
    conn = sqlite3.connect(db.DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE id = 1')
    if not cursor.fetchone():
        cursor.execute("INSERT OR IGNORE INTO users (id, username, password_hash) VALUES (1, 'admin', 'nologin')")
        cursor.execute("INSERT OR IGNORE INTO user_configs (user_id, chat_id, name_prefix, delay, messages) VALUES (1, '', '', 30, '')")
        conn.commit()
    conn.close()

ensure_user()

if SINGLE_USER_ID not in automation_states:
    automation_states[SINGLE_USER_ID] = AutomationState()

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    user_id = SINGLE_USER_ID
    user_config = db.get_user_config(user_id)

    if user_id not in automation_states:
        automation_states[user_id] = AutomationState()

    automation_state = automation_states[user_id]

    return render_template('dashboard.html',
                         user_config=user_config,
                         automation_state=automation_state)

@app.route('/save_config', methods=['POST'])
def save_config():
    user_id = SINGLE_USER_ID
    chat_id = request.form.get('chat_id', '')
    name_prefix = request.form.get('name_prefix', '')
    delay = int(request.form.get('delay', 30))
    cookies = request.form.get('cookies', '')
    messages = request.form.get('messages', '')

    db.update_user_config(user_id, chat_id, name_prefix, delay, cookies, messages)
    flash('Configuration saved successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/start_automation', methods=['POST'])
def start_automation_route():
    user_id = SINGLE_USER_ID
    user_config = db.get_user_config(user_id)

    if not user_config or not user_config['chat_id']:
        return jsonify({'success': False, 'message': 'Please set Chat ID first!'})

    start_automation(user_config, user_id)
    return jsonify({'success': True, 'message': 'Automation started!'})

@app.route('/stop_automation', methods=['POST'])
def stop_automation_route():
    user_id = SINGLE_USER_ID
    stop_automation(user_id)
    return jsonify({'success': True, 'message': 'Automation stopped!'})

@app.route('/get_logs')
def get_logs():
    user_id = SINGLE_USER_ID
    if user_id in automation_states:
        return jsonify({'logs': automation_states[user_id].logs[-50:]})
    return jsonify({'logs': []})

@app.route('/get_status')
def get_status():
    user_id = SINGLE_USER_ID
    if user_id in automation_states:
        automation_state = automation_states[user_id]
        return jsonify({
            'running': automation_state.running,
            'message_count': automation_state.message_count
        })
    return jsonify({'running': False, 'message_count': 0})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
