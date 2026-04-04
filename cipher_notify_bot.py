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
# SIGNAL STORAGE — Supabase (survives restarts)
# ============================================================
def save_signal(user_id, symbol, signal, entry, target, stop, timeframe, price):
    """Save/update signal in Supabase"""
    sb_request("POST", "active_signals", body={
        "user_id": user_id,
        "symbol": symbol.upper(),
        "signal": signal,
        "entry": str(entry) if entry else None,
        "target": str(target) if target else None,
        "stop": str(stop) if stop else None,
        "timeframe": timeframe,
        "price": float(price) if price else 0,
        "registered_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    })
    # Use upsert via headers
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates",
    }
    try:
        requests.post(
            f"{SUPABASE_URL}/rest/v1/active_signals",
            headers=headers,
            json={
                "user_id": user_id,
                "symbol": symbol.upper(),
                "signal": signal,
                "entry": str(entry) if entry else None,
                "target": str(target) if target else None,
                "stop": str(stop) if stop else None,
                "timeframe": timeframe,
                "price": float(price) if price else 0,
                "updated_at": datetime.utcnow().isoformat(),
            },
            timeout=10
        )
        log.info(f"Signal saved: {symbol} {signal}")
    except Exception as e:
        log.error(f"Save signal error: {e}")

def delete_signal(user_id, symbol):
    """Remove signal from monitoring"""
    sb_request("DELETE", "active_signals", params={
        "user_id": f"eq.{user_id}",
        "symbol": f"eq.{symbol.upper()}"
    })

def get_all_signals():
    """Get all active signals from Supabase"""
    try:
        result = sb_request("GET", "active_signals", params={"select": "*"})
        return result if isinstance(result, list) else []
    except Exception as e:
        log.error(f"Get signals error: {e}")
        return []

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
    """Check signals — interval adapts to shortest active timeframe"""
    time.sleep(60)
    log.info("Signal monitor loop started")

    TIMEFRAME_INTERVALS = {'15m': 300, '1h': 600, '4h': 1200, '1d': 3600, '1w': 7200}

    while True:
        try:
            signals = get_all_signals()
            if not signals:
                log.info("No active signals to monitor")
                time.sleep(600)
                continue

            # Sleep = shortest timeframe interval of all active signals
            active_tfs = [s.get('timeframe', '1h') for s in signals]
            sleep_time = min(TIMEFRAME_INTERVALS.get(tf, 600) for tf in active_tfs)
            log.info(f"Monitoring {len(signals)} signals — interval {sleep_time//60}min")

            for stored in signals:
                try:
                    user_id   = stored.get('user_id')
                    symbol    = stored.get('symbol')
                    old_signal = stored.get('signal')
                    entry     = stored.get('entry')
                    tp        = stored.get('target')
                    sl        = stored.get('stop')
                    timeframe = stored.get('timeframe', '1h')

                    if not user_id or not symbol or not old_signal:
                        continue

                    # Get user's chat_id
                    profile = get_profile_by_user_id(user_id)
                    if not profile or not profile.get('telegram_verified'):
                        continue
                    chat_id = profile['telegram_chat_id']

                    # Get fresh signal
                    fresh = get_fresh_signal(symbol, timeframe)
                    if not fresh:
                        continue

                    new_signal    = fresh.get('signal')
                    current_price = float(str(fresh.get('entry', 0)).replace('$','') or 0)
                    prev_emoji    = "🟢" if old_signal == "LONG" else "🔴"
                    new_emoji     = "🟢" if new_signal == "LONG" else "🔴"

                    # ── LIMIT MISS DETECTION ──
                    # Check if price never hit entry and is now running away
                    try:
                        entry_price   = float(str(entry).replace('$','')) if entry else 0
                        price_at_reg  = float(str(stored.get('price', 0)) or 0)
                        filled        = stored.get('filled', False)

                        if not filled and entry_price and current_price and price_at_reg:
                            # Calculate ATR as % of price for threshold
                            atr_est = price_at_reg * 0.02  # 2% estimate

                            # LONG limit miss — price ran UP without filling
                            if old_signal == "LONG" and current_price > entry_price:
                                move_pct = ((current_price - entry_price) / entry_price) * 100
                                # Price moved up 2x ATR from entry without touching it
                                if move_pct >= 2.0:
                                    advice = "CHASE" if (new_signal == "LONG" and fresh.get('confidence', 0) >= 70) else "WAIT"
                                    chase_msg = (
                                        f"LIMIT NOT FILLED — {symbol}\n\n"
                                        f"Your LONG limit at <b>{entry}</b> was not hit.\n"
                                        f"Price ran up <b>+{move_pct:.1f}%</b> to <b>${current_price}</b>\n\n"
                                    )
                                    if advice == "CHASE":
                                        chase_msg += (
                                            f"AI says: CHASE IT\n"
                                            f"Signal still LONG ({fresh.get('confidence')}% confidence)\n"
                                            f"New entry: <b>{fresh.get('entry')}</b>\n"
                                            f"TP: <b>{fresh.get('target')}</b> | SL: <b>{fresh.get('stop')}</b>\n\n"
                                            f"📝 {fresh.get('reasoning','')}\n\n"
                                            f"<i>NOT FINANCIAL ADVICE</i>"
                                        )
                                    else:
                                        chase_msg += (
                                            f"AI says: WAIT FOR PULLBACK\n"
                                            f"Momentum weakening — wait for price to pull back\n"
                                            f"to EMA or support before entering.\n\n"
                                            f"📝 {fresh.get('reasoning','')}\n\n"
                                            f"<i>NOT FINANCIAL ADVICE</i>"
                                        )
                                    tg(chat_id, chase_msg)
                                    # Mark as filled to avoid repeated alerts
                                    sb_request("PATCH", "active_signals", body={"filled": True}, params={
                                        "user_id": f"eq.{user_id}",
                                        "symbol":  f"eq.{symbol}"
                                    })

                            # SHORT limit miss — price ran DOWN without filling
                            elif old_signal == "SHORT" and current_price < entry_price:
                                move_pct = ((entry_price - current_price) / entry_price) * 100
                                if move_pct >= 2.0:
                                    advice = "CHASE" if (new_signal == "SHORT" and fresh.get('confidence', 0) >= 70) else "WAIT"
                                    chase_msg = (
                                        f"LIMIT NOT FILLED — {symbol}\n\n"
                                        f"Your SHORT limit at <b>{entry}</b> was not hit.\n"
                                        f"Price dropped <b>-{move_pct:.1f}%</b> to <b>${current_price}</b>\n\n"
                                    )
                                    if advice == "CHASE":
                                        chase_msg += (
                                            f"AI says: CHASE IT\n"
                                            f"Signal still SHORT ({fresh.get('confidence')}% confidence)\n"
                                            f"New entry: <b>{fresh.get('entry')}</b>\n"
                                            f"TP: <b>{fresh.get('target')}</b> | SL: <b>{fresh.get('stop')}</b>\n\n"
                                            f"📝 {fresh.get('reasoning','')}\n\n"
                                            f"<i>NOT FINANCIAL ADVICE</i>"
                                        )
                                    else:
                                        chase_msg += (
                                            f"AI says: WAIT FOR PULLBACK\n"
                                            f"Momentum weakening — wait for price to bounce\n"
                                            f"to EMA or resistance before entering short.\n\n"
                                            f"📝 {fresh.get('reasoning','')}\n\n"
                                            f"<i>NOT FINANCIAL ADVICE</i>"
                                        )
                                    tg(chat_id, chase_msg)
                                    sb_request("PATCH", "active_signals", body={"filled": True}, params={
                                        "user_id": f"eq.{user_id}",
                                        "symbol":  f"eq.{symbol}"
                                    })

                            # Mark as filled if price hit entry zone (within 0.5%)
                            elif not filled and abs(current_price - entry_price) / entry_price < 0.005:
                                sb_request("PATCH", "active_signals", body={"filled": True}, params={
                                    "user_id": f"eq.{user_id}",
                                    "symbol":  f"eq.{symbol}"
                                })

                    except Exception as e:
                        log.warning(f"Limit miss check error: {e}")

                    # Check TP hit
                    try:
                        tp_price = float(str(tp).replace('$','')) if tp else 0
                        sl_price = float(str(sl).replace('$','')) if sl else 0

                        if tp_price and current_price:
                            tp_hit = (old_signal == "LONG" and current_price >= tp_price) or \
                                     (old_signal == "SHORT" and current_price <= tp_price)
                            if tp_hit:
                                tg(chat_id,
                                    f"🎯 <b>TAKE PROFIT HIT — {symbol}</b>\n\n"
                                    f"Your {old_signal} position reached TP!\n"
                                    f"Current: <b>${current_price}</b> | TP: <b>{tp}</b>\n\n"
                                    f"Consider closing your position. 💰\n\n"
                                    f"<i>⚠️ NOT FINANCIAL ADVICE</i>"
                                )
                                delete_signal(user_id, symbol)
                                continue

                        # Check SL hit
                        if sl_price and current_price:
                            sl_hit = (old_signal == "LONG" and current_price <= sl_price) or \
                                     (old_signal == "SHORT" and current_price >= sl_price)
                            if sl_hit:
                                tg(chat_id,
                                    f"🛑 <b>STOP LOSS HIT — {symbol}</b>\n\n"
                                    f"Your {old_signal} position hit SL!\n"
                                    f"Current: <b>${current_price}</b> | SL: <b>{sl}</b>\n\n"
                                    f"Fresh analysis: {new_emoji} <b>{new_signal}</b> ({fresh.get('confidence')}%)\n"
                                    f"📝 {fresh.get('reasoning','')}\n\n"
                                    f"<i>⚠️ NOT FINANCIAL ADVICE</i>"
                                )
                                delete_signal(user_id, symbol)
                                continue

                    except Exception as e:
                        log.warning(f"TP/SL check error: {e}")

                    # Check signal reversal
                    if new_signal and new_signal != "NEUTRAL" and new_signal != old_signal:
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
                        # Update to new signal in Supabase
                        save_signal(user_id, symbol, new_signal,
                            fresh.get('entry'), fresh.get('target'),
                            fresh.get('stop'), timeframe, current_price)

                    time.sleep(1)

                except Exception as e:
                    log.error(f"Monitor error for {stored.get('symbol','?')}: {e}")

        except Exception as e:
            log.error(f"Signal monitor loop error: {e}")

        time.sleep(sleep_time)

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
        user_id   = data.get('user_id')
        symbol    = data.get('symbol', '').upper()
        signal    = data.get('signal')
        entry     = data.get('entry')
        target    = data.get('target')
        stop      = data.get('stop')
        timeframe = data.get('timeframe', '1h').lower()
        price     = data.get('price', 0)

        if not user_id or not symbol or not signal:
            return jsonify({'error': 'user_id, symbol and signal required'}), 400

        if signal == 'NEUTRAL':
            delete_signal(user_id, symbol)
            return jsonify({'status': 'removed'})

        save_signal(user_id, symbol, signal, entry, target, stop, timeframe, price)
        log.info(f"Signal registered: {symbol} {signal} for user {user_id[:8]}...")
        return jsonify({'status': 'registered', 'symbol': symbol, 'signal': signal})

    except Exception as e:
        log.error(f"Register signal error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/active-signals', methods=['GET'])
def get_active_signals_route():
    """Get all active signals being monitored"""
    signals = get_all_signals()
    return jsonify({'total': len(signals), 'signals': [{'symbol': s['symbol'], 'signal': s['signal']} for s in signals]})

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
# NEWS SCANNER — checks CryptoPanic every 30 mins
# ============================================================
CRYPTOPANIC_KEY = os.environ.get("CRYPTOPANIC_KEY", "8182afa64e0f0ccf4e3fc1a4a18a8e01ca8e329b")
seen_news_ids = set()  # track already sent news

def get_crypto_news():
    """Fetch latest crypto news from CryptoPanic"""
    try:
        r = requests.get(
            f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTOPANIC_KEY}&public=true&kind=news&filter=hot",
            timeout=10
        )
        return r.json().get("results", [])
    except Exception as e:
        log.error(f"News fetch error: {e}")
        return []

def extract_symbols_from_news(news_item):
    """Extract token symbols mentioned in news"""
    symbols = []
    # From CryptoPanic currencies field
    currencies = news_item.get("currencies", [])
    for c in currencies:
        sym = c.get("code", "").upper()
        if sym and len(sym) <= 10:
            symbols.append(sym)
    return symbols

def classify_news_sentiment(title, body=""):
    """Quick sentiment classification"""
    text = (title + " " + body).lower()
    negative = ["hack", "hacked", "exploit", "breach", "scam", "rug", "stolen", "attack", "vulnerability", "drain", "phishing", "fraud", "arrested", "sued", "ban", "banned", "shutdown"]
    positive = ["launch", "listing", "partnership", "upgrade", "mainnet", "airdrop", "integration", "adoption", "etf", "approved", "record", "milestone", "institutional"]
    
    neg_count = sum(1 for w in negative if w in text)
    pos_count = sum(1 for w in positive if w in text)
    
    if neg_count > pos_count: return "BEARISH", neg_count
    if pos_count > neg_count: return "BULLISH", pos_count
    return "NEUTRAL", 0

def news_scanner_loop():
    """Scan for crypto news every 30 minutes and alert on impactful news"""
    time.sleep(90)  # wait for startup
    log.info("News scanner loop started")

    while True:
        try:
            news_items = get_crypto_news()
            new_alerts = []

            for item in news_items:
                news_id = item.get("id")
                if not news_id or news_id in seen_news_ids:
                    continue

                seen_news_ids.add(news_id)
                title  = item.get("title", "")
                url    = item.get("url", "")
                source = item.get("source", {}).get("title", "Unknown")
                symbols = extract_symbols_from_news(item)
                sentiment, strength = classify_news_sentiment(title)

                # Only alert on strong signals
                if strength == 0 or not symbols:
                    continue

                new_alerts.append({
                    "title": title,
                    "url": url,
                    "source": source,
                    "symbols": symbols,
                    "sentiment": sentiment,
                    "strength": strength,
                })

            if not new_alerts:
                time.sleep(1800)
                continue

            # Get all verified users
            profiles = sb_request("GET", "profiles", params={
                "telegram_verified": "eq.true",
                "select": "user_id,telegram_chat_id,notification_prefs"
            })
            if not profiles:
                time.sleep(1800)
                continue

            for alert in new_alerts:
                sentiment = alert["sentiment"]
                symbols   = alert["symbols"]
                title     = alert["title"]
                url       = alert["url"]
                source    = alert["source"]

                sent_label  = "BEARISH" if sentiment == "BEARISH" else "BULLISH" if sentiment == "BULLISH" else "NEUTRAL"
                sent_icon   = "▼" if sentiment == "BEARISH" else "▲" if sentiment == "BULLISH" else "—"

                # Run AI analysis on first symbol mentioned
                analysis_text = ""
                main_sym = symbols[0] if symbols else None
                if main_sym and main_sym not in ["BTC", "ETH", "USDT", "USDC"]:
                    try:
                        fresh = get_fresh_signal(main_sym, "4h")
                        if fresh and fresh.get("signal"):
                            sig = fresh["signal"]
                            conf = fresh.get("confidence", 0)
                            analysis_text = (
                                f"\n\nAI ANALYSIS — {main_sym} (4H)\n"
                                f"Signal: {sig} ({conf}% confidence)\n"
                                f"{fresh.get('reasoning','')}\n"
                                f"Entry: {fresh.get('entry','—')} | TP: {fresh.get('target','—')} | SL: {fresh.get('stop','—')}"
                            )
                    except: pass

                msg = (
                    f"{'NEWS ALERT' if sentiment == 'NEUTRAL' else 'MARKET ALERT'} — {sent_icon} {sent_label}\n\n"
                    f"<b>{title}</b>\n\n"
                    f"Source: {source}\n"
                    f"Tokens: {' '.join(symbols[:5])}\n"
                    f"{url}"
                    f"{analysis_text}\n\n"
                    f"<i>NOT FINANCIAL ADVICE</i>"
                )

                # Send to all verified users
                for p in profiles:
                    try:
                        chat_id = p.get("telegram_chat_id")
                        if not chat_id: continue
                        prefs = p.get("notification_prefs") or {}
                        if prefs.get("news") == False: continue
                        tg(chat_id, msg)
                        time.sleep(0.05)
                    except: pass

            log.info(f"News scan complete — {len(new_alerts)} new alerts sent")

        except Exception as e:
            log.error(f"News scanner error: {e}")

        time.sleep(1800)  # every 30 minutes

# ============================================================
# PRE-PUMP DETECTOR — scans MEXC every hour for accumulation
# ============================================================
pump_alerts_sent = set()  # track already alerted tokens

def detect_pre_pump_signals():
    """Detect tokens showing pre-pump accumulation patterns"""
    try:
        r = requests.get(f"{CIPHER_SERVER}/mexc-scan", timeout=15)
        data = r.json()
        if not data or "error" in data:
            return []

        suspects = []
        for sym, d in data.items():
            price  = d.get("price", 0)
            change = d.get("change", 0)
            high   = d.get("high", 0)
            low    = d.get("low", 0)
            vol    = d.get("volume", 0)

            if not price or price <= 0: continue
            if sym in ["USDT","USDC","BUSD","DAI"]: continue

            range_pct = ((high - low) / low * 100) if low > 0 else 0

            score = 0
            signals = []

            # 1. High volume but price barely moved (accumulation)
            if vol > 0 and range_pct > 20 and abs(change) < 5:
                score += 40
                signals.append("High volume + price suppressed (accumulation)")

            # 2. Price near 30-day low but volume spiking
            if change < -5 and range_pct > 15:
                score += 20
                signals.append("Dip + volume spike (smart money buying)")

            # 3. Tight range after big drop (coiling)
            if abs(change) < 3 and range_pct > 10:
                score += 20
                signals.append("Tight consolidation after movement")

            # 4. Very small cap + unusual range
            if price < 0.001 and range_pct > 50:
                score += 30
                signals.append("Micro-cap with extreme range (high pump risk)")

            if score >= 40:
                suspects.append({
                    "sym": sym,
                    "price": price,
                    "change": change,
                    "range_pct": range_pct,
                    "score": score,
                    "signals": signals,
                })

        # Sort by score
        suspects.sort(key=lambda x: x["score"], reverse=True)
        return suspects[:10]

    except Exception as e:
        log.error(f"Pre-pump detector error: {e}")
        return []

def pre_pump_loop():
    """Run pre-pump detector every hour"""
    time.sleep(120)  # wait for startup
    log.info("Pre-pump detector loop started")

    while True:
        try:
            suspects = detect_pre_pump_signals()
            if not suspects:
                time.sleep(3600)
                continue

            profiles = sb_request("GET", "profiles", params={
                "telegram_verified": "eq.true",
                "select": "telegram_chat_id,notification_prefs"
            })
            if not profiles:
                time.sleep(3600)
                continue

            for s in suspects:
                sym = s["sym"]
                alert_key = f"{sym}:{round(s['price'], 8)}"
                if alert_key in pump_alerts_sent:
                    continue
                pump_alerts_sent.add(alert_key)

                # Get AI analysis
                analysis_text = ""
                try:
                    fresh = get_fresh_signal(sym, "1h")
                    if fresh and fresh.get("signal"):
                        analysis_text = (
                            f"\nAI: {fresh['signal']} ({fresh.get('confidence')}%) — "
                            f"{fresh.get('reasoning','')[:120]}..."
                        )
                except: pass

                msg = (
                    f"PRE-PUMP ALERT — {sym}\n\n"
                    f"Score: {s['score']}/100\n"
                    f"Price: ${s['price']} ({s['change']:+.2f}%)\n"
                    f"24H Range: {s['range_pct']:.1f}%\n\n"
                    f"Signals:\n" +
                    "\n".join(f"  • {sig}" for sig in s["signals"]) +
                    f"{analysis_text}\n\n"
                    f"<b>HIGH RISK — DYOR. This may be a pump and dump.</b>\n"
                    f"<i>NOT FINANCIAL ADVICE</i>"
                )

                for p in profiles:
                    try:
                        chat_id = p.get("telegram_chat_id")
                        if not chat_id: continue
                        prefs = p.get("notification_prefs") or {}
                        if prefs.get("pumpalert") == False: continue
                        tg(chat_id, msg)
                        time.sleep(0.05)
                    except: pass

            log.info(f"Pre-pump scan done — {len(suspects)} suspects found")

        except Exception as e:
            log.error(f"Pre-pump loop error: {e}")

        time.sleep(3600)  # every hour

# ============================================================
# STARTUP
# ============================================================
if __name__ == '__main__':
    register_commands()
    threading.Thread(target=polling_loop, daemon=True).start()
    threading.Thread(target=keep_alive_loop, daemon=True).start()
    threading.Thread(target=signal_monitor_loop, daemon=True).start()
    threading.Thread(target=news_scanner_loop, daemon=True).start()
    threading.Thread(target=pre_pump_loop, daemon=True).start()
    log.info("CIPHER Notification Bot started — all systems online")
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port, debug=False)
