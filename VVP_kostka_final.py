import matplotlib.pyplot as plt
import numpy as np
from itertools import product
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from random import choice
from typing import List, Annotated

class Cube_Piece:
    '''Represents a single piece of the cube'''
    def __init__(self, pos: Annotated[List[int], 3], coloring: Annotated[List[chr], 6]):
        self.pos = pos
        self.coloring = coloring

    def draw_piece(self, ax: plt.Axes) -> None:
        '''Draws and adds a single piece of the cube to the plot'''
        color_id = 0
        for i in [2, 1, 0]:
            for j in range(2):
                if i == 2:
                    x = [self.pos[0], self.pos[0] + 1, self.pos[0] + 1, self.pos[0]]
                    y = [self.pos[1], self.pos[1], self.pos[1] + 1, self.pos[1] + 1]
                    z = [self.pos[2], self.pos[2], self.pos[2], self.pos[2]]
                    if z[0] in [1, 2]:
                        self.pos[i] = self.pos[i] + 1
                        color_id += 1
                        continue
                elif i == 1:
                    x = [self.pos[0], self.pos[0] + 1, self.pos[0] + 1, self.pos[0]]
                    y = [self.pos[1], self.pos[1], self.pos[1], self.pos[1]]
                    z = [self.pos[2], self.pos[2], self.pos[2] + 1, self.pos[2] + 1]
                    if y[0] in [1, 2]:
                        self.pos[i] = self.pos[i] + 1
                        color_id += 1
                        continue
                elif i == 0:
                    x = [self.pos[0], self.pos[0], self.pos[0], self.pos[0]]
                    y = [self.pos[1], self.pos[1] + 1, self.pos[1] + 1, self.pos[1]]
                    z = [self.pos[2], self.pos[2], self.pos[2] + 1, self.pos[2] + 1]
                    if x[0] in [1, 2]:
                        self.pos[i] = self.pos[i] + 1
                        color_id += 1
                        continue
                verts = [list(zip(x, y, z))]
                square = Poly3DCollection(verts)
                square.set_edgecolor('black')
                square.set_facecolor(self.coloring[color_id])
                ax.add_collection3d(square)
                color_id += 1
                self.pos[i] = self.pos[i] + 1
            self.pos[i] = self.pos[i] - 2

    def x_rot(self, count: int) -> None:
        '''Rotates a single piece of the cube around the x-axis'''
        for rotation in range(count):
            helper = self.coloring[0]
            self.coloring[0] = self.coloring[3]
            self.coloring[3] = self.coloring[1]
            self.coloring[1] = self.coloring[2]
            self.coloring[2] = helper

    def y_rot(self, count: int) -> None:
        '''Rotates a single piece of the cube around the y-axis'''
        for rotation in range(count):
            helper = self.coloring[0]
            self.coloring[0] = self.coloring[5]
            self.coloring[5] = self.coloring[1]
            self.coloring[1] = self.coloring[4]
            self.coloring[4] = helper

    def z_rot(self, count: int) -> None:
        '''Rotates a single piece of the cube around the z-axis'''
        for rotation in range(count):
            helper = self.coloring[2]
            self.coloring[2] = self.coloring[5]
            self.coloring[5] = self.coloring[3]
            self.coloring[3] = self.coloring[4]
            self.coloring[4] = helper


