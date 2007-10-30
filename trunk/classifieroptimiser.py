"""
    classifieroptimiser.py - ES class.
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

import logging
from archive import Archive

class ClassifierOptimiser(object):
    """ This class provides an evolution strategy optimiser.
    """
    def __init__(self, wrappedClassifier, iterations, singleChain = True):
        """ Create an ES from a given initial config.
            If singleChain is False then solutions from the
            archive are selected to be perturbed (this is very likely
            a bad idea).
        """
        self.initialConfig = wrappedClassifier
        self.currentConfig = self.initialConfig
        self.singleChain = singleChain
        self.iterations = iterations
        self.archive = Archive()
        self.archive.updateWith(self.initialConfig)
        for i in range(iterations):
            logging.debug("Iteration %d" % i)
            self.iteration()
            logging.debug("Rates TPR: %f FPR: %f" %(self.currentConfig.tpr, self.currentConfig.fpr))
        
    def iteration(self):
        """ Perform an iteration of the optimiser
        """
        if self.singleChain:
            sourceConfig = self.currentConfig
        else:
            sourceConfig = self.archive.randomMember()
        proposal = sourceConfig.perturb()
        if self.archive.updateWith(proposal):
            self.currentConfig = proposal
        
