from PIL import Image
import numpy as np
import os
import math

######
#Author:  Mike van der Naald
#Python 2 was used
# Date: 6/21/2016
######






#This function will take in the name of the file 


def addTo(xyCoordinates,imageDimensions,dwelltime,blankOrNotBottom,blankOrNotTop,textFile):
        xCoordinate=xyCoordinates[:,0]
        yCoordinate=xyCoordinates[:,1]
        #Then lets find how many points there are
        numCoordinate=xyCoordinates[0].size
        #This will hold the y-coordinates
        
        
        #Now that we have loaded in the xycoordinates from the image we need to
        #scale them so that they are actually in the FIB's xy range 56576
        
        #xScale=math.floor(56576/imageDimensions[0])
        #yScale=math.floor(56576/imageDimensions[1])
        #    
        #xCoordinate=xCoordinate*xScale
        #yCoordinate=yCoordinate*yScale
        #Now they have been scaled.
        
        #
        #Let's find the dwelltimes column and formate it as well.
        dwellTimes=dwelltime*np.ones(len(xCoordinate))
        dwellTimes.dot(dwellTimes.transpose())
        dwellTimes.shape = (numCoordinate,1)

        #Now let's concantenate the arrays before printing
        array=np.hstack((dwellTimes,xCoordinate,yCoordinate))
        #Now we open the file such that we can append a numpy array.


        file=open(textFile,'ab')
    
    
        #We now check whether or not we need to insert a unblank at the top
        #using the parameter blankOrNotTop and also whether or not we need to
        #insert a blank at the end of the array using blankOrNotBottom

        if blankOrNotBottom==1 and blankOrNotTop==1:
            numStuff=array.shape
            numRows=numStuff[0]
            topRow=array[0,:]
            bottomRow=array[numRows-1,:]
            middleRows=array[1:numRows-1,:]
            #We append the 1 for unblanking
            newTopRow=np.append(topRow,[1])
            newBottomRow=np.append(bottomRow,[0])
            #Now to print it all to the text file.
            np.savetxt(file,newTopRow[np.newaxis], fmt='%d', newline=os.linesep)
            np.savetxt(file,middleRows, fmt='%d', newline=os.linesep)
            np.savetxt(file,newBottomRow[np.newaxis], fmt='%d', newline=os.linesep)

        
   
        if blankOrNotBottom==1 and blankOrNotTop!=1:
            numStuff=array.shape
            numRows=numStuff[0]
            main=array[0:numRows-1,:]
            endRow=array[numRows-1,:]  
        #blank the endRow
            newEndRow=np.append(endRow,[0])
            np.savetxt(file,main, fmt='%d', newline=os.linesep)
            np.savetxt(file,newEndRow[np.newaxis], fmt='%d')


        if blankOrNotTop==1 and blankOrNotBottom!=1:
            numStuff=array.shape
            numRows=numStuff[0]
            main=array[1:,:]
            topRow=array[0,:]
            newTopRow=np.append(topRow,[1])
            np.savetxt(file,newTopRow[np.newaxis], fmt='%d', newline=os.linesep)
            np.savetxt(file,main, fmt='%d', newline=os.linesep)



            
        if blankOrNotTop!=1 and blankOrNotBottom!=1:
            np.savetxt(file,array, fmt='%d', newline=os.linesep)

        file.close()



def streamFileGenerator(imageFilePath):
    
    #This opens the image in the PIL library "Drawing1-Model.png"
    im = Image.open(imageFilePath)

    #This declares the size of the image
    col,row =  im.size

    #This initializes an array that will hold the black pixels (cuts) in a format like:
    blackPixels=np.zeros((1,2))
    
    #This turns the pixels into a numpy array
    pixels = np.array(im)
    
    #This pours through the array and turns data into a properly formatted data array
    for i in range(1,row):
        for j in range(1,col):
            r,g,b =  pixels[i,j]
            #data[i*col + j,:] = r,g,b,i,j
            #While we're looping through each pixel lets pick out the 
            #black pixels which is where the cuts will be.
            if [r,g,b] == [0,0,0]:
                blackPixels = np.append(blackPixels,[[i,j]], axis=0)
        

    #Now that we have a list of all black cuts let's delete
    #The first row it is garbage.
    blackPixels = np.delete(blackPixels, (0), axis=0)
    
    
    

    #So now we want to use these balck pixels as cuts so we are going to do just that usin the above function.
    
    