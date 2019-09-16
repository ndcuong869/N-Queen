from QueenEnvironment import cal_heuristic
from QueenEnvironment import size
from itertools import combinations
import random
import time
from QueenEnvironment import State
from QueenEnvironment import nCk
import QueenEnvironment
import queue


class UCS:
    def __init__(self, start_state, goal, action):
        self.goal = goal
        self.states = queue.PriorityQueue()
        self.start_state = start_state
        self.action = action
        self.states.put((start_state.c, start_state))

    def is_goal(self, state):
        if self.goal is not None:
            return self.goal(state)

    def push_to_queue(self, new_states):
        for state in new_states:
            self.states.put((state.c, state))

    def search(self):
        (value, best_state) = self.states.get()
        start = time.process_time()
        count = 1
        while not self.is_goal(best_state):
            neighbor_states = self.action(best_state)
            self.push_to_queue(neighbor_states)
            if not self.states.empty():
                (value, best_state) = self.states.get()
                print('---------------------')
                print('Time %s' % count)
                print('C = %s' % best_state.c)
                print('Length of queue = %s' % self.states.qsize())
                count += 1
            else:
                return None

        duration = time.process_time() - start
        print(duration)
        return best_state


class AStar:
    def __init__(self, start_state, goal, action):
        self.goal = goal
        self.states = queue.PriorityQueue()
        self.start_state = start_state
        self.action = action
        self.states.put((start_state.c + start_state.h, start_state))

    def is_goal(self, state):
        if self.goal is not None:
            return self.goal(state)

    def push_to_queue(self, new_states):
        for state in new_states:
            self.states.put((state.c + state.h, state))

    def search(self):
        (value, best_state) = self.states.get()
        start = time.process_time()
        count = 1
        while not self.is_goal(best_state):
            neighbor_states = self.action(best_state)
            self.push_to_queue(neighbor_states)
            if not self.states.empty():
                (value, best_state) = self.states.get()
                print('---------------------')
                print('Time %s' % count)
                print('H = %s' % best_state.h)
                print('C = %s' % best_state.c)
                print('Length of queue = %s' % self.states.qsize())
                count += 1
            else:
                return None

        duration = time.process_time() - start
        print(duration)
        return best_state


def get_neighbor_highest(states):
    state = states.pop()
    min = cal_heuristic(state)

    for other in states:
        if cal_heuristic(other) < min:
            min = cal_heuristic(other)
            state = other

    return state


class Hill_climbing:
    def __init__(self, env):
        self.current_state = env.current_state
        self.current_state.h = cal_heuristic(self.current_state)
        self.goal = env.goal
        self.action = env.action
        self.env = env

    def search(self):
        start = time.process_time()
        count = 1
        while True:
            neighbor_states = self.action(self.current_state)

            if len(neighbor_states) < 1:
                print('Restart len 0')
                self.current_state = self.env.random_start_state()
                neighbor_states = self.action(self.current_state)

            highest_state = get_neighbor_highest(neighbor_states)
            highest_state.h = cal_heuristic(highest_state)
            self.current_state.h = cal_heuristic(self.current_state)
            if highest_state.h > self.current_state.h or self.goal(self.current_state):
                if self.current_state.h == 0:
                    self.current_state.show()
                    cal_heuristic(self.current_state)
                if self.goal(self.current_state):
                    duration = time.process_time() - start
                    print(duration)
                    return self.current_state
                else:
                    print('Restart stuck')
                    self.current_state = self.env.random_start_state()
            else:
                self.current_state = highest_state
                self.current_state.h = cal_heuristic(self.current_state)

            print('---------------------')
            print('Time %s' % count)
            print('H = %s' % self.current_state.h)
            count += 1


def random_selection(population):
    fitnessList = []

    for state in population:
        fitnessList.append(nCk(size, 2) - cal_heuristic(state))

    probaList = []
    total = sum(fitnessList)
    first = 0
    second = 0

    for item in fitnessList:
        probaList.append(item / total)

    for i in range(len(probaList)):
        if i > 0:
            probaList[i] += probaList[i - 1]

    random_value = random.uniform(0, 1)

    for i in range(len(probaList)):
        if random_value < probaList[i]:
            first = i
            break

    random_value = random.uniform(0, 1)

    for i in range(len(probaList)):
        if random_value < probaList[i]:
            second = i
            break

    return population[first], population[second]


def reproduce(father, mother):
    child_h = min([father.h, mother.h])
    child = State()
    for i in range(5):
        child = State()
        c = random.randint(0, size - 1)

        for column in range(c):
            for row in range(size):
                if father.map[row][column] == 1:
                    child.map[row][column] = 1
                    break

        for column in range(c, size):
            for row in range(size):
                if mother.map[row][column] == 1:
                    child.map[row][column] = 1
                    break

        child.h = cal_heuristic(child)

        if child.h < child_h:
            break

    return child


def mutate(child):
    number_mutate = random.randint(0, size / 2)

    for i in range(number_mutate):
        row = random.randint(0, size - 1)
        column = random.randint(0, size - 1)

        for i in range(size):
            if child.map[i][column] == 1:
                child.map[i][column] = 0
                break
        child.map[row][column] = 1

    return child


class Genetic:
    def __init__(self, states, state_size):
        self.states = states
        self.state_size = state_size

    def is_best_individual(self):
        for state in self.states:
            if cal_heuristic(state) == 0:
                return True

        return False

    def search(self):
        count = 1
        print(nCk(size, 2))
        start = time.process_time()

        while not self.is_best_individual():
            fitness = ''
            new_states = []
            avg = 0
            print('Time %s' % count)
            for i in range(self.state_size):
                father, mother = random_selection(self.states)

                child = reproduce(father, mother)
                if random.uniform(0, 1) < 0.3:
                    child = mutate(child)
                new_states.append(child)
                child.h = cal_heuristic(child)
                avg += child.h
                fitness += str(child.h) + ' '

            avg = avg / self.state_size
            list_childs = []
            for item in new_states:
                if item.h <= avg:
                    list_childs.append(item)

            print(fitness)
            self.states = list_childs
            count += 1

        duration = time.process_time() - start
        print(duration)
        for state in self.states:
            if cal_heuristic(state) == 0:
                return state

        return None


def print_board(state):
    line = ''
    for i in range(size):
        line += ' - '
    print(line)

    for row in range(size):
        line = ''
        for column in range(size):
            if state.map[row][column] == 1:
                line += '|x|'
            else:
                line += '| |'
        print(line)

        line = ''
        for i in range(size):
            line += ' - '
        print(line)


env = QueenEnvironment.QueenEnvironment()

env.current_state = env.random_start_state()
env.current_state.show()

print('1. UCS')
print('2. A*')
print('3. Random restart Hill-climbing')
print('4. Genetic Algorithm')

choose = int(input())

agent = UCS(env.current_state, env.goal, env.action)
if choose == 1:
    agent = UCS(env.current_state, env.goal, env.action)
elif choose == 2:
    agent = AStar(env.current_state, env.goal, env.action)
elif choose == 3:
    agent = Hill_climbing(env)
elif choose == 4:
    state_list = []
    for i in range(20):
        state_list.append(env.random_start_state())

    agent = Genetic(state_list, 30)

#agent = Hill_climbing(env)
#agent = AStar(env.current_state, env.goal, env.action)
#agent = UCS(env.current_state, env.goal, env.action)

#agent = Genetic(state_list, 30)

solution = agent.search()

state = solution
state.show()

result = ''
for column in range(size):
    for row in range(size):
        if state.map[row][column] == 1:
            result += str(row + 1) + ' '
            break

print(result)