import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class Cube:
    def __init__(self):
        self.face = {
            "Top": [["W", "W", "W"], ["W", "W", "W"], ["W", "W", "W"]],
            "Bottom": [["Y", "Y", "Y"], ["Y", "Y", "Y"], ["Y", "Y", "Y"]],
            "Left": [["G", "G", "G"], ["G", "G", "G"], ["G", "G", "G"]],
            "Right": [["B", "B", "B"], ["B", "B", "B"], ["B", "B", "B"]],
            "Front": [["R", "R", "R"], ["R", "R", "R"], ["R", "R", "R"]],
            "Back": [["O", "O", "O"], ["O", "O", "O"], ["O", "O", "O"]],
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
    cubo = Cube()
    cubo.plot_cube()
