import copy

class RubikCube:
    # Colores fijos de las caras resueltas (orden: U, D, L, R, F, B)
    CENTERS = ['W', 'Y', 'B', 'G', 'R', 'O']
    
    # Definición de las posiciones de las esquinas (cada una con 3 stickers)
    # Usamos la convención de cada cara como lista de 9 elementos (índices 0..8):
    # 0 1 2
    # 3 4 5
    # 6 7 8
    CORNER_INDICES = [
        ((0,8), (4,2), (3,0)),  # UFR
        ((0,6), (2,2), (4,0)),  # UFL
        ((0,0), (5,2), (2,0)),  # UBL
        ((0,2), (3,2), (5,0)),  # UBR
        ((1,2), (3,6), (4,8)),  # DFR
        ((1,0), (4,6), (2,8)),  # DFL
        ((1,6), (2,6), (5,8)),  # DBL
        ((1,8), (5,6), (3,8))   # DBR
    ]
    
    # Definición de las posiciones de las aristas (cada una con 2 stickers)
    EDGE_INDICES = [
        ((0,7), (4,1)),   # UF
        ((0,5), (3,1)),   # UR
        ((0,1), (5,1)),   # UB
        ((0,3), (2,1)),   # UL
        ((4,5), (3,3)),   # FR
        ((4,3), (2,5)),   # FL
        ((5,3), (2,7)),   # BL
        ((5,5), (3,7)),   # BR
        ((1,1), (4,7)),   # DF
        ((1,5), (3,5)),   # DR
        ((1,7), (5,7)),   # DB
        ((1,3), (2,3))    # DL
    ]
    
    def __init__(self):
        # Representación interna: lista de 6 caras, cada una con 9 stickers.
        # Orden de caras: 0: U, 1: D, 2: L, 3: R, 4: F, 5: B.
        self.cube = [ [RubikCube.CENTERS[i]] * 9 for i in range(6) ]
    
    def print_cube(self):
        labels = ['U', 'D', 'L', 'R', 'F', 'B']
        for i, face in enumerate(self.cube):
            print(f"{labels[i]}: {face}")
    
    def clone(self):
        new_cube = RubikCube()
        new_cube.cube = copy.deepcopy(self.cube)
        return new_cube
    
    def get_state(self):
        # Representación inmutable del estado (tupla de tuplas)
        return tuple(tuple(face) for face in self.cube)
    
    def is_solved(self):
        # El cubo está resuelto si cada cara tiene todos los stickers iguales.
        return all(all(sticker == face[0] for sticker in face) for face in self.cube)
    
    def rotate_face(self, face, clockwise=True):
        # Rota una cara (lista de 9 elementos) 90° en sentido horario o antihorario.
        if clockwise:
            self.cube[face] = [
                self.cube[face][6], self.cube[face][3], self.cube[face][0],
                self.cube[face][7], self.cube[face][4], self.cube[face][1],
                self.cube[face][8], self.cube[face][5], self.cube[face][2]
            ]
        else:
            self.cube[face] = [
                self.cube[face][2], self.cube[face][5], self.cube[face][8],
                self.cube[face][1], self.cube[face][4], self.cube[face][7],
                self.cube[face][0], self.cube[face][3], self.cube[face][6]
            ]
    
    @staticmethod
    def rotate_face_list(face, times=1):
        # Rota una lista que representa una cara 'times' veces 90° en sentido horario.
        new_face = face[:]
        if times == 0:
            return new_face
        times = times % 4
        for _ in range(times):
            new_face = [new_face[6], new_face[3], new_face[0],
                        new_face[7], new_face[4], new_face[1],
                        new_face[8], new_face[5], new_face[2]]
        return new_face
    
    # Movimientos del cubo (cada uno admite rotación en sentido horario y antihorario)
    def move_U(self, clockwise=True):
        self.rotate_face(0, clockwise)
        if clockwise:
            temp = self.cube[4][:3]
            self.cube[4][:3] = self.cube[3][:3]
            self.cube[3][:3] = self.cube[5][:3]
            self.cube[5][:3] = self.cube[2][:3]
            self.cube[2][:3] = temp
        else:
            temp = self.cube[4][:3]
            self.cube[4][:3] = self.cube[2][:3]
            self.cube[2][:3] = self.cube[5][:3]
            self.cube[5][:3] = self.cube[3][:3]
            self.cube[3][:3] = temp
    
    def move_D(self, clockwise=True):
        self.rotate_face(1, clockwise)
        if clockwise:
            temp = self.cube[4][6:]
            self.cube[4][6:] = self.cube[2][6:]
            self.cube[2][6:] = self.cube[5][6:]
            self.cube[5][6:] = self.cube[3][6:]
            self.cube[3][6:] = temp
        else:
            temp = self.cube[4][6:]
            self.cube[4][6:] = self.cube[3][6:]
            self.cube[3][6:] = self.cube[5][6:]
            self.cube[5][6:] = self.cube[2][6:]
            self.cube[2][6:] = temp
    
    def move_L(self, clockwise=True):
        self.rotate_face(2, clockwise)
        if clockwise:
            temp = [self.cube[0][0], self.cube[0][3], self.cube[0][6]]
            self.cube[0][0], self.cube[0][3], self.cube[0][6] = self.cube[5][8], self.cube[5][5], self.cube[5][2]
            self.cube[5][8], self.cube[5][5], self.cube[5][2] = self.cube[1][0], self.cube[1][3], self.cube[1][6]
            self.cube[1][0], self.cube[1][3], self.cube[1][6] = self.cube[4][0], self.cube[4][3], self.cube[4][6]
            self.cube[4][0], self.cube[4][3], self.cube[4][6] = temp
        else:
            temp = [self.cube[0][0], self.cube[0][3], self.cube[0][6]]
            self.cube[0][0], self.cube[0][3], self.cube[0][6] = self.cube[4][0], self.cube[4][3], self.cube[4][6]
            self.cube[4][0], self.cube[4][3], self.cube[4][6] = self.cube[1][0], self.cube[1][3], self.cube[1][6]
            self.cube[1][0], self.cube[1][3], self.cube[1][6] = self.cube[5][8], self.cube[5][5], self.cube[5][2]
            self.cube[5][8], self.cube[5][5], self.cube[5][2] = temp
    
    def move_R(self, clockwise=True):
        self.rotate_face(3, clockwise)
        if clockwise:
            temp = [self.cube[0][2], self.cube[0][5], self.cube[0][8]]
            self.cube[0][2], self.cube[0][5], self.cube[0][8] = self.cube[4][2], self.cube[4][5], self.cube[4][8]
            self.cube[4][2], self.cube[4][5], self.cube[4][8] = self.cube[1][2], self.cube[1][5], self.cube[1][8]
            self.cube[1][2], self.cube[1][5], self.cube[1][8] = [self.cube[5][6], self.cube[5][3], self.cube[5][0]]
            self.cube[5][6], self.cube[5][3], self.cube[5][0] = temp
        else:
            temp = [self.cube[0][2], self.cube[0][5], self.cube[0][8]]
            self.cube[0][2], self.cube[0][5], self.cube[0][8] = [self.cube[5][6], self.cube[5][3], self.cube[5][0]]
            self.cube[5][6], self.cube[5][3], self.cube[5][0] = self.cube[1][2], self.cube[1][5], self.cube[1][8]
            self.cube[1][2], self.cube[1][5], self.cube[1][8] = self.cube[4][2], self.cube[4][5], self.cube[4][8]
            self.cube[4][2], self.cube[4][5], self.cube[4][8] = temp
    
    def move_F(self, clockwise=True):
        self.rotate_face(4, clockwise)
        if clockwise:
            temp = self.cube[0][6:9]
            self.cube[0][6], self.cube[0][7], self.cube[0][8] = self.cube[2][8], self.cube[2][5], self.cube[2][2]
            self.cube[2][8], self.cube[2][5], self.cube[2][2] = self.cube[1][2], self.cube[1][1], self.cube[1][0]
            self.cube[1][2], self.cube[1][1], self.cube[1][0] = self.cube[3][0], self.cube[3][3], self.cube[3][6]
            self.cube[3][0], self.cube[3][3], self.cube[3][6] = temp
        else:
            temp = self.cube[0][6:9]
            self.cube[0][6], self.cube[0][7], self.cube[0][8] = self.cube[3][0], self.cube[3][3], self.cube[3][6]
            self.cube[3][0], self.cube[3][3], self.cube[3][6] = self.cube[1][2], self.cube[1][1], self.cube[1][0]
            self.cube[1][2], self.cube[1][1], self.cube[1][0] = self.cube[2][8], self.cube[2][5], self.cube[2][2]
            self.cube[2][8], self.cube[2][5], self.cube[2][2] = temp
    
    def move_B(self, clockwise=True):
        self.rotate_face(5, clockwise)
        if clockwise:
            temp = self.cube[0][0:3]
            self.cube[0][0], self.cube[0][1], self.cube[0][2] = self.cube[3][2], self.cube[3][5], self.cube[3][8]
            self.cube[3][2], self.cube[3][5], self.cube[3][8] = self.cube[1][8], self.cube[1][7], self.cube[1][6]
            self.cube[1][8], self.cube[1][7], self.cube[1][6] = self.cube[2][0], self.cube[2][3], self.cube[2][6]
            self.cube[2][0], self.cube[2][3], self.cube[2][6] = temp
        else:
            temp = self.cube[0][0:3]
            self.cube[0][0], self.cube[0][1], self.cube[0][2] = self.cube[2][0], self.cube[2][3], self.cube[2][6]
            self.cube[2][0], self.cube[2][3], self.cube[2][6] = self.cube[1][8], self.cube[1][7], self.cube[1][6]
            self.cube[1][8], self.cube[1][7], self.cube[1][6] = self.cube[3][2], self.cube[3][5], self.cube[3][8]
            self.cube[3][2], self.cube[3][5], self.cube[3][8] = temp
    
    def apply_move(self, move):
        if move.endswith("'"):
            clockwise = False
            move = move[0]
        else:
            clockwise = True
        
        if move == 'U':
            self.move_U(clockwise)
        elif move == 'D':
            self.move_D(clockwise)
        elif move == 'L':
            self.move_L(clockwise)
        elif move == 'R':
            self.move_R(clockwise)
        elif move == 'F':
            self.move_F(clockwise)
        elif move == 'B':
            self.move_B(clockwise)
        else:
            raise ValueError(f"Movimiento desconocido: {move}")
    
    def heuristic(self):
        # Heurística: cuenta el número de esquinas y aristas mal colocadas.
        h = 0
        for corner in RubikCube.CORNER_INDICES:
            colors = [self.cube[face][idx] for (face, idx) in corner]
            expected = {RubikCube.CENTERS[face] for (face, _) in corner}
            if set(colors) != expected:
                h += 1
        for edge in RubikCube.EDGE_INDICES:
            colors = [self.cube[face][idx] for (face, idx) in edge]
            expected = {RubikCube.CENTERS[face] for (face, _) in edge}
            if set(colors) != expected:
                h += 1
        return h

