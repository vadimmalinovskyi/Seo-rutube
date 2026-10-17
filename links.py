"""Поиск по базе ссылок clck.su: python3 links.py "запрос" [ещё запрос ...]
Ищет без учёта регистра по слагу, названию и длинной ссылке. Без запроса — 20 последних."""
import json, os, sys, urllib.request

def page(n):
    req = urllib.request.Request(f"https://clck.su/api/urls?limit=100&page={n}")
    if os.environ.get("CLCK_API_KEY"):  # локальный запуск; в облаке ключ подставляет прокси
        req.add_header("Authorization", "Bearer " + os.environ["CLCK_API_KEY"])
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.load(r)
    if d.get("error"):
        print("API error:", d); sys.exit(1)
    return d["data"]

urls, n = [], 1
while True:
    d = page(n)
    urls += d["urls"]
    if not d.get("nextpage") or n >= d.get("maxpage", n):
        break
    n += 1
qs = [q.lower() for q in sys.argv[1:]]
hits = [u for u in urls if all(q in f'{u["alias"]} {u["title"]} {u["longurl"]}'.lower() for q in qs)] if qs else urls[:20]
for u in hits:
    print(f'{u["shorturl"]} | {u["title"]} | клики {u["clicks"]} | {u["date"][:10]} | {u["longurl"]}')
print(f"Найдено: {len(hits)} из {len(urls)}")
