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
        if self.isCheckMate(currentState):
            return True
        if depth > self.depthMax:
            return False

        self.listVisitedStates.append(currentState)
        for state in self.getListNextStatesW(currentState):
            if not self.isVisited(state):
                start, to, piece = self.getMoveFromStates(currentState, state)
                self.pathToTarget.append((start, to, piece))
                self.chess.moveSim(start, to)

                if self.DepthFirstSearch(state, depth + 1):
                    return True

                self.chess.moveSim(to, start)
                self.pathToTarget.remove((start, to, piece))

        return False

    def BreadthFirstSearch(self, currentState, depth):
        """
        Check mate from currentStateW

        intentar que en vez de cojer el currentMove, a cada iteracion
        del while, hacer todos los moves the moveQueue con un for, y luego
        deshacerlos (lineas 173,174, 180, 194)
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
                if(len(self.listVisitedStates) >= 74):
                    print("ListVisitedState[73]: ", self.listVisitedStates[73])
                self.chess.moveSim(move[0], move[1])
                if (len(self.listVisitedStates) >= 74):
                    print("ListVisitedState[73]: ", self.listVisitedStates[73])
            self.chess.boardSim.print_board()
            print("AS:" ,self.chess.boardSim.currentStateW)
            print("VS: ", self.listVisitedStates)
            print("NEXT: ", self.getListNextStatesW(self.chess.boardSim.currentStateW))
            print("VS: ", self.listVisitedStates)
            actualState = self.chess.boardSim.currentStateW
            #print("STATE: ", self.chess.boardSim.currentStateW)
            #print("PTT: ", self.pathToTarget)
            #print("NEXTSTATES: ", self.getListNextStatesW(self.chess.boardSim.currentStateW))
            if self.isCheckMate(actualState):                           #check if resulting state is CheckMate
                self.pathToTarget = currentMove
                return True
            for state in self.getListNextStatesW(self.chess.boardSim.currentStateW):
                ##print("VL: ", self.listVisitedStates)
                if not self.isVisited(state):
                    start, to, piece = self.getMoveFromStates(self.chess.boardSim.currentStateW, state)
                    new_moveSequence = list(currentMove)
                    print("PTT: ", currentMove)
                    newMove = [start, to, piece]
                    new_moveSequence.append(newMove)
                    print("NEW PTT: ", new_moveSequence)
                    #print("NMS: ", new_moveSequence)
                    moveQueue.append(new_moveSequence)
                    self.listVisitedStates.append(state)

                print("DONE")
            for i in range(len(currentMove)-1, -1, -1):
                start = currentMove[i][1]
                to = currentMove[i][0]
                self.chess.moveSim(start,to)
                if depth > 10000:
                    print("YOs")
                    return False
            depth += 1
        return False








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
    print(aichess.BreadthFirstSearch(currentState, depth))
    print("BFS End")


    aichess.chess.boardSim.print_board()
    print("#Move sequence...  ", aichess.pathToTarget)
    print("#Visited States:  ", len(aichess.listVisitedStates))
    print("#Visited sequence...  ", aichess.listVisitedStates)

    print("#Current State...  ", aichess.chess.boardSim.currentStateW)
    print("#CheckMate Status: ", aichess.checkMate)
