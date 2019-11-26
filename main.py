import tetris_ai.tetris_ai as t
import tetris_ai.ga as ga
import matplotlib.pyplot as plt

def main():
    # Config
    NUM_GEN      = 5
    NUM_POP      = 15
    MUTATION_RATE   = 0.3
    CROSSOVER_RATE = 0.5
    N_SELECTION  = 5

    genetic_alg      = ga.GA(NUM_POP)

    
    best_chromos = []
    best_pop_score = []
    avg_pop_gen  = []

    game_speed = 600
    for j in range(NUM_GEN):
        print (' \n')
        print (' - - - - Geração atual: {} - - - - ' .format(j+1))
        print (' \n')

        for i in range(NUM_POP):
            game_state = t.run_game(genetic_alg.chromosomes[i], game_speed, max_score = 200000, show_game = False)
            genetic_alg.chromosomes[i].calc_fitness(game_state)
            print("Individuo: "+ (i + 1).__str__() + " score:" + genetic_alg.chromosomes[i].score.__str__())

        selected_pop = genetic_alg.roulette(N_SELECTION, best_pop_score, avg_pop_gen, best_chromos)
        children = genetic_alg.arithmetic_crossover(selected_pop, CROSSOVER_RATE)
        new_chldren = genetic_alg.uniform_mutation(children, MUTATION_RATE)
        # insert new children in pop
        genetic_alg.chromosomes[-(len(new_chldren)):] = new_chldren
    
    
    print("Melhores Individuos:")
    print(best_pop_score)
    plt.subplot(211)

    plt.title('Fitness dos melhores indivíduos por geração')
    plt.plot(best_pop_score)
    plt.ylabel("Fitness dos melhores indivíduos")
    plt.xlabel("Gerações")

    plt.subplot(212)
    print("Medias do fitness por gerações:")
    print(avg_pop_gen)
    plt.title('Médias do fitness dos indivíduos por geração')
    plt.plot(avg_pop_gen)
    plt.ylabel("Media do Fitness por Geração")
    plt.xlabel("Gerações")
    plt.subplots_adjust(top=0.89, bottom=0.11, left=0.12, right=0.95, hspace=0.85,
                        wspace=0.35)

    plt.show()
    

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