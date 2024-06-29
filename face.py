from rib import Rib
from typing import Dict

class Face():
    def __init__(self, point1: int, point2: int, point3: int, face_index: int, global_dict_of_ribs: Dict) -> None:
        self._list_of_ribs = []
        self._visited = False

        r1 = Rib(point1, point2)
        if r1.tuple_point in global_dict_of_ribs:
            global_dict_of_ribs[r1.tuple_point].Append_parent(face_index)
        else:
            global_dict_of_ribs[r1.tuple_point] = r1
            global_dict_of_ribs[r1.tuple_point].Append_parent(face_index)
        r2 = Rib(point2, point3)
        if r2.tuple_point in global_dict_of_ribs:
            global_dict_of_ribs[r2.tuple_point].Append_parent(face_index)
        else:
            global_dict_of_ribs[r2.tuple_point] = r2
            global_dict_of_ribs[r2.tuple_point].Append_parent(face_index)
        r3 = Rib(point1, point3)
        if r3.tuple_point in global_dict_of_ribs:
            global_dict_of_ribs[r3.tuple_point].Append_parent(face_index)
        else:
            global_dict_of_ribs[r3.tuple_point] = r3
            global_dict_of_ribs[r3.tuple_point].Append_parent(face_index)

        self._list_of_ribs.append(global_dict_of_ribs[r1.tuple_point])
        self._list_of_ribs.append(global_dict_of_ribs[r2.tuple_point])
        self._list_of_ribs.append(global_dict_of_ribs[r3.tuple_point])

    def Get_ribs(self) -> Rib:
        for r in self._list_of_ribs:
            yield r

    @property
    def visited(self):
        return  self._visited

    def visit(self):
        self._visited = True