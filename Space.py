import pymunk


def TargetBall(arbiter, space, data):
    target = arbiter.shapes[1]
    target.body.velocity = [0, 0]
    target.body.color = 8
    return True
