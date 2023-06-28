# Joshua Liu
# 2023-06-26
# Rover Path Generation 
# This program was created to create a path with coordinates from a file
# It has not been altered to run alongside with the rover
# This program is not dependent on ROS, but can be implemented in a pub/sub if necessary, 
# all it needs is a log of latitude and longitude coordinates

# 111 meters = 1° of latitude or longitude

import pygame
from numpy import interp
from cmath import inf

pygame.init()

PATH_SIZE = 1 # This sets the thickness of the path drawn (Integer)

BACKGROUND, PATH_COLOR = (0, 0, 0), (255, 255, 255) #Colors used in the display

SCREEN_HEIGHT = 800
SCREEN_WIDTH = SCREEN_HEIGHT * 0.6 # 60% for the height of the screen (This is the porportion that I found works best for the testing I did)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Rover Path"), screen.fill(BACKGROUND)

stringCoordinates = [] # Stores the coordinates read directly from the file
floatCoordinates = [] # Stores the coordinates converted to floats from the stringCoordinates list

minLat, maxLat = inf, -inf # Stores the minimum and maximum latitude coordinates for remapping purposes
minLon, maxLon = inf, -inf # Stores the minimum and maximum longitue coordinates for remapping purposes

done = False

# This function replaces a for loop used in readCoordinatesFromFile
def readingCoordinatesMap(coordinate):
    stringCoordinates.append(coordinate.split(","))

# This function reads the coordinates from the file and parses it to a usable format
def readCoordinatesFromFile(file_name):
    try:
        opened_file = open(file_name, "r")
        line = opened_file.readline()
        opened_file.close()
        # TODO Any other parsing will be done here
        separateCoordinates = line.split(" ")
        list(map(readingCoordinatesMap, separateCoordinates))
    except FileNotFoundError:
        print("No such file directory.")

# This function replaces a for loop used to convert the coordinates from strings to floats
def convertStringToFloat(coordinate):
    if coordinate[0] != "" and coordinate[1] != "":
        floatCoordinates.append([float(coordinate[0]), float(coordinate[1])])

# This function determines the minimum and maximum of the coordinates
def getMinMaxLatLon():
    minLat, maxLat = inf, -inf
    minLon, maxLon = inf, -inf

    for i, coordinate in enumerate(floatCoordinates):
        # Perform a manual zoom in by changing the 2 values in the first if statement. 
        # No zoom would be len(floatCoordinates) > i > -1
        if len(floatCoordinates) > i > -1:
            if minLat > coordinate[0]:
                minLat = coordinate[0]
            if maxLat < coordinate[0]:
                maxLat = coordinate[0]
            if minLon > coordinate[1]:
                minLon = coordinate[1]
            if maxLon < coordinate[1]:
                maxLon = coordinate[1]

    return minLat, maxLat, minLon, maxLon

if __name__ == "__main__":
    readCoordinatesFromFile("Coordinates.txt") # Reads the coordinates from a file and stores the values in stringCoordinates
    list(map(convertStringToFloat,stringCoordinates)) # Converts the stringCoordinates to floatCoordinates
    minLat, maxLat, minLon, maxLon = getMinMaxLatLon() # Get the min/max coordinate values

    for i, coord in enumerate(floatCoordinates):
        # If it is not the first coordinate recorded on file 
        # then draw a line between the current and the previous coordinate
        if i > 0: 
            # Maps the current coordinates to the screen as an x,y position
            x = interp(coord[0], [minLat, maxLat], [SCREEN_WIDTH, 0]) 
            y = interp(coord[1], [minLon, maxLon], [0, SCREEN_HEIGHT])
            # Maps the previous coordinates to the screen as an x,y position
            x1 = interp(floatCoordinates[i - 1][0], [minLat, maxLat],[SCREEN_WIDTH, 0])
            y1 = interp(floatCoordinates[i - 1][1], [minLon, maxLon],[0, SCREEN_HEIGHT])
            # Draws the line connecting the 2 coordinates
            pygame.draw.line(screen, PATH_COLOR, (x,y), (x1,y1), PATH_SIZE)
    pygame.display.update()# Draws everything on screen once

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
