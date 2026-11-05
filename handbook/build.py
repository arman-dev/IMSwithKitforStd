#!/usr/bin/env python3
"""Build the IMS teacher handbook (part 1) as a print-quality PDF.

Usage:  /home/user/.venv/bin/python build.py
Output: out/IMS_Handbook_Part1_Teacher.pdf
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True)

PARTS = [
    "00_front.html",
    "01_ch1.html",
    "02_ch2.html",
    "03_ch3.html",
    "04_ch4.html",
    "05_ch5.html",
]

CSS = (SRC / "style.css").read_text(encoding="utf-8")
BODY = "\n".join((SRC / name).read_text(encoding="utf-8") for name in PARTS)

HTML = f"""<!doctype html>
<html lang="bn"><head><meta charset="utf-8">
<title>IMS যেভাবে তৈরি হলো — শিক্ষক হ্যান্ডবুক (প্রথম খণ্ড)</title>
<style>{CSS}</style>
</head><body>
{BODY}
</body></html>
"""

html_path = OUT / "handbook_part1.html"
html_path.write_text(HTML, encoding="utf-8")

pdf_path = OUT / "IMS_Handbook_Part1_Teacher.pdf"

FOOTER = """
<div style="width:100%;font-size:8pt;color:#94a3b8;font-family:sans-serif;
     padding:0 16mm;display:flex;justify-content:space-between;">
  <span>IMS যেভাবে তৈরি হলো · শিক্ষক হ্যান্ডবুক · প্রথম খণ্ড</span>
  <span><span class="pageNumber"></span> / <span class="totalPages"></span></span>
</div>
"""

CHROME = "/home/user/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome"

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
    page = browser.new_page()
    page.goto(html_path.as_uri(), wait_until="load")
    page.wait_for_timeout(600)          # let the Bengali webfont settle
    page.pdf(
        path=str(pdf_path),
        format="A4",
        print_background=True,
        margin={"top": "18mm", "bottom": "16mm", "left": "16mm", "right": "16mm"},
        display_header_footer=True,
        header_template="<div></div>",
        footer_template=FOOTER,
        prefer_css_page_size=False,
    )
    browser.close()

size_mb = pdf_path.stat().st_size / 1e6
print(f"wrote {pdf_path}  ({size_mb:.2f} MB)")
