import tetris_ai.ga as ga
import tetris_ai.tetris_base as game
import tetris_ai.tetris_ai as ai
import matplotlib.pyplot as plt
import argparse

def main(no_show):
    # GENERAL CONFIG
    NUM_GEN        = 3
    NUM_POP        = 3
    MUTATION_RATE  = 0.3
    CROSSOVER_RATE = 0.75

    genetic_alg    = ga.GA(NUM_POP)

    best_chromos   = []
    best_pop_score = []
    avg_pop_gen    = []

    game_speed     = 600

    for j in range(NUM_GEN):
        print (' \n')
        print (f' - - - - Geração atual: {j+1} - - - - ')
        print (' \n')

        # Select chromosomes using roulette method
        selected_pop = genetic_alg.selection(genetic_alg.chromosomes, NUM_POP, \
                                             type="roulette")
        # Apply crossover and mutation
        new_chromo   = genetic_alg.operator(selected_pop, \
                                            crossover="uniform", \
                                            mutation="random", \
                                            crossover_rate=CROSSOVER_RATE, \
                                            mutation_rate=MUTATION_RATE)

        for i in range(NUM_POP):
            # Run the game for each chromosome
            game_state = ai.run_game(genetic_alg.chromosomes[i], game_speed, \
                                    max_score = 200000, no_show = no_show)
            # Calculate the fitness
            genetic_alg.chromosomes[i].calc_fitness(game_state)

            # Print information
            print(f"Individuo: {(i + 1)}:")
            print(f"   Score: {genetic_alg.chromosomes[i].score}")
            print(f"   Weights: {genetic_alg.chromosomes[i].weights}")
            print('--')

        # Insert new children in pop
        genetic_alg.chromosomes[-(len(new_chromo)):] = new_chromo

    return best_chromos

if __name__ == "__main__":
    # Define argparse options
    parser = argparse.ArgumentParser(description="Tetris AI")
    parser.add_argument('--train',
                        action='store_true',
                        help='Whether or not to train the AI')
    parser.add_argument('--game',
                        action='store_true',
                        help='Run the base game without AI')
    parser.add_argument('--no-show',
                        action='store_true',
                        help='Whether to show the game')

    args = parser.parse_args()

    if (args.train):
        # Train the AI and after play the game with the get chromosome
        best_chromos = main(args.no_show)

    elif (args.game):
        # Just run the base game
        game.MANUAL_GAME = True
        game.main()

    else:
        # Run tetris AI with optimal weights
        # FIXME: Define the optimal weights
        optimal_weights = [-0.97, 5.47, -13.74, -0.73,  7.99, -0.86, -0.72]
        chromo = ga.Chromosome(optimal_weights)
        ai.run_game(chromo, speed=600, max_score=200000, no_show=False)

