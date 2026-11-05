import pymupdf, os
from pathlib import Path
order = [
    ("00_overview.pdf",        "০০ · কোর্স ওভারভিউ", None),
    ("part1_concept.pdf",      "পর্ব ১ · কনসেপ্ট", 4),
    ("part2_plan.pdf",         "পর্ব ২ · প্ল্যান", 6),
    ("part3_design.pdf",       "পর্ব ৩ · ডিজাইন", 5),
    ("part4_code.pdf",         "পর্ব ৪ · কোডিং", 8),
    ("part5_test.pdf",         "পর্ব ৫ · টেস্টিং", 4),
    ("part6_deploy.pdf",       "পর্ব ৬ · ডিপ্লয়", 3),
    ("part7_maintain.pdf",     "পর্ব ৭ · মেইনটেন্যান্স", 2),
    ("part8_docs.pdf",         "পর্ব ৮ · ডকুমেন্ট", 3),
    ("part9_future.pdf",       "পর্ব ৯ · ভবিষ্যৎ", 1),
    ("part10_demo.pdf",        "পর্ব ১০ · উপস্থাপন", 1),
    ("d1_database_design.pdf", "D1 · ডেটাবেস ডিজাইন", None),
    ("d2_stack_connections.pdf","D2 · স্ট্যাক ও সংযোগ", None),
    ("d3_security.pdf",        "D3 · নিরাপত্তা", None),
    ("d4_lifecycle_ops.pdf",   "D4 · লাইফসাইকেল ও অপস", None),
    ("d5_design_system.pdf",   "D5 · ডিজাইন সিস্টেম", None),
]
root = Path("/home/user")
out = pymupdf.open()
toc, total = [], 0
for fname, label, classes in order:
    src = pymupdf.open(root / fname)
    out.insert_pdf(src)
    toc.append([1, f"{label} — {src.page_count} স্লাইড", total + 1])
    total += src.page_count
    src.close()
out.set_toc(toc)
out.set_metadata({"title": "IMS ক্লাস কিট — সম্পূর্ণ কোর্স (১৭ PDF একত্রে)",
                  "author": "Web Development Project 28566", "subject": "শিক্ষক কিট"})
p = root / "IMS_Full_Course_Kit.pdf"
out.save(p, garbage=4, deflate=True)
print("pages:", out.page_count, "| MB:", round(os.path.getsize(p)/1e6, 2))
print("toc:", [(t[1], t[2]) for t in toc])
