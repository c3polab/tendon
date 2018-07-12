# Riley Karp
# C3PO
# Created 7/2/2018
# analysis.py

import sys
import matplotlib.pyplot as plt
import collection
import numpy as np

# length getPlateaus
def getLengthPlateaus( data ):

    plats = []
    lenPlat = 30 # num pts corresponding to last 3sec of plateau
    # length: 10 pts/sec

    # loop through the points to find plateaus
    idx = 30
    while idx < len(data):
        # calculate difference between points
        dif = abs( data[idx] - data[idx-30] )
        # if dif is too large, calc median of plateau before it
        if (dif > 0.02) or (idx == ( len(data)-1 )):
            median = np.median( data[idx-lenPlat : idx] )

            # if plateau is found more than once (2 consecutive plateaus are
            # close in value), then average the values found
            if len(plats) > 0 and abs(median - plats[-1]) < 0.2:
                plats[-1] = abs(median+plats[-1])/2
            else:
                plats.append(median)
            idx += 30
        else:
            idx += 1

    return plats


# Takes in a list of data and returns a list of the median value at each plateau
def getForcePlateaus( data ):

    plats = []
    lenPlat = 30 # num pts corresponding to last 3sec of plateau
    # force: 10 pts/sec = 30 pts in 3sec

    s = []
    step = 4
    # loop through all points
    idx = step
    while idx < len(data):
        # calculate magnitude of the slope between two consecutive points
        slope = abs( data[idx] - data[idx-step] )/step
        # if slope is too steep, calc median of plateau before it
        if (slope > 0.75) or (idx == ( len(data)-1 )):
            median = np.median( data[idx-lenPlat : idx] )

            # if plateau is found more than once (2 consecutive plateaus are
            # close in value), then average the values found
            if len(plats) > 0 and abs(median - plats[-1]) < ( max(data)*0.05 ):
                plats[-1] = abs(median+plats[-1])/2
            else:
                plats.append(median)
            idx +=20

        else:
            idx += 1
    return plats


# Takes in 2 lists of data (independent & dependent variables) and plots them
# if only one list is given, it is plotted as the dependent variable with index
# as independent variable.
def plotData( dep, indep=[], xlabel='Length (cm)', ylabel='Force (N)', title = 'Force vs. Length' ):
    if indep == []:
        plt.plot(dep, 'bo')
        xlabel = 'Reading Number'
    else:
        if len(indep) != len(dep):
            print 'Inputs are not equal lengths. X has length ', len(indep) , \
            ' and Y has length ' , len(dep)
            return
        plt.plot(indep, dep, 'bo')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


def subplots( force, length ):
    plt.subplot(2,1,1)
    plt.plot(force, 'bo')
    plt.xlabel('Reading #')
    plt.ylabel('Force (N)')
    plt.title('Force & Length vs. Reading #')

    plt.subplot(2,1,2)
    plt.plot(length, 'bo')
    plt.xlabel('Reading #')
    plt.ylabel('Length (cm)')

    plt.show()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        filename = sys.argv[1]

        if 'force' in filename:
            data = collection.readForce(filename)
            plats = getForcePlateaus( data )
            print plats
            print len(plats)
            plotData(data)

        elif 'length' in filename:
            data = collection.readLength(filename)
            plats = getLengthPlateaus( data )
            print plats
            print len(plats)
            plotData(data)

        else:
            force = collection.readForce(filename + '_force.csv')
            length = collection.readLength(filename + '_length.csv')

            fplats = getForcePlateaus( force )
            lplats = getLengthPlateaus( length )

            print 'force plats: ', fplats, len(fplats)
            print 'length plats: ', lplats, len(lplats)

            subplots(force,length)
