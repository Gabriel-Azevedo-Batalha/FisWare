import pymunk
import pyxel


# Collision Handlers
def BallTarget(arbiter, space, data):
    target = arbiter.shapes[1]
    ball = arbiter.shapes[0]
    target.body.velocity = [0, 0]
    target.body.color = 0
    if not target.sensor and not ball.body.mute:
        pyxel.play(0, 58)
    target.sensor = True
    return True


def WallTarget(arbiter, space, data):
    target = arbiter.shapes[1]
    target.sensor = False
    return True


def PlayerTarget(arbiter, space, data):
    target = arbiter.shapes[1]
    # Lose game
    if target.body.velocity[0] > 0:
        target.body.position = [190, 0]
    elif target.body.velocity[0] < 0:
        target.body.position = [-10, 0]
    elif target.body.velocity[0] == 0 and target.body.velocity[1] != 0:
        target.body.position = [0, 130]
    return True


def PlayerBall(arbiter, space, data):
    player = arbiter.shapes[0]
    # Lose game
    player.body.position = (-5, 0)
    return False


# Space Class - Exclusive for Pong (Self-implemented)
class Space():
    # Apply Velocity
    def applyVel(self, position, velocity):
        position[0] += velocity[0]
        position[1] += velocity[1]
        return position

    # Check and apply collisions
    def checkCollision(self, ball, ballVelocity, body="Walls", mute=False):
        x, y = ballVelocity
        # Check for Player/Enemy Collisions
        if body != "Walls":
            if ((ball[0] == body[0]
               or (body[0] == 1 and x + ball[0] <= 2)            # If is player
               or (body[0] != 1 and x + ball[0] >= body[0]-1))   # If is enemy
               and ball[1] > body[1] - 10
               and ball[1] <= body[1] + 10):
                x *= -1.1  # Reflect and accelerate ball
                angle = ball[1] - body[1]
                y += angle/10  # Changing vertical velocity
                if not mute:
                    pyxel.play(0, 60)
        # Check for Wall Collisions
        else:
            if ball[1] <= 0 or ball[1] >= 119:
                y *= -1  # Reflect ball
                if not mute:
                    pyxel.play(0, 63)
            # Lose
            elif ball[0] < 0:
                return False
            # Win
            elif ball[0] > 179:
                return True
        return x, y
