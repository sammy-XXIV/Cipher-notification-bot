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
            f"Enter this code on <b>tradewithcipher.xyz</b>\n"
            f"Settings → Notifications → Link Telegram\n\n"
            f"⏱ Code expires in <b>10 minutes</b>\n\n"
            f"<i>@Cipher_notificationbot</i>"
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
    # Drain any queued updates on startup
    updates = tg_get_updates(offset)
    if updates:
        offset = updates[-1]["update_id"] + 1
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
# SIGNAL MONITOR — stores and monitors active signals 24/7
# ============================================================
# In-memory store: { user_id: { symbol: signal_data } }
active_signals = {}

CIPHER_SERVER = os.environ.get("CIPHER_SERVER_URL", "https://back-end-1-928p.onrender.com")

def get_fresh_signal(symbol, timeframe='1h'):
    """Fetch fresh candles and get AI signal from CIPHER backend"""
    try:
        # Get candles from backend
        r = requests.get(f"{CIPHER_SERVER}/candles?symbol={symbol}&interval={timeframe}&limit=80", timeout=15)
        data = r.json()
        candles = data.get("candles", [])
        if not candles:
            return None

        closes = [c["c"] for c in candles]
        highs  = [c["h"] for c in candles]
        lows   = [c["l"] for c in candles]
        vols   = [c["v"] for c in candles]
        n = len(closes)

        # RSI
        g = l = 0
        for i in range(1, min(15, n)):
            d = closes[-(15-i+1)] - closes[-(15-i+2)] if (15-i+2) <= n else 0
            if d > 0: g += d
            else: l -= d
        rsi = round(100 - (100 / (1 + (g/l if l else 100))))

        # EMA
        def ema(data, p):
            k = 2/(p+1); e = data[0]
            for v in data[1:]: e = v*k + e*(1-k)
            return round(e, 8)

        ema20 = ema(closes, 20) if n >= 20 else closes[-1]
        ema50 = ema(closes, 50) if n >= 50 else closes[-1]
        price = closes[-1]
        trend = "BULLISH" if price > ema20 > ema50 else "BEARISH" if price < ema20 < ema50 else "MIXED"

        # ATR
        trs = [max(highs[i]-lows[i], abs(highs[i]-closes[i-1]), abs(lows[i]-closes[i-1])) for i in range(1, min(15, n))]
        atr = round(sum(trs)/len(trs), 8) if trs else 0

        # Volume
        avg_vol = sum(vols[-20:]) / 20 if n >= 20 else vols[-1]
        vol_sig = "HIGH" if vols[-1] > avg_vol * 1.5 else "LOW" if vols[-1] < avg_vol * 0.5 else "NORMAL"

        prompt = f"""You are CIPHER. Analyze {symbol} for a quick signal check.

TIMEFRAME: {timeframe.upper()}
Price: ${price} | RSI: {rsi} | EMA20: ${ema20} | EMA50: ${ema50}
Trend: {trend} | ATR: ${atr} | Volume: {vol_sig}

Respond ONLY in JSON:
{{"signal":"LONG or SHORT or NEUTRAL","confidence":40-92,"entry":"{price}","target":"price","stop":"price","reasoning":"1-2 sentences"}}"""

        r2 = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": os.environ.get("ANTHROPIC_API_KEY",""), "anthropic-version": "2023-06-01", "Content-Type": "application/json"},
            json={"model": "claude-sonnet-4-20250514", "max_tokens": 200, "messages": [{"role": "user", "content": prompt}]},
            timeout=30
        )
        raw = r2.json()["content"][0]["text"].strip().replace("```json","").replace("```","").strip()
        return json.loads(raw)

    except Exception as e:
        log.error(f"get_fresh_signal error for {symbol}: {e}")
        return None

