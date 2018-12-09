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

class Node():
    # node class created for A* search, will reimplement rest of the code use Node class if there is time
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

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
        self.backingPaused = False
        self.backingWithGold = False
        pass

        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction(self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================

#        print()
#        print()
        self.visited.add((self.curX, self.curY))

        if(len(self.nextActions) != 0):
            action = self.nextActions.popleft()
#            print("backing = {}".format(self.backing))
#            print("current action = {}".format(action))
#            print("curDir: {}".format(self.curDir))
#            print("(x, y): ({}, {})".format(self.curX, self.curY))
#            print("visited: {}".format(self.visited))
#            print("previous Moves: {}".format(self.preMoves))
#            print("next Moves: {}".format(self.nextActions))
#            print("x-limit {}".format(self.x_bound))
#            print("y-limit {}".format(self.y_bound))
            return action
        
        if(self.curX == 0 and self.curY == 0 and not self.backingWithGold):
            up = (self.curX+1, self.curY)
            right = (self.curX, self.curY+1)
            if(up in self.visited and right in self.visited):
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
#            print("******** Gold Grabbed ****************")
            self.notHaveGold = False
            return Agent.Action.GRAB
        elif(not self.notHaveGold):
            if(self.curX == 0 and self.curY == 0):
                return Agent.Action.CLIMB
            self.backToStart()
            self.backingWithGold = True
        elif(breeze or stench):
            if(self.curX == 0 and self.curY == 0):
                return Agent.Action.CLIMB
            else:
                self.preMoves.pop()
                # head in opposite direction of facing
                if(self.curDir == 0):
                    self.moveSouth()
                elif(self.curDir == 1):
                    self.moveWest()
                elif(self.curDir == 2):
                    self.moveNorth()
                elif(self.curDir == 3):
                    self.moveEast()
        else:
            self.makeMove()
        
#        print("next Moves: {}".format(self.nextActions))
        action = self.nextActions.popleft()
#        print("backing = {}".format(self.backing))
#        print("current action = {}".format(action))
#        print("curDir: {}".format(self.curDir))
#        print("(x, y): ({}, {})".format(self.curX, self.curY))
#        print("next Moves: {}".format(self.nextActions))
#        print("visited: {}".format(self.visited))
#        print("previous Moves: {}".format(self.preMoves))
#        print("x-limit {}".format(self.x_bound))
#        print("y-limit {}".format(self.y_bound))
        return action
        
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================
    def backToStart(self):
        x = self.curX
        y = self.curY
        path = self.getPathToStart(x, y)
        for step in path:
#            print("curX: ", self.curX)
#            print("curY: ", self.curY)
#            print("step: ", step)
            xDiff = self.curX - step[0]
            yDiff = self.curY - step[1]
            if(xDiff == 1):
#                print("move West")
                self.moveWest()
            if(xDiff == -1):
#                print("move East")
                self.moveEast()
            if(yDiff == 1):
#                print("move South")
                self.moveSouth()
            if(yDiff == -1):
#                print("move North")
                self.moveNorth()
        self.nextActions.append(Agent.Action.CLIMB)
        
    # use A* search to find path to start
    def getPathToStart(self, x, y):
#        print()
#        print("Staring A* search")
        # Create start and end node
        startNode = Node(None, (x, y))
        startNode.g = startNode.h = startNode.f = 0
        endNode = Node(None, (0, 0))
        endNode.g = endNode.h = endNode.f = 0
    
        # Initialize both open and closed list
        openList = []
        closedList = []
    
        # Add the start node
        openList.append(startNode)
    
        # Loop until you find the end
#        print("entering while loop")
        while(len(openList) > 0):
            # Get the current node
            curNode = openList[0]
            curIndex = 0
#            print("entering for loop")
            for index, item in enumerate(openList):
                if item.f < curNode.f:
                    curNode = item
                    curIndex = index
#            print("exited for loop")
            # Pop current off open list, add to closed list
            openList.pop(curIndex)
            closedList.append(curNode)
            
#            print("curNode.pos: ", curNode.position)
#            print("endNode.pos: ", endNode.position)
    
            # Found the goal
            if(curNode.position == endNode.position):
                path = []
                current = curNode
                while current is not None:
                    path.append(current.position)
                    current = current.parent
#                print("path: ", path)
                return path[::-1] # Return reversed path
    
            # Generate neighbors
            neighbors = []
            #print("getting neighbors")
            for pos in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                # Get node position
                nodePos = (curNode.position[0] + pos[0], curNode.position[1] + pos[1])
    
                # Make sure within range
                if(not self.checkInBounds(nodePos[0], nodePos[1])):
                    continue
    
                # Make sure walkable terrain
                if(not self.checkVisited(nodePos[0], nodePos[1])):
                    continue
    
                # Create new node
                newNode = Node(curNode, nodePos)
    
                # Append
                neighbors.append(newNode)
                
            #print("neighbors: ", neighbors)
            # Loop through neighbors
            for neighbor in neighbors:
                skipThis = False
                
#                print("in neighbors")
                # Create the f, g, and h values
                neighbor.g = curNode.g + 1
                neighbor.h = (neighbor.position[0] - endNode.position[0]) + (neighbor.position[1] - endNode.position[1])
                neighbor.f = neighbor.g + neighbor.h
    
                # Neighbor is already in the open list
                for openNode in openList:
                    if(neighbor.position == openNode.position and neighbor.f > openNode.f):
                        skipThis = True
                        continue
                if(skipThis):
                    continue
                
                # Neighbor is on the closed list
                for closedNode in closedList:
                    if neighbor.position == closedNode.position:
                        skipThis = True
                        continue
                if(skipThis):
                    continue
                # Add the child to the open list
                openList.append(neighbor)
#            print("openList: ", openList)
    
    def checkVisited(self, x, y):
        cor = (x, y)
        if(not self.checkInBounds(x, y)):
#            print("{} not in bounds".format(cor))
            return True
#        print("{} in visited = {}".format(cor, cor in self.visited))
        return cor in self.visited
    
    def checkInBounds(self, x, y):
        if((x<0) or (x>self.x_bound-1) or (y<0) or (y>self.y_bound-1)):
            return False
        return True
    
    def makeMove(self):
#        print("makeing move")
        #always prioritize moving forward
        #facing North
        if(self.curDir == 0):
            if(not self.checkVisited(self.curX, self.curY+1)):
                self.moveNorth()
                self.preMoves.append('N')
            elif(not self.checkVisited(self.curX-1, self.curY)):
                self.moveWest()
                self.preMoves.append('W')
            elif(not self.checkVisited(self.curX+1, self.curY)):
                self.moveEast()
                self.preMoves.append('E')
            else:
                self.backTrack()
        #facing East
        elif(self.curDir == 1):
            if(not self.checkVisited(self.curX+1, self.curY)):
                self.moveEast()
                self.preMoves.append('E')
            elif(not self.checkVisited(self.curX, self.curY+1)):
                self.moveNorth()
                self.preMoves.append('N')
            elif(not self.checkVisited(self.curX, self.curY-1)):
                self.moveSouth()
                self.preMoves.append('S')
            else:
                self.backTrack()
        #facing South       
        elif(self.curDir == 2):
            if(not self.checkVisited(self.curX, self.curY-1)):
                self.moveSouth()
                self.preMoves.append('S')
            elif(not self.checkVisited(self.curX-1, self.curY)):
                self.moveWest()
                self.preMoves.append('W')
            elif(not self.checkVisited(self.curX+1, self.curY)):
                self.moveEast()
                self.preMoves.append('E')
            else:
                self.backTrack()
        #facing West
        elif(self.curDir == 3):
            if(not self.checkVisited(self.curX-1, self.curY)):
                self.moveWest()
                self.preMoves.append('W')
            elif(not self.checkVisited(self.curX, self.curY+1)):
                self.moveNorth()
                self.preMoves.append('N')
            elif(not self.checkVisited(self.curX, self.curY-1)):
                self.moveSouth()
                self.preMoves.append('S')
            else:
                self.backTrack()
        
    def moveNorth(self):
        if(self.curDir == 3):
            self.nextActions.append(Agent.Action.TURN_RIGHT)
            self.curDir = 0
        else:
            while(self.curDir > 0):
                self.nextActions.append(Agent.Action.TURN_LEFT)
                self.curDir -= 1
        self.nextActions.append(Agent.Action.FORWARD)
        self.curY += 1
    
    def moveEast(self):
        if(self.curDir == 0):
            self.nextActions.append(Agent.Action.TURN_RIGHT)
            self.curDir = 1
        else:
            while(self.curDir > 1):
                self.nextActions.append(Agent.Action.TURN_LEFT)
                self.curDir -= 1
        self.nextActions.append(Agent.Action.FORWARD)
        self.curX += 1
        
    def moveSouth(self):
        if(self.curDir == 3):
            self.nextActions.append(Agent.Action.TURN_LEFT)
            self.curDir = 2
        else:
            while(self.curDir < 2):
                self.nextActions.append(Agent.Action.TURN_RIGHT)
                self.curDir += 1
        self.nextActions.append(Agent.Action.FORWARD)
        self.curY -= 1
    
    def moveWest(self):
        if(self.curDir == 0):
            self.nextActions.append(Agent.Action.TURN_LEFT)
            self.curDir = 3
        else:
            while(self.curDir < 3):
                self.nextActions.append(Agent.Action.TURN_RIGHT)
                self.curDir += 1
        self.nextActions.append(Agent.Action.FORWARD)
        self.curX -= 1
    
    def backTrack(self):
        preMove = self.preMoves.pop()
        if(preMove == 'N'):
            self.moveSouth()
        elif(preMove == 'E'):
            self.moveWest()
        elif(preMove == 'S'):
            self.moveNorth()
        elif(preMove == 'W'):
            self.moveEast()

    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
