from cubo import RubikCube
from solver import Solver
from cubo2D import Cube2d
import random  




if __name__ == '__main__':

    cube = RubikCube()
    
    
    #Generación aleatoria de movimientos
    moves = ["U", "U'", "D", "D'", "L", "L'", "R", "R'", "F", "F'", "B", "B'"]
    #Modificar el rango para generar más o menos movimientos
    scramble = [random.choice(moves) for _ in range(5)]
    
    print("Estado inicial (resuelto):")
    cube.print_cube()
    cube2d = Cube2d(*cube.get_parameters())
    cube2d.plot_cube()
    
    print("\nAplicando scramble:", scramble)
    for move in scramble:
        cube.apply_move(move)
    cube.print_cube()
    cube2d = Cube2d(*cube.get_parameters())
    cube2d.plot_cube()
    
    solver = Solver()
    print("\nBuscando solución...")
    solution = solver.ida_star(cube)
    if solution is not None:
        print("Solución encontrada:", solution)
        print("Nodos expandidos:", solver.nodes_searched)
    else:
        print("No se encontró solución.")
    for move in solution:
        cube.apply_move(move)
        cube2d = Cube2d(*cube.get_parameters())
        cube2d.plot_cube() 
    cube2d = Cube2d(*cube.get_parameters())
    cube2d.plot_cube()   
    cube.print_cube()
