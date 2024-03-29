"""
    stumpclassifier.py - Stump classifier.
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

import math
import random
import logging
from kevrandom import KevRandom

class StumpClassifier(object):
    """ Stump Classifier
    """
    def __init__(self, feature, threshold, hardStump, checkGreaterThanThreshold = None, beta = None):
        """ Construct a classifier with the specified number of features and
            the given config.
        """
        self.feature = feature
        self.threshold = threshold
        self.hardStump = hardStump
        self.checkGreaterThanThreshold = checkGreaterThanThreshold
        self.beta = beta
        self.enabled = True
    
    def classify(self, inputValue):
        """ Classify the provided input.
            Inputs should be a single value for the correct feature. 
            Return is the classification / probability.
        """
        if self.hardStump:
            return self.hardClassify(inputValue)
        else:
            return self.softClassify(inputValue)
    
    def hardClassify(self, inputValue):
        """ Performs a hard classification on the provided value.
        """
        inputCopy = inputValue
        thresholdCopy = self.threshold
        if not self.checkGreaterThanThreshold:
            inputCopy = 0 - inputCopy
            thresholdCopy = 0 - thresholdCopy
        if inputCopy > thresholdCopy:
            classification = 1
        else:
            classification = 0
        
    def softClassify(self, inputValue):
        """ Performs a soft classification on the provided value.
        """
        result = 1.0 / (1 + math.e ** (-self.beta * (inputValue - self.threshold)))
        logging.debug("Classification of %f on value %f for feature %d" %(result, inputValue, self.feature))
        return result
    
    def _perturbInPlaceSoft(self):
        """ Perturbs a soft stump in place.
        """
        kevRandom = KevRandom()
        if random.random() < 0.5:
            newThreshold = -1
            while newThreshold < 0 or newThreshold > 1:
                newThreshold = self.threshold + kevRandom.laplacian() #* 0.1
            self.threshold = newThreshold
        else:
            self.beta += kevRandom.laplacian() #* 0.1
            
    def _perturbInPlaceHard(self):
        """ Perturbs a hard stump in place.
        """
        die
        
    def perturbInPlace(self):
        """ Perturbs the object in place. 
        """
        if self.hardStump:
            self._perturbInPlaceHard()
        else:
            self._perturbInPlaceSoft()
        
    def __str__(self):
        """ Overload for str(object).
        """
        if self.hardStump:
            return self._strHard()
        else:
            return self._strSoft()
            
    def _strHard(self):
        """ Overload for str(obj) on hard stumps.
        """
        if self.checkGreaterThanThreshold:
            operator += ">"
        else:
            operator += "<"
        return "(Hard) %s %f Enabled: %s" %(operator, self.threshold, str(self.enabled))

    def _strSoft(self):
        """ Overload for str(obj) on soft stumps.
        """
        return "(Soft) Beta:%f Threshold:%f Enabled: %s" % (self.beta, self.threshold, str(self.enabled))
