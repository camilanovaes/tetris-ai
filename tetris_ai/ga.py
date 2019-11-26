import pygame
import random
import numpy as np
import tetris_ai.tetris_base as t


class Chromosome():
    """
    A classe Individuo incializa o individuo com score nulo e um vetor de pesos.
    Ela tambem implementa a funcao fitness utilizada para avaliar o score de
    cada individuo e calcula a direcao para a qual o jogador se move (para
    esquerda ou direita e se deve rotacionar) a partir do resultado calculado
    multiplicando-se o vetor de pesos daquele individuo por uma entrada.

    """

    def __init__(self, weights):
        self.weights = weights
        self.score   = 0

    def __str__(self):
        s = "   Weights:"
        for i in range(len(self.weights)):
            s += "%5.2f "%(self.weights[i])
        return s

    def calc_fitness(self, game_state):
        #gameState = [numero de pecas, linhas destruidas(combos de 1,2,3,4), score normal de tetris, ganhou]
        # k1*t - abs(deltaY(morreu)[player-bolinha))
        self.score = game_state[0]

    def calc_best_move(self, board, piece, show_game = False):
        """
        Seleciona a direcao em que o jogador vai se mover a partir do valor computado pelo
        produto entre o vetor entrada e o vetor pesos de cada individuo. Se esse valor
        for maior que meio, o jogador sobe, caso contrario ele desce.

        """
        best_X     = 0          # Melhor posição em X
        best_R     = 0          # Melhor rotação
        best_Y     = 0          # Melhor posição em Y
        best_score = -100000    # Melhor pontuação

        # Calculate the total the holes and blocks above holes before play
        num_holes_bef, num_blocking_blocks_bef = t.calc_initial_move_info(board)
        for r in range(len(t.PIECES[piece['shape']])):
            # Iterate through every possible rotation
            for x in range(-2,t.BOARDWIDTH-2):
                #Iterate through every possible position

                #retorna: [jogadaValida, alturaTotal, numLinhasCompletas, buracosFormados, tampasFormadas, ladosPecas, ladosChao, ladosParede]
                movement_info = t.calc_move_info(board, piece, x, r, num_holes_bef, num_blocking_blocks_bef)

                # Check if it's a valid movement
                if (movement_info[0]):
                    # Calculate movement score
                    movement_score = 0
                    for i in range(1, len(movement_info)):
                        movement_score += self.weights[i-1]*movement_info[i]

                    # Update best movement
                    if (movement_score > best_score):
                        best_score = movement_score
                        best_X = x
                        best_R = r
                        best_Y = piece['y'] #p ir mais rapido

        if (show_game):
            piece['y'] = best_Y
        else:
            piece['y'] = -2

        piece['x'] = best_X
        piece['rotation'] = best_R

        return best_X, best_R