class Cube:
    '''Represents the cube made from 27 cube pieces'''
    def __init__(self):
        self.cube_matrix = np.ndarray((3, 3, 3), dtype=object)

    def create_cube(self) -> None:
        '''Fills the cube's matrix with cube pieces with appropriate properties'''
        for (z, y, x) in product(range(3), range(3), range(3)):
            colors = ['white', 'yellow', 'blue', 'green', 'orange', 'red']
            self.cube_matrix[x, y, z] = Cube_Piece([x, y, z], colors.copy())

    def draw_cube(self, ax: plt.Axes) -> None:
        '''Calls the draw piece method for each cube piece to draw the whole cube'''
        for (x, y, z) in product(range(3), range(3), range(3)):
            self.cube_matrix[x, y, z].draw_piece(ax)
        
    def Turn_U(self, count: int = 1) -> None:
        '''Turns the upper side of the cube clockwise 'count' times'''
        for turn in range(count):
            self.cube_matrix[:, :, 2] = np.rot90(self.cube_matrix[:, :, 2], 3)
            side_U = self.cube_matrix[:, :, 2]
            for (i, j) in product(range(3), range(3)):
                piece = side_U[i, j]
                piece.z_rot(1)
                piece.pos[0] = i
                piece.pos[1] = j
                piece.pos[2] = 2
    
    def Turn_D(self, count: int = 1) -> None:
        '''Turns the down side of the cube clockwise 'count' times'''
        for turn in range(count):
            self.cube_matrix[:, :, 0] = np.rot90(self.cube_matrix[:, :, 0])
            side_D = self.cube_matrix[:, :, 0]
            for (i, j) in product(range(3), range(3)):
                piece = side_D[i, j]
                piece.z_rot(3)
                piece.pos[0] = i
                piece.pos[1] = j
                piece.pos[2] = 0
    
    def Turn_F(self, count: int = 1) -> None:
        '''Turns the front side of the cube clockwise 'count' times'''
        for turn in range(count):
            self.cube_matrix[:, 0, :] = np.rot90(self.cube_matrix[:, 0, :], 3)
            side_F = self.cube_matrix[:, 0, :]
            for (i, j) in product(range(3), range(3)):
                piece = side_F[i, j]
                piece.y_rot(1)
                piece.pos[0] = i
                piece.pos[1] = 0
                piece.pos[2] = j
    
    def Turn_B(self, count: int = 1) -> None:
        '''Turns the back side of the cube clockwise 'count' times'''
        for turn in range(count):
            self.cube_matrix[:, 2, :] = np.rot90(self.cube_matrix[:, 2, :])
            side_B = self.cube_matrix[:, 2, :]
            for (i, j) in product(range(3), range(3)):
                piece = side_B[i, j]
                piece.y_rot(3)
                piece.pos[0] = i
                piece.pos[1] = 2
                piece.pos[2] = j
    
    def Turn_R(self, count: int = 1) -> None:
        '''Turns the right side of the cube clockwise 'count' times'''
        for turn in range(count):
            self.cube_matrix[2, :, :] = np.rot90(self.cube_matrix[2, :, :], 3)
            side_R = self.cube_matrix[2, :, :]
            for (i, j) in product(range(3), range(3)):
                piece = side_R[i, j]
                piece.x_rot(1)
                piece.pos[0] = 2
                piece.pos[1] = i
                piece.pos[2] = j
    
    def Turn_L(self, count: int = 1) -> None:
        '''Turns the left side of the cube clockwise 'count' times'''
        for turn in range(count):
            self.cube_matrix[0, :, :] = np.rot90(self.cube_matrix[0, :, :])
            side_L = self.cube_matrix[0, :, :]
            for (i, j) in product(range(3), range(3)):
                piece = side_L[i, j]
                piece.x_rot(3)
                piece.pos[0] = 0
                piece.pos[1] = i
                piece.pos[2] = j
    
    def scramble(self) -> None:
        '''Chooses 20 moves randomly and then applies them on the cube to scramble it'''
        possible_moves = ['U', 'D', 'F', 'B', 'R', 'L']
        scramble = []
        for i in range(20):
            random_move = choice(possible_moves)
            scramble.append(random_move)
        for move in scramble:
            match move:
                case 'U':
                    cube.Turn_U()
                case 'D':
                    cube.Turn_D()
                case 'R':
                    cube.Turn_R()
                case 'L':
                    cube.Turn_L()
                case 'B':
                    cube.Turn_B()
                case 'F':
                    cube.Turn_F()
    
        
