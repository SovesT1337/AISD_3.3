import fileinput


class Item:
    def __init__(self, weight: int, cost: int):
        self.weight = weight
        self.cost = cost
        self.cost_scaled = cost


class Bag:
    def __init__(self):
        self.__e = 0
        self.__max_mass = 0
        self.__items = list()
        self.__max_cost = 0

    def init(self, e, max_mass_):
        self.__e = e
        self.__max_mass = max_mass_

    def add_item(self, w, c):
        if w <= self.__max_mass:
            self.__items.append(Item(w, c))
            self.__max_cost = max(c, self.__max_cost)
        if w > self.__max_mass:
            self.__items.append(Item(0, 0))

    def solve(self):
        if not self.__items:
            return list(), 0, 0
        scale = self.__e * self.__max_cost / (len(self.__items) * (1 + self.__e))
        sols = {0: [list(), 0, 0]}
        for i_ in range(len(self.__items)):
            if self.__items[i_].cost != 0:
                self.__items[i_].cost_scaled = int(self.__items[i_].cost / scale)
                for sol in list(sols.values()):
                    new_weight, new_cost = sol[1] + self.__items[i_].weight, sol[2] + self.__items[i_].cost_scaled
                    if new_weight > self.__max_mass:
                        continue
                    if new_cost not in sols or new_weight < sols[new_cost][1]:
                        sols[new_cost] = [sol[0] + [i_], new_weight, new_cost]

        best = sols.get(max(sols.keys()))
        best[2] = 0
        for i_ in best[0]:
            best[2] += self.__items[i_].cost
        return best


if __name__ == '__main__':
    bag = Bag()
    e_ = float(input())
    max_mass = int(input())
    bag.init(e_, max_mass)
    for line in fileinput.input():
        if line != '\n':
            s = line.strip().split(' ')
            bag.add_item(int(s[0]), int(s[1]))
    solution = bag.solve()
    print(solution[1], solution[2])
    for id in solution[0]:
        print(id + 1)