import numpy as np
from typing import List, Set

class Rib():
    def __init__(self, point1: int, point2: int) -> None:
        points = [point1, point2]
        # Sorting to avoid rib duplication
        # point1-point2 and point2-point1 are the same rib
        points.sort()
        # cast to tuple for making hashable
        # tuple can be used as a key in global Dict of ribs
        self._tuple_points = tuple(points)
        self._list_of_parents_faces = []
        self._intersect_point = None

    def Append_parent(self, index: int) -> None:
        self._list_of_parents_faces.append(index)

    def Get_parents(self) -> List: #int:
        #for parent in self._list_of_parents_faces:
        #    yield parent
        return self._list_of_parents_faces

    @property
    def intersect_point(self) -> np.array:
        return self._intersect_point

    @intersect_point.setter
    def intersect_point(self, point: np.array) -> None:
        self._intersect_point = point

    @property
    def tuple_point(self) -> Set:
        return self._tuple_points