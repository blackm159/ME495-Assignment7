from solution import SOLUTION
import constants as c
import copy

class HILL_CLIMBER:
    def __init__(self):
        self.parent = SOLUTION()

    def Evolve(self):
        self.parent.Evaluate("GUI")
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate("Direct")
        self.Print()
        self.Select()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)

    def Mutate(self):
        self.child.Mutate()
        # print("Parent's Weights:")
        # print(self.parent.weights)
        # print("Child's Weights:")
        # print(self.child.weights)

    def Select(self):
        # print("Parent Fitness:")
        # print(self.parent.fitness)
        # print("Child Fitness:")
        # print(self.child.fitness)

        if (self.parent.fitness > self.child.fitness):
            self.parent = self.child

    def Print(self):
        myStr = "\nParent Fitness: " + "{:.2f}".format(self.parent.fitness) + "\tChild Fitness: " + "{:.2f}".format(self.child.fitness)
        print(myStr)

    def Show_Best(self):
        self.parent.Evaluate("GUI")
