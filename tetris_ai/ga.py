import pygame
import random
import numpy as np
import copy
import tetris_ai.tetris_base as t


class Chromosome():
    def __init__(self, weights):
        self.weights = weights
        self.score   = 0

    def __str__(self):
        s = "   Weights:"
        for i in range(len(self.weights)):
            s += "%5.2f "%(self.weights[i])
        return s

    def calc_fitness(self, game_state):
        """Calculate fitness"""
        self.score = game_state[2]

    def calc_best_move(self, board, piece, show_game = False):
        """Calculate best movement
        Select the best move based on the chromosome weights.

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
                movement_info = t.calc_move_info(board, piece, x, r, \
                                                 num_holes_bef, \
                                                 num_blocking_blocks_bef)

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
                        best_Y = piece['y']

        if (show_game):
            piece['y'] = best_Y
        else:
            piece['y'] = -2

        piece['x'] = best_X
        piece['rotation'] = best_R

        return best_X, best_R


class GA:
    def __init__ (self, num_pop, num_weights=7, lb=-1, ub=1):
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

    def selection(self, chromosomes, num_selection, type = "roulette"):
        """Define the selection method to use

        Args:
            chromosomes: Chromosomes to select
            type       : Selection type. (Defalt: roulette)

        """

        if (type == "roulette"):
            selected_chromos = self._roulette(chromosomes, num_selection)
        else:
            raise ValueError(f"Selection type {type} not defined")

        return selected_chromos

    def _roulette(self, chromosomes, num_selection):
        """Selection method using roulette wheel"""

        fitness = np.array([chrom.score for chrom in chromosomes])

        # Normalized fitness
        norm_fitness  = fitness/fitness.sum()

        # Roulette probability
        roulette_prob = np.cumsum(norm_fitness)

        # Run the roulette wheel
        pop_selected = []
        while len(pop_selected) < num_selection:
            pick = random.random()
            for index, individual in enumerate(self.chromosomes):
                if pick < roulette_prob[index]:
                    pop_selected.append(individual)
                    break

        return pop_selected

    def operator(self, chromosomes, crossover="arithmetic", mutation="uniform", \
                 crossover_rate=0.5, mutation_rate=0.1):
        """Define the genetic operators"""

        new_chromo = self.arithmetic_crossover(chromosomes, mutation, \
                                               crossover_rate, mutation_rate)

        return new_chromo

    def arithmetic_crossover(self, selected_pop, mutation, cross_rate=0.4, \
                             mutation_rate=0.1):
        """Create a new chromosome using arithmetic crossover"""

        N_genes    = len(selected_pop[0].weights) # Chromosome size
        new_chromo = [copy.deepcopy(c) for c in selected_pop]

        for i in range(0, len(selected_pop), 2):
            a = random.uniform(0,1)

            # Select a random number for each parent and compare with the
            # crossover rate, if both are lower than the crossover rate
            # apply the crossover. Else, just pass the parents for the new
            # population.
            tc_parent_1 = random.randint(0,100)
            tc_parent_2 = random.randint(0,100)
            if ( tc_parent_1 < cross_rate*100 and tc_parent_2 < cross_rate*100):
                try:
                    for j in range(0, N_genes):
                        new_chromo[i].weights[j]   = a*new_chromo[i].weights[j] \
                                                + (1 - a)*new_chromo[i+1].weights[j]

                        new_chromo[i+1].weights[j] = a*new_chromo[i+1].weights[j] \
                                                + (1 - a)*new_chromo[i].weights[j]

                    # Apply mutation and recalculates the fitness
                    self._mutation(new_chromo[i], mutation, mutation_rate)
                    new_chromo[i].calc_fitness()
                    self._mutation(new_chromo[i+1], mutation, mutation_rate)
                    new_chromo[i+1].calc_fitness()

                except IndexError:
                    pass

        return new_chromo

    def _mutation(self, chromosome, type, mutation_rate):
        """Select mutation type

        Args:
            chromosome : Chromosome to apply mutation
            type       : Select the mutation type

        """

        if (type == "random"):
            self._rand_mutation(chromosome, mutation_rate)
        else:
            raise ValueError(f"Type {type} not defined")

    def _rand_mutation(self, chromosome, mutation_rate):
        """Apply mutation to a specific chromosome using random mutation"""

        for point in chromosome.weights:
            if np.random.rand() < mutation_rate:
                chromosome.weights[point] = random.uniform(-1.0, 1.0)
        return chromosome