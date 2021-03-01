from typing import List, Any
from manim import *
import numpy as np

class PositionCommand:
    def __init__(self, line: List[Any]):
        if line[0] != "POSITION":
            raise ValueError()

        self.t = float(line[1])
        self.x = float(line[2])
        self.y = float(line[3])
        self.theta = float(line[4])

    def __str__(self):
        return f"POSITION {self.t} {self.x} {self.y} {self.theta}"


class Parser:
    def __init__(self, file_name):
        self.commands = []

        command_types = {
            "POSITION": PositionCommand,
        }

        with open(file_name, "r") as file:
            for line in file:
                args = line.split(" ")
                self.commands.append(command_types[args[0]](args))

        for c in self.commands:
            print(c)
