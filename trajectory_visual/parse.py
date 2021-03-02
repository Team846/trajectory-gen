from typing import List, Any
from manim import *
import numpy as np


class MarkerCommand:
    def __init__(self, line: List[Any]):
        if line[0] != "MARKER":
            raise ValueError()

        self.x = float(line[1])
        self.y = float(line[2])


class WaypointCommand:
    def __init__(self, line: List[Any]):
        if line[0] != "WAYPOINT":
            raise ValueError()

        self.x = float(line[1])
        self.y = float(line[2])


class TargetCommand:
    def __init__(self, line: List[Any]):
        if line[0] != "TARGET":
            raise ValueError()

        self.t = float(line[1])
        self.x = float(line[2])
        self.y = float(line[3])


class WaypointHitCommand:
    def __init__(self, line: List[Any]):
        if line[0] != "WAYPOINT_HIT":
            raise ValueError()

        self.t = float(line[1])
        self.x = float(line[2])
        self.y = float(line[3])


class PositionCommand:
    def __init__(self, line: List[Any]):
        if line[0] != "POSITION":
            raise ValueError()

        self.t = float(line[1])
        self.x = float(line[2])
        self.y = float(line[3])
        self.theta = float(line[4])


class VelocityCommand:
    def __init__(self, line: List[Any]):
        if line[0] != "VELOCITY":
            raise ValueError()

        self.t = float(line[1])
        self.v_l = float(line[2])
        self.v_r = float(line[3])


class Parser:
    def __init__(self, file_name):
        self.commands = []

        command_types = {
            "MARKER": MarkerCommand,
            "WAYPOINT": WaypointCommand,
            "TARGET": TargetCommand,
            "WAYPOINT_HIT": WaypointHitCommand,
            "POSITION": PositionCommand,
            "VELOCITY": VelocityCommand,
        }

        with open(file_name, "r") as file:
            for line in file:
                args = line.split(" ")
                self.commands.append(command_types[args[0]](args))

        for c in self.commands:
            print(c)
