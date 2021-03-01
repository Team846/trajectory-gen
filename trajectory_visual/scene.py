from manim import *
from parse import Parser
from math import atan


class VisualizeTrajectory( MovingCameraScene):
   
    # def setup(self):            
    #     # GraphScene.setup(self)
    #     MovingCameraScene.setup(self)

    def construct(self):
        
        self.camera_frame.set_width(80)
        self.camera_frame.set_height(45)
        parser = Parser("example.txt")

        robot = Square()
        self.add(robot)
        self.wait(1)

        #should start at first waypt
        t = 0
        x = 5
        y = 3.2
        for c in parser.commands:
            dt = c.t - t
            dx = c.x - x
            dy = c.y - y
            path = Line([x,y,0], [c.x, c.y, 0])
            t = c.t
            x = c.x
            y = c.y
            print([x,y,0])
            print([x+dx, y+dy, 0])
            self.add(Dot(point=[x,y,0]))
            print(atan((path.end[0] - path.start[0])/(path.end[1]-path.start[1])))
            # path = Line([x,y,0], [x+dx, y+dy, 0])
            self.play(MoveAlongPath(robot, path))
            self.play(Rotating(robot, radians=atan((path.end[0] - path.start[0])/(path.end[1]-path.start[1])), run_time = 1))

            # self.wait(dt)
