import laspy as lsp
import numpy as np
import os
import pyproj
import scipy.spatial
import random

class PointCloud:
    def __init__(self, filename:str):
        self.cwd = os.getcwd() #Saving current working directory

        self.las = lsp.read(self.cwd + '\\data\\' + filename) #Loading the las file
        
        self.dimensions = list(self.las.point_format.dimension_names) #loading the headers of the las file

        self.xyz_data = np.stack([self.las.x, self.las.y, self.las.z, self.las.classification],axis=0).transpose((1,0)) #Creating a 2D array with xyz
        
        #Calling starting methods
        self.convert_to_latlong()
        self.generate_heatmap_array()
        
    def convert_to_latlong(self):
        #Trandofrming data from a EPSG:32618 – WGS 84 / UTM zone 18N to Mercador Lat Long
        transformer = pyproj.Transformer.from_crs('epsg:32619','epsg:4326')
        
        
        for i in range(len(self.xyz_data - 1)):
            row = []
            
            x, y = transformer.transform(self.xyz_data[i][0], self.xyz_data[i][1]) #LatLong xy
            
            #Replacing the lat long with the official mercador lat long
            self.xyz_data[i][0] = x
            self.xyz_data[i][1] = y
            
        
        #Finding the number of x and y values and step
        self.maxes = np.max(self.xyz_data, axis=0) #finding the max of all the columns
        self.mins = np.min(self.xyz_data, axis=0) #finding the min value
        
    def find_heatmap_place(self, lat, long):
        """Finds the x and y needed for a heatmap array (not currently used)"""
        foundX = 0
        foundY = 0
        
        for x in range(len(self.xTicks) - 2):
            if lat >= self.xTicks[x] and lat < self.xTicks[x+1]:
                foundX  = x
        
        if foundX == 0:
            foundX = len(self.xTicks) - 1
            
        for y in range(len(self.yTicks) - 2):
            if long >= self.yTicks[y] and long < self.yTicks[y+1]:
                foundY  = y
        
        if foundY == 0:
            foundY = len(self.yTicks) - 1
        
        self.heatmapA[foundX][foundY] += 1
        
            
    def generate_heatmap_array(self):
        """Generates a zero heat map as well the ticks, heat map ticks go from bottom left to top right in a map"""
        #Calculating distance traveled in x and y 
        xdis = self.maxes[0] - self.mins[0]
        ydis = self.maxes[1] - self.mins[1]
        
        #Calulating scale so the smallest side is split by 100
        scale = min(xdis/100,ydis/100)
        
        #Finding minimum values
        x1, y1 = self.mins[:2]
        
        #Creating the x and y ticks as lists
        self.xTicks = []
        self.yTicks = []
        
        while x1 < self.maxes[0]:
            self.xTicks.append(x1)
            x1 += scale
            
        while y1 < self.maxes[1]:
            self.yTicks.append(y1)
            y1 += scale
        
        #Creating a numpy zeros array and saving it as an attribute of the PointCloud class
        self.heatmapA = np.zeros((len(self.xTicks), len(self.yTicks)))
        
        
    def calculate_nearest_points(self, point:list, amount:int):
        tree = scipy.spatial.cKDTree(self.xyz_data[:, :2]) #Creating a KD tree in C++ through SciPy
        distance, index = tree.query(point,amount) #Returns the n (amount) of points closest to point(point) and their distances and related indexes
        
        return(distance, index)

    def simulate_stream(self, start):
        x, y, z = start[:3] #Finding start x,y,z
        self.find_heatmap_place(x,y)
        stream_path = [[x,y,z]] #Creating an array of points to simulate the path
        
        while x < self.maxes[0] and x > self.mins[0] and y < self.maxes[1] and y > self.mins[1]: #Staying in bounds
            dis, ind = self.calculate_nearest_points([x,y], 5_000) #Calculate the indexes of the n nearest points
            
            #Loop to find the lowest z value in the close values
            minIndex = self.xyz_data[ind[0]]
            
            for i in ind:
                #If found a smaller z values, set it as our min index
                if self.xyz_data[i][2] < minIndex[2]:
                    minIndex = self.xyz_data[i]
            
            
            #If there is no change in z, we are in a rut 
            if z - minIndex[2] == 0:
                break
            
            #Resetting xyz 
            x = minIndex[0]
            y = minIndex[1]
            z = minIndex[2]
            
            #Adding new coordinates to the path
            self.find_heatmap_place(x,y)
            stream_path.append([x,y,z])
        
        return np.array(stream_path)
    
    def random_simulations(self, num_sim):
        dir = self.cwd + "\\streams2\\" #Defining the directory
        
        #Finding the number of simulations already in our directory
        files = [f for f in os.listdir(dir)]
        last_number = int(files[-1].strip("stream.txtcsv"))
        
        #Running the simulate_stream at random points until with reach the number of simulations desired
        for j in range(num_sim):
            a = self.xyz_data[random.randint(0, (np.shape(self.xyz_data)[0])-1)] #Finding a random number for our index of the starting point
            print(j)
            
            simulation = self.simulate_stream(a)
            np.savetxt(f"stream{last_number+1}.csv",simulation,delimiter=",") #Saving simulation as a csv file
            last_number += 1

        #WORK IN PROGRESS BELOW - generating a heat map
        myha = np.array(self.heatmapA) 
        np.savetxt(f"ha.csv",myha,delimiter=",",fmt='%d')
            
            
            
            
        
        
        
myPoints = PointCloud('points1.las')
myPoints.random_simulations(2500)