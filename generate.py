import pyrosim.pyrosim as pyrosim
import random

# def Generate_Body():
#     Create_World()
#     Create_Robot()

def Create_World():
    pyrosim.Start_SDF("world.sdf")
    length = 1
    width = 1
    height = 1
    x = -2
    y = -2
    z = height/2

    pyrosim.Send_Cube(name="Box", pos = [x,y,z], size = [length,width,height])

    pyrosim.End()

def Create_Robot():
    pyrosim.Start_URDF("body.urdf")

    length = 1
    width = 1
    height = 1

    x = 1.5
    y = 0
    z = 1.5
    pyrosim.Send_Cube(name="Torso", pos = [x,y,z], size = [length,width,height])

    x = -0.5
    y = -0.5
    z = -0.5
    pyrosim.Send_Cube(name="BackLeg", pos = [x,y,z], size = [length,width,height])

    x = 0.5
    y = -0.5
    z = -0.5
    pyrosim.Send_Cube(name="FrontLeg", pos = [x,y,z], size = [length,width,height])

    pyrosim.Send_Joint( name = "Torso_BackLeg", parent= "Torso", child = "BackLeg", \
        type = "revolute", position = [1,0.5,1])

    pyrosim.Send_Joint( name = "Torso_FrontLeg", parent= "Torso", child = "FrontLeg", \
        type = "revolute", position = [2,0.5,1])

    pyrosim.End()

def Generate_Brain():
    pyrosim.Start_NeuralNetwork("brain.nndf")
    
    pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
    pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
    pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
    pyrosim.Send_Motor_Neuron(name = 3 , jointName = "Torso_BackLeg")
    pyrosim.Send_Motor_Neuron(name = 4 , jointName = "Torso_FrontLeg")

    # pyrosim.Send_Synapse( sourceNeuronName = 0 , targetNeuronName = 3 , weight = 0.8 )
    # pyrosim.Send_Synapse( sourceNeuronName = 1 , targetNeuronName = 3 , weight = -0.8 )
    # pyrosim.Send_Synapse( sourceNeuronName = 0 , targetNeuronName = 4 , weight = 0.8 )
    # pyrosim.Send_Synapse( sourceNeuronName = 2 , targetNeuronName = 4 , weight = 0.8 )

    for i in range(2+1):
        for j in range(3,4+1):
            # print("i = " + str(i) + ", j = " + str(j))
            pyrosim.Send_Synapse( sourceNeuronName = i , targetNeuronName = j , weight = 2*random.random()-1 )

    pyrosim.End()



Create_World()
Create_Robot()

Generate_Brain()

