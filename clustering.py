#! /usr/bin/env python

from sys import argv
from os.path import exists
import numpy as np

def main():
    assert len(argv) == 2, "example usage: ./clustering.py small"
    c = ClusteringModel(argv[1] + ".points", argv[1] + ".labels")
    print "\nLABELS"
    print c.labelList
    print "\nPOINTS"
    print c.pointList

class ClusteringModel(object):
    """
    A parent class for clustering techniques.
    """
    def __init__(self, pointFile, labelFile):
        """
        Given a file of points (one point per line, with each dimension
        separated by whitespace) and given a file of unique labels for
        each point (one label per line, interpreted as strings), create
        a tree that clusters the points based on Euclidean distance in
        a greedy fashion.

        pointList is a list of numpy array objects
        labelList is a list of string labels associated with each point
        pointToLabel is a dictionary that maps a tuple of each point to its
        label
        dist is the method to use to determine the distance between two
        points
        """
        self.pointList = self.getPoints(pointFile)
        if exists(labelFile):
            self.labelList = self.getLabels(labelFile)
        else:
            self.labelList = [str(i) for i in range(len(self.pointList))]
        self.pointToLabel = self.makePointDict()
        self.dist = self.EuclideanDist #extension: change this to Manhattan

    def makePointDict(self):
        """
        Builds the pointToList dictionary.
        """
        d = {}
        for i in range(len(self.pointList)):
            d[tuple(self.pointList[i])] = self.labelList[i]
        return d

    def EuclideanDist(self, p1, p2):
        """
        Given two numpy arrays representing points, calculates the Euclidean
        distance between them by finding their difference, squaring it, and
        then taking the square root.
        """
        return np.linalg.norm(p1 - p2)

    def getLabels(self, filename):
        """
        Expects file to contain one string per line representing a unique
        label for each corresponding data point.
        Returns: A list of labels as strings
        """
        with open(filename) as f:
            labels = [line.strip() for line in f]
        return labels

    def getPoints(self, filename):
        """
        Expects file to contain one pattern per line.  Each pattern consists
        of a sequence of floating point value in the range [0,1] separated by
        whitespace.
        Returns: A list of data points as numpy arrays
        """
        with open(filename) as f:
            points = [[float(x) for x in line.strip().split()] for line in f]
            points = np.array(points)
        return points

if __name__ == '__main__':
    main()