def signal_monitor_loop():
    """Check all registered signals every 30 minutes"""
    time.sleep(60)  # wait for startup
    log.info("Signal monitor loop started")
    while True:
        try:
            if not active_signals:
                time.sleep(1800)
                continue

            log.info(f"Monitoring {sum(len(v) for v in active_signals.values())} active signals")

            for user_id, signals in list(active_signals.items()):
                profile = get_profile_by_user_id(user_id)
                if not profile or not profile.get('telegram_verified'):
                    continue
                chat_id = profile['telegram_chat_id']

                for symbol, stored in list(signals.items()):
                    try:
                        timeframe = stored.get('timeframe', '1h')
                        old_signal = stored.get('signal')
                        old_entry  = stored.get('entry')
                        tp = stored.get('target')
                        sl = stored.get('stop')
                        price_at_signal = float(stored.get('price', 0))

                        # Get fresh signal
                        fresh = get_fresh_signal(symbol, timeframe)
                        if not fresh:
                            continue

                        new_signal = fresh.get('signal')
                        current_price = float(fresh.get('entry', 0))

                        prev_emoji = "🟢" if old_signal == "LONG" else "🔴"
                        new_emoji  = "🟢" if new_signal == "LONG" else "🔴"

                        # Check TP hit
                        if tp and current_price and old_signal == "LONG" and current_price >= float(str(tp).replace('$','')):
                            tg(chat_id,
                                f"🎯 <b>TAKE PROFIT HIT — {symbol}</b>\n\n"
                                f"Your LONG position reached TP!\n"
                                f"Current: <b>${current_price}</b> | TP was: <b>{tp}</b>\n\n"
                                f"Consider closing your position. 💰\n\n"
                                f"<i>⚠️ NOT FINANCIAL ADVICE</i>"
                            )
                            del active_signals[user_id][symbol]
                            continue

                        if tp and current_price and old_signal == "SHORT" and current_price <= float(str(tp).replace('$','')):
                            tg(chat_id,
                                f"🎯 <b>TAKE PROFIT HIT — {symbol}</b>\n\n"
                                f"Your SHORT position reached TP!\n"
                                f"Current: <b>${current_price}</b> | TP was: <b>{tp}</b>\n\n"
                                f"Consider closing your position. 💰\n\n"
                                f"<i>⚠️ NOT FINANCIAL ADVICE</i>"
                            )
                            del active_signals[user_id][symbol]
                            continue

                        # Check SL hit
                        if sl and current_price and old_signal == "LONG" and current_price <= float(str(sl).replace('$','')):
                            tg(chat_id,
                                f"🛑 <b>STOP LOSS HIT — {symbol}</b>\n\n"
                                f"Your LONG position hit SL!\n"
                                f"Current: <b>${current_price}</b> | SL was: <b>{sl}</b>\n\n"
                                f"Running fresh analysis...\n\n"
                                f"New signal: {new_emoji} <b>{new_signal}</b> ({fresh.get('confidence')}%)\n"
                                f"📝 {fresh.get('reasoning','')}\n\n"
                                f"<i>⚠️ NOT FINANCIAL ADVICE</i>"
                            )
                            del active_signals[user_id][symbol]
                            continue

                        if sl and current_price and old_signal == "SHORT" and current_price >= float(str(sl).replace('$','')):
                            tg(chat_id,
                                f"🛑 <b>STOP LOSS HIT — {symbol}</b>\n\n"
                                f"Your SHORT position hit SL!\n"
                                f"Current: <b>${current_price}</b> | SL was: <b>{sl}</b>\n\n"
                                f"Running fresh analysis...\n\n"
                                f"New signal: {new_emoji} <b>{new_signal}</b> ({fresh.get('confidence')}%)\n"
                                f"📝 {fresh.get('reasoning','')}\n\n"
                                f"<i>⚠️ NOT FINANCIAL ADVICE</i>"
                            )
                            del active_signals[user_id][symbol]
                            continue

                        # Check signal reversal
                        if new_signal != "NEUTRAL" and new_signal != old_signal:
                            tg(chat_id,
                                f"🔄 <b>SIGNAL REVERSAL — {symbol}</b>\n\n"
                                f"Previous: {prev_emoji} <b>{old_signal}</b>\n"
                                f"New: {new_emoji} <b>{new_signal}</b> ({fresh.get('confidence')}% confidence)\n\n"
                                f"📝 {fresh.get('reasoning','')}\n\n"
                                f"🎯 New Entry: <b>{fresh.get('entry')}</b>\n"
                                f"✅ New TP: <b>{fresh.get('target')}</b>\n"
                                f"🛑 New SL: <b>{fresh.get('stop')}</b>\n\n"
                                f"⚠️ Consider closing your {old_signal} position.\n\n"
                                f"<i>⚠️ NOT FINANCIAL ADVICE</i>"
                            )
                            # Update stored signal to new one
                            active_signals[user_id][symbol].update({
                                'signal': new_signal,
                                'entry': fresh.get('entry'),
                                'target': fresh.get('target'),
                                'stop': fresh.get('stop'),
                                'price': current_price,
                                'updated_at': datetime.now().isoformat(),
                            })

                        time.sleep(1)  # small delay between tokens

                    except Exception as e:
                        log.error(f"Monitor error for {symbol}: {e}")

        except Exception as e:
            log.error(f"Signal monitor loop error: {e}")

        time.sleep(1800)  # check every 30 minutes

# ============================================================
# FLASK ROUTES — called by CIPHER web app to send notifications
# ============================================================
@app.after_request
def cors_h(r):
    r.headers['Access-Control-Allow-Origin'] = '*'
    r.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    r.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return r

@app.route('/register-signal', methods=['POST', 'OPTIONS'])
def register_signal():
    """Register a signal for monitoring — called by CIPHER web app after analysis"""
    if request.method == 'OPTIONS':
        return '', 204
    try:
        data = request.get_json()
        user_id  = data.get('user_id')
        symbol   = data.get('symbol', '').upper()
        signal   = data.get('signal')
        entry    = data.get('entry')
        target   = data.get('target')
        stop     = data.get('stop')
        timeframe = data.get('timeframe', '1h').lower()
        price    = data.get('price', 0)

        if not user_id or not symbol or not signal:
            return jsonify({'error': 'user_id, symbol and signal required'}), 400

        if signal == 'NEUTRAL':
            # Remove from monitoring if neutral
            if user_id in active_signals and symbol in active_signals[user_id]:
                del active_signals[user_id][symbol]
            return jsonify({'status': 'removed'})

        if user_id not in active_signals:
            active_signals[user_id] = {}

        active_signals[user_id][symbol] = {
            'signal': signal,
            'entry': entry,
            'target': target,
            'stop': stop,
            'timeframe': timeframe,
            'price': price,
            'registered_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
        }

        log.info(f"Registered {signal} signal for {symbol} — user {user_id[:8]}...")
        return jsonify({'status': 'registered', 'symbol': symbol, 'signal': signal})

    except Exception as e:
        log.error(f"Register signal error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/active-signals', methods=['GET'])
def get_active_signals():
    """Get all active signals being monitored (for debugging)"""
    total = sum(len(v) for v in active_signals.values())
    return jsonify({'total': total, 'users': len(active_signals)})

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
    threading.Thread(target=signal_monitor_loop, daemon=True).start()
    log.info("CIPHER Notification Bot started")
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port, debug=False)
