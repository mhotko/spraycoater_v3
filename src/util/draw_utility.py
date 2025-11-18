from dataclasses import dataclass
import numpy as np
import numpy.typing as npt
import cv2

type ColorBGR = tuple[int, int, int]

@dataclass
class Point:
    x: int
    y: int

    def get_point_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)
    
    def get_point_np(self) -> npt.NDArray:
        return np.array([self.x, self.y])

class Line:
    def __init__(self, start_point: Point, end_point: Point, color: ColorBGR = (18, 156, 243), thickness: int = 2) -> None:
        self.start_point= start_point
        self.end_point = end_point
        self.color = color
        self.thickness = thickness

    
    def draw_line(self, opencv_frame: npt.NDArray) -> None:
        cv2.line(opencv_frame, self.start_point.get_point_tuple(), self.end_point.get_point_tuple(), self.color, self.thickness)
    
    def draw_dashed_line(self, opencv_frame: npt.NDArray, dash_length = 5) -> None:
        line_vec = self.end_point.get_point_np() - self.start_point.get_point_np()
        line_len = np.linalg.norm(line_vec)
        if line_len == 0:
            return
        line_dir = line_vec / line_len

        # Step along the line in increments of dash_length*2
        n_dashes = int(line_len // (dash_length * 2))
        for i in range(n_dashes + 1):
            start_dist = i * dash_length * 2
            end_dist = min(start_dist + dash_length, line_len)
            start = self.start_point.get_point_np() + line_dir * start_dist
            end = self.start_point.get_point_np() + line_dir * end_dist
            cv2.line(opencv_frame, tuple(start.astype(int)), tuple(end.astype(int)), self.color, self.thickness)


# class Rectangle:
#     def __init__(self, ) -> None:
#         self.point_NW: Point = 

class DrawHandler:
    def __init__(self) -> None:
        self.start_point: Point = Point(-1, -1)
        self.end_point: Point = Point(-1, -1)

    def draw(self, opencv_frame: npt.NDArray, start_point: Point, end_point: Point) -> npt.NDArray:
        self.start_point = start_point
        self.end_point = end_point

        line = Line(self.start_point, self.end_point)
        line.draw_dashed_line(opencv_frame)
        return opencv_frame