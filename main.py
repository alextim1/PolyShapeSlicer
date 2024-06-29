import numpy as np
import pywavefront
from rib import Rib
from face import Face
from typing import List, Set

def parse_FTX(path):
    with open(path) as f:
        vertices = []
        faces = []
        for line in f:  # read rest of lines
            elements = [x for x in line.split(',')]
            if len(elements) == 5:
                vertices.append([float(x) for x  in elements[0:3]])
            elif len(elements) == 3:
                faces.append([int(x) for x  in elements])
    return np.array(vertices), np.array(faces)


def dot_product_vect(v1: np.array, v2: np.array) -> float:
    return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

def find_intersection(rib: Rib, plane_normal: np.array, plane_point: np.array, vertices: np.array) -> bool:
    indices = list(rib.tuple_point)
    point1 = vertices[indices[0]]
    point2 = vertices[indices[1]]
    vect1 = np.array([point1[0] - plane_point[0], point1[1] - plane_point[1], point1[2] - plane_point[2]])
    vect2 = np.array([point2[0] - plane_point[0], point2[1] - plane_point[1], point2[2] - plane_point[2]])
    if dot_product_vect(vect1, plane_normal)*dot_product_vect(vect2, plane_normal) > 0:
        return False

    rib_direct = np.array([point1[0] - point2[0], point1[1] - point2[1], point1[2] - point2[2]])
    D = -dot_product_vect(plane_normal, plane_point)
    gain = (dot_product_vect(point1, plane_normal) + D)/dot_product_vect(rib_direct, plane_normal)

    rib.intersect_point = np.array([point1[0] - gain*rib_direct[0], point1[1] - gain*rib_direct[1], point1[2] - gain*rib_direct[2]])
    return True

def propagate_slice_line_on_shape(rib: Rib,
                                  list_of_faces: List,
                                  vertices: np.array,
                                  analyzed_ribs: Set,
                                  slice_subline: List) -> None:

    for faceID in rib.Get_parents():
        if not list_of_faces[faceID].visited:
            list_of_faces[faceID].visit()
            for r in list_of_faces[faceID].Get_ribs():
                if r.tuple_point not in analyzed_ribs and find_intersection(r, NORMAL, POINT, vertices):
                    analyzed_ribs.add(r.tuple_point)
                    slice_subline.append(r)
                    # recursive call for propagation slice line
                    propagate_slice_line_on_shape(r, list_of_faces, vertices, analyzed_ribs, slice_subline)
            # propagation only to one side
            break


#########################################################
#######  INITIALIZATION OF CUTTING PLANE   ##############
####### Point on plane and Normal vector ################

POINT = np.array([0.5, 0.5, 0.5])
NORMAL = np.array([1, 1, 1])
CLOSED_SHAPE = True

# Creating Slice line by cutting shape with plane.
if __name__ == '__main__':
    ####### Importing geometry for tests #####################
    #scene = pywavefront.Wavefront('cube.obj', collect_faces=True)
    #scene = pywavefront.Wavefront("diamond.obj", collect_faces=True)
    # scene = pywavefront.Wavefront("hedron.obj", collect_faces=True)
    #scene = pywavefront.Wavefront("wave.obj", collect_faces=True)
    #scene = pywavefront.Wavefront("formation.obj", collect_faces=True)

    #vertices = np.array(scene.vertices)
    dict_of_ribs = {}
    list_of_faces = []

    face_indexer = 0
    # for key, meshes in scene.meshes.items():
    #     for points in meshes.faces:
    #         list_of_faces.append(Face(points[0], points[1], points[2], face_indexer, dict_of_ribs))
    #         face_indexer += 1

    ################## FTX try
    vertices, faces = parse_FTX("Belloy (KSTN+50m) D2DV4.ftx")
    for points in faces:
        list_of_faces.append(Face(points[0], points[1], points[2], face_indexer, dict_of_ribs))
        face_indexer += 1

    #################### Finding first Rib of shape which intersects the cutting plane ##############
    #################### Then propagate a slice line for the neighbour faces and ribs  ##############

    analyzed_ribs = set()
    line_sequence = []
    slice_subline_right = []
    slice_subline_left = []
    for (key, r) in dict_of_ribs.items():
        if find_intersection(r, NORMAL, POINT, vertices):
            slice_subline_right.append(r)
            line_sequence.append(slice_subline_right)
            line_sequence.append(slice_subline_left)
            analyzed_ribs.add(r.tuple_point)
            propagate_slice_line_on_shape(r, list_of_faces, vertices, analyzed_ribs, slice_subline_right)
            propagate_slice_line_on_shape(r, list_of_faces, vertices, analyzed_ribs, slice_subline_left)
            break

    ##################  EXPORT RESULTS FOR CHECK ##############################
    i = 1
    for line in line_sequence:
        with open("slice{}.obj".format(i), 'w') as f:
            f.write("# OBJ file\n")
            for r in line:
                f.write("v %.4f %.4f %.4f\n" % (r.intersect_point[0], r.intersect_point[1], r.intersect_point[2]))
            for l in range(len(line) - 1):
                f.write("l %d %d" % (l + 1, l + 2))
                f.write("\n")
            if CLOSED_SHAPE and len(line) >= 2:
                f.write("l %d %d" % (l + 2, 1))
        i += 1

