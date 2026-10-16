"""Проверка комплектов: python3 check.py sets.json
Формат: {"url": "https://clck.su/...", "sets": [{"title": "...", "description": "..."}]}
"""
import json, sys

data = json.load(open(sys.argv[1], encoding="utf-8"))
url = data["url"]
ok = True
for i, s in enumerate(data["sets"], 1):
    t, d = s["title"], s["description"]
    errs = []
    if len(t) != 50:
        errs.append(f"тайтл {len(t)} != 50")
    if len(d) != 1000:
        errs.append(f"описание {len(d)} != 1000")
    if "\r" in d:
        errs.append("CR в описании (нужен только LF)")
    lines = d.split("\n")
    if len(lines) < 2 or lines[1] != "":
        errs.append("нет пустой строки после первой строки")
    if url not in lines[0]:
        errs.append("ссылка не найдена в первой строке")
    if "смотреть" in t.lower():
        errs.append("«смотреть» в тайтле")
    print(f"#{i}: тайтл={len(t)} описание={len(d)}", "OK" if not errs else "; ".join(errs))
    ok &= not errs
titles = [s["title"] for s in data["sets"]]
if len(set(titles)) != len(titles):
    print("Повторяющиеся тайтлы"); ok = False
sys.exit(0 if ok else 1)
