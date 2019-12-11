import tetris_ai.ga as ga
import tetris_ai.tetris_base as game
import tetris_ai.tetris_ai as ai
import tetris_ai.analyser as analyser
import matplotlib.pyplot as plt
import argparse, copy
import pdb

def main(no_show_game):
    # GENERAL CONFIG
    GAME_SPEED     = 600
    NUM_GEN        = 100
    NUM_POP        = 15
    NUM_EXP        = 10
    GAP            = 0.3
    NUM_CHILD      = round(NUM_POP*GAP)
    MUTATION_RATE  = 0.2
    CROSSOVER_RATE = 0.75
    MAX_SCORE      = 200000

    genetic_alg    = ga.GA(NUM_POP)

    best_chromos   = []
    best_pop_score = []
    avg_pop_gen    = []

    # Define datasets
    experiments = []
    best_chromo = []

    # Initialize population
    init_pop    = ga.GA(NUM_POP)

    for e in range(NUM_EXP):
        # Make a copy from initial population so that we can run all experiments
        # with the same initial population
        pop         = copy.deepcopy(init_pop)

        # Initialize generation list
        generations = []

        for g in range(NUM_GEN):
            print (' \n')
            print (f' - - - - Exp: {e}\t Geração: {g} - - - - ')
            print (' \n')

            # Save generation
            generations.append(copy.deepcopy(pop))

            # Select chromosomes using roulette method
            selected_pop = pop.selection(pop.chromosomes, NUM_CHILD, \
                                         type="roulette")
            # Apply crossover and mutation
            new_chromo   = pop.operator(selected_pop, \
                                        crossover="uniform", \
                                        mutation="random", \
                                        crossover_rate=CROSSOVER_RATE, \
                                        mutation_rate=MUTATION_RATE)

            for i in range(NUM_CHILD):
                # Run the game for each chromosome
                game_state = ai.run_game(pop.chromosomes[i], GAME_SPEED, \
                                         MAX_SCORE, no_show_game)
                # Calculate the fitness
                new_chromo[i].calc_fitness(game_state)

            # Insert new children in pop
            pop.replace(new_chromo)
            fitness = [chrom.score for chrom in pop.chromosomes]
            print(fitness)

            # Print population
            print(pop)

        # Save experiments results
        experiments.append(generations)

        # Plot results
    an = analyser.Analyser(experiments)
    an.plot(type="best")
    an.plot(type="pop")
    an.plot(type="mdf", show_std=False)


    #Return the best choromosome from all generation and experiments
    return an.weights

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
        #FIXME:
        #chromo       = ga.Chromosome(best_chromos)
        #ai.run_game(chromo, speed=500, max_score=200000, no_show=False)

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
