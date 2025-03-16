from cubo import Cube

class Solver:
    def __init__(self, cube):
        self.initial_cube = cube
        self.moves = ["U", "U'", "D", "D'", "L", "L'", "R", "R'", "F", "F'", "B", "B'"]
        self.cache = {} 
    
    def heuristic(self, cube):
        return sum(
            1
            for face in cube.face.values()
            for row in face
            for cell in row
            if cell != face[1][1]  
        )
    
    def is_solved(self, cube):
        solved_state = Cube().state_key()  
        return cube.state_key() == solved_state
    
    def copy_cube(self, cube):
        new_cube = Cube()
        new_cube.face = {k: [row[:] for row in v] for k, v in cube.face.items()}
        return new_cube
    
    def inverse_move(self, move):
        return move[:-1] if move.endswith("'") else move + "'"
    
    def apply_move(self, cube, move):
        try:
            if move == "U":
                cube.rotate_top_clockwise()
            elif move == "U'":
                cube.rotate_top_counterclockwise()
            elif move == "D":
                cube.rotate_bottom_clockwise()
            elif move == "D'":
                cube.rotate_bottom_counterclockwise()
            elif move == "L":
                cube.rotate_left_clockwise()
            elif move == "L'":
                cube.rotate_left_counterclockwise()
            elif move == "R":
                cube.rotate_right_clockwise()
            elif move == "R'":
                cube.rotate_right_counterclockwise()
            elif move == "F":
                cube.rotate_front_clockwise()
            elif move == "F'":
                cube.rotate_front_counterclockwise()
            elif move == "B":
                cube.rotate_back_clockwise()
            elif move == "B'":
                cube.rotate_back_counterclockwise()
            else:
                raise ValueError(f"Movimiento no válido: {move}")
        except Exception as e:
            print(f"Error al aplicar el movimiento {move}: {e}")
    
    def canonical_key(self, cube):
        rotations = [cube.state_key()]
        for _ in range(3):
            new_cube = self.copy_cube(cube)
            new_cube.rotate_top_clockwise()
            rotations.append(new_cube.state_key())
        return min(rotations)  
    
    def search(self, cube, g, threshold, path, last_move):
        key = self.canonical_key(cube)
        if key in self.cache and self.cache[key] <= g:
            return float('inf')
        self.cache[key] = g
        
        f = g + self.heuristic(cube)
        if f > threshold:
            return f
        if self.is_solved(cube):
            return path
        
        min_cost = float('inf')
        children = []
        for move in self.moves:
            if last_move and (move == self.inverse_move(last_move) or move == last_move):
                continue 
            new_cube = self.copy_cube(cube)
            self.apply_move(new_cube, move)
            h = self.heuristic(new_cube)
            children.append((h, move, new_cube))
        children.sort(key=lambda x: x[0])
        
        for h, move, new_cube in children:
            path.append(move)
            temp = self.search(new_cube, g + 1, threshold, path, move)
            if isinstance(temp, list):
                return temp
            if temp < min_cost:
                min_cost = temp
            path.pop()
        return min_cost
    
    def solve(self):
        threshold = self.heuristic(self.initial_cube)
        path = []
        while True:
            self.cache = {} 
            temp = self.search(self.initial_cube, 0, threshold, path, None)
            if isinstance(temp, list):
                return temp
            if temp == float('inf'):
                return None
            threshold = temp