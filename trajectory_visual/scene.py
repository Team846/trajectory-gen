from manim import *
from parse import *
from math import atan, pi,radians, cos, sin

class PointAnim(Animation):
    def __init__(self, point, start_time, rate_func, scene, wmobject, *kwargs):
        self.point =point
        self.start_time = start_time
        self.scene = scene
        self.mobject = mobject
        scene.add(point)

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

        animations = []
        
        line_half = 5
        self.camera_frame.set_width(30)
        self.camera_frame.set_height(20)
        parser = Parser("truncated.txt")
        corner_bot = Square()
        corner_bot.move_to(5*RIGHT + 3*UP)
        

        sq = Square()
        line = Line([ -line_half,0, 0], [line_half,0,0])

        robot = Group(sq, line)
        self.add(robot)

        #should start at first waypt

        t_og = 122.700924
        t = 122.700924
        x = -8.923275006028492
        y = -8.190662038694752
        start_angle = 145.67926025390625

        curr_vel_left = Arrow()
        curr_vel_right = Arrow()
        
        self.play(Rotate(robot, -pi/2 + radians(start_angle)))
        # print(start_angle)
        robot.move_to([x, y, start_angle])
        for c in parser.commands:
            if(type(c) is WaypointCommand):
                self.add(Dot(color=RED, point=[c.x, c.y, 0]))
            else:
                continue
        for c in parser.commands:
            if(type(c) is PositionCommand):
                dt = c.t - t
                dx = c.x - x
                dy = c.y - y
                dtheta = c.theta - start_angle

            
                path = Line([x,y,0], [c.x, c.y, 0])

                animations.append(Rotate(robot,angle=radians(-dtheta), start_time=c.t, run_time = dt, rate_func=rate_functions.linear))
                animations.append(MoveAlongPath(robot, path, start_time=c.t,run_time=dt, rate_func=rate_functions.linear))
                
                t = c.t
                x = c.x
                y = c.y

                
                # self.play(Rotate(robot,angle=radians(-dtheta) , run_time = dt),MoveAlongPath(robot, path, run_time=dt, rate_func=rate_functions.linear))
                start_angle = c.theta
                # print(start_angle)
            elif(type(c) is WaypointHitCommand):
                print("Waypoint Hit")
                # dot = Dot(color=GREEN, point=[c.x, c.y, 0])
                animations.append(ShowCreation(Dot(color=GREEN, point=[c.x, c.y, 0]),start_time=t, rate_func=rate_functions.linear))
            elif(type(c) is TargetCommand):
                dot = Dot(color=BLUE, point=[c.x, c.y, 0])
                animations.append(ShowCreation(dot, start_time=t))
            elif(type(c) is VelocityCommand):
                dt_this = c.t-t

                left_arrow = Arrow(4*RIGHT+4*UP, 4*RIGHT+4*UP+[0, c.v_l, 0])
                right_arrow = Arrow(6*RIGHT+4*UP,6*RIGHT+4*UP+[0, c.v_r, 0])

                animations.append(ReplacementTransform(curr_vel_left, left_arrow, start_time=c.t, run_time=dt_this))
                animations.append(ReplacementTransform(curr_vel_right, right_arrow, start_time=c.t,run_time = dt_this))

                # self.play(Transform(curr_vel_left, left_arrow, run_time=dt), Transform(curr_vel_right, right_arrow, run_time = dt))
                # self.play(FadeOut(curr_vel_left), FadeOut(curr_vel_right))
                curr_vel_left = left_arrow
                curr_vel_right = right_arrow
        print(animations)
        self.play(TimedAnimationGroup(*animations))
        