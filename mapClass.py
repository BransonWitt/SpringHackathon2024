import os
import prettymaps
import json


class Map:
    def __init__(self, lat_long:tuple, radius=300):
        #These should be constant for the pretty maps being used
        self.cornerOffset = 130 #White space pixels
        self.ImageLength = 1200 #Square dimensions of the image
        
        #Getting current working directory
        self.cwd = os.getcwd()
        
        #Creating two pretty maps, one with a simple preset and another for the types of boundaries filled in
        self.map1 = prettymaps.plot(lat_long, radius=radius, preset='minimal')
        self.map2 = prettymaps.plot(lat_long, radius=radius)
        
        #Lat Long boundary coordinates
        boundary_json = prettymaps.fetch.get_boundary(lat_long, radius).to_json()
        myJSON = json.loads(boundary_json)
        roughCoords = myJSON["features"][0]["geometry"]["coordinates"][0][:-1]
        
        #Seperating x and y in the array for the corners
        xs = [x[1] for x in roughCoords]
        ys = [y[0] for y in roughCoords]
        
        #Finding the mins and maxes for the lines of the map
        xmin = min(xs)
        xmax = max(xs)
        
        ymin = min(ys)
        ymax = max(ys)
        
        #Setting the mins and maxes into attributes
        self.maxCoord = [xmax, ymax]
        self.minCoord = [xmin, ymin]
        self.minmax = [xmax, ymin] #Top left
        
        #Finding total distances covered
        self.totalLat = abs(xmax - xmin)
        self.totalLong = abs(ymax - ymin)
        
        #Finding total distances covered in pizels
        self.LatperXpixel =  self.totalLat / (self.ImageLength - (self.cornerOffset * 2))
        self.LongperYpixel = self.totalLong / (self.ImageLength - (self.cornerOffset * 2)) 
        
        
    def save_images(self):
        """Method to save the image attributes as pngs"""
        self.map1.fig.savefig(self.cwd + "\\simpleMap.png")
        self.map2.fig.savefig(self.cwd + "\\complexMap.png")
        
    def convert_latlong_to_xy(self, ll:tuple): #ll = lat long
        """Converts lat and long coordinates into x and y for an image"""
        disX = round(abs((self.maxCoord[0] - ll[0]) / self.LatperXpixel)) + self.cornerOffset
        disY = round(abs((self.maxCoord[1] - ll[1]) / self.LongperYpixel)) + self.cornerOffset
        
        return(disX, disY)
        
#o = Map((42.25112,-71.82321))
#print(o.convert_latlong_to_xy(42.25112,-71.82321))