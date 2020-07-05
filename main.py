import nxt.locator
import pygame
import robot_controls
from nxt.motor import *
from nxt.sensor import *

import speech_recognition as sr

pygame.init()
pygame.display.set_caption('MindStorm')
win = pygame.display.set_mode((600, 400))
font = pygame.font.SysFont('comicsand', 30, True)
clock = pygame.time.Clock()


class AlphaRex:
    def __init__(self):
        # body
        self.brick = nxt.locator.find_one_brick(name='')
        self.m_left = Motor(self.brick, PORT_B)
        self.m_right = Motor(self.brick, PORT_C)
        self.m_middle = Motor(self.brick, PORT_A)
        # power for motors
        self.power_left_motor = 0
        self.power_right_motor = 0
        # sensors
        # self.ultrasonic = Ultrasonic(self.brick, PORT_4)
        # turning statements
        self.go_forward = False
        self.go_backwards = False
        self.turning_right = False
        self.turning_left = False
        # utility statements
        self.firing_cannon = False
        self.distance_sensor = 0
        # control options
        self.key_controlled = True
        self.voice_controlled = False
        # commands for voice control
        self.commands = ['go forward', 'go backwards', 'turn left', 'turn right', 'fire', 'stop']

    def run_motor(self):
        self.m_left.run(self.power_left_motor, True)
        self.m_right.run(self.power_right_motor, True)

    def spin_around(self):
        self.m_left.turn(100, 360)
        self.m_right.turn(-100, 360)

    def shut_down(self):
        self.m_left.idle()
        self.m_right.idle()
        self.m_middle.idle()

    def stop(self):
        if self.power_right_motor > 0:
            self.power_right_motor -= 1
            self.m_right.idle()
        elif self.power_right_motor < 0:
            self.power_right_motor += 1
            self.m_right.idle()

        if self.power_left_motor > 0:
            self.power_left_motor -= 1
            self.m_left.idle()
        elif self.power_left_motor < 0:
            self.power_left_motor += 1
            self.m_left.idle()

    def forward(self):
        if self.power_right_motor < 0:
            if self.power_left_motor < 0:
                self.power_left_motor = 0
                self.power_right_motor = 0

        if not self.turning_left:
            if self.power_left_motor != 100:
                self.power_left_motor += 1

        if not self.turning_right:
            if self.power_right_motor != 100:
                self.power_right_motor += 1

    def backward(self):
        if self.power_right_motor > 0:
            if self.power_left_motor > 0:
                self.power_left_motor = 0
                self.power_right_motor = 0

        if not self.turning_left:
            if self.power_left_motor != -100:
                self.power_left_motor -= 1

        if not self.turning_right:
            if self.power_right_motor != -100:
                self.power_right_motor -= 1

    def turn_left(self):
        if not self.go_backwards and not self.go_forward:
            if self.power_left_motor != -100:
                self.power_left_motor -= 1
            if self.power_right_motor != 100:
                self.power_right_motor += 1

        elif self.power_left_motor > 0:
            if self.power_left_motor != -100:
                self.power_left_motor -= 1
        elif self.power_left_motor < 0:
            if self.power_left_motor != 100:
                self.power_left_motor += 1

    def turn_right(self):
        if not self.go_backwards and not self.go_forward:
            if self.power_right_motor != -100:
                self.power_right_motor -= 1
            if self.power_left_motor != 100:
                self.power_left_motor += 1

        elif self.power_right_motor > 0:
            if self.power_right_motor != -100:
                self.power_right_motor -= 1
        elif self.power_right_motor < 0:
            if self.power_right_motor != 100:
                self.power_right_motor += 1

    def shoot(self):
        self.firing_cannon = True
        self.m_middle.turn(100, 360)

    def measure_distance(self):
        distance = self.ultrasonic.get_sample()
        self.distance_sensor = distance

