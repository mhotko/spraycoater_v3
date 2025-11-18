from dataclasses import dataclass
import numpy as np
import numpy.typing as npt
import cv2

type ColorBGR = tuple[int, int, int]

PIX_TO_REAL_FACTOR = 2.06

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
            cv2.line(opencv_frame, tuple(start.astype(int)), tuple(end.astype(int)), self.color, self.thickness, lineType=cv2.LINE_AA)


class Rectangle:
    def __init__(self, start_point: Point, end_point: Point, color: ColorBGR = (18, 156, 243), thickness: int = 1, padding = 0) -> None:
        self.start_point= start_point
        self.end_point = end_point
        self.color = color
        self.thickness = thickness
        self.padding: int = padding

    
    def pad(self):
        left = min(self.start_point.x, self.end_point.x)
        top = min(self.start_point.y, self.end_point.y)
        right = max(self.start_point.x, self.end_point.x)
        bottom = max(self.start_point.y, self.end_point.y)

        left -= self.padding
        top -= self.padding
        right += self.padding
        bottom += self.padding

        x = left
        y = top
        w = right - left
        h = bottom - top

        return (x, y, w, h)

    def draw_rectangle(self, opencv_frame: npt.NDArray) -> None:
        if self.start_point.x >= 0 and self.start_point.y >= 0 and self.end_point.x >= 0 and self.end_point.y >= 0:
            (x, y, w, h) = self.pad()
            cv2.rectangle(opencv_frame, (x, y), (x+w, y+h), self.color, self.thickness, lineType=cv2.LINE_AA)
    
    def draw_dashed_rectangle(self, opencv_frame: npt.NDArray):
        if self.start_point.x >= 0 and self.start_point.y >= 0 and self.end_point.x >= 0 and self.end_point.y >= 0:
            (x, y, w, h) = self.pad()
            p1 = Point(x, y)
            p2 = Point(x+w, y)
            p3 = Point(x+w, y+h)
            p4 = Point(x, y+h)

            top_line = Line(p1, p2)
            top_line.draw_dashed_line(opencv_frame)

            right_line = Line(p2, p3)
            right_line.draw_dashed_line(opencv_frame)

            bottom_line = Line(p3, p4)
            bottom_line.draw_dashed_line(opencv_frame)

            left_line = Line(p4, p1)
            left_line.draw_dashed_line(opencv_frame)

    
    def update_points(self, new_start_point: Point, new_end_point: Point):
        self.start_point = new_start_point
        self.end_point = new_end_point

class DrawHandler:
    def __init__(self) -> None:
        self.start_point: Point = Point(-1, -1)
        self.end_point: Point = Point(-1, -1)
        self.main_rect = Rectangle(Point(-1, -1), Point(-1, -1), color=(185, 128, 41), thickness=1)
        self.safety_rect = Rectangle(Point(-1, -1), Point(-1, -1), padding=int(10*PIX_TO_REAL_FACTOR))

    def draw(self, opencv_frame: npt.NDArray, start_point: Point, end_point: Point) -> npt.NDArray:
        self.start_point = start_point
        self.end_point = end_point

        self.main_rect.update_points(self.start_point, self.end_point)
        self.safety_rect.update_points(self.start_point, self.end_point)

        self.main_rect.draw_rectangle(opencv_frame)

        self.safety_rect.draw_dashed_rectangle(opencv_frame)

        return opencv_frame