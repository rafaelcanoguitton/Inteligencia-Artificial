import pygame
from checkers.constants import WIDTH,HEIGHT
from checkers.tablero import tablero

FPS=60
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Damas')

def main():
    #run = True
    clock=pygame.time.Clock()
    tablerito=tablero()
    while(True):
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                break;
            if event.type==pygame.MOUSEBUTTONDOWN:
                pass;
        tablerito.draw_squares(WIN)
        pygame.display.update()
    pygame.quit()
main()