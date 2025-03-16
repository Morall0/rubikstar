class Cube:
    def __init__(self):

        # The following numbers represents the color of each side of the cube
        # U: 0
        # R: 1
        # D: 2
        # L: 3
        # B: 4
        # F: 5

        self.centers = (0, 1, 2, 3, 4, 5)

        self.corners = {  # Defining the 8 corners
            "URF": (0, 1, 5), "ULF": (0, 3, 5), "ULB": (0, 3, 4), "URB": (0, 1, 4),
            "DRF": (2, 1, 5), "DLF": (2, 3, 5), "DLB": (2, 3, 4), "DRB": (2, 1, 4)
        }

        self.edges = {  # Defining the 12 edges
            "FU": (5, 0), "FR": (5, 1), "FD": (5, 2), "FL": (5, 3),
            "BU": (4, 0), "BR": (4, 1), "BD": (4, 2), "BL": (4, 3),
            "UR": (0, 1), "DR": (2, 1), "DL": (2, 3), "UL": (0, 3)
        }
        # TODO: Sort the edges and corners
        self.faces_map = {  # A map to facilitate rotations
            "U": {
                "corners": ["URF", "ULF", "ULB", "URB"],
                "edges": ["FU", "UL", "BU", "UR"]
            },
            "R": {
                "corners": ["URF", "URB", "DRB", "DRF"],
                "edges": ["FR", "UR", "BR", "DR"]
            },
            "D": {
                "corners": ["DRF", "DLF", "DLB", "DRB"],
                "edges": ["FD", "DL", "BD", "DR"]
            },
            "L": {
                "corners": ["ULF", "DLF", "DLB", "ULB"],
                "edges": ["FL", "DL", "BL", "UL"]
            },
            "B": {
                "corners": ["ULB", "DLB", "DRB", "URB"],
                "edges": ["BU", "BL", "BD", "BR"]
            },
            "F": {
                "corners": ["URF", "DRF", "DLF", "ULF"],
                "edges": ["FU", "FR", "FD", "FL"]
            }
        }

    def rotate_face_90deg(self, face: str, clockwise: bool):
        if face not in self.faces_map:
            print(f"ERROR the face '{face}' is not in the notation")
            return

        corners = self.faces_map[face]["corners"]
        edges = self.faces_map[face]["edges"]

        if clockwise:
            # Rotating corners
            self.corners[corners[0]], self.corners[corners[1]], self.corners[corners[2]], self.corners[corners[3]] = \
                self.corners[corners[3]], self.corners[corners[0]], self.corners[corners[1]], self.corners[corners[2]]

            # Rotating edges
            self.edges[edges[0]], self.edges[edges[1]], self.edges[edges[2]], self.edges[edges[3]] = \
                self.edges[edges[3]], self.edges[edges[0]], self.edges[edges[1]], self.edges[edges[2]]
        else:
            # Rotating corners
            self.corners[corners[0]], self.corners[corners[1]], self.corners[corners[2]], self.corners[corners[3]] = \
                self.corners[corners[1]], self.corners[corners[2]], self.corners[corners[3]], self.corners[corners[1]]

            # Rotating edges
            self.edges[edges[0]], self.edges[edges[1]], self.edges[edges[2]], self.edges[edges[3]] = \
                self.edges[edges[1]], self.edges[edges[2]], self.edges[edges[3]], self.edges[edges[1]]

    def print_state(self):
        print("Corners:", self.corners)
        print("Edges:", self.edges)
        print("Centers:", self.centers)


cube = Cube()
cube.print_state()
cube.rotate_face_90deg("B", True)
cube.print_state()
