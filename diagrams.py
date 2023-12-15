#-------------------------------------------------------------------------------
#
# diagrams.py -- new flock experiments
#
# Some non-polished code to generate 3d diagrams for documentation.
#
# Everything in one big file for now, more organization when it seems warranted.
#
# MIT License -- Copyright © 2023 Craig Reynolds
#
#-------------------------------------------------------------------------------

import open3d as o3d
import numpy as np # temp?
import time
import math
import copy
from Vec3 import Vec3

def add_line_as_cylinder(vis,
                         line_origin=Vec3(),
                         line_tangent=Vec3(0,0,1),
                         radius=0.03,
                         height=100,
                         chords=6,
                         color=Vec3()):
    cyl = o3d.geometry.TriangleMesh.create_cylinder(radius, height, chords, 100)
    default_axis = Vec3(0, 0, 1)
    line_tangent = line_tangent.normalize()
    rot_axis = default_axis.cross(line_tangent)
    if rot_axis.length() > 0:
        axis_dot = default_axis.dot(line_tangent)
        angle = math.acos(axis_dot)
        aa = rot_axis.normalize() * angle
        rotation = o3d.geometry.get_rotation_matrix_from_axis_angle(aa.asarray())
        cyl.rotate(rotation)
    cyl.translate(line_origin.asarray())
    cyl.compute_vertex_normals()
    cyl.paint_uniform_color(color.asarray())
    vis.add_geometry(cyl)

def diagram_visualizer_1():
    # Create Visualizer and a window for it.
    vis = o3d.visualization.VisualizerWithKeyCallback()
    vis.create_window()
    # The cylinder
    add_line_as_cylinder(vis, Vec3(5, 0, 0), Vec3(1, 2, 3), 1, 10, 1000, Vec3(0.5, 0.5, 0.5))
    # Global axes.
    add_line_as_cylinder(vis, line_tangent=Vec3(1, 0, 0))
    add_line_as_cylinder(vis, line_tangent=Vec3(0, 1, 0))
    add_line_as_cylinder(vis, line_tangent=Vec3(0, 0, 1))
    vis.run()

def aa_test():
    # Create Visualizer and a window for it.
    vis = o3d.visualization.VisualizerWithKeyCallback()
    vis.create_window()
    
    frame = o3d.geometry.TriangleMesh.create_coordinate_frame()
    frame.paint_uniform_color([0.2, 0.2, 0.2])
    vis.add_geometry(frame)

    box = o3d.geometry.TriangleMesh.create_box(0.5, 0.5, 0.5)
    box.compute_vertex_normals()
    for i in range(5):
        new_box = copy.deepcopy(box)
        aa = Vec3(1, 1, 1).normalize() * (math.pi * 2 / 3) * (i / 5)
        print('aa.asarray() =', aa.asarray())
        rotation = o3d.geometry.get_rotation_matrix_from_axis_angle(aa.asarray())
        new_box.rotate(rotation)
        vis.add_geometry(new_box)
    
    vis.run()


if __name__ == "__main__":
    diagram_visualizer_1()
#    aa_test()
