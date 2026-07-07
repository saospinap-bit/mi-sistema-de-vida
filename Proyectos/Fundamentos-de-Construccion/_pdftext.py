import fitz, sys
p = sys.argv[1]
doc = fitz.open(p)
print(f"=== {p}  paginas={len(doc)} ===")
for i, page in enumerate(doc):
    txt = page.get_text().strip()
    print(f"\n----- PAGINA {i+1} ({page.rect.width:.0f}x{page.rect.height:.0f}) -----")
    print(txt[:4000])
