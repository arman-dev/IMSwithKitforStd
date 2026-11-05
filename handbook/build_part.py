import sys, os
from pathlib import Path
part=sys.argv[1] if len(sys.argv)>1 else "1"
SRC=Path("src"); OUT=Path("out")
CSS=(SRC/"style3.css").read_text(encoding="utf-8")
frags=sorted(SRC.glob(f"part{part}_c*.html"), key=lambda p:int(p.stem.split("_c")[1]))
body="\n".join(f.read_text(encoding="utf-8") for f in frags)
page=OUT/f"part{part}.html"
page.write_text(f'<!doctype html><html lang="bn"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>',encoding="utf-8")
from playwright.sync_api import sync_playwright
CHROME="/home/user/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome"
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path=CHROME,args=["--no-sandbox"])
    pg=b.new_page(viewport={"width":1600,"height":900}); pg.goto(page.resolve().as_uri(),wait_until="load"); pg.wait_for_timeout(1200)
    names={"1":"part1_concept.pdf","2":"part2_plan.pdf","3":"part3_design.pdf","4":"part4_code.pdf","5":"part5_test.pdf","6":"part6_deploy.pdf","7":"part7_maintain.pdf","8":"part8_docs.pdf","9":"part9_future.pdf","10":"part10_demo.pdf"}
    pdf=OUT/names.get(part, f"part{part}.pdf")
    pg.pdf(path=str(pdf),width="338.7mm",height="190.5mm",print_background=True,
           margin={"top":"0","bottom":"0","left":"0","right":"0"},prefer_css_page_size=True); b.close()
import pymupdf
d=pymupdf.open(str(pdf))
print("frags:",[f.name for f in frags],"| slides:",d.page_count,"|",round(os.path.getsize(pdf)/1e6,2),"MB")
for i in range(d.page_count):
    d[i].get_pixmap(dpi=80).save(f"/tmp/p{part}_{i+1:02d}.png")
