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

# Import from temporary copies in this directory. To become submodule later.
import shape
from Vec3 import Vec3

def add_line_as_cylinder(vis,
                         line_origin=Vec3(),
                         line_tangent=Vec3(0,0,1),
                         radius=0.03,
#                         height=100,
                         height=50,
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

def add_two_point_cylinder(vis, ep1, ep2, radius=1, chords=100, color=Vec3()):
    mid = (ep1 + ep2) / 2
    ep_offset = ep2 - ep1
    height = ep_offset.length()
    add_line_as_cylinder(vis, mid, ep_offset, radius, height, chords, color)

#    def diagram_visualizer_1():
#        # Create Visualizer and a window for it.
#        vis = o3d.visualization.VisualizerWithKeyCallback()
#        vis.create_window()
#        # The cylinder
#    #    add_line_as_cylinder(vis, Vec3(5, 0, 0), Vec3(1, 2, 3), 1, 10, 1000, Vec3(0.5, 0.5, 0.5))
#    #    add_two_point_cylinder(vis, Vec3(-2, 5, 0), Vec3(-2, -5, 0), 1, 100, Vec3(1,0,0))
#        gray = Vec3(1, 1, 1) * 0.8
#    #    add_two_point_cylinder(vis, Vec3(8, -2, -2),  Vec3(3, 5, -9), 1, 100, gray)
#        add_two_point_cylinder(vis, Vec3(8, 1, -2),  Vec3(3, 8, -9), 1, 100, gray)
#        # Global axes.
#        add_line_as_cylinder(vis, line_tangent=Vec3(1, 0, 0))
#        add_line_as_cylinder(vis, line_tangent=Vec3(0, 1, 0))
#        add_line_as_cylinder(vis, line_tangent=Vec3(0, 0, 1))
#        vis.run()


#    ray_cylinder_intersection(ray_endpoint, ray_tangent,
#                              cyl_endpoint, cyl_tangent,
#                              cyl_radius, cyl_length)

def add_marker_at_intersection(vis, line_origin, line_tangent,
                               cyl_ep1, cyl_ep2, cyl_radius):
                               
#    print(line_origin, line_tangent, cyl_ep1, cyl_ep2, cyl_radius)
                               
    ep_offset = cyl_ep2 - cyl_ep1
    cyl_tangent = ep_offset.normalize()
    height = ep_offset.length()
    
    
#    print('line_origin =', line_origin)
#    print('line_tangent =', line_tangent)
#    print('cyl_ep1 =', cyl_ep1)
#    print('cyl_ep2 =', cyl_ep2)
#    print('cyl_radius =', cyl_radius)
#    print('ep_offset =', ep_offset)
#    print('cyl_tangent =', cyl_tangent)
#    print('height =', height)

    i = shape.ray_cylinder_intersection(line_origin, line_tangent,
                                        cyl_ep1,
                                        cyl_tangent,
                                        cyl_radius,
                                        height)
#    print(i)
    if i:
#        ball = o3d.geometry.TriangleMesh.create_sphere(radius=0.1, resolution=10)
#        ball = o3d.geometry.TriangleMesh.create_sphere(radius=0.06, resolution=10)
        ball = o3d.geometry.TriangleMesh.create_sphere(radius=0.15, resolution=10)
        ball.compute_vertex_normals()
        ball.paint_uniform_color([1, 0, 0])

        ball.translate(i.asarray())

        vis.add_geometry(ball)



def diagram_visualizer_1():
    # Create Visualizer and a window for it.
    vis = o3d.visualization.VisualizerWithKeyCallback()
    vis.create_window()
    # Cylinder for intersection.
#    top_ep = Vec3(3, 8, -9)
#    bot_ep = Vec3(8, 1, -2)
    top_ep = Vec3(8, 8, -9)
    bot_ep = Vec3(3, 1, -2)
    gray = Vec3(1, 1, 1) * 0.8
#    add_two_point_cylinder(vis, Vec3(8, 1, -2),  Vec3(3, 8, -9), 1, 100, gray)
    add_two_point_cylinder(vis, top_ep,  bot_ep, 1, 100, gray)
    
    # Lines for intersection.
#        add_line_as_cylinder(vis, Vec3(5, 5, -5), Vec3(1, 0, 0), color=Vec3(1,0,0))
#        add_line_as_cylinder(vis, Vec3(5, 5.5, -5), Vec3(1, 0, 0), color=Vec3(0,1,0))
#    #    add_line_as_cylinder(vis, Vec3(5, 8, -5), Vec3(1, 0, 0), color=Vec3(0,0,1))
#    #    add_line_as_cylinder(vis, Vec3(5, 6, -5), Vec3(1, 0, 0), color=Vec3(0,0,1))
#    #    add_line_as_cylinder(vis, Vec3(5, 7, -5), Vec3(1, 0, 0), color=Vec3(0,0,1))
#        add_line_as_cylinder(vis, Vec3(5, 9, -5), Vec3(1, 0, 0), color=Vec3(0,0,1))
    add_line_as_cylinder(vis, Vec3(5, 5, -5), Vec3(1, 0, 0), color=Vec3(1,1,0))
    add_line_as_cylinder(vis, Vec3(5, 5.5, -5), Vec3(1, 0, 0), color=Vec3(0,1,1))
    add_line_as_cylinder(vis, Vec3(5, 9, -5), Vec3(1, 0, 0), color=Vec3(1,0,1))


    # Global axes.
    add_line_as_cylinder(vis, line_tangent=Vec3(1, 0, 0))
    add_line_as_cylinder(vis, line_tangent=Vec3(0, 1, 0))
    add_line_as_cylinder(vis, line_tangent=Vec3(0, 0, 1))
    
    # TODO testing
    
    add_marker_at_intersection(vis,
#                               Vec3(5, 5, -5), Vec3(1, 0, 0),
                               Vec3(0, 5, -5), Vec3(1, 0, 0),
                               top_ep,  bot_ep, 1)

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
