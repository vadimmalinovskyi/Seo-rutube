"""Сокращение: python3 shorten.py "ДЛИННАЯ_ССЫЛКА" "слаг" ["Название ссылки"]"""
import json, os, sys, urllib.request, urllib.error
body = {"url": sys.argv[1]}
if len(sys.argv) > 2 and sys.argv[2]:
    body["custom"] = sys.argv[2]
if len(sys.argv) > 3 and sys.argv[3]:
    body["metatitle"] = sys.argv[3]
HDR = {"Content-Type": "application/json"}
if os.environ.get("CLCK_API_KEY"):  # локальный запуск; в облаке ключ подставляет прокси
    HDR["Authorization"] = "Bearer " + os.environ["CLCK_API_KEY"]
req = urllib.request.Request("https://clck.su/api/url/add", data=json.dumps(body).encode(), headers=HDR, method="POST")
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.load(r)
except urllib.error.HTTPError as e:
    print("HTTP", e.code, e.read().decode(errors="replace")); sys.exit(1)
if d.get("error"):
    print("API error:", d); sys.exit(1)
print(d["shorturl"])
