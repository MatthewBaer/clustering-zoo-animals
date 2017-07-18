#! /usr/bin/env python
########################################
# CS63: Artificial Intelligence, Lab 9
# Spring 2017, Swarthmore College
########################################
# full name(s): Matt Parker, Matt Baer
# username(s): mparker3, mbaer1
########################################

from clustering import ClusteringModel
from nltk import Tree
from sys import argv
import numpy as np

def main():
    assert len(argv) == 2, "example usage: ./hierarchical.py small"
    c = HierarchicalClustering(argv[1] + ".points", argv[1] + ".labels")
    c.buildTree()
    print c.tree
    c.plotTree()

class HierarchicalClustering(ClusteringModel):
    """
    A class to build agglomerative clusters from the bottom up.

    The dendrogram is represented as a tuple of the form (root, left, right).
        For example: ('cl1' ('cl0', 'a1', 'a2'), 'a3')
        Represents the tree:
                                  cl1
                                /     \
                              cl0     a3
                             /   \
                            a1   a2
    """

    def buildTree(self):
        """Starting with each point as its own cluster, initializes a
        dictionary clusterToPoint that maps cluster labels to their
        center points.

        Repeatedly calculates the distances between all current
        clusters and finds the pair with the minimum distance,
        clusterA and clusterB.  Removes clusterA and clusterB from the
        clusterToPoint dictionary and adds a new cluster with key:
        (clNUM, clusterA, clusterB).  Where the root is named using a
        counter NUM that is incremented after each cluster is formed.
        The value for this key is the average of the original cluster
        points for clusterA and clusterB. Continues this process until
        there is a single cluster joining together all points.

        The key of this final single cluster is a tuple in the form:
        (root, branch, branch) where each branch has the same format.
        The tuple represents the clustering tree. The leaves of this
        tree are the labels of the orginal points.

        Stores the tuple representing the final cluster formed in self.tree.

        NOTE: Create appropriate helper methods as needed. You should
        consider saving distance calucations so they don't have to
        recomputed from scratch each time.
        """
        self.clusters = -1
        self.clusterToPoint = {}
        self.distances = {}
        self.weights = {}
        for point in range(len(self.pointList)):
            self.clusterToPoint[self.labelList[point]] = self.pointList[point]
        for i in self.clusterToPoint.keys():
            self.weights[i] = 1
        while len(self.clusterToPoint) > 1:
            self.getDistances()
            minimum_pair =  self.getMinimumDistance()
            new_cluster = (self.newClusterName(), minimum_pair[0], minimum_pair[1])
            self.clusterToPoint[new_cluster] = self.getAveragePoint(self.clusterToPoint[minimum_pair[0]], self.clusterToPoint[minimum_pair[1]], self.weights[minimum_pair[0]], self.weights[minimum_pair[1]])
            self.weights[new_cluster] = self.weights[minimum_pair[0]] + self.weights[minimum_pair[1]]
            del self.clusterToPoint[minimum_pair[0]]
            del self.clusterToPoint[minimum_pair[1]]
            del self.weights[minimum_pair[0]]
            del self.weights[minimum_pair[1]]
            delete_these = []
            for distance in self.distances:
                if distance[0] or distance[1] in minimum_pair:
                    delete_these.append(distance)
            for entry in delete_these:
                del self.distances[entry]

            delete_these = []
            for weight in self.weights:
                if weight in minimum_pair:
                    delete_these.append(weight)
            for entry in delete_these:
                del self.weights[entry]
        print self.clusterToPoint
        self.tree = self.clusterToPoint.keys()[0]
        self.plotTree()



    def getDistances(self):
        """
        computes all possible distances
        """
        points = self.clusterToPoint.values()
        labels = self.clusterToPoint.keys()
        for i in range(len(points)):
            for j in range(i, len(points)):
                if i != j:
                    self.distances[(labels[i], labels[j])] = self.dist(points[i], points[j])

    def getMinimumDistance(self):
        vals = self.distances.values()
        keys = self.distances.keys()
        return keys[vals.index(min(vals))]

    def newClusterName(self):
        self.clusters += 1
        return "cl" + str(self.clusters)

    def getAveragePoint(self, p1, p2, w1, w2):
        newPoint = []
        for coord in range(len(p1)):
            newPoint.append((float(w1 * p1[coord]) + float(w2 * p2[coord]))/float(2))
        return np.array(newPoint)

    def plotTree(self):
        """
        Builds and plots a tree using the NLTK library.
        """
        t = self.make_nltk(self.tree)
        t.draw()

    def make_nltk(self, tree):
        """
        Recursively creates the tree using the tuple that was constructed
        in buildTree.
        """
        if type(tree) != type(()):
            return tree
        return Tree(tree[0], [self.make_nltk(tree[1]), self.make_nltk(tree[2])])

if __name__ == '__main__':
    main()
