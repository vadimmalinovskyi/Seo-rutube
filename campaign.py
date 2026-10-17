"""Кампания для AliasMode (как HTML-мастер): python campaign.py sets.json "Название кампании" "C:\\полный\\путь\\картинка.jpg"
Сначала гоняет check.py, потом пишет в ОБЩАЯ БАЗА РУТУБ/<кампания>/NN/ title.txt, description.txt, image.txt, _rutube_status.json (ready)
и делает кампанию активной (_rutube_active_campaign.txt). Публикации дописываются с первого свободного номера."""
import json, os, re, subprocess, sys
from datetime import datetime, timezone

BASE = os.environ.get("RUTUBE_BASE", r"C:\Users\malin\Downloads\ПРОЛИВКИ ЮТУБ ВИДЕО\ОБЩАЯ БАЗА РУТУБ")
sets_file, name, image = sys.argv[1], sys.argv[2].strip(), sys.argv[3].strip().strip('"\'')

if subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "check.py"), sets_file]).returncode:
    sys.exit("check.py не прошёл — кампанию не трогаю")
if not os.path.isfile(image):
    sys.exit(f"Картинки нет: {image}")
# те же правила имени, что safeFolderName в HTML
name = re.sub(r"\s+", " ", re.sub(r'[<>:"/\\|?*\x00-\x1f]', "-", name)).rstrip(". ")[:80]
if not name or name.startswith("_"):
    sys.exit("Плохое имя кампании")

def write(path, text):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)

def now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")

camp = os.path.join(BASE, name)
os.makedirs(camp, exist_ok=True)
links = os.path.join(camp, "ссылки.txt")
if not os.path.exists(links):
    write(links, "")
write(os.path.join(camp, "campaign_image.txt"), image)

used = {int(d) for d in os.listdir(camp) if d.isdigit() and os.path.isdir(os.path.join(camp, d))}
n = 1
for s in json.load(open(sets_file, encoding="utf-8"))["sets"]:
    while n in used:
        n += 1
    folder = f"{n:02d}"
    pub = os.path.join(camp, folder)
    os.makedirs(pub)
    write(os.path.join(pub, "_rutube_status.json"), json.dumps({"state": "drafting", "folder": folder, "createdAt": now()}, indent=2))
    write(os.path.join(pub, "title.txt"), s["title"])
    write(os.path.join(pub, "description.txt"), s["description"])
    write(os.path.join(pub, "image.txt"), image)
    write(os.path.join(pub, "_rutube_status.json"), json.dumps({"state": "ready", "folder": folder, "readyAt": now()}, indent=2))
    used.add(n)
    print(f"{name}/{folder}: {s['title']}")

write(os.path.join(BASE, "_rutube_active_campaign.txt"), name)
print(f"Активная кампания: {name}")
