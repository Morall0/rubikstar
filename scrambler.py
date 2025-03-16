from cubo import Cube
import random

def scramble_cube(cube: Cube, n: int = 15) -> None:
    """
    Realiza n movimientos aleatorios para revolver el cubo.
    Devuelve la secuencia de movimientos aplicados.
    """
    moves = [
        "rotate_top_clockwise",
        "rotate_top_counterclockwise",
        "rotate_bottom_clockwise",
        "rotate_bottom_counterclockwise",
        "rotate_left_clockwise",
        "rotate_left_counterclockwise",
        "rotate_right_clockwise",
        "rotate_right_counterclockwise",
        "rotate_front_clockwise",
        "rotate_front_counterclockwise",
        "rotate_back_clockwise",
        "rotate_back_counterclockwise"
    ]
    
    
    
    #sequence = []
    for _ in range(n):
        move = random.choice(moves)
        getattr(cube, move)()
        #sequence.append(move)
    #return sequence