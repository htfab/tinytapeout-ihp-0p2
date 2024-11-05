# SPDX-License-Identifier: Public Domain
# Remove empty cells from a GDS file.

import pya  # KLayout Python API

ly = pya.Layout()
ly.read("tt_um_urish_sram_test.gds")
opt = pya.SaveLayoutOptions()
opt.no_empty_cells = True
ly.write("tt_um_urish_sram_test.gds", opt)
