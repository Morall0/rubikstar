import copy
import random

# --- Helpers para manipulación de bits de esquinas y aristas ---
def get_corner(corners, i):
    """Extrae los 5 bits (3 para permutación, 2 para orientación) de la esquina i."""
    val = (corners >> (5 * i)) & 0x1F  # 5 bits
    perm = val & 0x7        # bits 0-2
    ori = (val >> 3) & 0x3    # bits 3-4 (valores 0,1,2)
    return perm, ori

def set_corner(corners, i, perm, ori):
    """Fija la esquina i con permutación y orientación en el entero 'corners'."""
    mask = ~(0x1F << (5 * i))
    corners &= mask
    val = (ori << 3) | perm
    corners |= (val << (5 * i))
    return corners

def get_edge(edges, i):
    """Extrae los 5 bits de la arista i: 4 para permutación y 1 para orientación."""
    val = (edges >> (5 * i)) & 0x1F
    perm = val & 0xF        # bits 0-3
    ori = (val >> 4) & 0x1    # bit 4
    return perm, ori

def set_edge(edges, i, perm, ori):
    """Fija la arista i con permutación y orientación en el entero 'edges'."""
    mask = ~(0x1F << (5 * i))
    edges &= mask
    val = (ori << 4) | perm
    edges |= (val << (5 * i))
    return edges

# --- Definición de las transformaciones para cada movimiento ---
# Cada entrada de MOVE_TABLE contiene:
#   - 'corner_cycle': lista de tuplas (dest, src, twist_delta)
#       -> El cubie de la esquina en posición 'src' se mueve a la posición 'dest'
#          y su orientación se ajusta sumándole twist_delta (mod 3).
#   - 'edge_cycle': lista de tuplas (dest, src, flip)
#       -> El cubie de arista en posición 'src' se mueve a 'dest'
#          y si flip es True se le cambia la orientación (XOR con 1).
MOVE_TABLE = {
    'U': {
        'corner_cycle': [(0, 1, 0), (1, 2, 0), (2, 3, 0), (3, 0, 0)],
        'edge_cycle':   [(0, 3, False), (1, 0, False), (2, 1, False), (3, 2, False)]
    },
    "U'": {
        'corner_cycle': [(0, 3, 0), (1, 0, 0), (2, 1, 0), (3, 2, 0)],
        'edge_cycle':   [(0, 1, False), (1, 2, False), (2, 3, False), (3, 0, False)]
    },
    'D': {
        'corner_cycle': [(4, 7, 0), (5, 4, 0), (6, 5, 0), (7, 6, 0)],
        'edge_cycle':   [(8, 11, False), (9, 8, False), (10, 9, False), (11, 10, False)]
    },
    "D'": {
        'corner_cycle': [(4, 5, 0), (5, 6, 0), (6, 7, 0), (7, 4, 0)],
        'edge_cycle':   [(8, 9, False), (9, 10, False), (10, 11, False), (11, 8, False)]
    },
    'R': {
        'corner_cycle': [(0, 3, 1), (3, 7, -1), (7, 4, -1), (4, 0, 1)],
        'edge_cycle':   [(1, 4, False), (4, 9, False), (9, 7, False), (7, 1, False)]
    },
    "R'": {
        'corner_cycle': [(0, 4, -1), (4, 7, 1), (7, 3, 1), (3, 0, -1)],
        'edge_cycle':   [(1, 7, False), (7, 9, False), (9, 4, False), (4, 1, False)]
    },
    'L': {
        'corner_cycle': [(1, 2, 1), (2, 6, -1), (6, 5, -1), (5, 1, 1)],
        'edge_cycle':   [(3, 5, False), (5, 11, False), (11, 6, False), (6, 3, False)]
    },
    "L'": {
        'corner_cycle': [(1, 5, -1), (5, 6, 1), (6, 2, 1), (2, 1, -1)],
        'edge_cycle':   [(3, 6, False), (6, 11, False), (11, 5, False), (5, 3, False)]
    },
    'F': {
        'corner_cycle': [(1, 0, 1), (0, 4, -1), (4, 5, -1), (5, 1, 1)],
        'edge_cycle':   [(0, 5, True), (5, 8, True), (8, 4, True), (4, 0, True)]
    },
    "F'": {
        'corner_cycle': [(1, 5, -1), (5, 4, 1), (4, 0, 1), (0, 1, -1)],
        'edge_cycle':   [(0, 4, True), (4, 8, True), (8, 5, True), (5, 0, True)]
    },
    'B': {
        'corner_cycle': [(3, 2, 1), (2, 6, -1), (6, 7, -1), (7, 3, 1)],
        'edge_cycle':   [(2, 7, True), (7, 10, True), (10, 6, True), (6, 2, True)]
    },
    "B'": {
        'corner_cycle': [(3, 7, -1), (7, 6, 1), (6, 2, 1), (2, 3, -1)],
        'edge_cycle':   [(2, 6, True), (6, 10, True), (10, 7, True), (7, 2, True)]
    }
}