def press(event) -> None:
    '''On each key-press event function clears the plot,
    makes changes to the cube according to which key was pressed and then rewrites all text and draws new state of the cube'''
    print('Pressed key =', event.key)

    current_azim = ax.azim
    current_elev = ax.elev

    ax.cla()

    ax.set_xlim3d(0, 3)
    ax.set_ylim3d(0, 3)
    ax.set_zlim3d(0, 3)
    ax.set_axis_off()

    ax.text2D(-0.8, 1, 'Rubikova kostka', fontsize=50, weight='bold', transform=ax.transAxes)
    y = 0.8
    for text in text_manual:
        ax.text2D(-0.8, y, text, fontsize=20, transform=ax.transAxes)
        y -= 0.05
    y = 0.65
    for i, text in enumerate(turn_manual):
        box = dict(boxstyle='round', facecolor=cube.cube_matrix[1, 1, 1].coloring[i], alpha=0.7)
        ax.text2D(-0.8, y, text, fontsize=20, bbox=box, verticalalignment='center', transform=ax.transAxes)
        y -= 0.1
    ax.text2D(-0.8, -0.05, esc_text, fontsize=20, transform=ax.transAxes)
    ax.text2D(-0.8, 0.05, scramble_text, fontsize=20, transform=ax.transAxes)
    ax.text2D(-0.8, 0, clear_text, fontsize=20, transform=ax.transAxes)
    ax.text2D(-0.8, -0.05, esc_text, fontsize=20, transform=ax.transAxes)

    match event.key:
        case 'U':
            cube.Turn_U()
        case 'alt+U':
            cube.Turn_U(3)
        case 'D':
            cube.Turn_D()
        case 'alt+D':
            cube.Turn_D(3)
        case 'R':
            cube.Turn_R()
        case 'alt+R':
            cube.Turn_R(3)
        case 'L':
            cube.Turn_L()
        case 'alt+L':
            cube.Turn_L(3)
        case 'B':
            cube.Turn_B()
        case 'alt+B':
            cube.Turn_B(3)
        case 'F':
            cube.Turn_F()
        case 'alt+F':
            cube.Turn_F(3)
        case 'S':
            cube.scramble()
        case 'C':
            cube.create_cube()
        case 'escape':
            plt.close()
    
    cube.draw_cube(ax)
    ax.view_init(elev=current_elev, azim=current_azim)
    fig.canvas.draw()

    

cube = Cube()
cube.create_cube()

fig = plt.figure()
ax = plt.subplot(111, projection='3d')
ax.set_xlim3d(0, 3)
ax.set_ylim3d(0, 3)
ax.set_zlim3d(0, 3)
ax.set_axis_off()
plt.subplots_adjust(left=0.4)

text_manual = ['(Toggle CapsLock "On")\n',
                'Press key to turn corresponding sides clockwise\n',
                'Press alt+key to turn those sides counterclockwise\n']
turn_manual = ['D: turns bottom side\n',
               'U: turns top side\n',
               'F: turns front side\n',
               'B: turns back side\n',
               'L: turns left side\n',
               'R: turns right side\n']

scramble_text = 'S: scrambles the cube'
clear_text = 'C: clears the cube'
esc_text = 'esc: closes program'

ax.text2D(-0.8, 1, 'Rubikova kostka', fontsize=50, weight='bold', transform=ax.transAxes)

y = 0.8
for text in text_manual:
    ax.text2D(-0.8, y, text, fontsize=20, transform=ax.transAxes)
    y -= 0.05

y = 0.65
for i, text in enumerate(turn_manual):
    box = dict(boxstyle='round', facecolor=cube.cube_matrix[1, 1, 1].coloring[i], alpha=0.7)
    ax.text2D(-0.8, y, text, fontsize=20, bbox=box, verticalalignment='center', transform=ax.transAxes)
    y -= 0.1

ax.text2D(-0.8, 0.05, scramble_text, fontsize=20, transform=ax.transAxes)
ax.text2D(-0.8, 0, clear_text, fontsize=20, transform=ax.transAxes)
ax.text2D(-0.8, -0.05, esc_text, fontsize=20, transform=ax.transAxes)


cube.draw_cube(ax)

fig.canvas.mpl_connect('key_press_event', press)

manager = plt.get_current_fig_manager()
manager.full_screen_toggle()

plt.show()
