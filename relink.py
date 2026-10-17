"""Перенаправить существующую короткую ссылку: python relink.py "слаг" "НОВАЯ_ДЛИННАЯ_ССЫЛКА"
Слаг и статистика остаются, меняется только длинная ссылка."""
import json, os, sys, urllib.request, urllib.error

alias, url = sys.argv[1], sys.argv[2]
HDR = {"Content-Type": "application/json"}
if os.environ.get("CLCK_API_KEY"):  # локальный запуск; в облаке ключ подставляет прокси
    HDR["Authorization"] = "Bearer " + os.environ["CLCK_API_KEY"]

def call(path, body=None, method="GET"):
    req = urllib.request.Request("https://clck.su/api/" + path, data=body and json.dumps(body).encode(), headers=HDR, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} {e.read().decode(errors='replace')}")

n = 1
while True:
    d = call(f"urls?limit=100&page={n}")["data"]
    hit = next((u for u in d["urls"] if u["alias"] == alias), None)
    if hit or not d.get("nextpage") or n >= d.get("maxpage", n):
        break
    n += 1
if not hit:
    sys.exit(f"Слаг не найден: {alias}")
d = call(f"url/{hit['id']}/update", {"url": url}, "PUT")
if d.get("error"):
    sys.exit(f"API error: {d}")
print(f"{hit['shorturl']}: {hit['longurl']} -> {url}")
