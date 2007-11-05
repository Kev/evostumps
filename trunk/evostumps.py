#!/usr/bin/env python
"""
    evostumps.py - Main file for the evostumps classifier/optimiser.
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
from optparse import OptionParser
import csv
import sys
from stumpsclassifier import StumpsClassifier
from wrappedclassifier import WrappedClassifier
from classifieroptimiser import ClassifierOptimiser


class EvoStumps(object):
    """ EvoStumps is a stumps classifier tuned through an evolutionary algorithm.
    """
    def __init__(self, trainingInputs, trainingOutputs, iterations):
        """ Create a classifierand train it with the provided inputs and outputs.
            trainingInputs should be a list of lists.
            trainingOutputs should be a list of desired outputs, with the 
            same indices as the inputs.
            The classifier will be optimised for the 
            given number of iterations.
        """
        logging.debug("evostumps.__init(%s, %s)" %(str(trainingInputs), str(trainingOutputs)))
        self.inputs = trainingInputs
        self.targets = trainingOutputs
        initialClassifier = WrappedClassifier(StumpsClassifier(len(trainingInputs[0])),self.inputs,self.targets)
        self.optimiser = ClassifierOptimiser(initialClassifier, iterations)

if __name__ == '__main__':
    optp = OptionParser()
    optp.add_option('-q','--quiet', help='set logging to ERROR', action='store_const', dest='loglevel', const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d','--debug', help='set logging to DEBUG', action='store_const', dest='loglevel', const=logging.DEBUG, default=logging.INFO)
    optp.add_option("-t","--training", dest="trainingfile", default="training.csv", help="File containing CSV training data. Final column should contain targets.")
    optp.add_option("-i","--iteratiosn", dest="iterations", default="100", help="Number of iterations to optimise the classifier.")
    optp.add_option("-s","--test", dest="testfile", default="test.csv", help="File containing CSV test data. Same format as training.")
    optp.add_option('-p','--plot', help='Plot the archive', action='store_const', dest='plot', const=True, default=False)
    opts,args = optp.parse_args()
    
    logging.basicConfig(level=opts.loglevel, format='%(levelname)-8s %(message)s')
    logging.info("evostumps launched")
    
    inputs = []
    outputs = []

    logging.debug("Opening file: %s" % opts.trainingfile)
    reader = csv.reader(open(opts.trainingfile, "rb"))
    logging.debug("Reading file: %s" % opts.trainingfile)
    try:
        for row in reader:
            inputRow = []
            for value in row[0:-1]:
                inputRow.append(float(value))
            inputs.append(inputRow)
            outputs.append(int(row[-1]))
            logging.debug(row)
    except csv.Error, e:
        logging.error("Error reading %s, line %d: %s" % (opts.trainingfile, reader.line_num, e))
        sys.exit()
    logging.debug("EOF: %s" % opts.trainingfile)
    logging.debug("Seeding RNG")
    system = EvoStumps(inputs, outputs, int(opts.iterations))
    if opts.plot:
        import matplotlib.pylab
        x = system.optimiser.archive.fpr()
        y = system.optimiser.archive.tpr()
        matplotlib.pylab.plot(x, y, 'rx')
        matplotlib.pylab.show()
    logging.info("Bye")
