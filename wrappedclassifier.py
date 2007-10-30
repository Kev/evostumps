"""
    wrappedclassifier.py - Wrapper around a classifier to add dominance etc.
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

class WrappedClassifier(object):
    """ This wraps a classifier in enough MOO to allow it to be optimised
        by the ClassifierOptimiser.
    """
    def __init__(self, classifier, data):
        """ Construct a wrapper around the specified classifier, using
            the provided data for evaluation
        """
        self.classifier = classifier
        self.data = data
        
    def perturb(self):
        """ Perturbs the contained classifier, evaluates it and returns a
            new WrappedClassifier containing it.
        """
        newWrapper = WrappedClassifier(self.classifier.perturb(), self.data)
        newWrapper._evaluate()
        return newWrapper
        
    def _evaluate(self):
        """ Evaluates the performance of the wrapped classifier.
        """
        results = self.classifier.classify(self.data)
        self.confusion = [[0,0][0,0]]
        for i in range(0,len(results)):
            self.confusion[self.trainingOutputs[i]][results[i]] += 1
        self.tpr = confusion[1][1]/sum(confusion[1])
        self.fpr = confusion[0][0]/sum(confusion[0])
        
    def dominates(self, other):
        """ Test for domination of other.
            Returns True where tpr/fpr are equivalent.
        """
        return self.tpr >= other.tpr and self.fpr <= other.fpr