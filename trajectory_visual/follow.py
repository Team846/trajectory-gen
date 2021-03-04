from manim import *
from parse import *
from math import atan, pi,radians, cos, sin
from scene import TimedAnimationGroup

class Waypoint(Dot):
    def __init__(self, point=ORIGIN, **kwargs):
        super().__init__(point=point, **kwargs)
        self.point=point
    def get_point(self):
        return self.point
        
class VisualizeTrajectory(MovingCameraScene):
   
    # def setup(self):            
    #     # GraphScene.setup(self)
    #     MovingCameraScene.setup(self)

    def construct(self):

        
        line_half = 5
        self.camera_frame.set_width(50)
        self.camera_frame.set_height(50)
        parser = Parser("truncated.txt")
    

        sq = Square()
        line = Line([ -line_half,0, 0], [line_half,0,0])

        # robot = sq
        # self.add(robot)

        #should start at first waypt
        dt = 0

        t = 36.755131999999996
        x = 0.0
        y = 0.0
        start_angle = 0.17705383896827698
        # current_target = Waypoint

        animations = []
        robot_movements = []
        arrow_movements = []
        waypts = []
        hit_waypoints = []
        init_wypts = []
        
        # self.play(Rotate(robot, -pi/2 + radians(start_angle)))
        # # print(start_angle)
        # robot.shift([x, y, 0])
        for c in parser.commands:
            # if(type(c) is PositionCommand):
            #     dt = c.t - t
            #     dx = c.x - x
            #     dy = c.y - y
            #     dtheta = c.theta - start_angle

            
            #     path = Line([x,y,0], [c.x, c.y, 0])

            #     robot_movements.append(AnimationGroup(Rotate(robot,angle=radians(-dtheta), run_time = dt, rate_func=rate_functions.linear), MoveAlongPath(robot, path, run_time=dt, rate_func=rate_functions.linear), self.camera.frame.animate.move_to([c.x, c.y, 0])))                
            #     t = c.t
            #     x = c.x
            #     y = c.y

            #     start_angle = c.theta
            if(type(c) is WaypointCommand):
                dot = Dot([c.x, c.y, 0])
                self.add(dot)
                self.play(FadeIn(dot, run_time = c.t-t))
            # elif(type(c) is WaypointHitCommand):
            #     dot = Dot(color=RED, point=[c.x, c.y, 0])
            #     dot_2 = Dot(color=GREEN, point=[c.x, c.y, 0])
            #     target_vec = Arrow([c.x, c.y, 0], [c.new_target_x, c.new_target_y, 0], color=BLUE)
            #     robot_movements.append(Succession(ReplacementTransform(dot,VGroup(dot_2, target_vec), run_time = c.t - t), FadeOut(target_vec), lag_time=0.1))
        # print(robot_movements)
        # self.play(AnimationGroup(Succession(*robot_movements)))
        