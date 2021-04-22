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
        if row==ROWS-1 or row==0:
            piece.make_king()
            if piece.color==WHITE:
                self.white_damas+=1
            else:
                self.red_damas+=1
    def get_piece(self,row,col):
        return self.tablero[row][col]
    def get_valid_moves(self,pieza):
        moves={}
        left=pieza.col-1
        right=pieza.col+1
        row=pieza.row
        if pieza.color==RED or pieza.king:
            moves.update(self._traverse_left(row-1,max(row-3,-1),-1,pieza.color,left))
            moves.update(self._traverse_left(row-1,max(row-3,-1),-1,pieza.color,right))
        if pieza.color==WHITE or pieza.king:
            moves.update(self._traverse_right(row+1,min(row+3,ROWS),1,pieza.color,left))
            moves.update(self._traverse_right(row+1,min(row+3,ROWS),1,pieza.color,right))
        return moves
    def _traverse_left(self,start,stop,step,color,left,skipped=[]):
        moves={}
        last=[]
        for r in range(start,stop,step):
            if left<0:
                break
            current=self.tablero[r][left]
            if current==0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,left)]=last+skipped
                else:
                    moves[(r,left)]=last
                if last:
                    if step==-1:
                        row = max(r-3,0)
                    else:
                        row=min(r+3,ROWS)
                    moves.update(self._traverse_left(r+step,row,step,color,left-1,skipped=last))
                    moves.update(self._traverse_right(r+step,row,step,color,left+1,skipped=last))
                break
            elif current.color==color:
                break
            else:
                last=[current]
            left-=1
        return moves
    def _traverse_right(self,start,stop,step,color,right,skipped=[]):
        moves={}
        last=[]
        for r in range(start,stop,step):
            if right>=COLS:
                break
            current=self.tablero[r][right]
            if current==0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)]=last+skipped
                else:
                    moves[(r,right)]=last
                if last:
                    if step==-1:
                        row = max(r-3,0)
                    else:
                        row=min(r+3,ROWS)
                    moves.update(self._traverse_left(r+step,row,step,color,right-1,skipped=last))
                    moves.update(self._traverse_right(r+step,row,step,color,right+1,skipped=last))
                break
            elif current.color==color:
                break
            else:
                last=[current]
            right+=1
        return moves
    def remove(self,pieces):
        for piece in pieces:
            self.tablero[piece.row][piece.col]=0