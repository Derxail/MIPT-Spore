import random
from perlin_noise import PerlinNoise
import matplotlib.pyplot as plt

# генерация основного шума и параметризация
def generate_noise(w, h, period=5, octaves=4, seed=random.randint(a=1, b=10000)):
    noise = PerlinNoise(octaves=octaves, seed=seed)
    res = [[0 for j in range(0, h)] for i in range(0, w)]
    for i in range(0, w):
        for j in range(0, h):
            res[i][j] = noise([i / period, j / period])
    return res