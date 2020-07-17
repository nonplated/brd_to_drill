import math

def calculate_azimuth(x1,y1,x2,y2): #Y verticale,  X horizontale
    '''
        Returning value in GRAD (400 GRAD == 2PI == 360 degress)
    '''
    if x1 is None or y1 is None or x2 is None or y2 is None: return None
    dy=y2-y1
    dx=x2-x1
    if dx==0:
        if dy>=0: return 0 # verticale
        else: return 200 # down
    if dy==0:
        if dx>=0: return 100 # verticale
        else: return 300 # down
    fi = math.atan(dy/dx) * 63.66197723 # RADIAN -> GRAD
    if dx>0 and dy>0: # I Q (right-upper)
        return 100-fi
    if dx>0 and dy<0: # II Q  (right-lower)
        return 100-fi
    if dx<0 and dy<0: # Q III (left, lower)
        return 300-fi
    if dx<0 and dy>0: # Q IV  (left, upper)
        return 300-fi
    return None # no azimuth --- the points are identical

def calculate_point_by_azimuth(x1, y1, a_grad, d):
    if x1 is None or y1 is None or a_grad is None or d is None: return None, None
    x2 = x1 + d*math.sin(a_grad/63.66197723)
    y2 = y1 + d*math.cos(a_grad/63.66197723)
    return x2, y2

def calculate_length(x1,y1,x2,y2): #OK
    if x1 is None or x2 is None or y1 is None or y2 is None:
        return None
    else:
        d = math.sqrt(((y2-y1)**2)+((x2-x1)**2))
        return d

