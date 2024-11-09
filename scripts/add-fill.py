#!/usr/bin/env python3

# fill generator inspired by https://github.com/IHP-GmbH/IHP-Open-DesignLib/tree/main/U_Hawaii_EE628_Spring_2024

import pya
import sys

project = sys.argv[1]
input_gds = f"{project}/{project}_orig.gds"
output_gds = f"{project}/{project}.gds"

fill_margin = 0

boundary_layer = (235, 4)
layer_map = {
    "Activ": 1,
    "GatPoly": 5,
    "NWell": 31,
    "Metal1": 8,
    "Metal2": 10,
    "Metal3": 30,
    "Metal4": 50,
    "Metal5": 67,
}
datatype_drawing = 0
datatype_filler = 22
fill_groups = [
    ("Metal1 (first round)", "Metal1_L", 4.8, 0.3, [("Metal1", 4.2)]),
    ("Metal1 (second round)", "Metal1_S", 1.6, 0.3, [("Metal1", 1)]),
    ("Metal2 (first round)", "Metal2_L", 4.8, 0.3, [("Metal2", 4.2)]),
    ("Metal2 (second round)", "Metal2_S", 1.6, 0.3, [("Metal2", 1)]),
    ("Metal3 (first round)", "Metal3_L", 4.8, 0.3, [("Metal3", 4.2)]),
    ("Metal3 (second round)", "Metal3_S", 1.6, 0.3, [("Metal3", 1)]),
    ("Metal4 (first round)", "Metal4_L", 4.8, 0.3, [("Metal4", 4.2)]),
    ("Metal4 (second round)", "Metal4_S", 1.6, 0.3, [("Metal4", 1)]),
    ("Metal5 (first round)", "Metal5_L", 4.8, 0.3, [("Metal5", 4.2)]),
    ("Metal5 (second round)", "Metal5_S", 1.6, 0.3, [("Metal5", 1)]),
]
fill_exclude = [
    ('dfpad', (41, 0)),
]

layout = pya.Layout()
layout.read(input_gds)
top = layout.top_cell()
u = round(1/layout.dbu)

fill_box = top.bbox_per_layer(layout.layer(boundary_layer)).enlarged(-fill_margin)
fill_region_init = pya.Region(fill_box)
for layer_name, (layer, datatype) in fill_exclude:
    layer_index = layout.layer(layer, datatype)
    exclude_region = pya.Region(top.begin_shapes_rec(layer_index))
    fill_region_init -= exclude_region

for group_desc, group_name, grid, spacing, layers in fill_groups:
    print(f"Generating fill for {group_desc}...")
    cell_index = layout.add_cell(f"FILL_{group_name}")
    cell_obj = layout.cell(cell_index)
    fill_region = fill_region_init.dup()
    for layer_name, size in layers:
        layer = layer_map[layer_name]
        drawing_layer_index = layout.layer(layer, datatype_drawing)
        filler_layer_index = layout.layer(layer, datatype_filler)
        shape_box = pya.Box(round((grid-size)/2*u), round((grid-size)/2*u), round((grid+size)/2*u), round((grid+size)/2*u))
        cell_obj.shapes(filler_layer_index).insert(shape_box)
        exclude_region = pya.Region(top.begin_shapes_rec(drawing_layer_index))
        fill_region -= exclude_region
        exclude_region = pya.Region(top.begin_shapes_rec(filler_layer_index))
        fill_region -= exclude_region
    cell_box = pya.Box(-spacing*u, -spacing*u, (grid+spacing)*u, (grid+spacing)*u)
    row_step = pya.Vector(grid*u, 0)
    column_step = pya.Vector(0, grid*u)
    origin = pya.Point(-spacing*u, -spacing*u)
    fill_margin = pya.Vector(0, 0)
    top.fill_region(fill_region, cell_index, cell_box, row_step, column_step, origin, fill_region, fill_margin, None)

for cell in layout.top_cells():
    if cell.name.startswith("FILL_"):
        cell.delete()

layout.write(output_gds)

