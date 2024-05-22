import numpy as np
import ctypes
import subprocess
from random import randint

class Ant:
	def __init__(self, num_stations, num_trains):
		self.num_stations = num_stations
		self.num_trains = num_trains
		self.reset()

	def reset(self):
		self.paths = [[] for _ in range(self.num_trains)]
		self.visited = [set() for _ in range(self.num_trains)]
		self.total_delays = 0

	def visit_station(self, train, station):
		self.paths[train].append(station)
		self.visited[train].add(station)

	def can_visit(self, train, station):
		# Make sure the ant hasn't visited the station before on its path (speed increase)
		return station not in self.visited[train]

def initialize_pheromones(num_stations, initial_pheromone):
	return np.full((num_stations, num_stations), initial_pheromone)

def choose_next_station(pheromones, current_station, alpha, beta, ant, train):
	probabilities = []
	for station in range(len(pheromones)):
		if ant.can_visit(train, station):
			#weighted probability ant will choose each station
			pheromone_level = pheromones[current_station, station] ** alpha
			heuristic_value = 1  #no heuristic value other than pheromone level
			probabilities.append(pheromone_level * heuristic_value)
		else:
			probabilities.append(0)
	#decide
	total = sum(probabilities)
	probabilities = [prob / total if total > 0 else 0 for prob in probabilities]
	return np.random.choice(len(pheromones), p=probabilities)

def calculate_delays(paths, num_stations):
	#add a delay if two trains are at the same index
	delays=0
	max_length = max(len(path) for path in paths)
	
	for station_index in range(max_length):
		stations_at_index = [path[station_index] for path in paths if station_index < len(path)]
		if len(stations_at_index) != len(set(stations_at_index)):
			delays += 1
	return delays


def update_pheromones(pheromones, ants, Q, decay):
	#evaporate pheremone
	pheromones *= (1 - decay)
	for ant in ants:
		for train in range(ant.num_trains):
			for i in range(len(ant.paths[train]) - 1):
				#drop some pheremone based on how fast current path is
				from_station = ant.paths[train][i]
				to_station = ant.paths[train][i + 1]
				pheromones[from_station, to_station] += Q / (ant.total_delays + 1)

def ant_colony_optimization(num_stations, num_trains, num_ants, num_iterations, alpha, beta, decay, Q, mininum_stations):
	initial_pheromone = 1.0 / num_stations
	pheromones = initialize_pheromones(num_stations, initial_pheromone)

	best_paths = None
	best_delays = float('inf')

	for iteration in range(num_iterations):
		ants = [Ant(num_stations, num_trains) for _ in range(num_ants)]

		for ant in ants:
			for train in range(num_trains):
				current_station = randint(0, num_stations - 1)
				ant.visit_station(train, current_station)

				# Constraint: ants must a certain number of stations
				while len(ant.paths[train]) < mininum_stations:
					next_station = choose_next_station(pheromones, current_station, alpha, beta, ant, train)
					ant.visit_station(train, next_station)
					current_station = next_station

			ant.total_delays = calculate_delays(ant.paths, num_stations)

		for ant in ants:
			if ant.total_delays < best_delays:
				best_delays = ant.total_delays
				best_paths = ant.paths

		update_pheromones(pheromones, ants, Q, decay)

	return best_paths, best_delays

def run(stations):
	num_stations = stations
	# Minimum stations each ant should visit in its solution
	# (the number of stations the train needs to service)
	mininum_stations = min(num_stations, (num_stations//3)+2)
	num_trains = (stations//3)+1

	num_ants = 20
	num_iterations = 10

	# Weight that pheremone has on direction decision
	alpha = 2.0

	# Weight that heuristic has on direction decision
	beta = 1.0

	# Decay rate of pheromones >0 && <1
	decay = 0.5

	# Constant used to determine amount of pheromone laid by ants (Q/total_time)
	Q = 100.0

	best_paths, best_delays = ant_colony_optimization(num_stations, num_trains, num_ants, num_iterations, alpha, beta, decay, Q, mininum_stations)

	return f"Best paths: {best_paths}\nTotal delays: {best_delays}"
	
if __name__=='__main__':
	result=run(5)
	print(result)