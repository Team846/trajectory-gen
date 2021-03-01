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
        start_angle = 0
        for c in parser.commands:
            dt = c.t - t
            dx = c.x - x
            dy = c.y - y
            path = Line([x,y,0], [c.x, c.y, 0])
            
            
            if(dx!=0):
                self.play(Rotate(robot, angle=atan(dy/dx)-start_angle, run_time = 1))
            t = c.t
            x = c.x
            y = c.y
            # print([x,y,0])
            # print([x+dx, y+dy, 0])
            self.add(Dot(point=[x,y,0]))
            self.play(MoveAlongPath(robot, path))
            if(dx != 0):
                start_angle = atan(dy/dx)
            else:
                start_angle = 0


            # self.wait(dt)
