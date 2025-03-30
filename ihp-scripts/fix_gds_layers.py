#!/usr/bin/env python3

# Fixes the GDS layers for designs that were previously hardened.
# See:
# - https://github.com/IHP-GmbH/IHP-Open-PDK/issues/345
# - https://github.com/IHP-GmbH/IHP-Open-PDK/commit/dd8ab7b2dfd2c5dddeab883046eb4e405721d859

import os
import os.path

import gdstk

script_dir = os.path.dirname(os.path.abspath(__file__))
GDS_ROOT = os.path.join(script_dir, "../tt-multiplexer/ol2/tt_top/gds")

for gds_file in os.listdir(GDS_ROOT):

    if not gds_file.startswith("tt_um_"):
        continue

    print(gds_file)

    gds = gdstk.read_gds(f"{GDS_ROOT}/{gds_file}")
    cell = gds.top_level()[0]

    for polygon in cell.polygons:
        if polygon.layer == 235:
            polygon.layer = 189

    gds.write_gds(f"{GDS_ROOT}/{gds_file}")
