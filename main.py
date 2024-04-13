# import Map
# map = Map.Map.LoadFromGeoJson("exercises/examples/silverrocks.json")
# print(map.items)

# map = Map.Map.LoadFromGeoJson("exercises/examples/silverrocks.json")
# print("Silverrocks bounding box:", map.bounding_box())
# map = Map.Map.LoadFromGeoJson("exercises/examples/bluemill_fort.json")
# print("Bluemill Fort bounding box:", map.bounding_box())
# map = Map.Map.LoadFromGeoJson("exercises/examples/thunty_city.json")
# print("Thunty City bounding box:", map.bounding_box())

# ---------- OUTPUT ----------
# Bluemill Fort bounding box: (-1289.15, -800.92, 1035.88, 924.96)
# Silverrocks bounding box: (-465.34, -1044.03, 663.93, 1180.06)
# Thunty City bounding box: (-600.2, -519.01, 433.8, 509.78)


# ---------- TESTING SVG ----------
# import chevron
# import Geometry

# data = {
#     "items": [
#         Geometry.Point(10, 20),
#         Geometry.Point(30, 40)
#     ]
# }

# out = chevron.render(open("exercises/template.svg"), data)
# print(out)

# ---------- OUTPUT ----------
# <svg>
#         <circle class='' cx='10' cy='20' r='5' fill='red' />
#         <circle class='' cx='30' cy='40' r='5' fill='red' />
# </svg>


# ---------- TESTING SVG 2 ----------
# import chevron
# import Geometry
# import Map

# map = Map.Map.LoadFromGeoJson("exercises/examples/silverrocks.json")
# (x1, y1, x2, y2) = map.bounding_box()
# data = {
#     "classes": [Map.Road, Map.River, Map.Wall, Map.Plank, Map.Building, Map.Prism, Map.Square, Map.Green, Map.Field, Map.Tree, Map.District, Map.Earth, Map.Water],
#     "bbox": {
#         "x": x1,
#         "y": y1,
#         "width": x2 - x1,
#         "height": y2 - y1
#     },
#     "items": map.items
# }

# svg = chevron.render(open("exercises/map-template.svg"), data)
# with open("map.svg", "w") as f:
#     f.write(svg)



import sys
from pathlib import Path
import Map
import chevron

folder = sys.argv[1]

p = Path(folder)
filelists = [file for file in p.iterdir() if file.suffix == ".json"]

for file in filelists:
    map = Map.Map.LoadFromGeoJson(file)
    (x1, y1, x2, y2) = map.bounding_box()
    data = {
        "classes": [Map.Road, Map.River, Map.Wall, Map.Plank, Map.Building, Map.Prism, Map.Square, Map.Green, Map.Field, Map.Tree, Map.District, Map.Earth, Map.Water],
        "bbox": {
            "x": x1,
            "y": y1,
            "width": x2 - x1,
            "height": y2 - y1
        },
        "items": map.items
    }

    svg = chevron.render(open("map-template.svg"), data)
    svg_file = file.with_suffix(".svg")
    with open(svg_file, "w") as f:
        f.write(svg)