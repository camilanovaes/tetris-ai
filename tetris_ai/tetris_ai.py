import random, time, pygame, sys
from pygame.locals import *
import tetris_ai.tetris_base as game

size   = [640, 480]
screen = pygame.display.set_mode((size[0], size[1]))

def run_game(chromosome, speed, max_score = 20000, no_show = False):

    game.FPS = int(speed)
    game.main()

    board            = game.get_blank_board()
    last_fall_time   = time.time()
    score            = 0
    level, fall_freq = game.calc_level_and_fall_freq(score)
    falling_piece    = game.get_new_piece()
    next_piece       = game.get_new_piece()

    # Calculate best move
    chromosome.calc_best_move(board, falling_piece)

    num_used_pieces = 0
    removed_lines   = [0,0,0,0] # Combos

    alive = True
    win   = False

    # Game loop
    while alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print ("Game exited by user")
                exit()

        if falling_piece == None:
            # No falling piece in play, so start a new piece at the top
            falling_piece = next_piece
            next_piece    = game.get_new_piece()

            # Decide the best move based on your weights
            chromosome.calc_best_move(board, falling_piece, no_show)

            # Update number of used pieces and the score
            num_used_pieces +=1
            score           += 1

            # Reset last_fall_time
            last_fall_time = time.time()

            if (not game.is_valid_position(board, falling_piece)):
                # GAME-OVER
                # Can't fit a new piece on the board, so game over.
                alive = False

        if no_show or time.time() - last_fall_time > fall_freq:
            if (not game.is_valid_position(board, falling_piece, adj_Y=1)):
                # Falling piece has landed, set it on the board
                game.add_to_board(board, falling_piece)

                # Bonus score for complete lines at once
                # 40   pts for 1 line
                # 120  pts for 2 lines
                # 300  pts for 3 lines
                # 1200 pts for 4 lines
                num_removed_lines = game.remove_complete_lines(board)
                if(num_removed_lines == 1):
                    score += 40
                    removed_lines[0] += 1
                elif (num_removed_lines == 2):
                    score += 120
                    removed_lines[1] += 1
                elif (num_removed_lines == 3):
                    score += 300
                    removed_lines[2] += 1
                elif (num_removed_lines == 4):
                    score += 1200
                    removed_lines[3] += 1

                falling_piece = None
            else:
                # Piece did not land, just move the piece down
                falling_piece['y'] += 1
                last_fall_time = time.time()

        if (not no_show):
            draw_game_on_screen(board, score, level, next_piece, falling_piece,
                                chromosome)

        # Stop condition
        if (score > max_score):
            alive = False
            win   = True

    # Save the game state
    game_state = [num_used_pieces, removed_lines, score, win]

    return game_state

def draw_game_on_screen(board, score, level, next_piece, falling_piece, chromosome):
    """Draw game on the screen"""

    game.DISPLAYSURF.fill(game.BGCOLOR)
    game.draw_board(board)
    game.draw_status(score, level)
    game.draw_next_piece(next_piece)

    if falling_piece != None:
        game.draw_piece(falling_piece)

    pygame.display.update()
    game.FPSCLOCK.tick(game.FPS)
