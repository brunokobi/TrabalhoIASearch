
from abc import ABC, abstractclassmethod
import cv2
import numpy as np

from src.problems import MazeProblem


class ViewerInterface(ABC):
    @abstractclassmethod
    def update(self, state=None, generated=[], expanded=[], path=[]) -> None:
        """ Update the viewer state """

    @abstractclassmethod
    def pause(self) -> None:
        """ Show the visualization continually until the user close the window or press enter. """


class MazeViewer(ViewerInterface):
    START_COLOR = (0, 255, 0)
    GOAL_COLOR = (0, 255, 255)
    EXPANDED_COLOR = (209, 206, 0)
    GENERATED_COLOR = (255, 0, 0)
    PATH_COLOR = (0,0, 255)
    WALL_COLOR = (255, 255, 255)

    def __init__(self, maze: MazeProblem, zoom: float = 50, step_time_miliseconds: int = -1):
        self._maze = maze
        self._zoom = zoom
        self._step = step_time_miliseconds

    def update(self, state=None, generated=[], expanded=[], path=[], titulo=None):
        # To understand the image representation in opencv, refer to the following links:
        # https://www.pyimagesearch.com/2021/01/20/opencv-getting-and-setting-pixels/
        # https://codewords.recurse.com/issues/six/image-processing-101#:~:text=In%20OpenCV%2C%20images%20are%20represented,of%20values%20representing%20its%20color.&text=Where%20%5B72%2099%20143%5D%20%2C,values%20of%20that%20one%20pixel.

        maze_img = np.array(self._maze._maze).astype(np.uint8) * 255

        # inverte pixels pretos e brancos para que os obstáculos fiquem pretos
        # e as áreas livres são brancas.
        maze_img = 255 - maze_img
        maze_img = cv2.cvtColor(maze_img, cv2.COLOR_GRAY2BGR)


        self._draw_cells(maze_img, path, MazeViewer.PATH_COLOR)

        self._draw_cell(maze_img,
                        self._maze.initial_state(),
                        MazeViewer.START_COLOR)

        self._draw_cell(maze_img,
                        self._maze._goal_state,
                        MazeViewer.GOAL_COLOR)

        self._draw_cells(maze_img, generated, MazeViewer.GENERATED_COLOR)
        self._draw_cells(maze_img, expanded, MazeViewer.EXPANDED_COLOR)

        maze_img = self._increase_image_size(maze_img, zoom=self._zoom)
        self._draw_grid(maze_img, self._zoom)

        cv2.imshow('  '+titulo + '   --------------  MAPA ='+self._maze.n_rows.__str__()+'x'+self._maze.n_cols.__str__(), maze_img)
        cv2.waitKey(self._step)

    def pause(self) -> None:
        cv2.waitKey(-1)

    def _increase_image_size(self, img, zoom=10):
        big_img = np.zeros((
            img.shape[0] * zoom,
            img.shape[1] * zoom,
            3
        ))

        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                r_st = zoom * i
                r_end = zoom * (i + 1)
                c_st = zoom * j
                c_end = zoom * (j + 1)
                big_img[r_st: r_end, c_st: c_end] = img[i, j]

        return big_img

    def _draw_grid(self, maze_img, zoom):
        for i in range(0, maze_img.shape[1], zoom):
            cv2.line(
                maze_img,
                (i, 0),
                (i, maze_img.shape[0]),
                color=(0, 0, 0),
                thickness=1
            )

        for j in range(0, maze_img.shape[0], zoom):
            cv2.line(
                maze_img,
                (0, j),
                (maze_img.shape[1], j),
                color=(0, 0, 0),
                thickness=1
            )

    def _draw_cells(self, maze_img, cells, color):
        for cell in cells:
            self._draw_cell(maze_img, cell, color)

    def _draw_cell(self, maze_img, cell, color):
        if type(cell) != tuple:
            cell = cell.state
        row, col = cell
        maze_img[row, col] = color
