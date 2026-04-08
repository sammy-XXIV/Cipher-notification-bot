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

def get_news_trade_signal(symbol, timeframe='1h', news_context=''):
    """Run full CIPHER-style analysis and return complete trade signal"""
    try:
        r = requests.get(f"{CIPHER_SERVER}/candles?symbol={symbol}&interval={timeframe}&limit=80", timeout=15)
        data = r.json()
        candles = data.get("candles", [])
        if not candles or len(candles) < 20:
            return None

        closes = [c["c"] for c in candles]
        highs  = [c["h"] for c in candles]
        lows   = [c["l"] for c in candles]
        vols   = [c["v"] for c in candles]
        n = len(closes)
        price = closes[-1]

        # RSI — Wilder smoothing
        rsi = 50
        if n >= 15:
            avg_g = avg_l = 0
            for i in range(1, 15):
                d = closes[i] - closes[i-1]
                if d > 0: avg_g += d
                else: avg_l -= d
            avg_g /= 14; avg_l /= 14
            for i in range(15, n):
                d = closes[i] - closes[i-1]
                avg_g = (avg_g * 13 + (d if d > 0 else 0)) / 14
                avg_l = (avg_l * 13 + (-d if d < 0 else 0)) / 14
            rsi = round(100 - (100 / (1 + avg_g / avg_l))) if avg_l > 0 else 100

        def ema_calc(data, p):
            k = 2/(p+1); e = data[0]
            for v in data[1:]: e = v*k + e*(1-k)
            return round(e, 8)

        ema20 = ema_calc(closes, 20) if n >= 20 else closes[-1]
        ema50 = ema_calc(closes, 50) if n >= 50 else closes[-1]

        # VWAP
        tpv = sum(((highs[i]+lows[i]+closes[i])/3)*vols[i] for i in range(n))
        tvol = sum(vols)
        vwap = tpv / tvol if tvol > 0 else price

        # ATR
        trs = [max(highs[i]-lows[i], abs(highs[i]-closes[i-1]), abs(lows[i]-closes[i-1])) for i in range(1, min(15,n))]
        atr = sum(trs)/len(trs) if trs else 0

        # MACD
        def ema_series(data, p):
            k = 2/(p+1); e = [data[0]]
            for v in data[1:]: e.append(v*k + e[-1]*(1-k))
            return e
        macd_line = [a-b for a,b in zip(ema_series(closes,12), ema_series(closes,26))]
        signal_line = ema_series(macd_line, 9)
        macd = macd_line[-1] - signal_line[-1]
        macd_pct = (macd / price * 100) if price > 0 else 0

        # ADX
        adx = 0
        try:
            trs2, pdm, mdm = [], [], []
            for i in range(1, n):
                tr = max(highs[i]-lows[i], abs(highs[i]-closes[i-1]), abs(lows[i]-closes[i-1]))
                up = highs[i]-highs[i-1]; dn = lows[i-1]-lows[i]
                trs2.append(tr)
                pdm.append(up if up > dn and up > 0 else 0)
                mdm.append(dn if dn > up and dn > 0 else 0)
            p = 14
            if len(trs2) > p:
                a14 = sum(trs2[:p]); pm = sum(pdm[:p]); mm = sum(mdm[:p])
                dx = []
                for i in range(p, len(trs2)):
                    a14 = a14-a14/p+trs2[i]; pm = pm-pm/p+pdm[i]; mm = mm-mm/p+mdm[i]
                    pdi = 100*pm/a14; mdi = 100*mm/a14
                    dx.append(100*abs(pdi-mdi)/(pdi+mdi or 1))
                adx = round(sum(dx[-14:])/min(14,len(dx)))
        except: pass

        # Support / Resistance
        sup = min(lows[-20:])
        res = max(highs[-20:])
        avg_vol = sum(vols[-20:])/min(20,n)
        vol_str = "HIGH" if vols[-1] > avg_vol*1.5 else "LOW" if vols[-1] < avg_vol*0.5 else "NORMAL"
        trend = "BULLISH" if price > ema20 > ema50 else "BEARISH" if price < ema20 < ema50 else "MIXED"

        prompt = f"""You are CIPHER, elite AI crypto analyst. Analyze {symbol} based on the following data AND the news context provided.

NEWS CONTEXT:
{news_context}

The news above may create a trading opportunity. Factor it into your analysis.

TIMEFRAME: {timeframe.upper()}
Price: ${price}
RSI(14): {rsi} {'(OVERBOUGHT)' if rsi > 70 else '(OVERSOLD)' if rsi < 30 else '(NEUTRAL)'}
EMA20: ${ema20} — {'ABOVE (bullish)' if price > ema20 else 'BELOW (bearish)'}
EMA50: ${ema50} — {'ABOVE (bullish)' if price > ema50 else 'BELOW (bearish)'}
VWAP: ${round(vwap,6)} — {'ABOVE (bullish)' if price > vwap else 'BELOW (bearish)'}
MACD: {'BULLISH' if macd > 0 else 'BEARISH'} ({macd_pct:.3f}% of price)
ADX: {adx} {'(STRONG TREND)' if adx > 25 else '(WEAK)'}
ATR: ${round(atr,6)} ({round(atr/price*100,2)}% of price)
Volume: {vol_str}
Support: ${round(sup,6)} | Resistance: ${round(res,6)}
Trend: {trend}

RULES:
- Factor the news into direction — bullish news = favour LONG, bearish news = favour SHORT
- Entry for LONG must be <= ${round(price,6)} (at or below current price)
- Entry for SHORT must be >= ${round(price,6)} (at or above current price)
- SL = 1.5x ATR from entry
- TP = 3x ATR from entry (min 1:2 R/R)

Respond ONLY in JSON:
{{"signal":"LONG or SHORT or NEUTRAL","confidence":55-92,"entry":"price","target":"price","stop":"price","rr":"1:X","roi":"+X.X%","position_size":"X% of capital","risk":"LOW or MEDIUM or HIGH","reasoning":"3 sentences covering news impact + technicals","caution":"one caution flag"}}"""

        r2 = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": os.environ.get("ANTHROPIC_API_KEY",""), "anthropic-version": "2023-06-01", "Content-Type": "application/json"},
            json={"model": "claude-sonnet-4-20250514", "max_tokens": 400, "messages": [{"role": "user", "content": prompt}]},
            timeout=30
        )
        raw = r2.json()["content"][0]["text"].strip().replace("```json","").replace("```","").strip()
        return json.loads(raw)

    except Exception as e:
        log.error(f"News trade signal error for {symbol}: {e}")
        return None
    """Fetch fresh candles and get AI signal from CIPHER backend"""
    try:
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

        # RSI — proper Wilder smoothing
        rsi = 50
        if n >= 15:
            avg_g = avg_l = 0
            for i in range(1, 15):
                d = closes[i] - closes[i-1]
                if d > 0: avg_g += d
                else: avg_l -= d
            avg_g /= 14; avg_l /= 14
            for i in range(15, n):
                d = closes[i] - closes[i-1]
                avg_g = (avg_g * 13 + (d if d > 0 else 0)) / 14
                avg_l = (avg_l * 13 + (-d if d < 0 else 0)) / 14
            rsi = round(100 - (100 / (1 + avg_g / avg_l))) if avg_l > 0 else 100

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

