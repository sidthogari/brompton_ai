#!/usr/bin/env python3
"""Generate both Noli Data Engineer interview presentations."""

from pathlib import Path

import build_section1
import build_section2

OUT = Path(__file__).resolve().parent / "output"
OUT.mkdir(exist_ok=True)


def main():
    p1 = OUT / "Noli_Section1_Attribution_Architecture.pptx"
    p2 = OUT / "Noli_Section2_SelfService_Revenue_Platform.pptx"
    build_section1.build(p1)
    build_section2.build(p2)
    print(f"Wrote {p1}")
    print(f"Wrote {p2}")


if __name__ == "__main__":
    main()