class GA:
    #TODO: Refazer toda essa parte de GA.

    def __init__ (self, num_pop, num_weights=7, lb=-1, ub=1):
        """Realiza a inicializacao dos pesos a partir das grandezas contidas nas variaveis numInd e numPesos.
        Cria um vetor de numPesos casas cujos valores iniciais sao randomicos distribuidos no intervalo
        de [-1,1].

        """
        self.chromosomes = []

        for _ in range(num_pop):
            weights = np.random.uniform(lb, ub, size=(num_weights))
            chrom   = Chromosome(weights)
            self.chromosomes.append(chrom)

    def __str__(self):
        for i in range(len(self.chromosomes)):
            print("Individuo %d:"%i)
            print(self.chromosomes[i])
        return ''

    def selection(self, num_selec, best_chroms, avg_score_gen):

        """
        Realiza a selecao dos numSelec melhor individuos baseados no score de uma simulacao do jogo.
        Ordena os individuos baseados nos scores e seleciona os numSelec melhores.

        TODO: Adicionar uma forma de seleção. Pode ser roleta ou torneio, pq
        aqui basicamente temos apenas uma seleção totalmente elitista. Apenas os
        melhores são selecionados para o cruzamento

        """
        self.chromosomes = sorted(self.chromosomes, key=lambda x: x.score, reverse=True)
        total_score     = 0
        num_pop         = len(self.chromosomes)

        for i in range(num_pop):
            total_score += self.chromosomes[i].score

        print("\n Average score: ", total_score / num_pop)
        avg_score_gen.append(total_score / num_pop);

        best_score_gen = 0
        for i in range(num_pop):
            if(self.chromosomes[i].score > best_score_gen):
                best_score_gen = self.chromosomes[i].score
                best_chroms.append(best_score_gen)

        print("Best score: ", best_score_gen, "\n")

        self.chromosomes = self.chromosomes[:num_selec]

        return self

    def operators(self, m, tx_crossover = 0.5, tx_mutation = 0.15):
        """
        A partir dos individuos selecionados em 'selecao' com melhor score, duplica os individuos
        comecando pelo de melhor score ate o numero de individuos chegar ao valor da variavel 'm'.
        Realiza o Crossing Over e a Mutacao nos individuos novos gerados.

        TODO: Arrumar essas funções de crossover e mutação

        """
        num_pop = len(self.chromosomes)

        k = 0
        while len(self.chromosomes) < m :
            weights = self.chromosomes[k].weights[:]
            chrom_1 = Chromosome(weights)
            weights = self.chromosomes[k+1].weights[:]
            chrom_2 = Chromosome(weights)

            self.arithmetic_crossover(chrom_1,chrom_2,tx_crossover)
            self.mutation(chrom_1,tx_mutation)
            self.mutation(chrom_2,tx_mutation)

            self.chromosomes.append(chrom_1)

            if len(self.chromosomes) < m:
                self.chromosomes.append(chrom_2)

            k += 2

        return self

    ### --------------------- genCrossOver:
    ## Aplica o crossing over 'numCO' vezes na duplicacao de cada individuo gerada por reproduzir.
    ## Seleciona randomicamente uma das casas do vetor de peso do individuo[0] (que e' o individuo
    ## com maior score
    def uniform_crossover(self, individuo1, individuo2, chanceCO):
        
        """
            Calculate uniform crossover with exchange between cromo genes 
            param1: individuo1 - frist individual
            param2: individuo2 - second individual
            param3: cross_rate - crossover rate, default = 0.4

        """
        for k in range (len(individuo1.weights)):
            r = random.random()
            if r < chanceCO:
                individuo1.weights[k], individuo2.weights[k] = individuo2.weights[k], individuo1.weights[k]

    # arithmetic crossover with cross_point
    def arithmetic_crossover(self, cromo_1, cromo_2, cross_rate = 0.4):
        """
            Calculate arithmetic crossover with cross point
            param1: cromo_1 - frist individual
            param2: cromo_2 - second individual
            param3: cross_rate - crossover rate, default = 0.4

        """
        r = random.random()
        if r < cross_rate:
            cross_point = random.randint(1, len(cromo_1.weights-1))
            
            # means for each gene bounded by cross point
            for i in range(cross_point):
                cromo_1.weights[i] = (cromo_1.weights[i] + cromo_2.weights[i])/2
            
            for j in range(cross_point, len(cromo_1.weights)):
                cromo_2.weights[j] = (cromo_2.weights[j] + cromo_1.weights[j])/2



    ### ----------------------- genMut:
    ## Para um 'numMut' de vezes, seleciona uma das casas do vetor de peso de um dos
    ## individuos duplicados e modifica o valor do peso daquela casa multiplicando-o
    ## por um numero randomico entre [-1,1].
    def mutation(self, individuo1, chanceMut):
        for k1 in range (len(individuo1.weights)):
            r = random.random()
            if r < chanceMut:
                #realizando a mutacao
                mut = 10 + individuo1.weights[k1]/10.0                   #mut eh um parametro relaxionado com a dispersao possivel de mutacao
                individuo1.weights[k1] += mut*(2*random.randrange(1000)/1000.0 - 1)       #randomicamente adiciona-se algo entre +- mut no gene