Give a directional signal. NEUTRAL should be rare — only when LONG and SHORT are perfectly balanced.
When unsure, give LOW confidence (50-65%) LONG or SHORT based on EMA position and RSI.
Entry must be at key support/resistance — NOT just current price.
For SHORT: entry >= current price. For LONG: entry <= current price.

Respond ONLY in JSON:
{{"signal":"LONG or SHORT or NEUTRAL","confidence":40-92,"entry":"price at key level","target":"price","stop":"price","rr":"1:X","reasoning":"1-2 sentences"}}"""

        r2 = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": os.environ.get("ANTHROPIC_API_KEY",""), "anthropic-version": "2023-06-01", "Content-Type": "application/json"},
            json={"model": "claude-sonnet-4-20250514", "max_tokens": 250, "messages": [{"role": "user", "content": prompt}]},
            timeout=30
        )
        raw = r2.json()["content"][0]["text"].strip().replace("```json","").replace("```","").strip()
        return json.loads(raw)

    except Exception as e:
        log.error(f"get_fresh_signal error for {symbol}: {e}")
        return None


def get_news_triggered_analysis(news_title, sentiment, symbols, is_macro):
    """Run full analysis on best token to trade given the news"""
    try:
        # Pick best symbol to analyse
        # For macro news → BTC first, then ETH
        # For crypto news → use mentioned symbols
        # For bearish news → look for SHORT opportunities
        # For bullish news → look for LONG opportunities

        MACRO_SYMBOLS = ["BTC", "ETH", "BNB", "SOL"]

        if is_macro:
            candidates = MACRO_SYMBOLS
        elif symbols:
            # Add BTC/ETH for context on crypto news too
            candidates = list(dict.fromkeys(symbols[:3] + ["BTC"]))
        else:
            candidates = MACRO_SYMBOLS

        best_signal = None
        best_sym = None
        best_tf = "1h"

        for sym in candidates[:4]:
            try:
                sig = get_fresh_signal(sym, "1h")
                if not sig or sig.get("signal") == "NEUTRAL":
                    continue
                conf = sig.get("confidence", 0)
                # For bullish news prefer LONG signals, bearish prefer SHORT
                direction_match = (
                    (sentiment == "BULLISH" and sig["signal"] == "LONG") or
                    (sentiment == "BEARISH" and sig["signal"] == "SHORT")
                )
                score = conf + (20 if direction_match else 0)
                if best_signal is None or score > best_signal.get("_score", 0):
                    sig["_score"] = score
                    sig["_sym"] = sym
                    best_signal = sig
                    best_sym = sym
                time.sleep(0.5)
            except: continue

        if not best_signal or not best_sym:
            return None, None

        return best_sym, best_signal

    except Exception as e:
        log.error(f"News triggered analysis error: {e}")
        return None, None

def signal_monitor_loop():
    """Check signals — interval adapts to shortest active timeframe"""
    time.sleep(60)
    log.info("Signal monitor loop started")

    # Much faster intervals — SL hits happen in minutes not hours
    TIMEFRAME_INTERVALS = {'5m': 60, '15m': 120, '1h': 180, '4h': 300, '1d': 600, '1w': 1200}
    # Major tokens that move fast — always check every 2 minutes
    MAJOR_TOKENS = {'BTC','ETH','BNB','SOL','XRP','ADA','AVAX','DOGE','DOT','MATIC','ARB','OP'}

    while True:
        try:
            signals = get_all_signals()
            if not signals:
                log.info("No active signals to monitor")
                time.sleep(120)
                continue

            # If any signal is a major token, use 2 min interval regardless
            symbols = [s.get('symbol','') for s in signals]
            has_major = any(sym in MAJOR_TOKENS for sym in symbols)

            if has_major:
                sleep_time = 120  # 2 minutes for major tokens
            else:
                active_tfs = [s.get('timeframe', '1h') for s in signals]
                sleep_time = min(TIMEFRAME_INTERVALS.get(tf, 180) for tf in active_tfs)

            log.info(f"Monitoring {len(signals)} signals — next check in {sleep_time}s")

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

                    # Get real current price from server ticker
                    current_price = 0
                    try:
                        pr = requests.get(f"{CIPHER_SERVER}/ticker?symbol={symbol}", timeout=8)
                        pd = pr.json()
                        current_price = float(pd.get('price', 0) or 0)
                    except: pass

                    # Get fresh signal for analysis
                    fresh = get_fresh_signal(symbol, timeframe)
                    if not fresh:
                        continue

                    new_signal = fresh.get('signal')
                    # Use ticker price if available, fallback to fresh signal entry
                    if not current_price:
                        current_price = float(str(fresh.get('entry', 0)).replace('$','') or 0)
                    prev_emoji = "▲" if old_signal == "LONG" else "▼"
                    new_emoji  = "▲" if new_signal == "LONG" else "▼"

                    # ── LIMIT MISS DETECTION ──
                    # Check if price never hit entry and is now running away
                    try:
                        # Parse entry price — handle ranges like "$585-587" or text descriptions
                        entry_str = str(entry).replace('$','').replace(',','').strip()
                        # Extract first number found
                        import re as _re
                        nums = _re.findall(r'\d+\.?\d*', entry_str)
                        entry_price = float(nums[0]) if nums else 0
                        price_at_reg  = float(str(stored.get('price', 0)) or 0)
                        filled        = stored.get('filled', False)

                        if not filled and entry_price and current_price and price_at_reg:
                            # Calculate ATR as % of price for threshold
                            atr_est = price_at_reg * 0.02  # 2% estimate

                            # LONG limit miss — price ran UP without filling
                            if old_signal == "LONG" and current_price > entry_price:
                                move_pct = ((current_price - entry_price) / entry_price) * 100
                                # Price moved up 2x ATR from entry without touching it
                                if move_pct >= 0.8:
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
                                if move_pct >= 0.8:
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
                        import re as _re
                        def parse_price(s):
                            """Extract first number from price string like '$69,200' or '$68,200-68,300 zone'"""
                            if not s: return 0
                            nums = _re.findall(r'[\d,]+\.?\d*', str(s).replace('$',''))
                            if not nums: return 0
                            return float(nums[0].replace(',',''))

                        tp_price = parse_price(tp)
                        sl_price = parse_price(sl)

                        if tp_price and current_price:
                            tp_hit = (old_signal == "LONG" and current_price >= tp_price) or \
                                     (old_signal == "SHORT" and current_price <= tp_price)
                            if tp_hit:
                                tg(chat_id,
                                    f"🎯 <b>TAKE PROFIT HIT — {symbol}</b>\n\n"
                                    f"Your {old_signal} position reached TP!\n"
                                    f"Current: <b>${current_price}</b> | TP: <b>{tp}</b>\n\n"
                                    f"Consider closing your position. 💰\n\n"
                                    f"<i>NOT FINANCIAL ADVICE</i>"
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
                                    f"Fresh signal: {new_emoji} <b>{new_signal}</b> ({fresh.get('confidence')}%)\n"
                                    f"📝 {fresh.get('reasoning','')}\n\n"
                                    f"<i>NOT FINANCIAL ADVICE</i>"
                                )
                                delete_signal(user_id, symbol)
                                continue

                    except Exception as e:
                        log.warning(f"TP/SL check error: {e}")

                    # ── ADVERSE MOVE ALERT — price moving against position ──
                    try:
                        price_at_signal = float(str(stored.get('price', 0)) or 0)
                        # Lower threshold for major tokens — they move faster
                        adverse_threshold = 1.5 if symbol in MAJOR_TOKENS else 3.0
                        if price_at_signal > 0 and current_price > 0:
                            adverse_key = f"adverse:{user_id}:{symbol}"
                            if old_signal == "SHORT":
                                adverse_pct = ((current_price - price_at_signal) / price_at_signal) * 100
                                if adverse_pct >= adverse_threshold and adverse_key not in pump_alerts_sent:
                                    pump_alerts_sent.add(adverse_key)
                                    tg(chat_id,
                                        f"⚠️ <b>ADVERSE MOVE — {symbol}</b>\n\n"
                                        f"Your SHORT is moving against you!\n"
                                        f"Signal price: <b>${price_at_signal}</b>\n"
                                        f"Current: <b>${current_price}</b> (+{adverse_pct:.1f}%)\n\n"
                                        f"SL is at <b>{sl}</b> — consider closing now to limit losses.\n\n"
                                        f"<i>NOT FINANCIAL ADVICE</i>"
                                    )
                            elif old_signal == "LONG":
                                adverse_pct = ((price_at_signal - current_price) / price_at_signal) * 100
                                if adverse_pct >= adverse_threshold and adverse_key not in pump_alerts_sent:
                                    pump_alerts_sent.add(adverse_key)
                                    tg(chat_id,
                                        f"⚠️ <b>ADVERSE MOVE — {symbol}</b>\n\n"
                                        f"Your LONG is moving against you!\n"
                                        f"Signal price: <b>${price_at_signal}</b>\n"
                                        f"Current: <b>${current_price}</b> (-{adverse_pct:.1f}%)\n\n"
                                        f"SL is at <b>{sl}</b> — consider closing now to limit losses.\n\n"
                                        f"<i>NOT FINANCIAL ADVICE</i>"
                                    )
                    except Exception as e:
                        log.warning(f"Adverse move check error: {e}")

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
# NEWS SCANNER — multi-source: crypto + macro + geopolitical
# ============================================================
CRYPTOPANIC_KEY = os.environ.get("CRYPTOPANIC_KEY", "8182afa64e0f0ccf4e3fc1a4a18a8e01ca8e329b")
seen_news_ids = set()

# Keywords that affect crypto markets
BULLISH_KEYWORDS = [
    # Crypto specific
    "etf approved", "etf approval", "spot etf", "etf launch", "listing", "listed on",
    "mainnet launch", "mainnet live", "launch", "partnership", "adoption", "integration",
    "airdrop", "upgrade", "institutional", "record high", "all time high", "ath",
    "bull", "rally", "surge", "breakout", "accumulation", "buy", "bullish",
    "inflows", "institutional buying", "whale accumulation", "mass adoption",
    "legal tender", "accepts bitcoin", "accepts crypto", "pays in crypto",
    "store of value", "reserve asset", "national reserve", "strategic reserve",
    "coinbase listing", "binance listing", "kraken listing", "okx listing",
    "sec approves", "sec approved", "cftc approves", "regulated", "regulation clarity",
    "staking rewards", "yield", "tvl increase", "protocol upgrade", "v2 launch", "v3 launch",
    "layer 2", "scaling solution", "faster", "cheaper", "burn", "token burn", "buyback",
    "partnership with", "collaboration", "deal signed", "mou signed",
    "government adopts", "country adopts", "nation adopts", "central bank buys",
    "hedge fund buys", "pension fund", "endowment", "sovereign wealth",
    "bitcoin treasury", "crypto treasury", "balance sheet",
    "positive", "growth", "expansion", "profit", "revenue increase",

    # Macro bullish
    "peace deal", "peace agreement", "ceasefire", "ceasefire agreement", "peace talks",
    "treaty signed", "conflict resolved", "war ends", "tensions ease", "de-escalation",
    "rate cut", "rate cuts", "interest rate cut", "fed cuts", "dovish", "pivot",
    "fed pivot", "quantitative easing", "qe", "stimulus", "stimulus package",
    "inflation cooling", "inflation falls", "inflation lower", "cpi drops", "cpi lower",
    "soft landing", "no recession", "economic growth", "gdp growth", "strong jobs",
    "unemployment falls", "trade deal", "trade agreement", "tariffs removed",
    "sanctions lifted", "sanctions removed", "sanctions eased",
    "deregulation", "pro crypto", "pro bitcoin", "pro innovation",
    "risk on", "market rally", "stock market up", "s&p rally", "nasdaq rally",
    "dollar weakens", "dxy falls", "dollar index falls", "weak dollar",
    "oil price falls", "energy prices fall", "commodity prices fall",
    "banking system stable", "financial stability", "liquidity injection",
    "positive gdp", "economic recovery", "economic expansion",
    "election victory", "pro crypto candidate wins", "pro crypto government",
    "trump bitcoin", "trump crypto", "strategic bitcoin reserve",

    # Geopolitical bullish
    "diplomacy", "diplomatic solution", "negotiations succeed", "summit agreement",
    "nuclear deal", "arms reduction", "military withdrawal", "troops withdraw",
    "sanctions relief", "embargo lifted", "trade restored",
]

BEARISH_KEYWORDS = [
    # Crypto specific
    "hack", "hacked", "exploit", "exploited", "breach", "breached",
    "scam", "rug pull", "rug pulled", "stolen", "theft", "drained",
    "attack", "attacked", "vulnerability", "zero day", "phishing",
    "fraud", "fraudulent", "ponzi", "pyramid scheme",
    "arrested", "arrested for", "charged with", "indicted", "convicted",
    "sued", "lawsuit", "legal action", "court order", "injunction",
    "ban", "banned", "banning", "prohibit", "prohibited", "outlawed",
    "shutdown", "shut down", "closed", "exit scam", "exit",
    "delisted", "delisting", "removed from", "suspended trading",
    "sec sues", "sec charges", "doj charges", "cftc charges",
    "money laundering", "sanctions violation", "compliance failure",
    "insolvency", "insolvent", "bankrupt", "bankruptcy", "chapter 11",
    "withdrawal halt", "withdrawals paused", "withdrawals suspended",
    "frozen", "freeze", "assets frozen", "funds frozen",
    "crash", "crashed", "dump", "dumping", "collapse", "collapsed",
    "death spiral", "depeg", "depegged", "stablecoin collapse",
    "outflows", "institutional selling", "whale selling", "sell off",
    "bear", "bearish", "downtrend", "resistance", "rejected",
    "security breach", "private key", "seed phrase exposed",
    "exchange collapse", "exchange bankrupt", "ftx", "celsius", "luna",

    # Macro bearish
    "war", "warfare", "military strike", "airstrike", "bombing", "invasion",
    "nuclear threat", "nuclear weapon", "missile launch", "missile strike",
    "terror attack", "terrorist", "assassination",
    "rate hike", "rate hikes", "interest rate hike", "fed hikes", "hawkish",
    "quantitative tightening", "qt", "liquidity drain",
    "inflation spike", "inflation surges", "cpi rises", "cpi higher", "hot inflation",
    "recession", "recessionary", "economic contraction", "gdp falls", "gdp shrinks",
    "unemployment rises", "job losses", "layoffs massive",
    "trade war", "tariff increase", "tariffs imposed", "trade sanctions",
    "sanctions imposed", "new sanctions", "financial sanctions",
    "bank failure", "bank run", "banking crisis", "financial crisis",
    "debt ceiling", "debt default", "sovereign default", "credit downgrade",
    "dollar strengthens", "dxy rises", "strong dollar",
    "oil price spike", "energy crisis", "commodity shortage",
    "market crash", "stock market crash", "black monday", "circuit breaker",
    "pandemic", "outbreak", "lockdown", "quarantine",
    "political crisis", "government collapse", "coup", "civil war",
    "regulatory crackdown", "crypto ban", "bitcoin ban", "mining ban",
    "capital controls", "currency crisis", "hyperinflation",
    "contagion", "systemic risk", "too big to fail", "bailout needed",

    # Geopolitical bearish
    "escalation", "escalates", "tensions rise", "conflict escalates",
    "military buildup", "troops mobilize", "naval blockade",
    "proxy war", "regional conflict", "middle east conflict",
    "north korea", "missile test", "nuclear test",
    "china taiwan", "taiwan strait", "south china sea",
    "russia ukraine", "nato conflict",
]

MACRO_KEYWORDS = [
    # Central banks
    "federal reserve", "fed ", "fomc", "powell", "interest rate", "rate decision",
    "bank of england", "boe", "ecb", "european central bank", "boj", "bank of japan",
    "inflation", "cpi", "pce", "deflation", "stagflation",
    "quantitative easing", "quantitative tightening", "money supply",
    "yield curve", "bond yield", "treasury yield", "10 year yield",

    # Economic indicators
    "gdp", "unemployment", "nonfarm payroll", "jobs report", "retail sales",
    "manufacturing", "pmi", "ism", "consumer confidence", "housing data",
    "trade balance", "current account", "budget deficit", "national debt",

    # Geopolitical
    "war", "peace", "ceasefire", "conflict", "invasion", "military",
    "iran", "russia", "china", "usa", "ukraine", "israel", "north korea",
    "taiwan", "nato", "g7", "g20", "united nations", "un security council",
    "sanctions", "embargo", "trade war", "tariff",
    "oil", "opec", "energy", "natural gas", "commodity",

    # Markets
    "s&p 500", "nasdaq", "dow jones", "stock market", "equity market",
    "risk on", "risk off", "safe haven", "gold price", "dollar index", "dxy",
    "emerging markets", "forex", "currency",

    # Political
    "election", "president", "congress", "senate", "parliament",
    "trump", "biden", "administration", "policy", "executive order",
    "regulation", "legislation", "law passed", "bill signed",

    # Crypto specific macro
    "bitcoin", "crypto", "blockchain", "defi", "cbdc", "digital currency",
    "stablecoin", "tether", "usdc", "digital dollar",
]

def fetch_all_news():
    """Fetch from multiple news sources"""
    all_news = []

    # 1. CryptoPanic — crypto specific
    try:
        r = requests.get(
            f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTOPANIC_KEY}&public=true&kind=news&filter=hot",
            timeout=10
        )
        items = r.json().get("results", [])
        for item in items:
            all_news.append({
                "id": f"cp_{item.get('id')}",
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "source": item.get("source", {}).get("title", "CryptoPanic"),
                "symbols": [c.get("code","").upper() for c in item.get("currencies", []) if c.get("code")],
                "type": "crypto"
            })
    except Exception as e:
        log.warning(f"CryptoPanic fetch error: {e}")

    # 2. CryptoPanic — also fetch important/bullish/bearish filtered
    for filter_type in ["important", "bullish", "bearish"]:
        try:
            r = requests.get(
                f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTOPANIC_KEY}&public=true&kind=news&filter={filter_type}",
                timeout=10
            )
            items = r.json().get("results", [])
            for item in items:
                news_id = f"cp_{filter_type}_{item.get('id')}"
                all_news.append({
                    "id": news_id,
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "source": item.get("source", {}).get("title", "CryptoPanic"),
                    "symbols": [c.get("code","").upper() for c in item.get("currencies", []) if c.get("code")],
                    "type": f"crypto_{filter_type}"
                })
        except Exception as e:
            log.warning(f"CryptoPanic {filter_type} fetch error: {e}")

    # 3. RSS feeds — macro & geopolitical (parsed as plain text)
    rss_sources = [
        ("https://feeds.reuters.com/reuters/businessNews", "Reuters Business"),
        ("https://feeds.bbci.co.uk/news/business/rss.xml", "BBC Business"),
        ("https://feeds.bloomberg.com/markets/news.rss", "Bloomberg Markets"),
    ]
    for rss_url, source_name in rss_sources:
        try:
            r = requests.get(rss_url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
            if not r.ok: continue
            content = r.text
            # Simple RSS parsing — extract titles
            import re as _re
            titles = _re.findall(r'<title><!\[CDATA\[(.*?)\]\]></title>|<title>(.*?)</title>', content)
            links  = _re.findall(r'<link>(.*?)</link>', content)
            for i, title_match in enumerate(titles[:15]):
                title = (title_match[0] or title_match[1]).strip()
                if not title or title == source_name: continue
                url = links[i] if i < len(links) else rss_url
                all_news.append({
                    "id": f"rss_{source_name}_{hash(title)}",
                    "title": title,
                    "url": url,
                    "source": source_name,
                    "symbols": [],
                    "type": "macro"
                })
        except Exception as e:
            log.warning(f"RSS {source_name} error: {e}")

    return all_news

def classify_news(title, news_type="crypto"):
    """Classify news sentiment and impact"""
    text = title.lower()

    # Count bullish/bearish keywords
    bull_hits = [kw for kw in BULLISH_KEYWORDS if kw in text]
    bear_hits  = [kw for kw in BEARISH_KEYWORDS if kw in text]
    macro_hits = [kw for kw in MACRO_KEYWORDS if kw in text]

    is_macro = len(macro_hits) > 0 or news_type == "macro"
    strength = max(len(bull_hits), len(bear_hits))

    if len(bear_hits) > len(bull_hits):
        return "BEARISH", strength, is_macro, bear_hits[:3]
    elif len(bull_hits) > len(bear_hits):
        return "BULLISH", strength, is_macro, bull_hits[:3]
    return "NEUTRAL", 0, is_macro, []

def extract_crypto_symbols_from_title(title):
    """Extract crypto symbols mentioned in news title"""
    import re as _re
    known = ["BTC","ETH","BNB","SOL","XRP","ADA","DOGE","AVAX","DOT","MATIC",
             "LINK","UNI","AAVE","ARB","OP","SUI","APT","INJ","TIA","ATOM",
             "LTC","BCH","ETC","FIL","ICP","NEAR","FTM","ALGO","VET","SAND",
             "MANA","AXS","GALA","IMX","BLUR","PEPE","SHIB","FLOKI","WIF","BONK"]
    text = title.upper()
    found = []
    for sym in known:
        if sym in text or f"${sym}" in text:
            found.append(sym)
    return found

def news_scanner_loop():
    """Comprehensive news scanner — crypto + macro + geopolitical"""
    time.sleep(90)
    log.info("News scanner loop started — multi-source mode")

    while True:
        try:
            all_news = fetch_all_news()
            log.info(f"News scanner: fetched {len(all_news)} items from all sources")
            new_alerts = []

            for item in all_news:
                news_id = item["id"]
                if news_id in seen_news_ids:
                    continue
                seen_news_ids.add(news_id)

                title    = item["title"]
                url      = item["url"]
                source   = item["source"]
                symbols  = item.get("symbols", []) or extract_crypto_symbols_from_title(title)
                news_type = item.get("type", "crypto")

                if not title: continue

                sentiment, strength, is_macro, keywords = classify_news(title, news_type)

                # Skip truly neutral news with no keywords
                if sentiment == "NEUTRAL" and not is_macro:
                    continue

                # Skip weak non-macro news
                if strength == 0 and not is_macro:
                    continue

                new_alerts.append({
                    "title": title,
                    "url": url,
                    "source": source,
                    "symbols": symbols,
                    "sentiment": sentiment,
                    "strength": strength,
                    "is_macro": is_macro,
                    "keywords": keywords,
                    "news_type": news_type,
                })

            if not new_alerts:
                log.info("News scanner: no new alerts")
                time.sleep(1800)
                continue

            log.info(f"News scanner: {len(new_alerts)} new alerts to send")

            # Get all verified users
            profiles = sb_request("GET", "profiles", params={
                "telegram_verified": "eq.true",
                "select": "user_id,telegram_chat_id,notification_prefs"
            })
            if not profiles:
                time.sleep(1800)
                continue

            for alert in new_alerts:
                sentiment  = alert["sentiment"]
                symbols    = alert["symbols"]
                title      = alert["title"]
                url        = alert["url"]
                source     = alert["source"]
                is_macro   = alert["is_macro"]
                keywords   = alert["keywords"]
                news_type  = alert["news_type"]

                sent_icon = "▲" if sentiment == "BULLISH" else "▼" if sentiment == "BEARISH" else "—"

                # Determine alert type label
                if is_macro:
                    alert_label = "MACRO ALERT"
                    impact = "⚠️ This affects ALL crypto — check open positions"
                elif "important" in news_type:
                    alert_label = "BREAKING NEWS"
                    impact = ""
                elif sentiment == "BEARISH":
                    alert_label = "BEARISH ALERT"
                    impact = ""
                elif sentiment == "BULLISH":
                    alert_label = "BULLISH ALERT"
                    impact = ""
                else:
                    alert_label = "NEWS ALERT"
                    impact = ""

                # Run AI analysis on first mentioned symbol
                # Run full news-triggered analysis
                analysis_text = ""
                trade_sym, trade_sig = get_news_triggered_analysis(
                    title, sentiment, symbols, is_macro
                )
                if trade_sym and trade_sig and trade_sig.get("signal") != "NEUTRAL":
                    sig_icon = "▲" if trade_sig["signal"] == "LONG" else "▼"
                    analysis_text = (
                        f"\n\n📊 <b>AUTO ANALYSIS — {trade_sym} 1H</b>\n"
                        f"Signal: {sig_icon} <b>{trade_sig['signal']}</b> ({trade_sig.get('confidence')}% confidence)\n"
                        f"Entry: <b>{trade_sig.get('entry','—')}</b>\n"
                        f"TP: <b>{trade_sig.get('target','—')}</b>\n"
                        f"SL: <b>{trade_sig.get('stop','—')}</b>\n"
                        f"R/R: {trade_sig.get('rr','—')}\n\n"
                        f"📝 {trade_sig.get('reasoning','')}"
                    )

                msg = (
                    f"{sent_icon} <b>{alert_label} — {sentiment}</b>\n\n"
                    f"<b>{title}</b>\n\n"
                    f"Source: {source}\n"
                    + (f"Tokens: <b>{' '.join(symbols[:5])}</b>\n" if symbols else "")
                    + (f"Why: {', '.join(keywords[:3])}\n" if keywords else "")
                    + (f"\n{impact}\n" if impact else "")
                    + f"\n{url}\n\n"
                    f"<i>NOT FINANCIAL ADVICE</i>"
                )

                # Run full trade analysis on affected token(s)
                trade_msgs = []
                tokens_to_analyze = symbols[:2] if symbols else (["BTC"] if is_macro else [])

                for sym in tokens_to_analyze:
                    try:
                        news_context = f"{sentiment} news: {title}\nSource: {source}\nKeywords: {', '.join(keywords)}"
                        tf = "1h" if is_macro else "4h"
                        signal = get_news_trade_signal(sym, tf, news_context)

                        if signal and signal.get("signal") != "NEUTRAL":
                            sig     = signal["signal"]
                            conf    = signal.get("confidence", 0)
                            entry   = signal.get("entry", "—")
                            tp      = signal.get("target", "—")
                            sl      = signal.get("stop", "—")
                            rr      = signal.get("rr", "—")
                            roi     = signal.get("roi", "—")
                            size    = signal.get("position_size", "—")
                            risk    = signal.get("risk", "—")
                            reason  = signal.get("reasoning", "")
                            caution = signal.get("caution", "")
                            sig_icon = "▲" if sig == "LONG" else "▼"

                            trade_msg = (
                                f"{sig_icon} <b>NEWS TRADE SIGNAL — {sym}</b>\n\n"
                                f"Signal: <b>{sig}</b> ({conf}% confidence)\n"
                                f"Timeframe: {tf.upper()} | Risk: {risk}\n\n"
                                f"Entry: <b>{entry}</b>\n"
                                f"TP: <b>{tp}</b> ({roi})\n"
                                f"SL: <b>{sl}</b>\n"
                                f"R/R: {rr} | Size: {size}\n\n"
                                f"📝 {reason}\n"
                                + (f"⚠️ {caution}\n" if caution else "")
                                + f"\n<i>NOT FINANCIAL ADVICE</i>"
                            )
                            trade_msgs.append(trade_msg)
                    except Exception as e:
                        log.error(f"Trade signal error for {sym}: {e}")

                for p in profiles:
                    try:
                        chat_id = p.get("telegram_chat_id")
                        if not chat_id: continue
                        prefs = p.get("notification_prefs") or {}
                        if isinstance(prefs, str):
                            try: prefs = json.loads(prefs)
                            except: prefs = {}
                        if prefs.get("news") == False: continue
                        # Send news alert first
                        tg(chat_id, msg)
                        time.sleep(0.3)
                        # Then send trade signals
                        for trade_msg in trade_msgs:
                            tg(chat_id, trade_msg)
                            time.sleep(0.3)
                    except: pass

            log.info(f"News scan complete — {len(new_alerts)} alerts sent")

        except Exception as e:
            log.error(f"News scanner error: {e}")

        time.sleep(900)  # every 15 minutes

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
            log.warning(f"Pre-pump: mexc-scan returned error or empty")
            return []

        log.info(f"Pre-pump: scanning {len(data)} tokens")
        suspects = []
        for sym, d in data.items():
            price  = d.get("price", 0)
            change = d.get("change", 0)
            high   = d.get("high", 0)
            low    = d.get("low", 0)
            vol    = d.get("volume", 0)

            if not price or price <= 0: continue
            if sym in ["USDT","USDC","BUSD","DAI","FDUSD","TUSD"]: continue
            if price < 0.0000001: continue

            range_pct = ((high - low) / low * 100) if low > 0 else 0

            score = 0
            signals = []

            # 1. High range but price barely moved (accumulation pattern)
            if range_pct > 20 and abs(change) < 5:
                score += 40
                signals.append(f"High range {range_pct:.1f}% but price flat — accumulation")

            # 2. Dip + big range = smart money buying the dip
            if change < -8 and range_pct > 20:
                score += 30
                signals.append(f"Sharp dip {change:.1f}% + high range — potential reversal")

            # 3. Tight range after movement (coiling for breakout)
            if abs(change) < 2 and range_pct > 15:
                score += 25
                signals.append(f"Tight consolidation ({change:+.1f}%) — coiling for breakout")

            # 4. Micro-cap with extreme range (pump risk)
            if price < 0.001 and range_pct > 40:
                score += 35
                signals.append(f"Micro-cap ${price} with extreme range {range_pct:.0f}%")

            # 5. Strong positive momentum building
            if 5 < change < 50 and range_pct > 15:
                score += 20
                signals.append(f"Building momentum +{change:.1f}%")

            # 6. Volume spike
            if vol > 0 and vol > 100000:  # $100k+ volume (lowered from 500k)
                score += 15
                signals.append(f"Volume ${vol/1e6:.2f}M")

            if score >= 25 and signals:  # lowered from 40 to 25
                suspects.append({
                    "sym": sym,
                    "price": price,
                    "change": change,
                    "range_pct": range_pct,
                    "score": score,
                    "signals": signals,
                })

        suspects.sort(key=lambda x: x["score"], reverse=True)
        log.info(f"Pre-pump: found {len(suspects)} suspects")
        return suspects[:10]

    except Exception as e:
        log.error(f"Pre-pump detector error: {e}")
        return []

def pre_pump_loop():
    """Run pre-pump detector every hour"""
    time.sleep(120)
    log.info("Pre-pump detector loop started")

    while True:
        try:
            suspects = detect_pre_pump_signals()
            if not suspects:
                log.info("Pre-pump: no suspects this scan")
                time.sleep(1200)
                continue

            profiles = sb_request("GET", "profiles", params={
                "telegram_verified": "eq.true",
                "select": "telegram_chat_id,notification_prefs"
            })
            if not profiles:
                log.warning("Pre-pump: no verified profiles found")
                time.sleep(1200)
                continue

            log.info(f"Pre-pump: sending alerts to {len(profiles)} users")

            for s in suspects:
                sym = s["sym"]
                # Reset key every hour
                alert_key = f"{sym}:{datetime.now().strftime('%Y%m%d%H')}"
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
                    f"🔥 <b>PRE-PUMP ALERT — {sym}</b>\n\n"
                    f"Score: <b>{s['score']}/100</b>\n"
                    f"Price: ${s['price']} ({s['change']:+.2f}%)\n"
                    f"24H Range: {s['range_pct']:.1f}%\n\n"
                    f"<b>Signals:</b>\n" +
                    "\n".join(f"• {sig}" for sig in s["signals"]) +
                    f"{analysis_text}\n\n"
                    f"<b>HIGH RISK — DYOR. This may be a pump and dump.</b>\n"
                    f"<i>NOT FINANCIAL ADVICE</i>"
                )

                for p in profiles:
                    try:
                        chat_id = p.get("telegram_chat_id")
                        if not chat_id: continue
                        # Parse prefs safely — could be dict or JSON string
                        prefs = p.get("notification_prefs") or {}
                        if isinstance(prefs, str):
                            try: prefs = json.loads(prefs)
                            except: prefs = {}
                        if prefs.get("pumpalert") == False: continue
                        tg(chat_id, msg)
                        log.info(f"Pre-pump alert sent for {sym} to {chat_id}")
                        time.sleep(0.05)
                    except Exception as e:
                        log.error(f"Pre-pump send error: {e}")

            log.info(f"Pre-pump scan done — {len(suspects)} suspects found")

        except Exception as e:
            log.error(f"Pre-pump loop error: {e}")

        time.sleep(1200)  # every 20 minutes

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


