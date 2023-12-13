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
#import Utilities as util  # temp?
#from Vec3 import Vec3     # temp?
#import random             # temp?
#from LocalSpace import LocalSpace


def start_visualizer():
    # Create Visualizer and a window for it.
    vis = o3d.visualization.VisualizerWithKeyCallback()
    vis.create_window()

    cyl = o3d.geometry.TriangleMesh.create_cylinder(radius=1.0,
                                                    height=2.0,
                                                    resolution=20,
                                                    split=4,
                                                    create_uv_map=False)
    cyl.compute_vertex_normals()
    vis.add_geometry(cyl)
    return vis


if __name__ == "__main__":
    vis = start_visualizer()
    vis.run()
