
def print_cube_net(cube):
   
    U = cube.cube[0]
    D = cube.cube[1]
    L = cube.cube[2]
    R = cube.cube[3]
    F = cube.cube[4]
    B = cube.cube[5]
    
   
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


    
    





