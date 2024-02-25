import cv2
import numpy as np
from PIL import Image
import os
from mapClass import Map

#Getting Current Working Dir
cwd = os.getcwd()    

#Opening the image and converting it to an Array
img = Image.open(cwd + "\\simpleMap.png")
imgA = np.array(img)

#Creating a map object
myMap = Map((42.25112,-71.82321))

#Function to display a folder full of water paths as vectors on a map
def show_simulation(a, i):
    #Code below opens a single file, converts it from a csv to an array of floats :)
    with open(f"{dir}\\stream{a}.csv", "r") as f:
        f = f.read()
        f = f.split("\n")
        for q in range(len(f)):
            f[q] = f[q].split(',')
            if f[q] == ['']:
                f = f[:-1]
                break
            for j in range(3):
                f[q][j] = float(f[q][j])
    
    n = 0
    #For loops for every line in the csv
    while n < (len(f) -2):
        #Defining starting and ending positions
        startingCoords = (f[n][0],f[n][1])
        endingCoords = (f[n+1][0],f[n+1][1])    
        
        #Converting starting and ending postions to x and y in the array for the image
        x1, y1 = myMap.convert_latlong_to_xy(startingCoords)
        x2, y2 = myMap.convert_latlong_to_xy(endingCoords)
        
        #Displaying an arrow in the array from the start x and y to the end x and y
        i = cv2.arrowedLine(i, (1200-y1,x1), (1200-y2,x2), color=(255, 255, 255), thickness=1) #Yeah im not sure about why I need to subract the y from 1200 and mix the two up, but its the only way that works so I don't question it
        
        n+=1

#Setting the directory of the folder from this code
dir = cwd + "\\streams1\\"

#Getting the number of simulations in the folder
files = [f for f in os.listdir(dir)]
last_number = int(files[-1].strip("stream.txtcsv"))

for fileNum in range(2,last_number):
    #For every simulation csv file in the folder, display that simulation on the png
    show_simulation(fileNum, imgA)

#Convert the image from an array back into a png and save it
Image.fromarray(imgA).save("result.png")