# --- Clase BitboardCube ---
class BitboardCube:
    CENTER_COLORS = ['W', 'Y', 'B', 'G', 'R', 'O']
    # Tablas de mapeo para impresión, basadas en la versión con listas.
    CORNER_MAPPING = [
        ((0,8), (4,2), (3,0)),  # Slot 0: UFR
        ((0,6), (2,2), (4,0)),  # Slot 1: UFL
        ((0,0), (5,2), (2,0)),  # Slot 2: UBL
        ((0,2), (3,2), (5,0)),  # Slot 3: UBR
        ((1,2), (3,6), (4,8)),  # Slot 4: DFR
        ((1,0), (4,6), (2,8)),  # Slot 5: DFL
        ((1,6), (2,6), (5,8)),  # Slot 6: DBL
        ((1,8), (5,6), (3,8))   # Slot 7: DBR
    ]
    EDGE_MAPPING = [
        ((0,7), (4,1)),   # Slot 0: UF
        ((0,5), (3,1)),   # Slot 1: UR
        ((0,1), (5,1)),   # Slot 2: UB
        ((0,3), (2,1)),   # Slot 3: UL
        ((4,5), (3,3)),   # Slot 4: FR
        ((4,3), (2,5)),   # Slot 5: FL
        ((5,3), (2,7)),   # Slot 6: BL
        ((5,5), (3,7)),   # Slot 7: BR
        ((1,1), (4,7)),   # Slot 8: DF
        ((1,5), (3,5)),   # Slot 9: DR
        ((1,7), (5,7)),   # Slot 10: DB
        ((1,3), (2,3))    # Slot 11: DL
    ]

    def __init__(self):
        # Estado resuelto: cada esquina i tiene perm = i, ori = 0; cada arista i tiene perm = i, ori = 0.
        self.corners = 0
        for i in range(8):
            self.corners = set_corner(self.corners, i, i, 0)
        self.edges = 0
        for i in range(12):
            self.edges = set_edge(self.edges, i, i, 0)

    def clone(self):
        new_cube = BitboardCube()
        new_cube.corners = self.corners
        new_cube.edges = self.edges
        return new_cube

    def get_state(self):
        # Retorna la tupla (corners, edges) que identifica el estado.
        return (self.corners, self.edges)

    def is_solved(self):
        solved_corners = 0
        for i in range(8):
            solved_corners = set_corner(solved_corners, i, i, 0)
        solved_edges = 0
        for i in range(12):
            solved_edges = set_edge(solved_edges, i, i, 0)
        return self.corners == solved_corners and self.edges == solved_edges

    def apply_move(self, move):
        new_corners = [get_corner(self.corners, i) for i in range(8)]
        new_edges = [get_edge(self.edges, i) for i in range(12)]

        mapping = MOVE_TABLE[move]
        for (dest, src, twist_delta) in mapping['corner_cycle']:
            perm, ori = get_corner(self.corners, src)
            ori = (ori + twist_delta) % 3
            new_corners[dest] = (perm, ori)
        for (dest, src, flip) in mapping['edge_cycle']:
            perm, ori = get_edge(self.edges, src)
            if flip:
                ori ^= 1
            new_edges[dest] = (perm, ori)

        new_corners_int = 0
        for i in range(8):
            perm, ori = new_corners[i]
            new_corners_int = set_corner(new_corners_int, i, perm, ori)
        new_edges_int = 0
        for i in range(12):
            perm, ori = new_edges[i]
            new_edges_int = set_edge(new_edges_int, i, perm, ori)

        self.corners = new_corners_int
        self.edges = new_edges_int

    def apply_moves(self, moves):
        for move in moves:
            self.apply_move(move)

    def heuristic(self):
        h = 0
        for i in range(8):
            perm, ori = get_corner(self.corners, i)
            if perm != i or ori != 0:
                h += 1
        for i in range(12):
            perm, ori = get_edge(self.edges, i)
            if perm != i or ori != 0:
                h += 1
        return h

    def to_list_cube(self):
        """
        Reconstruye una representación estilo lista de 6 caras (cada una de 9 stickers)
        a partir del estado bitboard.
        """
        faces = [ [' ']*9 for _ in range(6) ]
        # Colocar centros fijos:
        for i in range(6):
            faces[i][4] = BitboardCube.CENTER_COLORS[i]

        for slot in range(8):
            perm, ori = get_corner(self.corners, slot)
            solved_facelets = [ BitboardCube.CENTER_COLORS[face] for face, pos in BitboardCube.CORNER_MAPPING[perm] ]
            rotated = solved_facelets[ori:] + solved_facelets[:ori]
            for color, (face, pos) in zip(rotated, BitboardCube.CORNER_MAPPING[slot]):
                faces[face][pos] = color

        for slot in range(12):
            perm, ori = get_edge(self.edges, slot)
            solved_facelets = [ BitboardCube.CENTER_COLORS[face] for face, pos in BitboardCube.EDGE_MAPPING[perm] ]
            if ori == 1:
                solved_facelets = solved_facelets[::-1]
            for color, (face, pos) in zip(solved_facelets, BitboardCube.EDGE_MAPPING[slot]):
                faces[face][pos] = color
        return faces

