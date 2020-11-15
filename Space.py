import pymunk


def BallTarget(arbiter, space, data):
    target = arbiter.shapes[1]
    target.body.velocity = [0, 0]
    target.body.color = 0
    # If bellow line is commented target turns touchable
    target.sensor = True
    return True

def PlayerTarget(arbiter, space, data):
    target = arbiter.shapes[1]
    if target.body.velocity[0] > 0:
        target.body.position = [190 , 0]
    elif target.body.velocity[0] < 0:
        target.body.position = [-10 , 0]
    elif target.body.velocity[0] == 0 and target.body.velocity[1] != 0:
        target.body.position = [0 , 130]
    return True
