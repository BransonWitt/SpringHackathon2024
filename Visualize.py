import open3d as o3d
import laspy as lsp
import numpy as np
import os
import random

cwd = os.getcwd() #Saving current working directory

las = lsp.read(cwd + '\\data\\points1.las') #Reading the las file

#Converting the las file into a numpy array
xyz_data = np.stack([las.x,las.y,las.z],axis=0).transpose((1,0))

#Displaying the numpy array using open3d
geometry = o3d.geometry.PointCloud()
geometry.points = o3d.utility.Vector3dVector(xyz_data)
o3d.visualization.draw_geometries([geometry])