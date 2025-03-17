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
    
    # Definición de las posiciones de las aristas
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
        self.cube = [
            [RubikCube.CENTERS[i]] * 9 for i in range(6)
        ]
    
    def print_cube(self):
        labels = ['U', 'D', 'L', 'R', 'F', 'B']
        for i, face in enumerate(self.cube):
            print(f"{labels[i]}: {face}")
    
    def clone(self):
        new_cube = RubikCube()
        new_cube.cube = copy.deepcopy(self.cube)
        return new_cube
    
    def get_state(self):
        return tuple(tuple(face) for face in self.cube)
    
    def is_solved(self):
        return all(all(sticker == face[0] for sticker in face) for face in self.cube)
    
    def rotate_face(self, face, clockwise=True):
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
        new_face = face[:]
        if times == 0:
            return new_face
        times = times % 4
        for _ in range(times):
            new_face = [new_face[6], new_face[3], new_face[0],
                        new_face[7], new_face[4], new_face[1],
                        new_face[8], new_face[5], new_face[2]]
        return new_face
    
    
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
            temp = self.cube[0][6:9]  # Fila inferior de U
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
            temp = self.cube[0][0:3]  # Fila superior de U
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
    
    
    #Esquinas y aristas mal colocadas
    def heuristic(self):
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
    
    
    #Aprovecha simetría
    def rotate_cube_y(self, clockwise=True):
        new_cube = RubikCube()
        new_cube.cube[0] = self.cube[0][:]
        new_cube.cube[1] = self.cube[1][:]
        if clockwise:
            new_cube.cube[4] = RubikCube.rotate_face_list(self.cube[2], 1)
            # Nueva R = antigua F
            new_cube.cube[3] = RubikCube.rotate_face_list(self.cube[4], 1)
            # Nueva B = antigua R
            new_cube.cube[5] = RubikCube.rotate_face_list(self.cube[3], 1)
            # Nueva L = antigua B
            new_cube.cube[2] = RubikCube.rotate_face_list(self.cube[5], 1)
        else:
            new_cube.cube[4] = RubikCube.rotate_face_list(self.cube[3], 3)
            new_cube.cube[3] = RubikCube.rotate_face_list(self.cube[5], 3)
            new_cube.cube[5] = RubikCube.rotate_face_list(self.cube[2], 3)
            new_cube.cube[2] = RubikCube.rotate_face_list(self.cube[4], 3)
        return new_cube
    
    def canonical_state(self):
        states = []
        current = self.clone()
        for _ in range(4):
            states.append(current.get_state())
            current = current.rotate_cube_y(clockwise=True)
        return min(states)