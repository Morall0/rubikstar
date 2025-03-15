class Cube:
    def __init__(self):
        self.face = {
            "Top": [
                ["W", "W", "W"],
                ["W", "W", "W"],
                ["W", "W", "W"]
                ],
            "Bottom": [
                ["Y", "Y", "Y"],
                ["Y", "Y", "Y"],
                ["Y", "Y", "Y"]
                ],
            "Left": [
                ["G", "G", "G"],
                ["G", "G", "G"],
                ["G", "G", "G"]
                ],
            "Right": [
                ["B", "B", "B"],
                ["B", "B", "B"],
                ["B", "B", "B"]
                ],
            "Front": [
                ["R", "R", "R"],
                ["R", "R", "R"],
                ["R", "R", "R"]
                ],
            "Back": [
                ["O", "O", "O"],
                ["O", "O", "O"],
                ["O", "O", "O"]
                ]
        }

    def rotate_face_clockwise(self, face_name):
        self.face[face_name] = [list(row) for row in zip(*self.face[face_name][::-1])]

    def rotate_face_counterclockwise(self, face_name):
        self.face[face_name] = [list(row) for row in zip(*self.face[face_name])][::-1]

    def rotate_top_clockwise(self):
        self.rotate_face_clockwise("Top")
        temp = self.face["Front"][0]
        self.face["Front"][0] = self.face["Right"][0]
        self.face["Right"][0] = self.face["Back"][0]
        self.face["Back"][0] = self.face["Left"][0]
        self.face["Left"][0] = temp

    def rotate_bottom_clockwise(self):
        self.rotate_face_clockwise("Bottom")
        temp = self.face["Front"][2]
        self.face["Front"][2] = self.face["Left"][2]
        self.face["Left"][2] = self.face["Back"][2]
        self.face["Back"][2] = self.face["Right"][2]
        self.face["Right"][2] = temp

    def rotate_left_clockwise(self):
        self.rotate_face_clockwise("Left")
        temp_col = [self.face["Top"][i][0] for i in range(3)]
        for i in range(3):
            self.face["Top"][i][0] = self.face["Back"][2 - i][2]
            self.face["Back"][2 - i][2] = self.face["Bottom"][i][0]
            self.face["Bottom"][i][0] = self.face["Front"][i][0]
            self.face["Front"][i][0] = temp_col[i]

    def rotate_right_clockwise(self):
        self.rotate_face_clockwise("Right")
        temp_col = [self.face["Top"][i][2] for i in range(3)]
        for i in range(3):
            self.face["Top"][i][2] = self.face["Front"][i][2]
            self.face["Front"][i][2] = self.face["Bottom"][i][2]
            self.face["Bottom"][i][2] = self.face["Back"][2 - i][0]
            self.face["Back"][2 - i][0] = temp_col[i]

    def rotate_front_clockwise(self):
        self.rotate_face_clockwise("Front")
        temp = [self.face["Top"][2][i] for i in range(3)]
        for i in range(3):
            self.face["Top"][2][i] = self.face["Left"][2 - i][2]
            self.face["Left"][2 - i][2] = self.face["Bottom"][0][i]
            self.face["Bottom"][0][i] = self.face["Right"][i][0]
            self.face["Right"][i][0] = temp[i]

    def rotate_back_clockwise(self):
        self.rotate_face_clockwise("Back")
        temp = [self.face["Top"][0][i] for i in range(3)]
        for i in range(3):
            self.face["Top"][0][i] = self.face["Right"][i][2]
            self.face["Right"][i][2] = self.face["Bottom"][2][2 - i]
            self.face["Bottom"][2][2 - i] = self.face["Left"][i][0]
            self.face["Left"][i][0] = temp[i]

    def rotate_top_counterclockwise(self):
        self.rotate_face_counterclockwise("Top")
        temp = self.face["Front"][0]
        self.face["Front"][0] = self.face["Left"][0]
        self.face["Left"][0] = self.face["Back"][0]
        self.face["Back"][0] = self.face["Right"][0]
        self.face["Right"][0] = temp

    def rotate_bottom_counterclockwise(self):
        self.rotate_face_counterclockwise("Bottom")
        temp = self.face["Front"][2]
        self.face["Front"][2] = self.face["Right"][2]
        self.face["Right"][2] = self.face["Back"][2]
        self.face["Back"][2] = self.face["Left"][2]
        self.face["Left"][2] = temp

    def rotate_left_counterclockwise(self):
        self.rotate_face_counterclockwise("Left")
        temp_col = [self.face["Top"][i][0] for i in range(3)]
        for i in range(3):
            self.face["Top"][i][0] = self.face["Front"][i][0]
            self.face["Front"][i][0] = self.face["Bottom"][i][0]
            self.face["Bottom"][i][0] = self.face["Back"][2 - i][2]
            self.face["Back"][2 - i][2] = temp_col[i]

    def rotate_right_counterclockwise(self):
        self.rotate_face_counterclockwise("Right")
        temp_col = [self.face["Top"][i][2] for i in range(3)]
        for i in range(3):
            self.face["Top"][i][2] = self.face["Back"][2 - i][0]
            self.face["Back"][2 - i][0] = self.face["Bottom"][i][2]
            self.face["Bottom"][i][2] = self.face["Front"][i][2]
            self.face["Front"][i][2] = temp_col[i]

    def rotate_front_counterclockwise(self):
        self.rotate_face_counterclockwise("Front")
        temp = [self.face["Top"][2][i] for i in range(3)]
        for i in range(3):
            self.face["Top"][2][i] = self.face["Right"][i][0]
            self.face["Right"][i][0] = self.face["Bottom"][0][i]
            self.face["Bottom"][0][i] = self.face["Left"][2 - i][2]
            self.face["Left"][2 - i][2] = temp[i]

    def rotate_back_counterclockwise(self):
        self.rotate_face_counterclockwise("Back")
        temp = [self.face["Top"][0][i] for i in range(3)]
        for i in range(3):
            self.face["Top"][0][i] = self.face["Left"][i][0]
            self.face["Left"][i][0] = self.face["Bottom"][2][2 - i]
            self.face["Bottom"][2][2 - i] = self.face["Right"][i][2]
            self.face["Right"][i][2] = temp[i]

    def rotate_from_notation(self, rot_string):
        rotations = rot_string.split()
        self.rotate_from_list(rotations)

    def rotate_from_list(self, rotations):
        for mov in rotations:
            tick = True if mov.find("'") != -1 else False
            rot_twice = 2 if mov.find("2") != -1 else 1
            for i in range(rot_twice):
                if mov.find("F") != -1:
                    self.rotate_front_counterclockwise() if tick else self.rotate_front_clockwise()
                elif mov.find("B") != -1:
                    self.rotate_back_counterclockwise() if tick else self.rotate_back_clockwise()
                elif mov.find("L") != -1:
                    self.rotate_left_counterclockwise() if tick else self.rotate_left_clockwise()
                elif mov.find("R") != -1:
                    self.rotate_right_counterclockwise() if tick else self.rotate_right_clockwise()
                elif mov.find("U") != -1:
                    self.rotate_top_counterclockwise() if tick else self.rotate_top_clockwise()
                elif mov.find("D") != -1:
                    self.rotate_bottom_counterclockwise() if tick else self.rotate_bottom_clockwise()

    def print_cube(self):
        for face, grid in self.face.items():
            print(f"{face}:")
            for row in grid:
                print(" ".join(row))
            print()


cubo = Cube()
print("Initial state")
cubo.print_cube()
print("\n")
rotations = "R' L U' D F' B R' L"
cubo.rotate_from_notation(rotations)
print("After rotating " + rotations)
cubo.print_cube()
print("\n")
