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
        self.gotGold = False
        self.nextTurn = "left"
        self.backs = 0
        self.x_bound = 7
        self.y_bound = 7
        pass
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        if(len(self.nextActions) != 0):        
            action = self.nextActions.popleft()
            if(action == "forward"):
                self.moveForward()
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
        
        if(breeze or stench):
            if(self.curX == 0 and self.curY == 0):
                return Agent.Action.CLIMB
            else:
                cordinate = str(self.curX) + ', ' + str(self.curY)
                self.visited.add(cordinate)
                self.turnAround()
                self.preMoves.pop()
                self.nextActions.append(Agent.Action.FORWARD)
#                self.nextTurn = "right"
                self.back += 1
        elif(glitter and not self.gotGold):
            self.preMoves.append("grab")
            return Agent.Action.GRAB
        elif(self.gotGold):
            if(self.curX == 0 and self.curY == 0):
                return Agent.Action.CLIMB
            preMove = self.preMoves.pop()
            if(preMove == "grab"):
                self.turnAround()
            elif(preMove == "forward"):
                self.nextActions.append(Agent.Action.FORWARD)
            elif(preMove == "left"):
                self.nextActions.append(Agent.Action.TURN_RIGHT)
            elif(preMove == "right"):
                self.nextActions.append(Agent.Action.TURN_LEFT)
        else:
            self.makeMove()
        

            
        
        
        action = self.nextActions.popleft()
        if(action == "forward")
            self.moveForward()
        return action
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================

    def turnAround(self):
        self.curDir += 2
        if(self.curDir > 3):
            self.curDir -= 4
        self.nextActions.append(Agent.Action.TURN_LEFT)
        self.nextActions.append(Agent.Action.TURN_LEFT)
        pass
    
    def moveForward(self):
        if(self.curDir == 0):
            self.curX += 1
        elif(self.curDir == 1):
            self.curY += 1
        if(self.curDir == 2):
            self.curX -= 1
        if(self.curDir == 3):
            self.curY -= 1
    
    def checkVisited(self, x, y):
        if(not self.checkInBounds(x, y)):
                return False
        cor = str(x) + ',' + str(y)
        return cor in self.visited
    
    def checkInBounds(self, x, y):
        if((x<0) or (x>=7) or (y<0) or (y>=7)):
            return False
        return True
    
    def makeMove():
        if(self.curDir == 0):
            if(not self.checkVisited(self.curX, self.curY+1)):
                self.nextActions.append(Agent.Action.FORWARD)
                self.preMoves.append("forward")
            elif(not self.checkVisited(self.curX+1, self.curY)):
                self.nextActions.append(Agent.Action.TURN_RIGHT)
                self.preMoves.append("right")
                self.nextActions.append(Agent.Action.FORWARD)
                self.preMoves.append("forward")
            elif(not self.checkVisited(self.curX-1, self.curY)):
                self.nextActions.append(Agent.Action.TURN_LEFT)
                self.preMoves.append("left")
                self.nextActions.append(Agent.Action.FORWARD)
                self.preMoves.append("forward")
        elif(self.curDir == 1):
            if(not self.checkVisited(self.curX+1, self.curY)):
                self.nextActions.append(Agent.Action.FORWARD)
                self.preMoves.append("forward")
            elif(not self.checkVisited(self.curX, self.curY-1)):
                self.nextActions.append(Agent.Action.TURN_RIGHT)
                self.preMoves.append("right")
                self.nextActions.append(Agent.Action.FORWARD)
                self.preMoves.append("forward")
            elif(not self.checkVisited(self.curX, self.curY+1)):
                self.nextActions.append(Agent.Action.TURN_LEFT)
                self.preMoves.append("left")
                self.nextActions.append(Agent.Action.FORWARD)
                self.preMoves.append("forward")
        elif(self.curDir == 2):
            if(not self.checkVisited(self.curX, self.curY-1)):
                self.nextActions.append(Agent.Action.FORWARD)
                self.preMoves.append("forward")
            elif(not self.checkVisited(self.curX-1, self.curY)):
                self.nextActions.append(Agent.Action.TURN_RIGHT)
                self.preMoves.append("right")
                self.nextActions.append(Agent.Action.FORWARD)
                self.preMoves.append("forward")
            elif(not self.checkVisited(self.curX+1, self.curY)):
                self.nextActions.append(Agent.Action.TURN_LEFT)
                self.preMoves.append("left")
                self.nextActions.append(Agent.Action.FORWARD)
                self.preMoves.append("forward")
        elif(self.curDir == 3):
            if(not self.checkVisited(self.curX-1, self.curY)):
                self.nextActions.append(Agent.Action.FORWARD)
                self.preMoves.append("forward")
            elif(not self.checkVisited(self.curX, self.curY+1)):
                self.nextActions.append(Agent.Action.TURN_RIGHT)
                self.preMoves.append("right")
                self.nextActions.append(Agent.Action.FORWARD)
                self.preMoves.append("forward")
            elif(not self.checkVisited(self.curX, self.curY-1)):
                self.nextActions.append(Agent.Action.TURN_LEFT)
                self.preMoves.append("left")
                self.nextActions.append(Agent.Action.FORWARD)
                self.preMoves.append("forward")
        
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================