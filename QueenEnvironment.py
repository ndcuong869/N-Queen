import random
from operator import mul    # or mul=lambda x,y:x*y
from fractions import Fraction
from functools import reduce

print('Enter n: ')
size = int(input())


def nCk(n,k):
    return int( reduce(mul, (Fraction(n-i, i+1) for i in range(k)), 1))


def create_matrix(length):
    map = []
    for i in range(length):
        map.append(list())

    for row in range(length):
        for column in range(length):
            map[row].append(0)

    return map


class State:
    def __init__(self):
        self.map = create_matrix(size)
        self.c = 0
        self.h = 0
        self.prev = None
        self.next = None

    def show(self):
        print('---------------')
        for row in range(size):
            print(self.map[row])

    def __lt__(self, other):
        return True


def copy_list(src):
    des = create_matrix(size)
    for row in range(size):
        for column in range(size):
            des[row][column] = src[row][column]
    return des


def find_state(state, new_state):
    temp = state.prev
    while temp is not None:
        if temp.map == new_state.map:
            return True
        temp = temp.prev

    return False


def cal_sum_right_line(arr, row, column):
    sum = 0
    sum += arr[row][column]

    temp_row = row + 1
    temp_column = column + 1

    while -1 < temp_row < size and -1 < temp_column < size:
        sum += arr[temp_row][temp_column]
        temp_row += 1
        temp_column += 1

    return sum


def cal_sum_left_line(arr, row, column):
    sum = 0
    sum += arr[row][column]

    temp_row = row + 1
    temp_column = column - 1
    while -1 < temp_row < size and -1 < temp_column < size:
        sum += arr[temp_row][temp_column]
        temp_row += 1
        temp_column -= 1

    return sum


def cal_sum_row(arr, row):
    sum = 0
    for column in range(size):
        sum += arr[row][column]

    return sum


def check_rows(arr):
    for row in range(size):
        sum = cal_sum_row(arr, row)

        if sum > 1:
            return False

    return True


def check_left_line(arr):
    for row in range(size):
        sum = cal_sum_left_line(arr, row, size - 1)
        if sum > 1:
            return False

    for column in range(size):
        sum = cal_sum_left_line(arr, 0, column)
        if sum > 1:
            return False

    return True


def check_right_line(arr):
    for row in range(size):
        sum = cal_sum_right_line(arr, row, 0)
        if sum > 1:
            return False

    for column in range(size):
        sum = cal_sum_right_line(arr, 0, column)
        if sum > 1:
            return False

    return True


def cal_heuristic(state):
    h = 0
    for row in range(size):
        sum = cal_sum_right_line(state.map, row, 0)
        h += nCk(sum, 2)

    for column in range(1, size):
        sum = cal_sum_right_line(state.map, 0, column)
        h += nCk(sum, 2)

    for row in range(size):
        sum = cal_sum_left_line(state.map, row, size - 1)
        h += nCk(sum, 2)

    for column in range(0, size - 1):
        sum = cal_sum_left_line(state.map, 0, column)
        h += nCk(sum, 2)

    for row in range(size):
        sum = cal_sum_row(state.map, row)
        h += nCk(sum, 2)

    return h


def convert_state_to_string(my_state):
    my_string = ''
    for column in range(size):
        for row in range(size):
            if my_state.map[row][column] == 1:
                my_string += str(row + 1) + ' '
                break
    return my_string


class QueenEnvironment:
    def __init__(self):
        self.current_state = State()

    def random_start_state(self):
        new_state = State()
        for i in range(size):
            row = random.randint(0, size - 1)
            new_state.map[row][i] = 1

        return new_state

    def goal(self, state):
        if not check_right_line(state.map):
            return False
        if not check_left_line(state.map):
            return False
        if not check_rows(state.map):
            return False

        return True

    def action(self, state):
        neighbor_states = []
        for column in range(size):
            for row in range(size):
                if state.map[row][column] == 1:

                    adj_row = []
                    for i in range(size):
                        adj_row.append(i)

                    adj_row.remove(row)

                    for new_row in adj_row:
                        new_state = State()
                        new_state.map = copy_list(state.map)
                        new_state.map[row][column] = 0
                        new_state.map[new_row][column] = 1

                        if not find_state(state, new_state):
                            new_state.prev = state
                            new_state.c = state.c + 1
                            new_state.h = cal_heuristic(new_state)
                            neighbor_states.append(new_state)
                    break

        print(len(neighbor_states))
        return neighbor_states
