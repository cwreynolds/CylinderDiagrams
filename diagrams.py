#-------------------------------------------------------------------------------
#
# diagrams.py -- CylinderDiagrams
#
# Some non-polished code to generate 3d diagrams for documentation.
# See diagram on https://en.wikipedia.org/wiki/Line-cylinder_intersection
#
# Everything in one big file for now, more organization when it seems warranted.
#
# MIT License -- Copyright © 2023 Craig Reynolds -- Created December 11, 2023.
#
#-------------------------------------------------------------------------------

import open3d as o3d
import numpy as np # temp?
import time
import math
import copy

# Pathname hackery to access utility files in "flock" sibling directory.
import sys
sys.path.append('../flock')  # Add flock dir to search path.
import shape
from Vec3 import Vec3
from obstacle import CylinderObstacle

red = Vec3(1, 0, 0)
cyan = Vec3(0, 1, 1)
green = Vec3(0, 1, 0)
yellow = Vec3(1, 1, 0)
magenta = Vec3(1, 0, 1)
gray = Vec3(1, 1, 1) * 0.8

def add_line_as_cylinder(vis,
                         line_origin=Vec3(),
                         line_tangent=Vec3(0,0,1),
                         radius=0.03,
                         height=1000,
                         chords=6,
                         color=Vec3(),
                         reset_bounding_box=False,
                         shaded=False):
    # Create cylinder mesh of given shape in default orientation (along Z axis).
    cyl = o3d.geometry.TriangleMesh.create_cylinder(radius, height, chords, 100)
    # Rotate cylinder mesh from default axis to given tangent
    aa = Vec3.rotate_vec_to_vec(Vec3(0, 0, 1), line_tangent)
    rotation = o3d.geometry.get_rotation_matrix_from_axis_angle(aa.asarray())
    cyl.rotate(rotation)
    cyl.translate(line_origin.asarray())
    if shaded:
        cyl.compute_vertex_normals()
    cyl.paint_uniform_color(color.asarray())
    vis.add_geometry(cyl, reset_bounding_box)

def add_two_point_cylinder(vis, ep1, ep2, radius=1, chords=100, color=Vec3()):
    mid = (ep1 + ep2) / 2
    ep_offset = ep2 - ep1
    height = ep_offset.length()
    add_line_as_cylinder(vis, mid, ep_offset, radius, height, chords, color, True, True)

def add_marker_at_intersection(vis, line_origin, line_tangent,
                               cyl_ep1, cyl_ep2, cyl_radius):
    ep_offset = cyl_ep2 - cyl_ep1
    cyl_tangent = ep_offset.normalize()
    cyl_height = ep_offset.length()
    intersection = shape.ray_cylinder_intersection(line_origin, line_tangent,
                                                   cyl_ep1, cyl_tangent,
                                                   cyl_radius, cyl_height)
    if intersection:
        ball = o3d.geometry.TriangleMesh.create_sphere(0.10, 10)
        ball.paint_uniform_color(red.asarray())
        ball.translate(intersection.asarray())
        vis.add_geometry(ball)

def add_line_along_cylinder(vis, ep1, ep2, radius=1, color=Vec3()):
    ref_dir = Vec3(1, 1.6, 0)
    cyl = CylinderObstacle(radius, ep1, ep2)
    normal_ref_dir = ref_dir.perpendicular_component(cyl.tangent).normalize()
    mid_axis = (ep1 + ep2) / 2
    add_line_as_cylinder(vis,
                         line_origin=mid_axis + normal_ref_dir,
                         line_tangent=cyl.tangent,
                         radius=0.06,
                         height=cyl.length,
                         chords=20,
                         color=red,
                         reset_bounding_box=False)
    add_line_as_cylinder(vis,
                         line_origin=mid_axis + normal_ref_dir,
                         line_tangent=cyl.tangent,
                         radius=0.03,
                         height=1000,
                         chords=6,
                         color=color,
                         reset_bounding_box=False)

def diagram_visualizer_1():
    # Create Visualizer and a window for it.
    vis = o3d.visualization.VisualizerWithKeyCallback()
    vis.create_window()

    # Global axes.
    add_line_as_cylinder(vis, line_tangent=Vec3(1, 0, 0))
    add_line_as_cylinder(vis, line_tangent=Vec3(0, 1, 0))
    add_line_as_cylinder(vis, line_tangent=Vec3(0, 0, 1))

    # Cylinder for intersection.
    ep1 = Vec3(8, 8, -9)
    ep2 = Vec3(3, 1, -2)
    add_two_point_cylinder(vis, ep1, ep2, 1, 1000, gray)
    
    # Lines for intersection.
    line_origin_1 = Vec3(0, 5, -4)
    line_origin_2 = Vec3(0, 5.414, -5)
    line_tangent_1 = Vec3(1, -0.6, 0.4).normalize()
    
    plus_x = Vec3(1, 0, 0)  # Parallel to x axis.
    add_line_as_cylinder(vis, line_origin_1, line_tangent_1, color=green)
    add_line_as_cylinder(vis, line_origin_2, plus_x, color=cyan)
    add_line_as_cylinder(vis, Vec3(0, 3, -3), Vec3(1, -2, 0), color=magenta)
    add_line_along_cylinder(vis, ep1, ep2, radius=1, color=yellow)

    # Intersection markers.
    add_marker_at_intersection(vis, line_origin_1, line_tangent_1, ep1, ep2, 1)
    add_marker_at_intersection(vis, line_origin_2, plus_x, ep1, ep2, 1)
    add_marker_at_intersection(vis, line_origin_2, plus_x, ep1, ep2, 1)
    line_origin_1b = line_origin_1 + line_tangent_1 * 10  # only get 1 of 2 for ray.
    add_marker_at_intersection(vis, line_origin_1b, -line_tangent_1, ep1, ep2, 1)

    vis.run()

#def aa_test():
#    # Create Visualizer and a window for it.
#    vis = o3d.visualization.VisualizerWithKeyCallback()
#    vis.create_window()
#    
#    frame = o3d.geometry.TriangleMesh.create_coordinate_frame()
#    frame.paint_uniform_color([0.2, 0.2, 0.2])
#    vis.add_geometry(frame)
#
#    box = o3d.geometry.TriangleMesh.create_box(0.5, 0.5, 0.5)
#    box.compute_vertex_normals()
#    for i in range(5):
#        new_box = copy.deepcopy(box)
#        aa = Vec3(1, 1, 1).normalize() * (math.pi * 2 / 3) * (i / 5)
#        print('aa.asarray() =', aa.asarray())
#        rotation = o3d.geometry.get_rotation_matrix_from_axis_angle(aa.asarray())
#        new_box.rotate(rotation)
#        vis.add_geometry(new_box)
#    
#    vis.run()

if __name__ == "__main__":
    diagram_visualizer_1()
#    aa_test()
