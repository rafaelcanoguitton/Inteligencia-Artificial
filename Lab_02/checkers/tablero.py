import pygame
from .constants import BLACK,ROWS,RED,SQUARE_SIZE
class tablero:
    def __init__(self):
        self.tablero=[]
        self.pieza_selecionada=None
        self.red_left=self.white_left=12
        self.red_damas=self.white_damas=0

    def draw_squares(self,win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row%2, ROWS,2):
                pygame.draw.rect(win,RED,(row*SQUARE_SIZE,col*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
