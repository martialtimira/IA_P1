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
        self.itCount = 0

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
        else:
            return False

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

    def BreadthFirstSearch(self, q):
        """
        Check mate from currentStateW
        """
        # your code
        self.itCount +=1
        if len(q) == 0:
            return False
        currentState = q.pop(0)

        estat = currentState[0]
        stackPath = currentState[1]
        depth = currentState[2]

        self.boardConfig(stackPath, estat)

        if self.isCheckMate(estat):
            self.moveSequence(stackPath.append(estat))
            return True
        if depth > self.depthMax:
            return False

        self.listVisitedStates.append(currentState)
        stack = stackPath.copy()
        stack.append(estat)
        for state in self.getListNextStatesW(estat):
            if not self.isBFSVisited(state):
                self.listVisitedStates.append([state, stack, depth + 1])
                q.append([state, stack, depth + 1])

        return self.BreadthFirstSearch(q)

    def statePerm(self, state):
        finalState = []

        finalState.append([state[0], state[1]])
        finalState.append([state[1], state[0]])

        return finalState
    def isBFSVisited(self, state):
        estat = self.statePerm(state)
        vs = self.listVisitedStates
        for s in vs:
            if s[0] in estat:
                return True
        return False

    def getStack(self, state):
        estat = list(permutations(state))
        for i in range(len(self.listVisitedStates)):
            for j in range(len(estat)):
                if self.listVisitedStates[i][0] == list(estat[j]):
                    return self.listVisitedStates[i][1]

    def boardConfig(self, stateStack, objectiu):
        boardStack = self.getStack(self.currentStateW)

        if self.itCount > 16:
            # 746 756
            ...


        if boardStack is None:
            return

        if len(boardStack) == 0:
            start, to, piece = self.getMoveFromStates(stateStack[0], objectiu)
            self.chess.moveSim(start, to)
            return


        fatherState = []

        # Busquem estat comu
        i = len(stateStack) - 1
        found = False
        while i >= 0 and not found:
            j = len(boardStack) - 1
            while j >= 0 and not found:
                if stateStack[i] == boardStack[j]:
                    fatherState = stateStack[i]
                    found = True
                j -= 1
            i -= 1

        i += 1 # Index d'estat comu a l'stack de l'estat objectiu

        # Moure de l'estat actual a l'estat comu
        while self.currentStateW != fatherState:
            j = len(boardStack) - 1
            start, to, piece = self.getMoveFromStates(self.currentStateW, boardStack[j])
            self.chess.moveSim(start, to)
            j -= 1

        # Moure de l'estat comu a l'estat objectiu
        while self.currentStateW != stateStack[-1]:
            start, to, piece = self.getMoveFromStates(self.currentStateW, stateStack[i])
            if start is not None and to is not None:
                self.chess.moveSim(start, to)
            i += 1
        if self.currentStateW != objectiu:
            start, to, piece = self.getMoveFromStates(self.currentStateW, objectiu)
            self.chess.moveSim(start, to)

        return

    def moveSequence(self, stackPath):
        for i in range(len(stackPath) - 1):
            self.pathToTarget.append((self.getMoveFromStates(stackPath[i], stackPath[i + 1])))
        return


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

    estat = [currentState, [], depth]
    q = [estat]

    print(aichess.BreadthFirstSearch(q))

    #print(aichess.DepthFirstSearch(currentState, depth))
    print("DFS End")


    aichess.chess.boardSim.print_board()
    print("#Move sequence...  ", aichess.pathToTarget)
    print("#Visited States:  ", len(aichess.listVisitedStates))
    print("#Visited sequence...  ", aichess.listVisitedStates)

    print("#Current State...  ", aichess.chess.board.currentStateW)
    print("#CheckMate States: ", aichess.isCheckMate(currentState))
