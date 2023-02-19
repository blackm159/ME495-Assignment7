import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c


class SOLUTION:
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        # a = 3
        # b = 2
        self.weights = np.empty(shape=(c.numSensorNeurons,c.numMotorNeurons), dtype='object')
        # self.weights = np.empty(shape=(a,b), dtype='object')
        for row in range(0, c.numSensorNeurons):
            for col in range(0, c.numMotorNeurons):
                self.weights[row,col] = np.random.rand()
        self.weights = self.weights * 2 - 1

        random.seed(c.seed)
        print("seed = " + str(c.seed))

        self.x = []
        self.y = []
        self.z = []

        for ind in range(0, c.numLinks):
            self.x.append(random.uniform(0.25,1.25)) #random.random()
            self.y.append(random.uniform(0.25,1.25)) #random.random()
            self.z.append(random.uniform(0.25,1.25)) #random.random()

        self.linkNames = []
        self.jointNames = []

        self.randSensors = random.sample(range(0,c.numLinks), c.numSensorNeurons)
        self.randSensors.sort()

    def Evaluate(self, directOrGUI):
        # pass
        self.Create_Body()
        self.Create_Brain()

        os.system("start /B py simulate.py " + directOrGUI + " " + str(self.myID))

        # fitnessFileName = "fitness" + str(self.myID) + ".txt"
        # while not os.path.exists(fitnessFileName):
        #     time.sleep(0.01)

        # fitnessFile = open(fitnessFileName, "r")
        # self.fitness = float(fitnessFile.read())
        # print("self.fitness = " + str(self.fitness))
        # fitnessFile.close()

    def Start_Simulation(self, directOrGUI):
        
        self.Create_Body()
        self.Create_Brain()

        #print("start /B py simulate.py " + directOrGUI + " " + str(self.myID))
        os.system("start /B py simulate.py " + directOrGUI + " " + str(self.myID))
        

    def Wait_For_Simulation_To_End(self):
        fitnessFileName = "fitness" + str(self.myID) + ".txt"
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)

        fitnessFile = open(fitnessFileName, "r")
        self.fitness = float(fitnessFile.read())
        # print("\nself.fitness = " + str(self.fitness))
        fitnessFile.close()
        os.system("del " + fitnessFileName)

    def Mutate(self):
        randRow = random.randint(0,c.numSensorNeurons-1)
        randCol = random.randint(0,c.numMotorNeurons-1)

        self.weights[randRow, randCol] = random.random()*2 - 1

    def Set_ID(self, newID):
        self.myID = newID

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        # length = 1
        # width = 1
        # height = 1
        # x = -2
        # y = -2
        # z = height/2

        # pyrosim.Send_Cube(name="Box", pos = [-2,-2,height/2], size = [length,width,height])

        pyrosim.End()

    def Create_Body(self):
        self.Create_World()

        pyrosim.Start_URDF("body" + str(self.myID) + ".urdf")

        # for ind in range(0,2):
        ind = 0
        self.linkNames.append("Body"+str(ind))
        pyrosim.Send_Cube(name=self.linkNames[ind], pos = [0, 0, self.z[0]/2], size = [self.x[ind], self.y[ind], self.z[ind]])

        ind = 1
        self.linkNames.append("Body"+str(ind))
        self.jointNames.append("Body"+str(ind-1)+"_Body"+str(ind))
        pyrosim.Send_Joint( name =  self.jointNames[ind-1], parent= "Body"+str(ind-1), child = "Body"+str(ind), \
            type = "revolute", position = [self.x[0]/2, 0, self.z[0]/2], jointAxis="0 1 0")

        pyrosim.Send_Cube(name=self.linkNames[ind], pos = [self.x[1]/2, 0, 0], size = [self.x[ind], self.y[ind], self.z[ind]])

        for ind in range(2, c.numLinks):
            self.linkNames.append("Body"+str(ind))
            self.jointNames.append("Body"+str(ind-1)+"_Body"+str(ind))

            pyrosim.Send_Joint( name = self.jointNames[ind-1], parent= "Body"+str(ind-1), child = "Body"+str(ind), \
                type = "revolute", position = [self.x[ind-1], 0, 0], jointAxis="0 1 0")

            pyrosim.Send_Cube(name=self.linkNames[ind], pos = [self.x[ind]/2, 0, 0], size = [self.x[ind], self.y[ind], self.z[ind]])
           

        print(self.linkNames)
        print(self.jointNames)
        print(self.x)
        print(self.y)
        print(self.z)
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        # for joint in joint names create motor
        # have a counter variable for name ID
        # do sensors first

        print(self.randSensors)

        counter = 0
        for ind in self.randSensors:
            pyrosim.Send_Sensor_Neuron(name = counter , linkName = self.linkNames[ind])
            counter = counter + 1

        for ind in range(0, c.numMotorNeurons):
            pyrosim.Send_Motor_Neuron(name = counter , jointName = self.jointNames[ind])
            counter = counter + 1
        

        for currentRow in range(0, c.numSensorNeurons):
            for currentColumn in range(0,c.numMotorNeurons):
                # print("i = " + str(i) + ", j = " + str(j))
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn+c.numSensorNeurons , weight = self.weights[currentRow][currentColumn] )

        pyrosim.End()