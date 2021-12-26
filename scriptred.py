from random import randint

def get_bluebase_loc(base):
        x,y=base.GetPosition()
        canvas_x=base.GetDimensionX()
        canvas_y=base.GetDimensionY()
        bluebase_y=y
        bluebase_x=canvas_x-x
        return (bluebase_x,bluebase_y)


def robot_investigate(robot):
        up=robot.investigate_up()
        down=robot.investigate_down()
        left=robot.investigate_left()
        right=robot.investigate_right()
        nw=robot.investigate_nw()
        ne=robot.investigate_ne()
        sw=robot.investigate_sw()
        se=robot.investigate_se()
        return (up,down,left,right,nw,ne,sw,se)

def ActRobot(robot):
        investigate_tuple=robot_investigate(robot)
        if 'enemy-base' in investigate_tuple:
                v=robot.GetVirus()
                robot.DeployVirus(v)
                

        robot_x,robot_y=robot.GetPosition()
        initial_signal=robot.GetInitialSignal()
        initial_signal_len=len(initial_signal)
        if(initial_signal[0]=="r"):
                if(robot_x<int(initial_signal[1:])):
                        return 2
                else:
                        return 0
        elif(initial_signal[0]=="l"):
                if(robot_x>int(initial_signal[1:])):
                        return 4
                else:
                        return 0
        else:
                return randint(1,4)
        
        
        


def ActBase(base):
    '''
    Add your code here
    
    '''
    list_of_signals=base.GetListOfSignals()
    no_of_robots=len(list_of_signals)
    elixir=base.GetElixir()
    

    
    
    base_x,base_y=base.GetPosition()
    send_signal="m"
    bluebase_x,bluebase_y=get_bluebase_loc(base)
    if base_x>(int(bluebase_x)/2):
        send_signal="l"
    else:
        send_signal="r"

    if(elixir>1000):
            base.create_robot("m")
    elif base.GetElixir()>100:
            base.create_robot(send_signal+str(bluebase_x))

    return