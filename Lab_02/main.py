# Assets: https://techwithtim.net/wp-content/uploads/2020/09/assets.zip
import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from checkers.minmax import minimax

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    #print('¿Qué ficha empezará la partida?\nPara blanco (minmax) escriba "blanco" y para que empiece negro escriba "negro" ')
    inputsito=input('¿Qué ficha empezará la partida?\nPara blanco (minmax) escriba "blanco" y para que empiece negro escriba "negro" ')
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    if inputsito=='blanco':
        game.turn=WHITE
    else:
        game.turn=RED
    profundidad_arbol=input('¿Qué profundidad tendrá el arbol del algoritmo MINMAX?(Dificultad) ')
    while run:
        clock.tick(FPS)
        
        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), int(profundidad_arbol), WHITE, game)
            game.ai_move(new_board)

        if game.winner() != None:
            color=game.winner()
            if color==WHITE:
                print('¡Ganó el blanco!')
            else:
                print('¡Ganó el negro!')

            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)
        game.update()
    
    pygame.quit()

main()