class ExploreRobot:
    def __init__(self):
        # body
        self.brick = nxt.locator.find_one_brick(debug=True, name='NXT')
        self.m_left = Motor(self.brick, PORT_B)
        self.m_right = Motor(self.brick, PORT_C)
        self.m_middle = Motor(self.brick, PORT_A)
        # power for motors
        self.power_left_motor = 0
        self.power_right_motor = 0
        # sensors
        self.ultrasonic = Ultrasonic(self.brick, PORT_4)
        # turning statements
        self.go_forward = False
        self.go_backwards = False
        self.turning_right = False
        self.turning_left = False
        # utility statements
        self.firing_cannon = False
        self.distance_sensor = 0
        # control options
        self.key_controlled = True
        self.voice_controlled = False
        # commands for voice control
        self.commands = ['go forward', 'go backwards', 'turn left', 'turn right', 'fire', 'stop']

    def run_motor(self):
        self.m_left.run(self.power_left_motor, True)
        self.m_right.run(self.power_right_motor, True)

    def spin_around(self):
        self.m_left.turn(100, 360)
        self.m_right.turn(-100, 360)

    def shut_down(self):
        self.m_left.idle()
        self.m_right.idle()
        self.m_middle.idle()

    def stop(self):
        if self.power_right_motor > 0:
            self.power_right_motor -= 1
            self.m_right.idle()
        elif self.power_right_motor < 0:
            self.power_right_motor += 1
            self.m_right.idle()

        if self.power_left_motor > 0:
            self.power_left_motor -= 1
            self.m_left.idle()
        elif self.power_left_motor < 0:
            self.power_left_motor += 1
            self.m_left.idle()

    def forward(self):
        if self.power_right_motor < 0:
            if self.power_left_motor < 0:
                self.power_left_motor = 0
                self.power_right_motor = 0

        if not self.turning_left:
            if self.power_left_motor != 100:
                self.power_left_motor += 1

        if not self.turning_right:
            if self.power_right_motor != 100:
                self.power_right_motor += 1

    def backward(self):
        if self.power_right_motor > 0:
            if self.power_left_motor > 0:
                self.power_left_motor = 0
                self.power_right_motor = 0

        if not self.turning_left:
            if self.power_left_motor != -100:
                self.power_left_motor -= 1

        if not self.turning_right:
            if self.power_right_motor != -100:
                self.power_right_motor -= 1

    def turn_left(self):
        if not self.go_backwards and not self.go_forward:
            if self.power_left_motor != -100:
                self.power_left_motor -= 1
            if self.power_right_motor != 100:
                self.power_right_motor += 1

        elif self.power_left_motor > 0:
            if self.power_left_motor != -100:
                self.power_left_motor -= 1
        elif self.power_left_motor < 0:
            if self.power_left_motor != 100:
                self.power_left_motor += 1

    def turn_right(self):
        if not self.go_backwards and not self.go_forward:
            if self.power_right_motor != -100:
                self.power_right_motor -= 1
            if self.power_left_motor != 100:
                self.power_left_motor += 1

        elif self.power_right_motor > 0:
            if self.power_right_motor != -100:
                self.power_right_motor -= 1
        elif self.power_right_motor < 0:
            if self.power_right_motor != 100:
                self.power_right_motor += 1

    def shoot(self):
        self.firing_cannon = True
        self.m_middle.turn(100, 360)

    def measure_distance(self):
        distance = self.ultrasonic.get_sample()
        self.distance_sensor = distance


class RoboArm:
    def __init__(self):
        self.name = 'Roboarm'
        # body
        self.brick = nxt.locator.find_one_brick(debug=True)
        self.m_base = Motor(self.brick, PORT_A)
        self.m_arm = Motor(self.brick, PORT_B)
        self.m_hand = Motor(self.brick, PORT_C)
        # power for motors
        self.power_m_base = 0
        self.power_m_arm = 0
        self.power_m_hand = 0

    def turn_base_right(self):
        self.m_base.turn(-100, 180)

    def turn_base_left(self):
        self.m_base.turn(100, 180)

    def lower_arm(self):
        try:
            self.m_arm.turn(10, 30)
        except:
            self.m_arm.idle()

    def rais_arm(self):
        try:
            self.m_arm.turn(-10  , 30)
        except:
            self.m_arm.idle()

roboarm1 = RoboArm()

#explore1 = ExploreRobot()

#alpharex1 = AlphaRex()


def draw_control_window(font, robot):
    if robot.name == 'explore1':
        win.fill((0, 0, 0))
        text = font.render('power motor: left ' + str(robot.power_left_motor) +
                           ' right ' + str(robot.power_right_motor), 1, (255, 255, 255))

        text1 = font.render('                forward =   ' + str(robot.go_forward), 1, (255, 255, 255))

        text2 = font.render('turning direction: ' + ' left= ' + str(robot.turning_left) +
                            '  right= ' + str(robot.turning_right), 1, (255, 255, 255))

        text3 = font.render(''*16 + 'backwards = ' + str(robot.go_backwards), 1, (255, 255, 255))

        text4 = font.render(''*16 + 'distance sensor = ' + str(robot.distance_sensor), 1, (255, 255, 255))

        text5 = font.render(''*16 + 'Cannon = ' + str(robot.firing_cannon), 1, (255, 255, 255))

        win.blit(text, (10, 10))
        win.blit(text1, (10, 40))
        win.blit(text2, (10, 60))
        win.blit(text3, (10, 80))
        win.blit(text4, (10, 100))
        win.blit(text5, (10, 120))

        pygame.display.update()
    if robot.name == 'roboarm':
        win.fill((0, 0, 0))

        pygame.display.update()


def main_robot_loop(robot):
    run = True
    while run:
        clock.tick(100)

        robot_controls.key_control_robot(robot)

        draw_control_window(font, robot)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                robot.shut_down()
                return False


#main_robot_loop(alpharex1)
#main_robot_loop(explore1)
main_robot_loop(roboarm1)