from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple


class GeometryObject(ABC):
    @staticmethod
    @abstractmethod
    def FromDict(data: dict) -> "GeometryObject":
        if data["type"] == "Point":
            return Point.FromDict(data)
        # Do the same for LineString, Polygon and Composite...
        elif data["type"] == "LineString":
            return LineString.FromDict(data)
        elif data["type"] == "Polygon":
            return Polygon.FromDict(data)
        elif data["type"] in (
            "MultiPoint",
            "MultiLineString",
            "MultiPolygon",
            "GeometryCollection",
        ):
            return Composite.FromDict(data)
    
    @abstractmethod
    def bounding_box(self) -> Tuple[float, float, float, float]:
        pass
    
    def to_svg(self, classname: str) -> str:
        return ""
    
    def __str__(self):
        return self.to_svg("")
    

@dataclass
class Point(GeometryObject):
    x: float
    y: float

    @staticmethod
    def FromDict(data: dict) -> "Point":
        coordinates = data["coordinates"]
        return Point(coordinates[0], coordinates[1])

    def bounding_box(self) -> Tuple[float, float, float, float]:
        return self.x, self.y, self.x, self.y
    
    def to_svg(self, classname: str) -> str:
        return f"<circle class='{classname}' cx='{self.x}' cy='{self.y}' r='5' fill='red' />"


# Do the same for LineString, Polygon and Composite
@dataclass
class LineString(GeometryObject):
    coordinates: List[Point]

    @staticmethod
    def FromDict(data: dict) -> "LineString":
        coords = [Point(x, y) for x, y in data["coordinates"]]
        return LineString(coords)

    def bounding_box(self) -> Tuple[float, float, float, float]:
        x_coords = [p.x for p in self.coordinates]
        y_coords = [p.y for p in self.coordinates]
        return min(x_coords), min(y_coords), max(x_coords), max(y_coords)
    
    def to_svg(self, classname: str) -> str:
        s = f'<polyline class="{classname}" points=\"'
        for p in self.coordinates:
            s += f"{p.x},{p.y} "
        s += "\" />"
        return s


@dataclass
class Polygon(GeometryObject):
    line_1: LineString

    @staticmethod
    def FromDict(data: dict) -> "Polygon":
        line_1 = LineString([Point(x, y) for x, y in data["coordinates"][0]])
        return Polygon(line_1)

    def bounding_box(self) -> Tuple[float, float, float, float]:
        return self.line_1.bounding_box()
    
    def to_svg(self, classname: str) -> str:
        s = f'<polygon class="{classname}" points=\''
        for p in self.line_1.coordinates:
            s += f"{p.x},{p.y} "
        s += "\' />"
        return s


@dataclass
class Composite(GeometryObject):
    objects: List[GeometryObject]

    @staticmethod
    def FromDict(data: dict) -> "Composite":
        objects = []
        if data["type"] == "MultiPoint":
            return Composite([Point(x, y) for x, y in data["coordinates"]])
        elif data["type"] == "MultiLineString":
            return Composite(
                [
                    LineString([Point(x, y) for x, y in line])
                    for line in data["coordinates"]
                ]
            )
        elif data["type"] == "MultiPolygon":
            for polygon in data["coordinates"]:
                line = polygon[0]
                pts = LineString([Point(x, y) for x, y in line])
                objects.append(Polygon(pts))
            return Composite(objects)
        elif data["type"] == "GeometryCollection":
            # ----- DO IT RECURSIVELY -----
            return Composite(
                [GeometryObject.FromDict(geometry) for geometry in data["geometries"]]
            )
        else:
            return Composite([GeometryObject.FromDict(e) for e in data["geometries"]])

    def bounding_box(self) -> Tuple[float, float, float, float]:
        if len(self.objects) == 0:
            return super().bounding_box()
        
        bboxes = [o.bounding_box() for o in self.objects]
        xmin = min(xmin for xmin, _, _, _ in bboxes)
        xmax = max(xmax for _, _, xmax, _ in bboxes)
        ymin = min(ymin for _, ymin, _, _ in bboxes)
        ymax = max(ymax for _, _, _, ymax in bboxes)
        
        return xmin, ymin, xmax, ymax
    
    def to_svg(self, classname: str) -> str:
        s = ""
        for o in self.objects:
            s += o.to_svg(classname) + "\n"
        return s
