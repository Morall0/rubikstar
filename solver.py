class Solver:
    def __init__(self):
        self.heuristic_cache = {}
        self.moves = ["U", "U'", "D", "D'", "L", "L'", "R", "R'", "F", "F'", "B", "B'"]
        self.solution = []
        self.nodes_searched = 0

    def get_heuristic(self, cube):
        state = cube.get_state()
        if state in self.heuristic_cache:
            return self.heuristic_cache[state]
        h = cube.heuristic()
        self.heuristic_cache[state] = h
        return h

    def ida_star(self, cube):
        threshold = self.get_heuristic(cube)
        path = []
        while True:
            temp = self.search(cube, 0, threshold, path, None)
            if temp == 'FOUND':
                return path
            if temp == float('inf'):
                return None
            threshold = temp

    def search(self, cube, g, threshold, path, previous_move):
        self.nodes_searched += 1
        f = g + self.get_heuristic(cube)
        if f > threshold:
            return f
        if cube.is_solved():
            return 'FOUND'
        min_cost = float('inf')
        successors = []
        for move in self.moves:
            if previous_move and move[0] == previous_move[0] and ((move.endswith("'") and not previous_move.endswith("'")) or (not move.endswith("'") and previous_move.endswith("'"))):
                continue
            new_cube = cube.clone()
            new_cube.apply_move(move)
            h = self.get_heuristic(new_cube)
            successors.append((h, move, new_cube))
        successors.sort(key=lambda x: x[0])
        for h, move, new_cube in successors:
            path.append(move)
            temp = self.search(new_cube, g + 1, threshold, path, move)
            if temp == 'FOUND':
                return 'FOUND'
            if temp < min_cost:
                min_cost = temp
            path.pop()
        return min_cost