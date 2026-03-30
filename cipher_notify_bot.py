"""
CIPHER NOTIFICATION BOT
========================
Separate from trading bot.
Handles Telegram linking via verification codes.
Sends personal notifications to each user.
"""

import os, json, time, random, string, logging, requests, threading
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS

# ============================================================
# CONFIG
# ============================================================
NOTIFY_TOKEN   = os.environ.get("NOTIFY_TOKEN", "8685607507:AAHSQ-8hz9ivTNaNmYTKy8Gl-l-ZQaNO9YQ")
SUPABASE_URL   = os.environ.get("SUPABASE_URL", "https://zttdlnavawepvhbtldgq.supabase.co")
SUPABASE_KEY   = os.environ.get("SUPABASE_KEY", "sb_publishable_PiRo_l11XVyrqnhmn5NldQ_Ju0ItrBV")
RENDER_URL     = os.environ.get("RENDER_EXTERNAL_URL", "")

def keep_alive_loop():
    """Ping self every 3 minutes to prevent Render sleep"""
    time.sleep(30)  # wait for server to start first
    while True:
        try:
            url = RENDER_URL or "http://localhost:5002"
            requests.get(f"{url}/ping", timeout=10)
            log.info("Keep-alive ping sent")
        except Exception as e:
            log.warning(f"Keep-alive failed: {e}")
        time.sleep(180)  # every 3 minutes

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger("CIPHER-NOTIFY")

app = Flask(__name__)
CORS(app, origins="*")

# ============================================================
# SUPABASE
# ============================================================
def sb_request(method, path, body=None, params=None):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }
    url = f"{SUPABASE_URL}/rest/v1/{path}"
    try:
        if method == "GET":
            r = requests.get(url, headers=headers, params=params, timeout=10)
        elif method == "POST":
            r = requests.post(url, headers=headers, json=body, timeout=10)
        elif method == "PATCH":
            r = requests.patch(url, headers=headers, json=body, params=params, timeout=10)
        elif method == "DELETE":
            r = requests.delete(url, headers=headers, params=params, timeout=10)
        return r.json() if r.text else []
    except Exception as e:
        log.error(f"Supabase error: {e}")
        return []

def get_profile_by_chat_id(chat_id):
    result = sb_request("GET", "profiles", params={"telegram_chat_id": f"eq.{chat_id}", "select": "*"})
    return result[0] if result else None

def get_profile_by_user_id(user_id):
    result = sb_request("GET", "profiles", params={"user_id": f"eq.{user_id}", "select": "*"})
    return result[0] if result else None

def save_verification_code(chat_id, username, code):
    expires = (datetime.utcnow() + timedelta(minutes=10)).isoformat()
    # Delete old codes for this chat_id first
    sb_request("DELETE", "pending_verifications", params={"chat_id": f"eq.{chat_id}"})
    # Insert new code
    sb_request("POST", "pending_verifications", body={
        "chat_id": str(chat_id),
        "username": username,
        "code": code,
        "expires_at": expires
    })

# ============================================================
# TELEGRAM
# ============================================================
def tg(chat_id, text, parse_mode="HTML"):
    try:
        requests.post(
            f"https://api.telegram.org/bot{NOTIFY_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": parse_mode},
            timeout=10
        )
    except Exception as e:
        log.error(f"TG send error: {e}")

def tg_get_updates(offset=None):
    try:
        params = {"timeout": 10, "allowed_updates": ["message"]}
        if offset: params["offset"] = offset
        r = requests.get(
            f"https://api.telegram.org/bot{NOTIFY_TOKEN}/getUpdates",
            params=params, timeout=15
        )
        return r.json().get("result", [])
    except:
        return []

def clear_updates():
    try:
        r = requests.get(f"https://api.telegram.org/bot{NOTIFY_TOKEN}/getUpdates", params={"offset": -1, "timeout": 0}, timeout=10)
        updates = r.json().get("result", [])
        if updates:
            last_id = updates[-1]["update_id"]
            requests.get(f"https://api.telegram.org/bot{NOTIFY_TOKEN}/getUpdates", params={"offset": last_id + 1, "timeout": 0}, timeout=10)
    except: pass

def generate_code():
    return ''.join(random.choices(string.digits, k=6))

def register_commands():
    commands = [
        {"command": "start", "description": "Get your verification code"},
        {"command": "code",  "description": "Get a new verification code"},
        {"command": "status","description": "Check your notification status"},
        {"command": "stop",  "description": "Stop notifications"},
    ]
    try:
        requests.post(
            f"https://api.telegram.org/bot{NOTIFY_TOKEN}/setMyCommands",
            json={"commands": commands}, timeout=10
        )
    except: pass

