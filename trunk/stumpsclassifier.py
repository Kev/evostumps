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

class StumpsClassifier(object):
    """ Stumps Classifier, wrapper around a selection of stumps.
    """
    def __init__(self, numFeatures):
        """ Construct a classifier with the specified number of features and
            the given config.
        """
        self.numFeatures = numFeatures
        self.numFeatures = len(self.trainingInput - 1)
    
    def classify(self, inputs):
        """ Classify the provided inputs.
            Inputs should be a list of lists, and the return will be a list
            of classifications.
        """
        classifications = []
        for input in inputs:
            for stump in self.config.stumps:
                classification = 0
                if stump.enabled:
                    classification += stump
                    if stump.hardStump:
                        if stump.checkGreaterThanThreshold:
                            stumpClassification = input[stump.feature] > stump.threshold
                        else:
                            stumpClassification = input[stump.feature] < stump.threshold
                    else:
                        softstumpscrash
            classifications.append(classification)
        

