
from random import randint


def ActRobot(robot):
        if robot.GetVirus() > 1000:
                robot.DeployVirus(200)
        
        return randint(1,4)


def ActBase(base):
    
    #Add your code here
    
    
    if base.GetElixir() > 500:
            base.create_robot('')

    return

    