class Solver:
    def __init__(self):
        self.moves = ["U", "U'", "D", "D'", "L", "L'", "R", "R'", "F", "F'", "B", "B'"]
        self.nodes_searched = 0
        self.heuristic_cache = {}  # Memoria cache agregada
    
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
            temp = self.search(cube, 0, threshold, path)
            if temp == 'FOUND':
                return path
            if temp == float('inf'):
                return None
            threshold = temp
    
    def search(self, cube, g, threshold, path):
        self.nodes_searched += 1
        f = g + self.get_heuristic(cube)
        if f > threshold:
            return f
        if cube.is_solved():
            return 'FOUND'
        min_cost = float('inf')
        for move in self.moves:
            new_cube = cube.clone()
            new_cube.apply_move(move)
            path.append(move)
            temp = self.search(new_cube, g + 1, threshold, path)
            if temp == 'FOUND':
                return 'FOUND'
            if temp < min_cost:
                min_cost = temp
            path.pop()
        return min_cost

if __name__ == '__main__':
    cube = RubikCube()
    scramble = ["R", "U", "R'", "U'"]
    print("Estado inicial (resuelto):")
    cube.print_cube()
    
    print("\nAplicando scramble:", scramble)
    for move in scramble:
        cube.apply_move(move)
    cube.print_cube()
    
    solver = Solver()
    print("\nBuscando solución...")
    solution = solver.ida_star(cube)
    if solution is not None:
        print("Solución encontrada:", solution)
        print("Nodos expandidos:", solver.nodes_searched)
    else:
        print("No se encontró solución.")

