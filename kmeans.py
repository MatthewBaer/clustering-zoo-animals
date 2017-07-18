#! /usr/bin/env python
########################################
# CS63: Artificial Intelligence, Lab 9
# Spring 2017, Swarthmore College
########################################
# full name(s):
# username(s):
########################################

from clustering import ClusteringModel
import matplotlib.pyplot as plt
from sys import argv
import numpy as np

def main():
    assert len(argv) == 3, "example usage: ./kmeans.py small 3"
    kmeans = KMeans(argv[1] + ".points", argv[1] + ".labels", int(argv[2]))
    kmeans.findCenters(verbose=False)
    #if using use verbose=False, then print/plot at the end:
    kmeans.findCenters()
    kmeans.plotClusters()
    kmeans.printClusters()

class KMeans(ClusteringModel):
    """
    A class to implement Kmeans.
    """
    def __init__(self, pointFile, labelFile, k):
        """k is the number of centers to create when clustering."""
        ClusteringModel.__init__(self, pointFile, labelFile)
        self.k = k

    def printClusters(self, verbose=False):
        """Display data about each center, including its central point,
        the number of points assigned to it. When verbose is True
        also show each of the member points."""
        self.computeError()
        print "Current error:", self.error
        for cluster in self.centroids:
            print "-"*20
            print "Cluster:", cluster, "Length:", len(self.members[cluster])
            print "Centroid:", self.centroids[cluster]
            if verbose:
                print self.members[cluster]

    def plotClusters(self):
        """Plots 2d data about each center and its members.  Uses 8 unique
        colors.  When the number of centers is 8 or less, each cluster
        will have a unique color.  Otherwise colors will be repeated.
        The center of each cluster is plotted as an x, all other points
        are plotted aas o's.
        """
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
        for i,cluster in enumerate(self.centroids.keys()):
            # plt.xlim(0,1)
            # plt.ylim(0,1)
            # x = np.array(self.members[cluster])[:,0]
            # y = np.array(self.members[cluster])[:,1]
            plt.xlim(.1,1.1)
            plt.ylim(-.1,1.1)
            x = np.array(self.members[cluster])[:,5]
            y = np.array(self.members[cluster])[:,11]
            plt.plot(x, y, colors[i%len(colors)]+ 'o')
            c = self.centroids[cluster]
            plt.plot(c[5], c[11], colors[i%len(colors)]+ 'x', markersize=20)
        plt.show()

    def computeError(self):
        """Sets self.error to the sum of squared distances from points to their
        centroids."""
        sumSquareDist = 0
        for cluster in self.centroids.keys():
            for point in self.members[cluster]:
                sumSquareDist += self.dist(point,self.centroids[cluster])**2
        self.error = sumSquareDist

    def findCenters(self, verbose=False):
        """
        Should create and use data structures:
        centroids: a dictionary that maps each cluster name 'c1', 'c2', ...
                   'ck' to the current center point of the cluster (represented
                   as a numpy array)
        members:   a dictionary that maps each cluster name to a numpy array
                   with all the points in that cluster
        labels:    a dictionary that maps each point (as a tuple) to the name
                   of the cluster to which it is currently assigned

        Initializes the centroids to random points in the data set. While the
        members of a cluster change, assigns points to the nearest centroid (E
        step) and moves the centroid to the average of its points (M step).

        If verbose is True the iteration is printed, and self.printCenters()
        and self.plotClusters() are called after each E step.
        """
        #Initialize k centroids to be random points from the data set
        self.centroids = {}
        sampleIndices = np.random.choice(len(self.pointList), self.k, False)
        
        j = 0
        for i in sampleIndices:
            self.centroids[self.labelList[j]] = self.pointList[i]
            j += 1

        #Initialize members and labels to be empty dictionaries
        self.members = {}
        self.labels = {}

        #While points change clusters:
        flag = False
        while flag != True:
            #Initialize each cluster's member list to be empty
            for cluster in self.centroids.keys():
                self.members[cluster] = []

            flag = self.EStep()
           
            for cluster in self.centroids.keys():
                average = self.findAverageOfPoints(self.members[cluster])
                if len(average) == 0:
                    index = np.random.choice(len(self.pointList))
                    self.centroids[cluster] = self.pointList[index]
                    self.EStep()
                else:
                    self.centroids[cluster] = self.findAverageOfPoints(self.members[cluster])


    def EStep(self):
        flag = False
        for point in self.pointList:
            clusterLabel = self.findClosestCentroid(point)
            if point not in np.array(self.members[clusterLabel]):
                flag = True
            self.members[clusterLabel].append(point)
            self.labels[tuple(point)] = clusterLabel
        return flag

    def findClosestCentroid(self, point):
        """

        """
        cents = []
        for centroid in self.centroids.keys():
            cents.append((self.dist(point, self.centroids[centroid]), centroid))
        sortedList = sorted(cents)
        return sortedList[0][1]

    def findAverageOfPoints(self,points):
        
        if len(points) == 0:
            return []
        array = np.array(points)
        totals = [ sum(x)/len(points) for x in zip(*array) ]
        return totals
        



if __name__ == '__main__':
    main()
