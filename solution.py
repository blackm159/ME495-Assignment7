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

        for ind in range(0, c.totalNumLinks):
            if ind in c.locTorso:
                self.x.append(random.uniform(1.0,1.25)) #random.random()
                self.y.append(random.uniform(0.5,1.25)) #random.random()
                self.z.append(random.uniform(0.5,1.25)) #random.random()
            else:
                self.x.append(random.uniform(0.25,0.75)) #random.random()
                self.y.append(random.uniform(0.25,0.75)) #random.random()
                self.z.append(random.uniform(0.5,0.75)) #random.random()

        self.linkNames = []
        self.jointNames = []

        self.randSensors = random.sample(range(0,c.totalNumLinks), c.numSensorNeurons)
        self.randSensors.sort()
        # print(self.randSensors)

        self.myColor = []
        for ind in range(0,c.totalNumLinks):
            if ind in self.randSensors:
                self.myColor.append("green")
            else:
                self.myColor.append("blue")

        self.counterTorso = []

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

        startZ = 3
        counter = -1
        for row in range(1, c.numLinks+1):
            counter = counter + 1
            # print("row = "+str(row))
            self.linkNames.append("Body"+str(row)+"."+str(0)+"."+str(0))
            
            jointDir = random.randint(1,3)
            # 1 is x axis
            # 2 is y axis
            # 3 is z axis
            if jointDir == 1:
                jointAxisStr = "1 0 0"
            elif jointDir == 2:
                jointAxisStr = "0 1 0"
            elif jointDir == 3:
                jointAxisStr = "0 0 1"


            if row > 2:
                self.jointNames.append("Body"+str(row-1)+"."+str(0)+"."+str(0)+"_Body"+str(row)+"."+str(0)+"."+str(0))
                pyrosim.Send_Joint( name = self.jointNames[counter-1], parent= self.linkNames[self.counterTorso[row-2]], child = self.linkNames[counter], \
                    type = "revolute", position = [self.x[self.counterTorso[row-2]], 0, self.z[0]/2], jointAxis=jointAxisStr)

                pyrosim.Send_Cube(name=self.linkNames[counter], pos = [self.x[counter]/2, 0, 0], size = [self.x[counter], self.y[counter], self.z[counter]], materialColor=self.myColor[counter])

            elif row == 2:
                self.jointNames.append("Body"+str(row-1)+"."+str(0)+"."+str(0)+"_Body"+str(row)+"."+str(0)+"."+str(0))
                pyrosim.Send_Joint( name = self.jointNames[counter-1], parent= self.linkNames[self.counterTorso[row-2]], child = self.linkNames[counter], \
                    type = "revolute", position = [self.x[self.counterTorso[row-2]]/2, 0, startZ-self.z[0]/2], jointAxis=jointAxisStr)

                pyrosim.Send_Cube(name=self.linkNames[counter], pos = [self.x[counter]/2, 0, self.z[0]/2], size = [self.x[counter], self.y[counter], self.z[counter]], materialColor=self.myColor[counter])
            
            else:
                pyrosim.Send_Cube(name=self.linkNames[counter], pos = [0, 0, startZ], size = [self.x[counter], self.y[counter], self.z[counter]], materialColor=self.myColor[counter])

            self.counterTorso.append(counter)
            # counter = counter + 1
            # print("counter = "+str(counter))

            for col in range(1,2+1):
                # print("col = "+str(col))

                for ind in range(1,c.numSubLinks[row-1,col-1]+1):
                    counter = counter + 1
                    # print("ind = "+str(ind))
                    # print("counter = "+str(counter))

                    self.linkNames.append("Body"+str(row)+"."+str(col)+"."+str(ind))
                    # self.jointNames.append("Body"+str(row)+"."+str(col)+"."+str(ind-1)+"_Body"+str(row)+"."+str(col)+"."+str(ind))

                    if col == 2: # negative side joint
                        negMultY = -1
                    else:
                        negMultY = 1


                    dir = random.randint(1,2)
                    if ind == 1:
                        dir = 2
                    # 1 is down in -z direction
                    # 2 is left/right in +/-y direction

                    jointDir = random.randint(1,3)
                    # 1 is x axis
                    # 2 is y axis
                    # 3 is z axis
                    if jointDir == 1:
                        jointAxisStr = "1 0 0"
                    elif jointDir == 2:
                        jointAxisStr = "0 1 0"
                    elif jointDir == 3:
                        jointAxisStr = "0 0 1"

                    if ind == 1 and row == 1:
                        self.jointNames.append("Body"+str(row)+"."+str(0)+"."+str(0)+"_Body"+str(row)+"."+str(col)+"."+str(ind))
                        pyrosim.Send_Joint( name = self.jointNames[counter-1], parent= self.linkNames[self.counterTorso[row-1]], child = self.linkNames[counter], \
                            type = "revolute", position = [0, negMultY*self.y[self.counterTorso[row-1]]/2, startZ], jointAxis=jointAxisStr)
                        pyrosim.Send_Cube(name=self.linkNames[counter], pos = [0, negMultY*self.y[counter]/2, 0], size = [self.x[counter], self.y[counter], self.z[counter]], materialColor=self.myColor[counter])
                        
                    elif ind == 1 and row == 2: 
                        self.jointNames.append("Body"+str(row)+"."+str(0)+"."+str(0)+"_Body"+str(row)+"."+str(col)+"."+str(ind))
                        pyrosim.Send_Joint( name = self.jointNames[counter-1], parent= self.linkNames[self.counterTorso[row-1]], child = self.linkNames[counter], \
                            type = "revolute", position = [self.x[self.counterTorso[row-1]]/2, negMultY*self.y[self.counterTorso[row-1]]/2, self.z[0]/2], jointAxis=jointAxisStr)
                        pyrosim.Send_Cube(name=self.linkNames[counter], pos = [0, negMultY*self.y[counter]/2, 0], size = [self.x[counter], self.y[counter], self.z[counter]], materialColor=self.myColor[counter])
                    
                    elif ind == 1 and row > 2: 
                        self.jointNames.append("Body"+str(row)+"."+str(0)+"."+str(0)+"_Body"+str(row)+"."+str(col)+"."+str(ind))
                        pyrosim.Send_Joint( name = self.jointNames[counter-1], parent= self.linkNames[self.counterTorso[row-1]], child = self.linkNames[counter], \
                            type = "revolute", position = [self.x[self.counterTorso[row-1]]/2, negMultY*self.y[self.counterTorso[row-1]]/2, 0], jointAxis=jointAxisStr)
                        pyrosim.Send_Cube(name=self.linkNames[counter], pos = [0, negMultY*self.y[counter]/2, 0], size = [self.x[counter], self.y[counter], self.z[counter]], materialColor=self.myColor[counter])
                    
                    elif dir == 1 and prevdir == 1: 
                        self.jointNames.append("Body"+str(row)+"."+str(col)+"."+str(ind-1)+"_Body"+str(row)+"."+str(col)+"."+str(ind))
                        pyrosim.Send_Joint( name =  self.jointNames[counter-1], parent= self.linkNames[counter-1], child = self.linkNames[counter], \
                            type = "revolute", position = [0, 0, -1*self.z[counter-1]], jointAxis=jointAxisStr)
                        pyrosim.Send_Cube(name=self.linkNames[counter], pos = [0, 0, -1*self.z[counter]/2], size = [self.x[counter], self.y[counter], self.z[counter]], materialColor=self.myColor[counter])

                    elif dir == 1 and prevdir == 2:
                        self.jointNames.append("Body"+str(row)+"."+str(col)+"."+str(ind-1)+"_Body"+str(row)+"."+str(col)+"."+str(ind))
                        pyrosim.Send_Joint( name =  self.jointNames[counter-1], parent= self.linkNames[counter-1], child = self.linkNames[counter], \
                            type = "revolute", position = [0, negMultY*self.y[counter-1]/2, -1*self.z[counter-1]/2], jointAxis=jointAxisStr)
                        pyrosim.Send_Cube(name=self.linkNames[counter], pos = [0, 0, -1*self.z[counter]/2], size = [self.x[counter], self.y[counter], self.z[counter]], materialColor=self.myColor[counter])
                    
                    elif dir == 2 and prevdir == 1: # change this one
                        self.jointNames.append("Body"+str(row)+"."+str(col)+"."+str(ind-1)+"_Body"+str(row)+"."+str(col)+"."+str(ind))
                        pyrosim.Send_Joint( name =  self.jointNames[counter-1], parent= self.linkNames[counter-1], child = self.linkNames[counter], \
                            type = "revolute", position = [0, negMultY*self.y[counter-1]/2, -1*self.z[counter-1]/2], jointAxis=jointAxisStr)
                        pyrosim.Send_Cube(name=self.linkNames[counter], pos = [0, negMultY*self.y[counter]/2, 0], size = [self.x[counter], self.y[counter], self.z[counter]], materialColor=self.myColor[counter])

                    elif dir == 2 and prevdir == 2:
                        self.jointNames.append("Body"+str(row)+"."+str(col)+"."+str(ind-1)+"_Body"+str(row)+"."+str(col)+"."+str(ind))
                        pyrosim.Send_Joint( name =  self.jointNames[counter-1], parent= self.linkNames[counter-1], child = self.linkNames[counter], \
                            type = "revolute", position = [0, negMultY*self.y[counter-1], 0], jointAxis=jointAxisStr)
                        pyrosim.Send_Cube(name=self.linkNames[counter], pos = [0, negMultY*self.y[counter]/2, 0], size = [self.x[counter], self.y[counter], self.z[counter]], materialColor=self.myColor[counter])


                    prevdir = dir

        print(self.linkNames)
        print(self.jointNames)
        # print(self.x)
        # print(self.y)
        # print(self.z)

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        # for joint in joint names create motor
        # have a counter variable for name ID
        # do sensors first

        print(self.randSensors)

        counterNeuron = 0
        for ind in self.randSensors:
            pyrosim.Send_Sensor_Neuron(name = counterNeuron , linkName = self.linkNames[ind])
            counterNeuron = counterNeuron + 1

        for ind in range(0, c.numMotorNeurons):
            pyrosim.Send_Motor_Neuron(name = counterNeuron , jointName = self.jointNames[ind])
            counterNeuron = counterNeuron + 1
        

        for currentRow in range(0, c.numSensorNeurons):
            for currentColumn in range(0,c.numMotorNeurons):
                # print("i = " + str(i) + ", j = " + str(j))
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn+c.numSensorNeurons , weight = self.weights[currentRow][currentColumn] )

        pyrosim.End()