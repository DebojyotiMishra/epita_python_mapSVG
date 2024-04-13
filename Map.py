from dataclasses import dataclass
from abc import ABC, abstractmethod
from Geometry import *
from typing import List, Tuple, ClassVar
import json

@dataclass
class MapElement(ABC):
    geometry: GeometryObject
    stroke: ClassVar[str] = "black"
    srtroke_width: ClassVar[float] = 1.0
    fill: ClassVar[str] = "none"
    marker: ClassVar[str] = "none"
    z_order: ClassVar[int] = 0
    filter: ClassVar[str] = "none"
    
    
    def __str__(self):
        return self.geometry.to_svg(self.__class__.__name__)

    @staticmethod
    def FromDict(data: dict) -> 'MapElement':
        # Create a GeometryObject from the data
        g = GeometryObject.FromDict(data)
        if data["id"] == "roads":
            return Road(geometry=g)
        # Do the same for the other classes
        if data["id"] == "rivers":
            return River(geometry=g)
        if data["id"] == "walls":
            return Wall(geometry=g)
        if data["id"] == "planks":
            return Plank(geometry=g)
        if data["id"] == "buildings":
            return Building(geometry=g)
        if data["id"] == "prisms":
            return Prism(geometry=g)
        if data["id"] == "squares":
            return Square(geometry=g)
        if data["id"] == "greens":
            return Green(geometry=g)
        if data["id"] == "fields":
            return Field(geometry=g)
        if data["id"] == "trees":
            return Tree(geometry=g)
        if data["id"] == "districts":
            return District(geometry=g)
        if data["id"] == "earth":
            return Earth(geometry=g)
        if data["id"] == "water":
            return Water(geometry=g)

class Road(MapElement):
    stroke: ClassVar[str] = "#FFF2C8"
    stroke_width: ClassVar[float] = 2.0
    z_order: ClassVar[int] = 1
    
## Do the same for the other classes
class River(MapElement):
    stroke: ClassVar[str] = "#779988"
    stroke_width: ClassVar[float] = 36.0
    z_order: ClassVar[int] = 999

class Wall(MapElement):
    stroke: ClassVar[str] = "#606661"
    stroke_width: ClassVar[float] = 7.6
    marker: ClassVar[str] = "url(#wall)"

class Plank(MapElement):
    stroke: ClassVar[str] = "#FFF2C8"

class Building(MapElement):
    fill: ClassVar[str] = "#D6A36E"
    filter: ClassVar[str] = "url(#shadow)"

class Prism(MapElement):
    pass

class Square(MapElement):
    fill: ClassVar[str] = "#F2F2DA"

class Green(MapElement):
    stroke: ClassVar[str] = "#99AA77"
    fill: ClassVar[str] = "url(#green)"

class Field(MapElement):
    stroke: ClassVar[str] = "#99AA77"
    fill: ClassVar[str] = "url(#green)"

class Tree(MapElement):
    fill: ClassVar[str] = "#667755"

class District(MapElement):
    stroke: ClassVar[str] = "none"

class Earth(MapElement):
    pass

class Water(MapElement):
    fill: ClassVar[str] = "#779988"

@dataclass
class Map:
    items : List[MapElement]
    
    def LoadFromGeoJson(filename: str) -> 'Map':
        items = []
        with open(filename, 'r') as file:
            data = json.load(file)
            for item_data in data["features"]:
                item = MapElement.FromDict(item_data)
                items.append(item)
        return Map(items)
    
    def bounding_box(self) -> Tuple[float, float, float, float]:
        bboxes = [o.geometry.bounding_box() for o in self.items if isinstance(o, District)]
        if not bboxes:
            return (0, 0, 0, 0) 
        else:
            xmin = min(xmin for xmin, _, _, _ in bboxes)
            xmax = max(xmax for _, _, xmax, _ in bboxes)
            ymin = min(ymin for _, ymin, _, _ in bboxes)
            ymax = max(ymax for _, _, _, ymax in bboxes)
        
        x_padding = 0.1 * (xmax - xmin)
        xmin -= x_padding
        xmax += x_padding
        xmin = round(xmin, 2)
        xmax = round(xmax, 2)
        
        y_padding = 0.1 * (ymax - ymin)
        ymin -= y_padding
        ymax += y_padding
        ymin = round(ymin, 2)
        ymax = round(ymax, 2)
        
        return xmin, ymin, xmax, ymax
