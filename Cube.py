import random

class Cube:
    def __init__(self):
        # 魔方的六个面：上(U)、下(D)、左(L)、右(R)、前(F)、后(B)
        # 魔方的颜色说明：W=白, Y=黄, G=绿, B=蓝, R=红, O=橙
        self.faces = {
            'U': [['W'] * 3 for _ in range(3)],
            'D': [['Y'] * 3 for _ in range(3)],
            'L': [['G'] * 3 for _ in range(3)],
            'R': [['B'] * 3 for _ in range(3)],
            'F': [['R'] * 3 for _ in range(3)],
            'B': [['O'] * 3 for _ in range(3)],
        }

    def rotate_face(self, face, clockwise=True):
        # 旋转面自身
        self.faces[face] = [list(x) for x in zip(*self.faces[face][::-1])] if clockwise else \
                           [list(x)[::-1] for x in zip(*self.faces[face])]

        # 旋转边
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


def play():
    cube = Cube()
    cube.shuffle()
    print("🎲 魔方已打乱。输入 'exit' 退出，输入 'U D L R F B' 或加 '（'）' 表示逆时针旋转")
    while True:
        cube.print_cube()
        cmd = input("请输入旋转命令（如 U, D', F 等）：").strip().upper()
        if cmd == 'EXIT':
            break
        if cmd:
            move = cmd[0]
            if move in 'UDLRFB':
                clockwise = not (len(cmd) > 1 and cmd[1] == "'")
                cube.rotate_face(move, clockwise)
            else:
                print("无效命令。请输入 U, D, L, R, F, B 或加 '（'）' 逆时针")

if __name__ == "__main__":
    play()
