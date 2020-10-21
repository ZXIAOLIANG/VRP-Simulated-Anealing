import numpy as np
import math
from random import randint
from itertools import combinations
import copy
import random
import operator

def construct_distance_matrix(coordinate_list):
    Distance = [[0 for x in range(len(coordinate_list))] for y in range(len(coordinate_list))]
    for i in range(len(coordinate_list)):
        for j in range(len(coordinate_list)):
            if i < j:
                # we only need to calulate the upper triangle
                # calculate Euclidean distance
                Distance[i][j] = math.sqrt((coordinate_list[i][0] - coordinate_list[j][0])**2 
                                            + (coordinate_list[i][1] - coordinate_list[j][1])**2)
    return Distance

def construct_initial_solution(places, trucks):
    initial_solution = [x for x in range(places)]

    random.shuffle(initial_solution)
    x = randint(2, len(initial_solution)-2)
    for i in range(trucks - 2):
        while True:
            if initial_solution[x-1] == 0 or initial_solution[x] == 0:
                x = randint(2, len(initial_solution)-1)
                continue
            else:
                break
        # a valid solution start with 0 (depot)
        initial_solution.insert(x, 0)
    initial_solution.insert(0, 0)
    return initial_solution



class SA:
    def __init__(self,alpha, initial_temp, initial_solution, max_iteration, temp_itr, 
                 final_temp, Distance, Service):
        self.alpha = alpha
        self.initial_temp = initial_temp
        self.initial_solution = initial_solution
        self.current_solution = self.initial_solution
        self.current_temp = self.initial_temp
        self.max_iteration = max_iteration
        self.temp_itr = temp_itr
        self.final_temp = final_temp
        self.Distance = Distance
        self.Service = Service
        self.current_cost = self.calculate_cost(self.current_solution)
        self.neighbourhood = list(combinations([x+1 for x in range(len(initial_solution)-1)],2))
        random.shuffle(self.neighbourhood)

    def check_consecutive_zero(self, solution):
        for i in range(len(solution)):
            if solution[i] == 0 and i == len(solution) - 1:
                return True
            if solution[i] == 0 and solution[i+1] == 0:
                return True
        return False

    def swap(self, solution, swap):
        if min(swap[0],swap[1]) == 0:
            print("invalid swap!!!!!")
            return
        new_solution = copy.deepcopy(solution)
        temp = new_solution[swap[0]]
        new_solution[swap[0]] = new_solution[swap[1]]
        new_solution[swap[1]] = temp
        return new_solution

    def select_new_solution(self):
        rand_index = randint(0,len(self.neighbourhood)-1)
        new_solution  = self.swap(self.current_solution, self.neighbourhood[rand_index])
        while True:
            if self.check_consecutive_zero(new_solution):
                rand_index = randint(0,len(self.neighbourhood)-1)
                new_solution  = self.swap(self.current_solution, self.neighbourhood[rand_index])
                continue
            else:
                break
        return new_solution

    def cooling(self):
        self.current_temp = self.alpha*self.current_temp

    def run(self):
        count = 0
        while True:
            for i in range(self.temp_itr):
                count += 1
                new_solution = self.select_new_solution()
                new_cost = self.calculate_cost(new_solution)
                delta_C = new_cost - self.current_cost
                if delta_C < 0:
                    self.current_solution = new_solution
                    self.current_cost = new_cost
                else:
                    x = random.random() # random number from [0,1)
                    if x < np.exp(-delta_C/self.current_temp):
                        # accept the solution
                        self.current_solution = new_solution
                        self.current_cost = new_cost
            
            self.cooling()
            if self.current_temp <= self.final_temp:
                print("current temp: {}".format(self.current_temp))
                print("final temp reached")
                break
        return self.current_cost, self.current_solution

    def calculate_cost(self, solution):
        cost = 0
        for i in range(len(solution)):
            if i < len(solution) - 1:
                cost += self.Distance[min(solution[i], solution[i+1])][max(solution[i], solution[i+1])]
            else:
                cost += self.Distance[min(solution[i], 0)][max(solution[i], 0)]
        return cost + sum(self.Service)



if __name__ == "__main__":
    vrp_file = "A-n39-k6.vrp"
    vrp_sol = "opt-A-n39-k6"
    coordinate_list = []
    Service = []
    num_of_truck = 6
    solution = [0, 37, 31, 14, 35, 25, 33, 19, 2, 0, 26, 11, 0, 24, 3, 38, 12, 9, 28, 29, 5, 0, 15, 30, 13, 0, 18, 27, 10, 16, 4, 8, 7, 0, 6, 1, 36, 17, 23, 21, 22, 34, 32, 20]
    # print(solution)
    with open(vrp_file) as fp:
        line = fp.readline()
        while line:
            # print(line)
            if line.strip() == "NODE_COORD_SECTION":
                while True:
                    line = fp.readline()
                    if line.strip() == "DEMAND_SECTION":
                        break
                    coordinate_list.append((int(line.split()[1]), int(line.split()[2])))
            if line.strip() == "DEMAND_SECTION":
                while True:
                    line = fp.readline()
                    if line.strip() == "DEPOT_SECTION":
                        break
                    Service.append(int(line.split()[1]))
            line = fp.readline()
    
    Distance = construct_distance_matrix(coordinate_list)

    initial_solution = construct_initial_solution(len(coordinate_list), num_of_truck)
    alpha = 0.9
    initial_temp = 10000
    max_iteration = 1000
    temp_itr = 1000
    final_temp = 0.1
    sa = SA(alpha, initial_temp, initial_solution, max_iteration, temp_itr, final_temp, Distance, Service)
    optimal_cost, optimal_solution = sa.run()
    print("initial solution: {}".format(sa.initial_solution))
    print("alpha: {}".format(alpha))
    print("initial_temp: {}".format(initial_temp))
    print("temp_itr: {}".format(temp_itr))
    print("final_temp: {}".format(final_temp))
    print("optimal cost: {}".format(optimal_cost))
    print("optimal solution: {}".format(optimal_solution))
