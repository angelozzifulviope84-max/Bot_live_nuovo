import os
import time
import requests

API_KEY = os.environ.get("API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

API_URL = "https://v3.football.api-sports.io/fixtures?live=all"
HEADERS = {"x-apisports-key": API_KEY}

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})

def get_live():
    try:
        r = requests.get(API_URL, headers=HEADERS, timeout=20)
        data = r.json()
        return data.get("response", [])
    except Exception as e:
        print(f"Errore API: {e}", flush=True)
        return []

def main():
    print("BOT NUOVO PARTITO - Tutti i campionati LIVE", flush=True)
    send_telegram("Bot gol live NUOVO partito ✅ Ora controllo TUTTE le partite live.")
    goals = {}

    while True:
        live = get_live()
        print(f"Totale live API: {len(live)}", flush=True)

        for f in live:
            fid = f["fixture"]["id"]
            home = f["teams"]["home"]["name"]
            away = f["teams"]["away"]["name"]
            league = f["league"]["name"]
            status = f["fixture"]["status"]["short"]
            elapsed = f["fixture"]["status"]["elapsed"]
            gh = f["goals"]["home"]
            ga = f["goals"]["away"]
            if gh is None: gh = 0
            if ga is None: ga = 0
            total = gh + ga

            if fid not in goals:
                goals[fid] = total
                print(f"Vedo live: {league} - {home} {gh}-{ga} {away} ({status} {elapsed}')", flush=True)
                continue

            if total > goals[fid]:
                goals[fid] = total
                msg = f"⚽ GOL! {league}\n{home} {gh}-{ga} {away}\nMinuto: {elapsed}'"
                print(msg, flush=True)
                send_telegram(msg)

        time.sleep(30)

if __name__ == "__main__":
    main()
