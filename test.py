from array import *
import random
from pprint import pprint


'''Create Graph'''
n = 40
graph = []
for i in range(n):
    vertex = []
    for j in range(n):
        vertex.append(random.randint(0, 1))
    graph.append(vertex)
for i in range(n):
    for j in range(0, i):
        graph[i][j] = graph[j][i]
for i in range(n):
    graph[i][i] = 0
pprint(graph)
pprint(sum(graph[39]))




# from array import *
# import random
# import matplotlib.pyplot as plt
# import numpy as np
# Gen = np.array([])
# Fit = np.array([])
#
# '''Create Graph'''
# n = 40
# graph = []
# for i in range(n):
# 	vertex = []
# 	for j in range(n):
# 		vertex.append(random.randint(0, 1))
# 	graph.append(vertex)
# for i in range(n):
# 	for j in range(0, i):
# 		graph[i][j] = graph[j][i]
# for i in range(n):
# 	graph[i][i] = 0
# for v in graph:
# 	print(v)
#
# '''Upper Bound for Coloring'''
# max_num_colors = 1
# for i in range(n):
# 	if sum(graph[i]) > max_num_colors:
# 		max_num_colors = sum(graph[i]) + 1
# print(max_num_colors)


# '''Create Individual using given # of colors'''
# number_of_colors = max_num_colors
# '''GA'''
# condition = True
# while(condition and number_of_colors > 0):
# 	def create_individual():
# 		individual = []
# 		for i in range(n):
# 			individual.append(random.randint(1, number_of_colors))
# 		return individual
# 	'''Create Population'''
# 	population_size = 200
# 	generation = 0
# 	population = []
# 	for i in range(population_size):
# 		individual = create_individual()
# 		population.append(individual)
#
# 	'''Fitness'''
# 	def fitness(graph, individual):
# 		fitness = 0
# 		for i in range(n):
# 			for j in range(i, n):
# 				if(individual[i] == individual[j] and graph[i][j] == 1):
# 					fitness += 1
# 		return fitness
#
# 	'''Crossover'''
# 	def crossover(parent1, parent2):
# 		position = random.randint(2, n-2)
# 		child1 = []
# 		child2 = []
# 		for i in range(position+1):
# 			child1.append(parent1[i])
# 			child2.append(parent2[i])
# 		for i in range(position+1, n):
# 			child1.append(parent2[i])
# 			child2.append(parent1[i])
# 		return child1, child2
#
# 	def mutation1(individual):
# 		probability = 0.4
# 		check = random.uniform(0, 1)
# 		if(check <= probability):
# 			position = random.randint(0, n-1)
# 			individual[position] = random.randint(1, number_of_colors)
# 		return individual
#
# 	def mutation2(individual):
# 		probability = 0.2
# 		check = random.uniform(0, 1)
# 		if(check <= probability):
# 			position = random.randint(0, n-1)
# 			individual[position] = random.randint(1, number_of_colors)
# 		return individual
#
# 	'''Tournament Selection'''
# 	def tournament_selection(population):
# 		new_population = []
# 		for j in range(2):
# 			random.shuffle(population)
# 			for i in range(0, population_size-1, 2):
# 				if fitness(graph, population[i]) < fitness(graph, population[i+1]):
# 					new_population.append(population[i])
# 				else:
# 					new_population.append(population[i+1])
# 		return new_population
#
# 	'''Roulette Wheel Selection'''
# 	def roulette_wheel_selection(population):
# 		total_fitness = 0
# 		for individual in population:
# 			total_fitness += 1/(1+fitness(graph, individual))
# 		cumulative_fitness = []
# 		cumulative_fitness_sum = 0
# 		for i in range(len(population)):
# 			cumulative_fitness_sum += 1 / \
# 				(1+fitness(graph, population[i]))/total_fitness
# 			cumulative_fitness.append(cumulative_fitness_sum)
#
# 		new_population = []
# 		for i in range(len(population)):
# 			roulette = random.uniform(0, 1)
# 			for j in range(len(population)):
# 				if (roulette <= cumulative_fitness[j]):
# 					new_population.append(population[j])
# 					break
# 		return new_population
# 	best_fitness = fitness(graph, population[0])
# 	fittest_individual = population[0]
# 	gen = 0
# 	while(best_fitness != 0 and gen != 10000):
# 		gen += 1
# 		population = roulette_wheel_selection(population)
# 		new_population = []
# 		random.shuffle(population)
# 		for i in range(0, population_size-1, 2):
# 			child1, child2 = crossover(population[i], population[i+1])
# 			new_population.append(child1)
# 			new_population.append(child2)
# 		for individual in new_population:
# 			if(gen < 200):
# 				individual = mutation1(individual)
# 			else:
# 				individual = mutation2(individual)
# 		population = new_population
# 		best_fitness = fitness(graph, population[0])
# 		fittest_individual = population[0]
# 		for individual in population:
# 			if(fitness(graph, individual) < best_fitness):
# 				best_fitness = fitness(graph, individual)
# 				fittest_individual = individual
# 		if gen % 10 == 0:
# 			print("Generation: ", gen, "Best_Fitness: ",
# 				best_fitness, "Individual: ", fittest_individual)
# 		Gen = np.append(Gen, gen)
# 		Fit = np.append(Fit, best_fitness)
# 	print("Using ", number_of_colors, " colors : ")
# 	print("Generation: ", gen, "Best_Fitness: ",
# 		best_fitness, "Individual: ", fittest_individual)
# 	print("\n\n")
# 	if(best_fitness != 0):
# 		condition = False
# 		print("Graph is ", number_of_colors+1, " colorable")
# 	else:
# 		Gen = np.append(Gen, gen)
# 		Fit = np.append(Fit, best_fitness)
# 		plt.plot(Gen, Fit)
# 		plt.xlabel("generation")
# 		plt.ylabel("best-fitness")
# 		plt.show()
# 		Gen = []
# 		Fit = []
# 		number_of_colors -= 1

