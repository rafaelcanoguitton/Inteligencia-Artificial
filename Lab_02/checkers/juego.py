import pygame
from checkers.tablero import tablero
from .constants import RED, WHITE
class Game:
    def __init__(self,win):
        self._init()
        self.win=win
    def update(self):
        self.tablerito.draw(self.win)
        pygame.display.update()
    def _init(self):
        self.selected=None
        self.tablerito=tablero()
        self.turn=RED
        self.valid_moves={}
    def reset(self):
        self._init()
    def select(self,row,col):
        if self.selected:
            result=self._move(row,col)
            if not result:
                self.selected=None
                self.select(row,col)
        else:
            piece=self.board.get_piece(row,col)
            if piece!=0 and piece.color==self.turn:
                self.selected=piece
                self.valid_moves=self.tablerito.get_valid_moves(piece)
                return True
            return False
    def _move(self,row,col):
        pieza=tablerito.get_piece(row,col)
        if self.selected and piece==0 and (row,col)in self.valid_moves:
            self.tablerito.move(self.selected,row,col)
            self.change_turn()
        else:
            return False
        return True

    def change_turn(self):
        if self.turn==RED:
            self.turn=WHITE
        else:
            self.turn=RED