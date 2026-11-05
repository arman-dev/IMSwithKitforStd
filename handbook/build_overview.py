import sys, os, re
from pathlib import Path
SRC = Path("src"); OUT = Path("out"); OUT.mkdir(exist_ok=True)
CSS = (SRC / "style3.css").read_text(encoding="utf-8")
frags = sorted(SRC.glob("ov_*.html"), key=lambda p: int(p.stem.split("_")[-1]))
body = "\n".join(f.read_text(encoding="utf-8") for f in frags)
page = OUT / "overview.html"
page.write_text(f'<!doctype html><html lang="bn"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>', encoding="utf-8")
from playwright.sync_api import sync_playwright
CHROME = "/home/user/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome"
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1600, "height": 900})
    pg.goto(page.resolve().as_uri(), wait_until="load"); pg.wait_for_timeout(1200)
    pdf = OUT / "00_overview.pdf"
    pg.pdf(path=str(pdf), width="338.7mm", height="190.5mm", print_background=True,
           margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}, prefer_css_page_size=True)
    b.close()
import pymupdf
d = pymupdf.open(str(pdf))
print("frags:", len(frags), "| slides:", d.page_count, "|", round(os.path.getsize(pdf)/1e6, 2), "MB")
for i in range(d.page_count):
    d[i].get_pixmap(dpi=80).save(f"/tmp/ov_{i+1:02d}.png")
