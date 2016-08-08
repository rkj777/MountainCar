from __future__ import division
from math import *
from numpy import *

#Values for tiles
numTilings = 4
sizeOfTilingsX = 9 
sizeOfTilingsY = 9
sizeOfTilings = sizeOfTilingsX * sizeOfTilingsY 


#Values for graph width
Width = 1.7 
Height = 1.4

#Values for width of each tile. At least two tile for sizeOfTilings so
#value is valid
tileWidth = 1.7/(sizeOfTilingsX -1) 
tileHeight = 1.4/(sizeOfTilingsY - 1)


#offest used for tilings 
offset = random.rand() * 0.25    
  
def tilecode(x,y,tileIndices):
    # write your tilecoder here (5 lines or so)
    #Scaling to 0,0
    x = x + 1.2
    y = y + 0.7
  
    for i in range(0,numTilings):
        
     
        
        
        #Moving x and y based on the tile
        #Note tileWidth is used for both as stated in the textbook
        newX = x + (tileWidth*(1/numTilings))*i
        newY = y + (tileWidth*(1/numTilings))*i
       
        #Finding out which tile the new X and Y fall into 
        newX = newX/tileWidth
        newY = newY/tileHeight
     
        #Moving the index of new x to match the array index
        newX = newX + ((sizeOfTilings) *i)
        
        
       
        #Flooring answers to see which tile x and y are in 
        newX = floor(newX)
        newY = floor(newY)
        
        #Counting up from x based on y
        tileIndices[i] = newX + (9 * newY )
def printTileCoderIndices(x,y):
    tileIndices = [-1]*numTilings
    tilecode(x,y,tileIndices)
    print 'Tile indices for input (',x,',',y,') are : ', tileIndices


