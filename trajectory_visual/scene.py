from manim import *
from parse import *
from math import atan, pi,radians, cos, sin

class Waypoint(Dot):
    def __init__(self, point=ORIGIN, **kwargs):
        super().__init__(point=point, **kwargs)
        self.point=point
    def get_point(self):
        return self.point

class TimedAnimationGroup(AnimationGroup):
    '''
    Timed animations may be defined by setting 'start_time' and 'end_time' or 'run_time' in CONFIG of an animation.
    If they are not defined, the Animation behaves like it would in AnimationGroup.
    However, lag_ratio and start_time combined might cause unexpected behavior.
    '''
    def build_animations_with_timings(self):
        """
        Creates a list of triplets of the form
        (anim, start_time, end_time)
        """
        '''
        mostly copied from manimlib.animation.composition (AnimationGroup)
        '''
        self.anims_with_timings = []
        curr_time = 0
        for anim in self.animations:
            # check for new parameters start_time and end_time,
            # fall back to normal behavior if not provided
            try:
                start_time = anim.start_time
            except:
                start_time = curr_time
            try:
                end_time = anim.end_time
            except:
                end_time = start_time + anim.get_run_time()
            self.anims_with_timings.append(
                (anim, start_time, end_time)
            )
            # Start time of next animation is based on
            # the lag_ratio
            curr_time = interpolate(
                start_time, end_time, self.lag_ratio
            )



class VisualizeTrajectory(MovingCameraScene):
   
    # def setup(self):            
    #     # GraphScene.setup(self)
    #     MovingCameraScene.setup(self)

    def construct(self):

        
        line_half = 5
        self.camera_frame.set_width(50)
        self.camera_frame.set_height(50)
        parser = Parser("slalom.txt")
    
        # corner_bot = Square()
        # corner_bot.move_to(5*RIGHT + 3*UP)
        # self.add(corner_bot)
        

        sq = Square()
        line = Line([ -line_half,0, 0], [line_half,0,0])

        robot = sq
        self.add(robot)

        #should start at first waypt
        dt = 0

        t = 579.6442099999999
        x = -7.127210879437951
        y = -0.3698073445908606
        start_angle = 132.33274841308597
        # current_target = Waypoint

        curr_vel_left = Arrow()
        curr_vel_right = Arrow()

        animations = []
        robot_movements = []
        arrow_movements = []
        waypts = []
        hit_waypoints = []
        init_wypts = []
        
        self.play(Rotate(robot, -pi/2 + radians(start_angle)))
        # print(start_angle)
        robot.shift([x, y, 0])
        for c in parser.commands:
            if(type(c) is PositionCommand):
                dt = c.t - t
                dx = c.x - x
                dy = c.y - y
                dtheta = c.theta - start_angle

            
                path = Line([x,y,0], [c.x, c.y, 0])

                robot_movements.append(AnimationGroup(Rotate(robot,angle=radians(-dtheta), run_time = dt, rate_func=rate_functions.linear), MoveAlongPath(robot, path, run_time=dt, rate_func=rate_functions.linear), self.camera.frame.animate.move_to([c.x, c.y, 0])))                
                t = c.t
                x = c.x
                y = c.y

                start_angle = c.theta
            elif(type(c) is WaypointHitCommand):
                dot = Dot(color=RED, point=[c.x, c.y, 0])
                dot_2 = Dot(color=GREEN, point=[c.x, c.y, 0])
                robot_movements.append(ReplacementTransform(dot,dot_2, run_time = c.t - t))
                
            # elif(type(c) is TargetCommand):
            #     robot_movements.append(FadeOut(Arrow([x,y,0], [c.x, c.y, 0])))
                # robot_movements.append(FadeIn)
                # robot_movements.append(FadeOut(dot))

            # elif(type(c) is VelocityCommand):
            #     dt_this = c.t-t

            #     left_arrow = Arrow(4*RIGHT+4*UP, 4*RIGHT+4*UP+[0, c.v_l, 0])
            #     right_arrow = Arrow(6*RIGHT+4*UP,6*RIGHT+4*UP+[0, c.v_r, 0])
            #     arrow_movements.append(AnimationGroup(ReplacementTransform(curr_vel_left, left_arrow, run_time=dt_this), ReplacementTransform(curr_vel_right, right_arrow, start_time=c.t,run_time = dt_this)))
            #     # arrow_movements.append(ReplacementTransform(curr_vel_left, left_arrow, start_time=c.t, run_time=dt_this))
            #     # animations.append(ReplacementTransform(curr_vel_right, right_arrow, start_time=c.t,run_time = dt_this))

            #     # self.play(Transform(curr_vel_left, left_arrow, run_time=dt), Transform(curr_vel_right, right_arrow, run_time = dt))
            #     # self.play(FadeOut(curr_vel_left), FadeOut(curr_vel_right))
            #     curr_vel_left = left_arrow
            #     curr_vel_right = right_arrow
        print(robot_movements)
        self.play(Succession(*robot_movements), TimedAnimationGroup(*animations))
        