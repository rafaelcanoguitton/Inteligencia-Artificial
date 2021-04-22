import pygame
from checkers.constants import WIDTH,HEIGHT,SQUARE_SIZE, RED
from checkers.tablero import tablero
from checkers.juego import Game
FPS=60
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Damas')
def get_row_col_from_mouse(pos):
    x,y=pos
    row=y//SQUARE_SIZE
    col=x//SQUARE_SIZE
    return row,col
def main():
    #run = True
    clock=pygame.time.Clock()
    juego=Game(WIN)
    # pieza=tablerito.get_piece(0,1)
    # tablerito.move(pieza,4,3)
    while(True):
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                break
            if event.type==pygame.MOUSEBUTTONDOWN:
                pos=pygame.mouse.get_pos()
                row,col=get_row_col_from_mouse(pos)
                juego.select(row,col)
        juego.update()
    pygame.quit()
main()