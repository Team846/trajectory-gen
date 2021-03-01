from manim import *
from parse import Parser


class VisualizeTrajectory(Scene):
    def construct(self):

        parser = Parser("trajectory_visual/example.txt")
        print(config.frame_width, config.frame_height)

        robot = Square()
        self.add(robot)
        self.wait(1)

        t = 0
        x = 0
        y = 0
        for c in parser.commands:
            dt = c.t - t
            dx = c.x - x
            dy = c.y - y
            t = c.t
            x = c.x
            y = c.y

            robot.shift([dx, dy, 0])
            self.wait(dt)
