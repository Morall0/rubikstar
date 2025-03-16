from cubo import Cube
from scrambler import scramble_cube
from solver import Solver

if __name__ == '__main__':
    cube = Cube()
  
    
    #scramble_cube(cube)
    cube.rotate_top_clockwise()
    cube.rotate_front_counterclockwise()
    
    print("Estado inicial del cubo (mezclado):")
    cube.print_cube()
    
    
    
    solver = Solver(cube)
    solution = solver.solve()
    
    if solution is not None:
        print("Secuencia de movimientos para resolver el cubo:", solution)
    else:
        print("No se encontró solución.")
        
    
