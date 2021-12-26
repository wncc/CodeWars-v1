import pygame
from robot import Robot

class Base():
    def __init__(self, screen, x, y, type, __robot_list, __robot_map, game):
        self.screen = screen
        self.type = type
        self.__robot_map = __robot_map
        self.__robot_list = __robot_list
        self.__myGame = game
        self.__SelfElixir = 2000
        self.__TotalTeamElixir = 2000
        self.__TotalVirus = 0
        self.__MovingAverage = 2000
        self.__Signal = ''
        
        if type == "red":
            self.image = pygame.image.load("assets/redbase.png")
        else:
            self.image = pygame.image.load("assets/bluebase.png")
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def actVirus(self, v, pos):
        g = self.__myGame
        if pos[0] < 0 or pos[0] >= g._Game__dim[0]:
            return
        if pos[1] < 0 or pos[1] >= g._Game__dim[1]:
            return
        if self.__robot_map[pos[1]][pos[0]]==0:
            g._Game__resources[pos[1]][pos[0]]-= v
            return
        if self.__robot_map[pos[1]][pos[0]]==1 and self ==g._Game__redbase:
            self.__TotalVirus += v
            return
        if self.__robot_map[pos[1]][pos[0]]==1 and self==g._Game__bluebase:
            g._Game__redbase.VirusOnRobot(pos, v)
            return
        if self.__robot_map[pos[1]][pos[0]]==2 and self==g._Game__bluebase:
            self.__TotalVirus += v
            return
        if self.__robot_map[pos[1]][pos[0]]==2 and self==g._Game__redbase:
            g._Game__bluebase.VirusOnRobot(pos, v)
            return
        if self.__robot_map[pos[1]][pos[0]]==3 and self==g._Game__bluebase:
            g._Game__redbase.__SelfElixir -= v
            g._Game__redbase.__TotalTeamElixir -= v
            return
        if self.__robot_map[pos[1]][pos[0]]==3 and self==g._Game__redbase:
            self.__TotalVirus += v
            return
        if self.__robot_map[pos[1]][pos[0]]==4 and self==g._Game__redbase:
            g._Game__bluebase.__SelfElixir -= v
            g._Game__bluebase.__TotalTeamElixir -= v
            return
        if self.__robot_map[pos[1]][pos[0]]==4 and self==g._Game__bluebase:
            self.__TotalVirus += v
            return

    def GetListOfSignals(self):
        res = []
        for x in self.__robot_list:
            res.append(x._Robot__Signal)
        return res

    def addResource(self, v):
        if v < 0:
            self.__TotalVirus -= v
        else:
            self.__SelfElixir += v
            self.__TotalTeamElixir += v
        
    def VirusOnRobot(self, pos,virus):
        robots = self.__myGame._Game__PositionToRobot[pos]
        if len(robots)==0:
            self.__myGame._Game__resources[pos[1]][pos[0]]-= virus
            return
        virus /= len(robots)
        delete = []
        for robot in robots:
            if robot._Robot__selfElixir <= virus:
                e = virus - robot._Robot__selfElixir
                self.__TotalTeamElixir -= robot._Robot__selfElixir
                delete.append(robot)
                robot.kill()
                self.__robot_map[pos[1]][pos[0]] = 0
                self.__myGame._Game__resources[pos[1]][pos[0]]+=e
            else:
                self.__TotalTeamElixir -= virus
                robot._Robot__selfElixir-=virus
        for d in delete:
            del self.__myGame._Game__PositionToRobot[pos][d]
    def create_robot(self, signal):
        if self.__SelfElixir >= 50:
            str = 'wncc'
            if type(signal)!=type(str) or len(signal) > 20:
                signal = ''
            self.__SelfElixir -= 50
            #self.GlobalRobotCount += 1
            robo = Robot(self.screen, self.rect.x, self.rect.y, self.type, signal, self)
            self.__robot_list.add(robo)
            if (self.rect.x//20, self.rect.y//20) in self.__myGame._Game__PositionToRobot:
                self.__myGame._Game__PositionToRobot[(self.rect.x//20, self.rect.y//20)][robo] = True
            else:
                self.__myGame._Game__PositionToRobot[(self.rect.x//20, self.rect.y//20)] = {}
                self.__myGame._Game__PositionToRobot[(self.rect.x//20, self.rect.y//20)][robo] = True
            if self.type == 'red':
                self.__robot_map[self.rect.y//20][self.rect.x//20] = 3
            else:
                self.__robot_map[self.rect.y//20][self.rect.x//20] = 4

    def investigate_up(self):
        if self.rect.y == 0:
            return "wall"
        elif self.__robot_map[self.rect.y//20  - 1][self.rect.x//20] == 1:
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__robot_map[self.rect.y//20  - 1][self.rect.x//20] == 3:
            if self.type == "red":
                return "friend-base"
            else:
                return "enemy-base"
        elif self.__robot_map[self.rect.y//20  - 1][self.rect.x//20] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__robot_map[self.rect.y//20  - 1][self.rect.x//20] == 4:
            if self.type == "red":
                return "enemy-base"
            else:
                return "friend-base"
        else:
            return "blank"
    

    def investigate_down(self):
        if self.rect.y == 780:
            return "wall"
        elif self.__robot_map[self.rect.y//20  + 1][self.rect.x//20] == 1 :
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__robot_map[self.rect.y//20  + 1][self.rect.x//20] == 3:
            if self.type == "red":
                return "friend-base"
            else:
                return "enemy-base"
        elif self.__robot_map[self.rect.y//20  + 1][self.rect.x//20] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__robot_map[self.rect.y//20  + 1][self.rect.x//20] == 4:
            if self.type == "red":
                return "enemy-base"
            else:
                return "friend-base"
        else:
            return "blank"
    
    def investigate_left(self):
        if self.rect.x == 0:
            return "wall"
        elif self.__robot_map[self.rect.y//20][self.rect.x//20 - 1] == 1 :
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__robot_map[self.rect.y//20][self.rect.x//20 - 1] == 3:
            if self.type == "red":
                return "friend-base"
            else:
                return "enemy-base"
        elif self.__robot_map[self.rect.y//20][self.rect.x//20 - 1] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__robot_map[self.rect.y//20][self.rect.x//20 - 1] == 4:
            if self.type == "red":
                return "enemy-base"
            else:
                return "friend-base"
        else:
            return "blank"

    
    def investigate_right(self):
        if self.rect.x == 780:
            return "wall"
        elif self.__robot_map[self.rect.y//20][self.rect.x//20 + 1] == 1 :
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__robot_map[self.rect.y//20][self.rect.x//20 + 1] == 3:
            if self.type == "red":
                return "friend-base"
            else:
                return "enemy-base"
        elif self.__robot_map[self.rect.y//20][self.rect.x//20 + 1] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__robot_map[self.rect.y//20][self.rect.x//20 + 1] == 4:
            if self.type == "red":
                return "enemy-base"
            else:
                return "friend-base"
        else:
            return "blank"

    
    def investigate_ne(self):
        if self.rect.x == 780 or self.rect.y == 0:
            return "wall"
        elif self.__robot_map[self.rect.y//20 - 1][self.rect.x//20 + 1] == 1 :
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__robot_map[self.rect.y//20 - 1][self.rect.x//20 + 1] == 3:
            if self.type == "red":
                return "friend-base"
            else:
                return "enemy-base"
        elif self.__robot_map[self.rect.y//20 - 1][self.rect.x//20 + 1] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__robot_map[self.rect.y//20 - 1][self.rect.x//20 + 1] == 4:
            if self.type == "red":
                return "enemy-base"
            else:
                return "friend-base"
        else:
            return "blank"

    def investigate_nw(self):
        if self.rect.x == 0 or self.rect.y == 0:
            return "wall"
        elif self.__robot_map[self.rect.y//20 - 1][self.rect.x//20 - 1] == 1 :
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__robot_map[self.rect.y//20 - 1][self.rect.x//20 - 1] == 3:
            if self.type == "red":
                return "friend-base"
            else:
                return "enemy-base"
        elif self.__robot_map[self.rect.y//20 - 1][self.rect.x//20 - 1] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__robot_map[self.rect.y//20 - 1][self.rect.x//20 - 1] == 4:
            if self.type == "red":
                return "enemy-base"
            else:
                return "friend-base"
        else:
            return "blank"

    def investigate_se(self):
        if self.rect.x == 780 or self.rect.y == 780:
            return "wall"
        elif self.__robot_map[self.rect.y//20 + 1][self.rect.x//20 + 1] == 1 :
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__robot_map[self.rect.y//20 + 1][self.rect.x//20 + 1] == 3:
            if self.type == "red":
                return "friend-base"
            else:
                return "enemy-base"
        elif self.__robot_map[self.rect.y//20 + 1][self.rect.x//20 + 1] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__robot_map[self.rect.y//20 + 1][self.rect.x//20 + 1] == 4:
            if self.type == "red":
                return "enemy-base"
            else:
                return "friend-base"
        else:
            return "blank"

    def investigate_sw(self):
        if self.rect.x == 0 or self.rect.y==780:
            return "wall"
        elif self.__robot_map[self.rect.y//20 + 1][self.rect.x//20 - 1] == 1 :
            if self.type == "red":
                return "friend"
            else:
                return "enemy"
        elif self.__robot_map[self.rect.y//20 + 1][self.rect.x//20 - 1] == 3:
            if self.type == "red":
                return "friend-base"
            else:
                return "enemy-base"
        elif self.__robot_map[self.rect.y//20 + 1][self.rect.x//20 - 1] == 2:
            if self.type == "red":
                return "enemy"
            else:
                return "friend"
        elif self.__robot_map[self.rect.y//20 + 1][self.rect.x//20 - 1] == 4:
            if self.type == "red":
                return "enemy-base"
            else:
                return "friend-base"
        else:
            return "blank"

    
    
    def GetYourSignal(self):
        return self.__Signal
    
    def SetYourSignal(self, s):
        str = 'wncc'
        if type(s)!=type(str) or len(s) > 20:
            return
        self.__Signal = s
    def GetTotalElixir(self):
        return self.__TotalTeamElixir
    def GetElixir(self):
        return self.__SelfElixir
    def GetVirus(self):
        return self.__TotalVirus
    
    def GetPosition(self):
        return (self.rect.x//20,self.rect.y//20)
    
    def GetDimensionX(self):
        return self.__myGame._Game__dim[0]

    def GetDimensionY(self):
        return self.__myGame._Game__dim[1]

    def DeployVirus(self, v):
        if v > self.__TotalVirus or v <= 0:
            return
        self.__TotalVirus -= v
        self.actVirus(v/8,(self.rect.x-1,self.rect.y))
        self.actVirus(v/8,(self.rect.x+1,self.rect.y))
        self.actVirus(v/8,(self.rect.x-1,self.rect.y+1))
        self.actVirus(v/8,(self.rect.x-1,self.rect.y-1))
        self.actVirus(v/8,(self.rect.x+1,self.rect.y+1))
        self.actVirus(v/8,(self.rect.x+1,self.rect.y-1))
        self.actVirus(v/8,(self.rect.x,self.rect.y+1))
        self.actVirus(v/8,(self.rect.x,self.rect.y-1))

    def blitme(self):
        self.screen.blit(self.image, self.rect)