# --- Función auxiliar para imprimir el cubo en forma de “net” ---
def print_bitboard_cube_net(cube):
    faces = cube.to_list_cube()
    U = faces[0]
    D = faces[1]
    L = faces[2]
    R = faces[3]
    F = faces[4]
    B = faces[5]

    print("        {} {} {}".format(U[0], U[1], U[2]))
    print("        {} {} {}".format(U[3], U[4], U[5]))
    print("        {} {} {}".format(U[6], U[7], U[8]))
    print()

    for i in range(3):
        print("{} {} {}   {} {} {}   {} {} {}   {} {} {}".format(
            L[3*i], L[3*i+1], L[3*i+2],
            F[3*i], F[3*i+1], F[3*i+2],
            R[3*i], R[3*i+1], R[3*i+2],
            B[3*i], B[3*i+1], B[3*i+2]
        ))
    print()

    print("        {} {} {}".format(D[0], D[1], D[2]))
    print("        {} {} {}".format(D[3], D[4], D[5]))
    print("        {} {} {}".format(D[6], D[7], D[8]))

# --- Solver ---
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

# --- Ejemplo de uso ---
if __name__ == '__main__':
    cube = BitboardCube()
    moves = ["U", "U'", "D", "D'", "L", "L'", "R", "R'", "F", "F'", "B", "B'"]
    scramble = [random.choice(moves) for _ in range(10)]
    print("Estado inicial (resuelto):")
    print_bitboard_cube_net(cube)

    cube.apply_moves(scramble)
    print("\nDespués de scramble:")
    print_bitboard_cube_net(cube)

    solver = Solver()
    print("\nBuscando solución...")
    solution = solver.ida_star(cube)
    if solution is not None:
        print("Solución encontrada:", solution)
        print("Nodos expandidos:", solver.nodes_searched)
    else:
        print("No se encontró solución.")
    cube.apply_moves(solution)
    print_bitboard_cube_net(cube)
