import pygame
import speech_recognition as sr
clock = pygame.time.Clock()


# to get audio for voice control
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ''

        try:
            said = r.recognize_google(audio)
            print('command:', said)
        except Exception as e:
            print('Exception: ' + str(e))

    return said


def key_control_robot(robot):
    if robot == 'explore1':
        if robot.key_controlled:

            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                robot.go_forward = True
                robot.forward()
            if not keys[pygame.K_UP]:
                robot.go_forward = False

            if keys[pygame.K_DOWN]:
                robot.go_backwards = True
                robot.backward()
            if not keys[pygame.K_DOWN]:
                robot.go_backwards = False

            if keys[pygame.K_LEFT]:
                robot.turning_left = True
                robot.turn_left()
            if not keys[pygame.K_LEFT]:
                robot.turning_left = False

            if keys[pygame.K_RIGHT]:
                robot.turning_right = True
                robot.turn_right()
            if not keys[pygame.K_RIGHT]:
                robot.turning_right = False

            if keys[pygame.K_u]:
                robot.measure_distance()

            if keys[pygame.K_SPACE]:
                print('fire')
                robot.shoot()
                robot.firing_cannon = True
            if not keys[pygame.K_SPACE]:
                robot.firing_cannon = False

            if not keys[pygame.K_UP]:
                if not keys[pygame.K_DOWN]:
                    if not keys[pygame.K_RIGHT]:
                        if not keys[pygame.K_LEFT]:
                            robot.stop()
                            return 'stopped'

            robot.run_motor()

    elif robot.name == 'Roboarm':
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            robot.lower_arm()

        if not keys[pygame.K_UP]:
            pass

        if keys[pygame.K_DOWN]:
            robot.rais_arm()

        if not keys[pygame.K_DOWN]:
            pass

        if keys[pygame.K_LEFT]:
            robot.turn_base_left()

        if not keys[pygame.K_LEFT]:
            pass

        if keys[pygame.K_RIGHT]:
            robot.turn_base_right()

        if not keys[pygame.K_RIGHT]:
            pass

        if keys[pygame.K_SPACE]:
            pass

        if not keys[pygame.K_SPACE]:
            pass






def voice_control_robot(robot):
    if robot.voice_controlled:
        run = True
        while run:
            clock.tick(10)

            print('explore1 awaiting command')

            command = get_audio().split()

            if 'go' in command and 'forward' in command:
                print('going forward')
                robot.forward()

            if 'go' in command and 'backwards' in command:
                print('going backwards')

                robot.backward()

            if 'turn' in command and 'left' in command:
                print('turning left')
                robot.turn_left()

            if 'turn' in command and 'right' in command:
                print('turning right')
                robot.turn_right()

            if 'fire' in command or 'fireball' in command:
                print('fire cannon')
                robot.shoot()

            if 'stop' in command:
                print('stopping')
                robot.stop()

            if 'shut' in command and 'down' in command:
                robot.stop()
                run = False

            if not command:
                robot.stop()