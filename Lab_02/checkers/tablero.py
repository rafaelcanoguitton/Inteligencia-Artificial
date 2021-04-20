import pygame
from .constants import BLACK,ROWS,RED,SQUARE_SIZE,COLS, WHITE
from .pieza import pieza
class tablero:
    def __init__(self):
        self.tablero=[]
        self.red_left=self.white_left=12
        self.red_damas=self.white_damas=0
        self.create_board()

    def draw_squares(self,win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row%2, ROWS,2):
                pygame.draw.rect(win,RED,(row*SQUARE_SIZE,col*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
    def create_board(self):
        for row in range(ROWS):
            self.tablero.append([])
            for col in range(COLS):
                if col%2==((row+1)%2):
                    if row<3:
                        self.tablero[row].append(pieza(row,col,WHITE))
                    elif row>4:
                        self.tablero[row].append(pieza(row,col,RED))
                    else:
                        self.tablero[row].append(0)
                else:
                    self.tablero[row].append(0)
    def draw(self,win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece=self.tablero[row][col]
                if piece!=0:
                    piece.draw(win)
    def move(self,piece,row,col):
        self.tablero[piece.row][piece.col],self.tablero[row][col]=self.tablero[row][col],self.tablero[piece.row][piece.col]
        piece.move(row,col)
        if row==ROWS or row==0:
            piece.make_king()
            if piece.color==WHITE:
                self.white_damas+=1
            else:
                self.red_damas+=1
    def get_piece(self,row,col):
        return self.tablero[row][col]