import tetris_ai.tetris_ai as t
import tetris_ai.ga as ga
import matplotlib.pyplot as plt

def main():
    # Config
    NUM_GEN      = 5
    NUM_POP      = 15
    TX_MUTACAO   = 0.3
    TX_CROSSOVER = 0.5
    TX_ELITISMO  = 5

    genetic_alg      = ga.GA(NUM_POP)

    best_pop_gen = []
    avg_pop_gen  = []

    game_speed = 500
    for j in range(NUM_GEN):
        print (' \n')
        print (' - - - - Geração atual: {} - - - - ' .format(j+1))
        print (' \n')

        for i in range(NUM_POP):
            game_state = t.run_game(genetic_alg.chromosomes[i], game_speed, max_score = 200000, show_game = False)
            genetic_alg.chromosomes[i].calc_fitness(game_state)
            print("Individuo: "+ (i + 1).__str__() + " score:" + genetic_alg.chromosomes[i].score.__str__())

        genetic_alg.selection(TX_ELITISMO, best_pop_gen, avg_pop_gen)
        genetic_alg.operators(NUM_POP, TX_CROSSOVER, TX_MUTACAO)

    print("Melhores Individuos:")
    print(best_pop_gen)
    plt.subplot(211)

    plt.title('Fitness dos melhores indivíduos por geração')
    plt.plot(best_pop_gen)
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

    return(genetic_alg)

gen = main()

