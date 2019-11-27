import tetris_ai.tetris_ai as t
import tetris_ai.ga as ga
import matplotlib.pyplot as plt

def main():
    # GENERAL CONFIG
    NUM_GEN        = 5
    NUM_POP        = 15
    MUTATION_RATE  = 0.3
    CROSSOVER_RATE = 0.5
    N_SELECTION    = 5

    genetic_alg    = ga.GA(NUM_POP)

    best_chromos   = []
    best_pop_score = []
    avg_pop_gen    = []

    game_speed     = 600

    for j in range(NUM_GEN):
        print (' \n')
        print (f' - - - - Geração atual: {j+1} - - - - ')
        print (' \n')

        for i in range(NUM_POP):
            # Run the game for each chromosome
            game_state = t.run_game(genetic_alg.chromosomes[i], game_speed, \
                                    max_score = 200000, show_game = False)
            # Calculate the fitness
            genetic_alg.chromosomes[i].calc_fitness(game_state)
            print(f"Individuo: {(i + 1)}, Score: {genetic_alg.chromosomes[i].score}")

        # Select chromosomes using roulette method
        selected_pop = genetic_alg.roulette(N_SELECTION, best_pop_score, \
                                            avg_pop_gen, best_chromos)
        # Apply crossover and mutation
        new_chromo   = genetic_alg.operator(selected_pop, \
                                            crossover="uniform", \
                                            mutation="random", \
                                            crossover_rate=CROSSOVER_RATE, \
                                            mutation_rate=MUTATION_RATE)

        # Insert new children in pop
        genetic_alg.chromosomes[-(len(new_chldren)):] = new_chromo

    return best_chromos

if __name__ == "__main__":
    # test looking for better chomossome
    # by genetic algorithm
    best_chromos = main()

    """
    # play game to the best chromos
    for chromo in best_chromos:
        print("bests chromo\n\n")
        # run game with choiced cromo
        t.run_game(chromo, 200, max_score=200000)
    """

    """
    # test for one especific cromossomo
    # generate weight randomly
    numPesos = 7
    pesos0 = numPesos*[0]
    for k2 in range (0,numPesos):
        pesos0[k2] = 2*random.random()-1

    # choice especific weight
    pesos0 = [-0.97, 5.47, -13.74, -0.73,  7.99, -0.86, -0.72]

    genetic_alg = ga.GA(10)

    # run game with choiced cromo
    indiv = ga.Chromosome(pesos0)
    t.run_game(indiv, 300, max_score=200000)

    """