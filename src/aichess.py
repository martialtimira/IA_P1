#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 11:22:03 2022

@author: ignasi
"""

import chess
import numpy as np
import sys

from itertools import permutations


class Aichess():
    """
    A class to represent the game of chess.

    ...

    Attributes:
    -----------
    chess : Chess
        represents the chess game

    Methods:
    --------
    startGame(pos:stup) -> None
        Promotes a pawn that has reached the other side to another, or the same, piece

    """

    def __init__(self, TA, myinit=True):

        if myinit:
            self.chess = chess.Chess(TA, True)
        else:
            self.chess = chess.Chess([], False)

        self.listNextStates = []
        self.listVisitedStates = []
        self.pathToTarget = []
        self.currentStateW = self.chess.boardSim.currentStateW;
        self.depthMax = 8;
        self.checkMate = False

    def getCurrentState(self):

        return self.myCurrentStateW

    def getListNextStatesW(self, myState):

        self.chess.boardSim.getListNextStatesW(myState)
        self.listNextStates = self.chess.boardSim.listNextStates.copy()

        return self.listNextStates

    def isSameState(self, a, b):

        isSameState1 = True
        # a and b are lists
        for k in range(len(a)):

            if a[k] not in b:
                isSameState1 = False

        isSameState2 = True
        # a and b are lists
        for k in range(len(b)):

            if b[k] not in a:
                isSameState2 = False

        isSameState = isSameState1 and isSameState2
        return isSameState

    def isVisited(self, mystate):

        if (len(self.listVisitedStates) > 0):
            perm_state = list(permutations(mystate))

            isVisited = False
            for j in range(len(perm_state)):

                for k in range(len(self.listVisitedStates)):

                    if self.isSameState(list(perm_state[j]), self.listVisitedStates[k]):
                        isVisited = True

            return isVisited
        else:
            return False

    def isCheckMate(self, mystate):
        checkMateStates = [[[0, 0, 2], [2, 4, 6]], [[0, 1, 2], [2, 4, 6]], [[0, 2, 2], [2, 4, 6]],
                           [[0, 6, 2], [2, 4, 6]], [[0, 7, 2], [2, 4, 6]]];
        perm_state = list(permutations(mystate))

        for j in range(len(perm_state)):
            for k in range(len(checkMateStates)):

                if self.isSameState(list(perm_state[j]), checkMateStates[k]):
                    self.checkMate = True

            return self.checkMate

    def getMoveFromStates(self, currentState, nextState):
        """
        Returns the "start" and "to" points of a move from its 2 states
        Args:
            currentState: Current State of the board
            nextState: State of the Board after the move

        Returns: Starting coordinates, To coordinates, piece ID

        """
        start = None
        to = None
        piece = None

        for element in currentState:
            if element not in nextState:
                start = (element[0], element[1])
                piece = element[2]
        for element in nextState:
            if element not in currentState:
                to = (element[0], element[1])


        return start, to, piece

    def DepthFirstSearch(self, currentState, depth):
        """
        Check mate from currentStateW
        """
        # your code here
        if self.isCheckMate(currentState):      #Check if current state is check mate
            return True
        if depth > self.depthMax:               #Check if current depth is bigger than max depth
            return False

        self.listVisitedStates.append(currentState)         #Add current State to visited states
        for state in self.getListNextStatesW(currentState):     #Iterate over all the possible next states
            if not self.isVisited(state):                       #if the state currently iterating over, has not been visited
                start, to, piece = self.getMoveFromStates(currentState, state)  #Get move coordinates to get to this state
                self.pathToTarget.append((start, to, piece))                    #add move to the path
                self.chess.moveSim(start, to)                                   #execute the move to get to this state

                if self.DepthFirstSearch(state, depth + 1):                     #Run DFS recursively, if it finds check mate, return True
                    return True

                self.chess.moveSim(to, start)                                   #Undo the previous move
                self.pathToTarget.remove((start, to, piece))                    #Remove the move from the path

        return False

    def BreadthFirstSearch(self, currentState, depth):
        """
        Check mate from currentStateW

        """
        moveQueue = []

        # your code
        print("STARTING: ", self.listVisitedStates)
        self.listVisitedStates.append(currentState)
        for state in self.getListNextStatesW(currentState):    #get initial set of moves in the queue
            if not self.isVisited(state):
                self.listVisitedStates.append(state)
                start, to, piece = self.getMoveFromStates(currentState, state)
                moveQueue.append([[start, to, piece]])

        while moveQueue:                                                #while there are still move sequences to explore
            currentMove = moveQueue.pop(0)                        #get the sequence of moves
            for move in currentMove:
                self.chess.moveSim(move[0], move[1])

            for state in self.getListNextStatesW(self.chess.boardSim.currentStateW):

                if self.isCheckMate(state):  # check if resulting state is CheckMate
                    start, to, piece = self.getMoveFromStates(self.chess.boardSim.currentStateW, state)
                    new_moveSequence = list(currentMove)
                    new_move = [start, to, piece]
                    new_moveSequence.append(new_move)
                    self.chess.moveSim(start, to)
                    self.pathToTarget = new_moveSequence
                    return True
                if not self.isVisited(state):
                    start, to, piece = self.getMoveFromStates(self.chess.boardSim.currentStateW, state)
                    new_moveSequence = list(currentMove)
                    newMove = [start, to, piece]
                    new_moveSequence.append(newMove)
                    moveQueue.append(new_moveSequence)
                    self.listVisitedStates.append(state)

            for i in range(len(currentMove)-1, -1, -1):
                start = currentMove[i][1]
                to = currentMove[i][0]
                self.chess.moveSim(start,to)
                if depth > 10000:
                    return False
            depth += 1
        return False

    def BestFirstSearch(self, currentState):
        #Your Code here
        return False

    def AStarSearch(self, currentState):
        # Your Code here
        priorityQueue = []

        print("STARTING: ", self.listVisitedStates)
        self.listVisitedStates.append(currentState)
        for state in self.getListNextStatesW(currentState):  # get initial set of moves in the queue
            if not self.isVisited(state):
                self.listVisitedStates.append(state)
                start, to, piece = self.getMoveFromStates(currentState, state)
                fN = self.heuristicDistance(to, piece, 0)
                priorityQueue.append((fN, [[start, to, piece]]))

        while priorityQueue:  # while there are still move sequences to explore
            priorityQueue.sort(reverse=True)
            currentMove = priorityQueue.pop()  # get the sequence of moves
            print("Current move: ", currentMove)
            for move in currentMove[1]:
                self.chess.moveSim(move[0], move[1])

            for state in self.getListNextStatesW(self.chess.boardSim.currentStateW):

                if self.isCheckMate(state):  # check if resulting state is CheckMate
                    start, to, piece = self.getMoveFromStates(self.chess.boardSim.currentStateW, state)
                    new_moveSequence = list(currentMove)
                    new_move = [start, to, piece]
                    new_moveSequence.append(new_move)
                    self.chess.moveSim(start, to)
                    self.pathToTarget = new_moveSequence
                    return True

                if not self.isVisited(state):
                    start, to, piece = self.getMoveFromStates(self.chess.boardSim.currentStateW, state)
                    fN = self.heuristicDistance(to, piece, currentMove[0])
                    new_moveSequence = list(currentMove[1])
                    newMove = [start, to, piece]
                    new_moveSequence.append(newMove)
                    priorityQueue.append((fN, new_moveSequence))
                    self.listVisitedStates.append(state)

            for i in range(len(currentMove[1]) - 1, -1, -1):
                start = currentMove[1][i][1]
                to = currentMove[1][i][0]
                self.chess.moveSim(start, to)


        return False



    def heuristicDistance(self, to, piece, gN):
        # Calcular distància manhattan
        hN = 0
        if piece == 2: # Torre
            hN += to[0]
            if to[1] == 4:
                hN += 1
        if piece == 6:
            hN += np.abs(to[0] - 2) + np.abs(to[1] - 4)

        return gN + hN



def translate(s):
    """
    Translates traditional board coordinates of chess into list indices
    """

    try:
        row = int(s[0])
        col = s[1]
        if row < 1 or row > 8:
            print(s[0] + "is not in the range from 1 - 8")
            return None
        if col < 'a' or col > 'h':
            print(s[1] + "is not in the range from a - h")
            return None
        dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        return (8 - row, dict[col])
    except:
        print(s + "is not in the format '[number][letter]'")
        return None


if __name__ == "__main__":
    #   if len(sys.argv) < 2:
    #       sys.exit(usage())

    # intiialize board
    TA = np.zeros((8, 8))
    TA[7][0] = 2
    TA[7][4] = 6
    TA[0][4] = 12

    # initialise board
    print("stating AI chess... ")
    aichess = Aichess(TA, True)
    currentState = aichess.chess.board.currentStateW.copy()

    print("printing board")
    aichess.chess.boardSim.print_board()

    # get list of next states for current state
    print("current State", currentState)

    # it uses board to get them... careful 
    aichess.getListNextStatesW(currentState)
    print("list next states ", aichess.listNextStates)

    testS, testT, testP = aichess.getMoveFromStates(currentState,
                                                    aichess.getListNextStatesW(currentState)[1])
    # starting from current state find the end state (check mate) - recursive function
    # find the shortest path, initial depth 0
    depth = 0
    #aichess.DepthFirstSearch(currentState, depth)
    #print("DFS End")
    #print(aichess.BreadthFirstSearch(currentState, depth))
    #print("BFS End")

    print(aichess.AStarSearch(currentState))


    aichess.chess.boardSim.print_board()
    print("#Move sequence...  ", aichess.pathToTarget)
    print("#Visited States:  ", len(aichess.listVisitedStates))
    print("#Visited sequence...  ", aichess.listVisitedStates)

    print("#Current State...  ", aichess.chess.boardSim.currentStateW)
    print("#CheckMate Status: ", aichess.checkMate)
