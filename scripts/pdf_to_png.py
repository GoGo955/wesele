#!/usr/bin/env python3
"""Render PDF pages to PNG for visual reading (image-based PDFs without text layer).

Usage:
    python scripts/pdf_to_png.py "raw/Wesele - Przystanek Południe.pdf" [out_dir] [dpi]

Defaults: out_dir = raw/png_<pdf-stem>, dpi = 150.
Requires: pip install pymupdf
"""
import sys, os
import fitz  # PyMuPDF


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    src = sys.argv[1]
    stem = os.path.splitext(os.path.basename(src))[0]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join("raw", f"png_{stem}")
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 150
    os.makedirs(out, exist_ok=True)
    doc = fitz.open(src)
    m = fitz.Matrix(dpi / 72, dpi / 72)
    for i, page in enumerate(doc, 1):
        page.get_pixmap(matrix=m).save(os.path.join(out, f"p{i:02d}.png"))
    print(f"rendered {doc.page_count} pages @ {dpi} dpi -> {out}")


if __name__ == "__main__":
    main()
