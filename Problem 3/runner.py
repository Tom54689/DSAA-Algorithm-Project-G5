import math

class Runner:
    def __init__(self, pos, e):
        self.position = pos
        self.end = e

        self.hscore = float(math.inf)
        self.gscore = 0
        self.fscore = float(math.inf)
        self.log = [self.position]

    def tile_to_score(self, id):
        t2s = {
            0: 1,
            2: 1,
            3: 1,
            4: 2,
            5: 4,
            6: 0.5,
            7: 0
        }
        return t2s[id]

    def calculate_hscore(self):
        return manhattan_distance(self.position, self.end)

    def find_paths(self, map):
        vectors = []
        for vector in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_pos = add_tuple(self.position, vector)
            if new_pos in map.keys() and map[new_pos] != 1: #check if blocked and exists
                vectors.append(vector)

        return vectors

    def move(self, vector, map):
        new_pos = add_tuple(self.position, vector)
        if not new_pos in map.keys() or map[new_pos] == 1:
            raise ValueError("Position {} not found in map".format(new_pos))
            return
        
        self.position = new_pos
        self.gscore += self.tile_to_score(map[new_pos])
        self.hscore = self.calculate_hscore()
        self.fscore = self.gscore + self.hscore

        self.log.append(self.position)
        
    
def add_tuple(tuple1, tuple2):
    return tuple(x + y for x, y in zip(tuple1, tuple2))

def manhattan_distance(start, end):
    return abs(end[1] - start[1]) + abs(end[0] - start[0])