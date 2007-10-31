"""
    archive.py - Class for managing an estimated Pareto set.
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

import random

class Archive(object):
    """ Class representing an estimated Pareto archive
    """
    def __init__(self):
        """ Boring constructor.
        """
        self.solutions = []
    
    def updateWith(self, newSolution):
        """ Tests if newSolution is non-dominated, add to archive (cleaning
            newly dominated members) if so and return True. Return False if
            not added.
        """
        if newSolution in self.solutions:
            return False
        for solution in self.solutions[:]:
            if solution.dominates(newSolution):
                return False
            if newSolution.dominates(solution):
                self.solutions.remove(solution)
        self.solutions.append(newSolution)
        return True

    def randomMember(self):
        """ Returns a random member of the archive
        """
        return self.solutions[random.randint(0,len(self.solutions) - 1)]