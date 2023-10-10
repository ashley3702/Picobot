#
# Powering Picobot via Genetic Algorithms, Starter version
#
# Name: Ashley Song
# Date: 6/9/2021

import random 
import time

HEIGHT = 25
WIDTH = 25
NUMSTATES = 5

class Program:
    """ represents a single picobot program (rule set) """

    def __init__(self):
        """ Constructs an empty dictionary for rules

            Return values: none
            Arguments: none
        """
        self.rules = {}   # dictionary of rules w/ tuples of state and surrounding


    def __repr__(self):
        """ Returns the full Picobot program sorted by the state of each rule.
            Each rule should be formatted to be copied and pasted into the Picobot simulator


            Return values: string representation of the program
            Arguments: none
        """
        unsortedKeys = list(self.rules.keys()) 
        sortedKeys = sorted(unsortedKeys) 
        S = ""
        for x in sortedKeys:
            S += (str(x[0]) + " " + x[1] + " -> " + self.rules[x][0] + " " + str(self.rules[x][1]) + "\n")
        
        return S


    def randomize(self):
        """ Generates a random, full set of rules for the program dictionary.
            45 rules total: 9 surroundings for each of the 5 states

            Return values: none
            Arguments: none
        """
        SURR = ['xxxx','Nxxx','NExx','NxWx','xxxS','xExS','xxWS','xExx','xxWx']
        
        for x in range(0, NUMSTATES):
            for y in SURR:
                possible_steps = []
                for step in 'NEWS':
                    if step not in SURR:
                        possible_steps += step
                # At this point, possible_steps holds only the "possible" steps!
                self.rules[(x,y)] = (random.choice(possible_steps), random.choice(range(0, NUMSTATES)))


        
