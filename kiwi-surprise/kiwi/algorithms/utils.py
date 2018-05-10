import math

def sigmoid(x, shift, scale):
    return 1 / (1 + math.exp(scale * x + shift))
