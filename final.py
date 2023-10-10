#
# Powering Picobot via Genetic Algorithms, Final version
#
# Name: Ashley Song
# Date: 6/11/2021

import random 

HEIGHT = 25
WIDTH = 25
NUMSTATES = 5

class Program:
    """ Represents a single picobot program (rule set) """

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
                    if step not in y:
                        possible_steps += step
                # At this point, possible_steps holds only the "possible" steps!
                self.rules[(x,y)] = (random.choice(possible_steps), random.choice(range(0, NUMSTATES)))


    def getMove(self, state, surroundings):
        """ Returns the entry of a given key in the program dictionary

            Return values: tuple of next move based on arguments
            Arguments: integer state and string surroundings
        """
        return self.rules[(state,surroundings)]


    def mutate(self):
        """ Changes the entry (move and new state) of a single rule

            Return values: none
            Arguments: none
        """
        LoK = list(self.rules.keys())
        randkey = random.choice(LoK)

        possible_steps = []
        for step in 'NEWS':
            if step not in randkey[1] and step not in self.rules[randkey][0]:
                possible_steps += step
        self.rules[randkey] = (random.choice(possible_steps), random.choice(range(0, NUMSTATES)))


    def crossover(self,other):
        """ Crosses self with the other program to create a hybrid program with rules from both.
            Uses a crossover state to avoid random scrambling

            Return values: returns a new "offspring" Program with rules taken from both the originals
            Arguments: other object of type Program
        """

        offspring = Program()
        cross_state = random.choice(range(0,4)) + 1
        
        for x in range(cross_state):
            for y in list(self.rules.keys()):
                offspring.rules[y] = self.rules[y]
        for x in range(cross_state, 5):
            for y in list(self.rules.keys()):
                offspring.rules[y] = other.rules[y]
        
        return offspring


    def __gt__(self, other):
        """ Overrides the greater than operator to break ties between Program classes

            Return values: randomly returns True or False
            Arguments: other object of type Program
        """
        return random.choice([True, False])

    def __lt__(self, other):
        """ Overrides the less than operator to break ties between Program classes

            Return values: randomly returns True or False
            Arguments: other object of type Program
        """
        return random.choice([True, False])
        

class World:
    """ Simulates a full picobot environment (including picobot's location and actions) """

    def __init__(self, initial_row, initial_col, program):
        """ Constructs the room and program as well as Picobot's initial location and state

            Return values: none
            Arguments: int values initial_row and initial_col, Program object program
        """
        self.row = initial_row       # current row of Pico's location (1,23 inclusive)
        self.col = initial_col       # current col of Pico's location (1,23 inclusive)
        self.state = 0               # current state of Pico
        self.prog = program          # object of type Program that controls the sim
        self.room = [[' ']*WIDTH for row in range(HEIGHT)]           # LoL that holds the 2D room
        
    
        for col in range(WIDTH):
              self.room[0][col] = '+'
              self.room[HEIGHT - 1][col] = '+'
        for row in range(HEIGHT):
            self.room[row][0] = '+'
            self.room[row][WIDTH - 1] = '+'     

        self.room[self.row][self.col] = 'P'   

    
    def __repr__(self):
        """ Returns the room with " " for unvisited rooms, "P" for picobot's position, and "o" for visited locations

            Return values: String representation of the full room
            Arguments: none
        """
        str = ''
        for row in self.room:
            for col in row:
                str += col
            str += '\n'
        
        return str

    
    def getCurrentSurroundings(self):
        """ Returns the surroundings in pico format, ie. 'xxxx'

            Return values: returns the surroundings string for pico's current position
            Arguments: none
        """
        surroundings = ''
        if self.room[self.row - 1][self.col] == '+':
            surroundings += "N"
        else:
            surroundings += "x"

        if self.room[self.row][self.col + 1] == '+':
            surroundings += "E"
        else:
            surroundings += "x"

        if self.room[self.row][self.col - 1] == '+':
            surroundings += "W"
        else:
            surroundings += "x"

        if self.room[self.row + 1][self.col] == '+':
            surroundings += "S"
        else:
            surroundings += "x"

        return surroundings


    def step(self):
        """ Moves the Picobot one step and updates all necessary object properties

            Return values: none
            Arguments: none
        """
        newmove = self.prog.getMove(self.state, self.getCurrentSurroundings())
        
        self.state = newmove[1]                               # update state
        step = newmove[0]
        self.room[self.row][self.col] = 'o'                   # set current position to be visited
        if step == 'N':                                       # determine pico position
            self.row -= 1
        elif step == 'E':
            self.col += 1
        elif step == 'W':
            self.col -= 1
        elif step == 'S':
            self.row += 1   

        self.room[self.row][self.col] = 'P'                   # update pico position


    def run(self,steps):
        """ Moves Picobot by some number of steps

            Return values: none
            Arguments: int steps
        """
        for x in range(steps):
            self.step()


    def fractionVisitedCells(self):
        """ Returns the percentage of cells that have been visited, insluding the current location
            (basic fitness score of the program)

            Return values: floating point fraction of visited cells
            Arguments: none
        """
        visited = 0

        for row in self.room:
            for col in row:
                if col == 'o':
                    visited += 1
        
        return visited/529


def LoProg(size):
    """ Returns a list of 'size' random picobot programs

        Return values: returns a list of size amount of random programs
        Arguments: int size (population size)
    """
    pop = []

    for i in range(size):
        p = Program()
        p.randomize()
        pop += [p]

    return pop


def evaluateFitness(program, trials, steps):
    """ Measures the fitness of a given program over an average of starting points

        Return values: floating point of average fitness
        Arguments: program object of type Program, int trials of starting points to be tested,
        int steps to take in each trial
    """
    totalfitness = 0
    
    for trial in range(trials):
        row = random.choice(range(1,24))
        col = random.choice(range(1,24))
        w = World(row,col,program)
        w.run(steps)
        totalfitness += w.fractionVisitedCells()

    return totalfitness/trials


def GA(popsize, numgens):
    """ Creates popsize random pico programs, and uses the best to create child programs 
        for numgens generations to find the best program in the last generation

        Return values: returns the program with the highest fitness from the last generation
        Arguments: ind popsize, ind numgens
    """
    poplist = LoProg(popsize)
    fitlist = []


    for pop in poplist:
        fitlist += [(evaluateFitness(pop, 42, 1000), pop)]      # initializes the list of tuples
    
    fitlist = sorted(fitlist)[::-1] 



    for i in range(numgens):
        print("Generation ", i)

        totalfit = 0.0
        for i in range(len(fitlist)):
            totalfit += fitlist[i][0]
        
        # print([i[0] for i in fitlist])

        print("   Average fitness: ", totalfit / len(fitlist))
        print("   Best fitness: ", fitlist[0][0])
        print()

        fitlist = fitlist[0: int((popsize * .1) + 1)]           # narrows parent program

        while len(fitlist) < popsize:                           # creating child programs
            proga = fitlist[random.choice(range(len(fitlist)))][1]
            progb = fitlist[random.choice(range(len(fitlist)))][1]
            child = proga.crossover(progb)
            if random.choice(range(1,4)) == 1:                  # random mutations in 1/3 
                child.mutate()
            fitlist += [(evaluateFitness(child, 42, 1111), child)]
        fitlist = sorted(fitlist)[::-1] 


    print("Best Picobot program: ")
    print(fitlist[0])
    return fitlist[0][1]



        


        
            
            
