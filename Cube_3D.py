import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# --- 可视化部分 ---
color_map = {
    'W': 'white',
    'Y': 'yellow',
    'G': 'green',
    'B': 'blue',
    'R': 'red',
    'O': 'orange'
}

def draw_face(ax, face_color, x, y, z, face):
    dx = dy = dz = 1
    faces = {
        'U': [[(x, y+dy, z+dz), (x+dx, y+dy, z+dz), (x+dx, y+dy, z), (x, y+dy, z)]],
        'D': [[(x, y, z), (x+dx, y, z), (x+dx, y, z+dz), (x, y, z+dz)]],
        'L': [[(x, y, z), (x, y+dy, z), (x, y+dy, z+dz), (x, y, z+dz)]],
        'R': [[(x+dx, y, z), (x+dx, y+dy, z), (x+dx, y+dy, z+dz), (x+dx, y, z+dz)]],
        'F': [[(x, y, z+dz), (x+dx, y, z+dz), (x+dx, y+dy, z+dz), (x, y+dy, z+dz)]],
        'B': [[(x, y, z), (x+dx, y, z), (x+dx, y+dy, z), (x, y+dy, z)]],
    }
    poly3d = faces[face]
    collection = Poly3DCollection(poly3d, facecolors=color_map[face_color], edgecolors='black')
    ax.add_collection3d(collection)

def draw_cube_state(cube_faces):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_axis_off()
    
    face_positions = {
        'U': lambda i, j: (j, 2, 2 - i),
        'D': lambda i, j: (j, 0, i),
        'F': lambda i, j: (j, i, 2),
        'B': lambda i, j: (2 - j, i, 0),
        'L': lambda i, j: (0, i, 2 - j),
        'R': lambda i, j: (2, i, j)
    }

    for face in cube_faces:
        for i in range(3):
            for j in range(3):
                x, y, z = face_positions[face](i, j)
                draw_face(ax, cube_faces[face][i][j], x, y, z, face)

    ax.set_xlim([0, 3])
    ax.set_ylim([0, 3])
    ax.set_zlim([0, 3])
    plt.tight_layout()
    plt.show()


# --- 魔方类 ---
class Cube:
    def __init__(self):
        self.faces = {
            'U': [['W'] * 3 for _ in range(3)],
            'D': [['Y'] * 3 for _ in range(3)],
            'L': [['G'] * 3 for _ in range(3)],
            'R': [['B'] * 3 for _ in range(3)],
            'F': [['R'] * 3 for _ in range(3)],
            'B': [['O'] * 3 for _ in range(3)],
        }

    def rotate_face(self, face, clockwise=True):
        self.faces[face] = [list(x) for x in zip(*self.faces[face][::-1])] if clockwise else \
                           [list(x)[::-1] for x in zip(*self.faces[face])]

        adj = {
            'U': [('B', 0), ('R', 0), ('F', 0), ('L', 0)],
            'D': [('F', 2), ('R', 2), ('B', 2), ('L', 2)],
            'F': [('U', 2), ('R', 'col0'), ('D', 0), ('L', 'col2')],
            'B': [('U', 0), ('L', 'col0'), ('D', 2), ('R', 'col2')],
            'L': [('U', 'col0'), ('F', 'col0'), ('D', 'col0'), ('B', 'col2')],
            'R': [('U', 'col2'), ('B', 'col0'), ('D', 'col2'), ('F', 'col2')],
        }

        seq = adj[face]
        temp = self._get_edge(*seq[-1])
        for i in range(3, 0, -1):
            self._set_edge(*seq[i], self._get_edge(*seq[i - 1]))
        self._set_edge(*seq[0], temp)

    def _get_edge(self, face, index):
        if isinstance(index, int):
            return self.faces[face][index][:]
        elif 'col' in str(index):
            col = int(str(index).replace('col', ''))
            return [row[col] for row in self.faces[face]]

    def _set_edge(self, face, index, values):
        if isinstance(index, int):
            self.faces[face][index] = values
        elif 'col' in str(index):
            col = int(str(index).replace('col', ''))
            for i in range(3):
                self.faces[face][i][col] = values[i]

    def print_cube(self):
        def fmt(face): return [' '.join(row) for row in self.faces[face]]
        print("\n    " + fmt('U')[0])
        print("    " + fmt('U')[1])
        print("    " + fmt('U')[2])
        for i in range(3):
            print(fmt('L')[i] + "  " + fmt('F')[i] + "  " + fmt('R')[i] + "  " + fmt('B')[i])
        print("    " + fmt('D')[0])
        print("    " + fmt('D')[1])
        print("    " + fmt('D')[2])

    def shuffle(self, steps=20):
        moves = ['U', 'D', 'L', 'R', 'F', 'B']
        for _ in range(steps):
            self.rotate_face(random.choice(moves), random.choice([True, False]))


# --- 控制函数 ---
def play():
    cube = Cube()
    cube.shuffle()
    print("🎲 魔方已打乱。输入 'exit' 退出，输入 'U D L R F B' 或加 `'` 表示逆时针旋转")
    while True:
        cube.print_cube()
        draw_cube_state(cube.faces)
        cmd = input("请输入旋转命令（如 U, D', F 等）：").strip().upper()
        if cmd == 'EXIT':
            break
        if cmd:
            move = cmd[0]
            if move in 'UDLRFB':
                clockwise = not (len(cmd) > 1 and cmd[1] == "'")
                cube.rotate_face(move, clockwise)
            else:
                print("无效命令。请输入 U, D, L, R, F, B 或加 `'` 表示逆时针")


if __name__ == "__main__":
    play()
