"""
    stumpsclassifier.py - Stumps classifier.
    This file is part of EvoStumps.

    EvoStumps is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This software is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this software; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

import copy
import logging 
from stumpclassifier import StumpClassifier
import random
import sets

class StumpsClassifier(object):
    """ Stumps Classifier, wrapper around a selection of stumps.
    """
    def __init__(self, numFeatures):
        """ Construct a classifier with the specified number of features and
            the given config.
        """
        self.numFeatures = numFeatures
        #poor man's enum
        self.multiplyStumps, self.addStumps = range(2)
        self.combinationType = self.addStumps
        self.weights = []
        self.stumps = []
        self.threshold = 0.5
        for i in range(numFeatures):
            self.stumps.append(StumpClassifier(i, 0.5, hardStump=False, beta=1.0))
            self.weights.append(1.0 / numFeatures)
    
    def numActiveStumps(self):
        """ Returns the number of active stumps/features.
        """
        active = 0
        for stump in self.stumps:
            if stump.enabled:
                active += 1
        if active == 0:
            logging.error("stumps classifier has no active stumps")
            diepleasepython("I should look up how to get python to backtrace 'gracefully'")
        return active
    
    def adjustedStumpWeight(self, stumpIndex):
        """ Returns the weight of the stump with the given index, compensating
            for any inactive stumps.
        """        
        return self.weights[stumpIndex] * self.numFeatures / self.numActiveStumps()
    
    def classify(self, inputs):
        """ Classify the provided inputs.
            Inputs should be a list of lists, and the return will be a list
            of classifications.
        """
        classifications = []
        for input in inputs:
            classification = 0
            for i in range(len(self.stumps)):
                stump = self.stumps[i]
                if stump.enabled:
                    stumpContribution = self.adjustedStumpWeight(i) * stump.classify(input[stump.feature])
                    if self.combinationType == self.multiplyStumps:
                        classification *= stumpContribution
                    else:
                        classification += stumpContribution
            if classification > self.threshold:
                classifications.append(1)
            else:
                classifications.append(0)
        return classifications
        
    def _perturbInPlace(self):
        """ Perturbs the object in place. Private call.
        """
        for i in range(len(self.stumps)):
            stump = self.stumps[i]
            if random.random() <= 0.05:
                stump.enabled = not stump.enabled
            if random.random() <= 0.1:
                logging.debug("Stump %d adjusting weight" % i)
                wantedDiff = random.uniform(-1,1)
                totalWeight = 0.0
                for j in self.listDifference(range(len(self.stumps)), [i]):
                    self.weights[j] += wantedDiff / (len(self.stumps) - 1.0)
                    if self.weights[j] < 0:
                        self.weights[j] = 0.0
                    if self.weights[j] > 1:
                        self.weights[j] = 1.0
                        totalWeight += self.weights[j]
                self.weights[i] = 1 - totalWeight
            if random.random() <= 0.8:
                stump.perturbInPlace()
        logging.debug("Perturbation generates:\n%s" % str(self))
    
    def listDifference(self, list1, list2):
        """ Returns the set difference between two lists
        """
        return sets.Set(list1).difference(sets.Set(list2))
    
    def doubleEquals(self, double1, double2, tolerance):
        """ Checks if two doubles are equal within tolerance.
            Python probably has a method for this which would be better.
        """
        zeroTest = double1 - double2            
        if zeroTest < 0:
            zeroTest = 0 - zeroTest
        return zeroTest < tolerance
        
    def perturb(self):
        """ Returns a perturbed classifier. Does not affect
            this object.
        """
        newClassifier = copy.deepcopy(self)
        newClassifier._perturbInPlace()
        return newClassifier
        
    def __str__(self):
        """ str(object) overload.
        """
        stumpStrings = []
        for stump in self.stumps:
            stumpStrings.append(str(stump))
        return "Weights: %s\nStumps: %s" %(str(self.weights), str(stumpStrings))