def lerp(a, b, t):
    return a + (b - a) * t

def inverse_lerp(a, b, value):
    if a != b:
        return (value - a) / (b - a)
    else:
        return 0