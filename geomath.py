import math


def calculate_azimuth(x1, y1, x2, y2):
    # X horizontale, Y verticale
    '''
        Returning azimuth value in GRADS
        (400 GRADS == 2 PI == 360 DEGREES)
    '''
    if None in (x1, y1, x2, y2):
        return None
    dy = y2-y1
    dx = x2-x1
    if dx == 0 and dy == 0: # if points are the same
        return None
    if dx == 0:
        if dy >= 0:
            return 0  # verticale up
        else:
            return 200  # verticale down
    if dy == 0:
        if dx >= 0:
            return 100  # horizontal right
        else:
            return 300  # horizontal left
    fi = math.atan(dy/dx) * 63.66197723  # RADIANS -> GRADS
    if dx > 0 and dy > 0:  # Q I (right, upper)
        return 100-fi
    if dx > 0 and dy < 0:  # Q II (right, lower)
        return 100-fi
    if dx < 0 and dy < 0:  # Q III (left, lower)
        return 300-fi
    if dx < 0 and dy > 0:  # Q IV  (left, upper)
        return 300-fi
    return None  # no azimuth


def calculate_point_by_azimuth(x1, y1, a_grad, d):
    if None in (x1, y1, a_grad, d):
        return None, None
    x2 = x1 + d*math.sin(a_grad/63.66197723)
    y2 = y1 + d*math.cos(a_grad/63.66197723)
    return x2, y2


def calculate_length(x1, y1, x2, y2):
    if None in (x1, y1, x2, y2):
        return None
    else:
        d = math.sqrt(((y2-y1)**2)+((x2-x1)**2))
        return d


if __name__ == "__main__":
    '''
    If run as a main program, run tests
    '''
    import unittest
    unittest.main()
