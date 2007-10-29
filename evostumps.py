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

class EvoStumps(object):
    """ EvoStumps is a stumps classifier tuned through an evolutionary algorithm.
    """
    def __init__(self, trainingInputs, trainingOutputs):
        """ Create a classifierand train it with the provided inputs and outputs.
            trainingInputs should be a list of lists.
            trainingOutputs should be a list of desired outputs, with the 
            same indices as the inputs.
        """
        logging.debug("evostumps.__init(%s, %s)" %(str(trainingInputs), str(trainingOutputs)))
        self.inputs = trainingInputs
        self.outputs = trainingOutputs
        initialClassifier = StumpsClassifier(len(trainingInputs[0]))
        self.optimiser = ClassifierOptimiser(initialClassifier, trainingInput, trainingOutputs)

if __name__ == '__main__':
    optp = OptionParser()
    optp.add_option('-q','--quiet', help='set logging to ERROR', action='store_const', dest='loglevel', const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d','--debug', help='set logging to DEBUG', action='store_const', dest='loglevel', const=logging.DEBUG, default=logging.INFO)
    optp.add_option("-t","--training", dest="trainingfile", default="training.csv", help="File containing CSV training data. Final column should contain targets.")
    optp.add_option("-s","--test", dest="testfile", default="test.csv", help="File containing CSV test data. Same format as training.")
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
            inputs.append(row[0:-1])
            outputs.append(row[-1])
            logging.debug(row)
    except csv.Error, e:
        logging.error("Error reading %s, line %d: %s" % (opts.trainingfile, reader.line_num, e))
        sys.exit()
    logging.debug("EOF: %s" % opts.trainingfile)
    logging.debug("Seeding RNG")
    system = EvoStumps(inputs, outputs)
