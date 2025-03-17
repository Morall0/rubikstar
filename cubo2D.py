import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class Cube2d:
    def __init__(self, U, D, L, R, F, B):
        self.face = {
            "Top": [U[:3], U[3:6], U[6:]],
            "Bottom": [D[:3], D[3:6], D[6:]],
            "Left": [L[:3], L[3:6], L[6:]],
            "Right": [R[:3], R[3:6], R[6:]],
            "Front": [F[:3], F[3:6], F[6:]],
            "Back": [B[:3], B[3:6], B[6:]],
        }
        self.colors = {"W": "white", "Y": "yellow", "G": "green", "B": "blue", "R": "red", "O": "orange"}

    def plot_face(self, ax, face_name, offset_x, offset_y):
        face = self.face[face_name]
        for i in range(3):
            for j in range(3):
                color = self.colors[face[i][j]]
                rect = Rectangle((j + offset_x, 2 - i + offset_y), 1, 1, facecolor=color, edgecolor="black")
                ax.add_patch(rect)
                ax.text(j + offset_x + 0.5, 2 - i + offset_y + 0.5, face[i][j],
                        ha="center", va="center", fontsize=12, fontweight="bold")

    def plot_cube(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 9)
        ax.set_aspect('equal')
        ax.axis('off')

        # Dibujar las caras en posiciones relativas
        self.plot_face(ax, "Top", 3, 6)
        self.plot_face(ax, "Left", 0, 3)
        self.plot_face(ax, "Front", 3, 3)
        self.plot_face(ax, "Right", 6, 3)
        self.plot_face(ax, "Back", 9, 3)
        self.plot_face(ax, "Bottom", 3, 0)

        plt.show()


if __name__ == "__main__":
    U = ['W'] * 9
    D = ['Y'] * 9
    L = ['B'] * 9
    R = ['G'] * 9
    F = ['R'] * 9
    B = ['O'] * 9
    
    cubo = Cube2d(U, D, L, R, F, B)
    cubo.plot_cube()
