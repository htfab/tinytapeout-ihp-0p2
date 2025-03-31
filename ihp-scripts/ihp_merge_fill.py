#!/usr/bin/env python3

import sys
import gdstk


def main(argv0, main_gds, fill_gds, out_gds):
    print(f"Reading {main_gds}")
    lib_main = gdstk.read_gds(main_gds)

    print(f"Reading {fill_gds}")
    lib_fill = gdstk.read_gds(fill_gds)

    top_main = lib_main.top_level()[0]
    top_fill = lib_fill.top_level()[0]

    top_main.add(gdstk.Reference(top_fill, origin=(0, 0)))

    lib_main.add(top_fill)
    lib_main.add(*top_fill.dependencies(True))

    print(f"Writing {out_gds}")
    lib_main.write_gds(out_gds)


if __name__ == "__main__":
    main(*sys.argv)