# ============================================================
# MESSAGE HANDLER
# ============================================================
def handle_update(update):
    if "message" not in update:
        return
    msg = update["message"]
    chat_id = msg["chat"]["id"]
    username = msg.get("chat", {}).get("username", "")
    text = msg.get("text", "").strip()

    if text in ["/start", "/code"]:
        code = generate_code()
        save_verification_code(chat_id, username, code)
        tg(chat_id,
            f"🔐 <b>CIPHER NOTIFICATIONS</b>\n\n"
            f"Your verification code:\n\n"
            f"<code>{code}</code>\n\n"
            f"Enter this code on <b>tradewithcipher.online</b>\n"
            f"Settings → Notifications → Link Telegram\n\n"
            f"⏱ Code expires in <b>10 minutes</b>"
        )
        log.info(f"Sent code {code} to {chat_id} (@{username})")

    elif text == "/status":
        profile = get_profile_by_chat_id(chat_id)
        if profile and profile.get("telegram_verified"):
            tg(chat_id,
                f"✅ <b>NOTIFICATIONS ACTIVE</b>\n\n"
                f"Your CIPHER account is linked.\n"
                f"You'll receive alerts for analysis results,\n"
                f"entry zones, setup invalidations and more.\n\n"
                f"Type /stop to disable notifications."
            )
        else:
            tg(chat_id,
                f"❌ <b>NOT LINKED</b>\n\n"
                f"Your Telegram is not linked to a CIPHER account.\n\n"
                f"Type /start to get a verification code."
            )

    elif text == "/stop":
        profile = get_profile_by_chat_id(chat_id)
        if profile:
            sb_request("PATCH", "profiles",
                body={"telegram_verified": False},
                params={"telegram_chat_id": f"eq.{chat_id}"}
            )
            tg(chat_id, "🔕 Notifications disabled. Type /start to re-enable.")
        else:
            tg(chat_id, "You don't have an active notification subscription.")

    else:
        tg(chat_id,
            f"🤖 <b>CIPHER Notifications Bot</b>\n\n"
            f"Commands:\n"
            f"/start — Get verification code\n"
            f"/code — Get a new code\n"
            f"/status — Check link status\n"
            f"/stop — Disable notifications"
        )

# ============================================================
# KEEP ALIVE — self ping every 3 minutes
# ============================================================
def keep_alive_loop():
    time.sleep(60)  # wait for server to start
    while True:
        try:
            url = os.environ.get("RENDER_EXTERNAL_URL", "")
            if url:
                requests.get(f"{url}/ping", timeout=10)
                log.info("Keep-alive ping sent")
        except: pass
        time.sleep(180)  # every 3 minutes

# ============================================================
# POLLING LOOP
# ============================================================
def polling_loop():
    offset = None
    clear_updates()
    log.info("Notification bot polling started")
    while True:
        updates = tg_get_updates(offset)
        for u in updates:
            offset = u["update_id"] + 1
            try:
                handle_update(u)
            except Exception as e:
                log.error(f"Handle error: {e}")
        time.sleep(1)

# ============================================================
# FLASK ROUTES — called by CIPHER web app to send notifications
# ============================================================
@app.after_request
def cors_h(r):
    r.headers['Access-Control-Allow-Origin'] = '*'
    r.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    r.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return r

@app.route('/notify', methods=['POST'])
def notify():
    """Send notification to a specific user by user_id"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        message = data.get('message')
        notif_type = data.get('type', 'general')

        if not user_id or not message:
            return jsonify({'error': 'user_id and message required'}), 400

        profile = get_profile_by_user_id(user_id)
        if not profile or not profile.get('telegram_verified'):
            return jsonify({'status': 'not_linked'})

        # Check user preferences
        prefs = profile.get('notification_prefs', {})
        pref_map = {
            'analysis': 'analysis',
            'entry': 'entry',
            'dead': 'dead',
            'expired': 'expired',
            'feargreed': 'feargreed',
        }
        pref_key = pref_map.get(notif_type)
        if pref_key and not prefs.get(pref_key, True):
            return jsonify({'status': 'muted'})

        chat_id = profile['telegram_chat_id']
        tg(chat_id, message)
        log.info(f"Sent {notif_type} notification to user {user_id}")
        return jsonify({'status': 'sent'})

    except Exception as e:
        log.error(f"Notify error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/notify/broadcast', methods=['POST'])
def broadcast():
    """Send to all verified users (admin only)"""
    try:
        data = request.get_json()
        message = data.get('message')
        if not message:
            return jsonify({'error': 'message required'}), 400

        profiles = sb_request("GET", "profiles", params={
            "telegram_verified": "eq.true",
            "select": "telegram_chat_id"
        })
        sent = 0
        for p in profiles:
            if p.get('telegram_chat_id'):
                tg(p['telegram_chat_id'], message)
                sent += 1
                time.sleep(0.05)

        return jsonify({'status': 'sent', 'count': sent})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ping')
def ping():
    return jsonify({'status': 'CIPHER Notify Bot online'})

# ============================================================
# STARTUP
# ============================================================
if __name__ == '__main__':
    register_commands()
    threading.Thread(target=polling_loop, daemon=True).start()
    threading.Thread(target=keep_alive_loop, daemon=True).start()
    log.info("CIPHER Notification Bot started")
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port, debug=False)
