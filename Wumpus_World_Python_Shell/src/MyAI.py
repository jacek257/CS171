# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent
from collections import deque

class MyAI ( Agent ):

    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        self.curX = 0
        self.curY = 0
        self.preMoves = []
        self.visited = set()
        self.heardScream = False
        #0 = North, 1 = East, 2 = South, 3 = West
        self.curDir = 1
        self.nextActions = deque()
        self.notHaveGold = True
        self.x_bound = 7
        self.y_bound = 7
        self.backing = False
        self.turnArounds = 0
        pass
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        
        cordinate = str(self.curX) + ', ' + str(self.curY)
        self.visited.add(cordinate)
        
        if(len(self.nextActions) != 0):
            action = self.nextActions.popleft()
            print("backing = {}".format(self.backing))
            print("current action = {}".format(action))
            print("curDir: {}".format(self.curDir))
            if(action == Agent.Action.FORWARD):
                self.moveForward()
            print(self.curX, self.curY)
            print("visited: {}".format(self.visited))
            print("previous Moves: {}".format(self.preMoves))
            print("next Moves: {}".format(self.nextActions))
            return action
        
        if(self.curX == 0 and self.curY == 0):
            cordinate1 = str(self.curX+1) + ', ' + str(self.curY)
            cordinate2 = str(self.curX) + ', ' + str(self.curY+1)
            if(cordinate1 in self.visited and cordinate2 in self.visited):
                return Agent.Action.CLIMB

        if(scream):
            self.heardScream = True
            
        if(self.heardScream):
            stench = False
            
        if(bump):
            if(self.curDir == 1):
                self.x_bound = self.curX
                self.curX -= 1
            elif(self.curDir == 0):
                self.y_bound = self.curY
                self.curY -= 1
            self.preMoves.pop()
            self.makeMove()
        elif(glitter and self.notHaveGold):
            print("******** Gold Grabbed ****************")
            self.notHaveGold = False
            self.preMoves.append("grab")
            return Agent.Action.GRAB
        elif(not self.notHaveGold):
            if(self.curX == 0 and self.curY == 0):
                return Agent.Action.CLIMB
            self.backtrack()
        elif(breeze or stench):
            if(self.curX == 0 and self.curY == 0):
                return Agent.Action.CLIMB
            elif(self.backing):
                self.backtrack()
            else:
                self.turnAround()
                self.preMoves.append("left")
                self.preMoves.append("left")
                self.nextActions.append(Agent.Action.FORWARD)
                self.preMoves.append("forward")
        else:
            self.makeMove()
        

        
        
        action = self.nextActions.popleft()
        print("backing = {}".format(self.backing))
        print("current action = {}".format(action))
        print("curDir: {}".format(self.curDir))
        if(action == Agent.Action.FORWARD):
            self.moveForward()
        print(self.curX, self.curY)
        print("visited: {}".format(self.visited))
        print("previous Moves: {}".format(self.preMoves))
        print("next Moves: {}".format(self.nextActions))
        return action
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================

    def turnAround(self):
        self.turnArounds += 1
        self.curDir -= 2
        self.keepDirBound()
        self.nextActions.append(Agent.Action.TURN_LEFT)
        self.nextActions.append(Agent.Action.TURN_LEFT)
        pass
    
    def moveForward(self):
        if(self.curDir == 0):
            self.curY += 1
        elif(self.curDir == 1):
            self.curX += 1
        if(self.curDir == 2):
            self.curY -= 1
        if(self.curDir == 3):
            self.curX -= 1
    
    def checkVisited(self, x, y):
        if(not self.checkInBounds(x, y)):
                return True
        cor = str(x) + ', ' + str(y)
        print("{} in visited = {}".format(cor, cor in self.visited))
        return cor in self.visited
    
    def checkInBounds(self, x, y):
        if((x<0) or (x>self.x_bound) or (y<0) or (y>self.y_bound)):
            return False
        return True
    
    def keepDirBound(self):
        if(self.curDir > 3):
            self.curDir -= 4
        if(self.curDir < 0):
            self.curDir += 4
    
    def backtrack(self):
        self.backing = True
        preMove = self.preMoves.pop()
        if(preMove == "grab"):
            self.turnAround()
        elif(preMove == "forward"):
            self.nextActions.append(Agent.Action.FORWARD)
        elif(self.turnArounds % 2):
            if(preMove == "left"):
                self.turnRight()
            elif(preMove == "right"):
                self.turnLeft()
        else:
            if(preMove == "left"):
                self.turnLeft()
            elif(preMove == "right"):
                self.turnRight()
        
    def turnRight(self):
        self.nextActions.append(Agent.Action.TURN_RIGHT)
        self.curDir += 1
        self.keepDirBound()
        
    def moveRight(self):
        self.turnRight()
        self.preMoves.append("right")
        self.nextActions.append(Agent.Action.FORWARD)
        self.preMoves.append("forward")
        
    
    def turnLeft(self):
        self.nextActions.append(Agent.Action.TURN_LEFT)
        self.curDir -= 1
        self.keepDirBound()
        
    def moveLeft(self):
        self.turnLeft()
        self.preMoves.append("left")
        self.nextActions.append(Agent.Action.FORWARD)
        self.preMoves.append("forward")
    
    def makeMove(self):
        if(self.curDir == 0):
            if(not self.checkVisited(self.curX, self.curY+1)):
                self.backing = False
                self.nextActions.append(Agent.Action.FORWARD)
                self.preMoves.append("forward")
            elif(not self.checkVisited(self.curX+1, self.curY)):
                self.backing = False
                self.moveRight()
            elif(not self.checkVisited(self.curX-1, self.curY)):
                self.backing = False
                self.moveLeft()
            else:
                if(not self.backing):
                    self.turnAround()
                self.backtrack()
        elif(self.curDir == 1):
            if(not self.checkVisited(self.curX+1, self.curY)):
                self.backing = False
                self.nextActions.append(Agent.Action.FORWARD)
                self.preMoves.append("forward")
            elif(not self.checkVisited(self.curX, self.curY-1)):
                self.backing = False
                self.moveRight()
            elif(not self.checkVisited(self.curX, self.curY+1)):
                self.backing = False
                self.moveLeft()
            else:
                if(not self.backing):
                    self.turnAround()
                self.backtrack()
        elif(self.curDir == 2):
            if(not self.checkVisited(self.curX, self.curY-1)):
                self.backing = False
                self.nextActions.append(Agent.Action.FORWARD)
                self.preMoves.append("forward")
            elif(not self.checkVisited(self.curX-1, self.curY)):
                self.backing = False
                self.moveRight()
            elif(not self.checkVisited(self.curX+1, self.curY)):
                self.backing = False
                self.moveLeft()
            else:
                if(not self.backing):
                    self.turnAround()
                self.backtrack()
        elif(self.curDir == 3):
            if(not self.checkVisited(self.curX-1, self.curY)):
                self.backing = False
                self.nextActions.append(Agent.Action.FORWARD)
                self.preMoves.append("forward")
            elif(not self.checkVisited(self.curX, self.curY+1)):
                self.backing = False
                self.moveRight()
            elif(not self.checkVisited(self.curX, self.curY-1)):
                self.backing = False
                self.moveLeft()
            else:
                if(not self.backing):
                    self.turnAround()
                self.backtrack()
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
