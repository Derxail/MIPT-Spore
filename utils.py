import pygame
import math

def rotate_image(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def angle_by_coords(pos0, pos):
    ang = math.atan2(
        (pos0[1] - pos[1]),
        (pos0[0] - pos[1])
    )
    if ang < 0:
        ang += 2*math.pi
    return ang

def gen_polygon(surface, code, color, size):
    half = size / 2
    if code == '1000':
        pygame.draw.polygon(surface, color, [[0, 0], [half, 0], [0, half]])
    elif code == '0100':
        pygame.draw.polygon(surface, color, [[half, 0], [size, 0], [size, half]])
    elif code == '0010':
        pygame.draw.polygon(surface, color, [[0, size], [0, half], [half, size]])
    elif code == '0001':
        pygame.draw.polygon(surface, color, [[size, size], [half, size], [size, half]])

    elif code == '0111':
        pygame.draw.polygon(surface, color, [[0, half], [0, size],
                                                                   [size, size], [size, 0], [half, 0]])
    elif code == '1011':
        pygame.draw.polygon(surface, color, [[0, 0], [0, size],
                                                                   [size, size], [size, half], [half, 0]])
    elif code == '1101':
        pygame.draw.polygon(surface, color, [[0, 0], [0, half],
                                                                   [half, size], [size, size], [size, 0]])
    elif code == '1110':
        pygame.draw.polygon(surface, color, [[0, 0], [0, size],
                                                                   [half, size], [size, half], [size, 0]])
    elif code == '1100':
        pygame.draw.polygon(surface, color, [[0, 0], [size, 0], [size, half], [0, half]])
    elif code == '0011':
        pygame.draw.polygon(surface, color, [[size, size], [size, half],
                                                                   [0, half], [0, size]])
    elif code == '1010':
        pygame.draw.polygon(surface, color, [[0, 0], [half, 0], [half, size], [0, size]])
    elif code == '0101':
        pygame.draw.polygon(surface, color, [[size, 0], [half, 0], [half, size], [size, size]])
    elif code == '1001':
        pygame.draw.polygon(surface, color, [[0, 0], [half, 0], [0, half]])
        pygame.draw.polygon(surface, color, [[size, size], [half, size], [size, half]])
    elif code == '0110':
        pygame.draw.polygon(surface, color, [[half, 0], [size, 0], [size, half]])
        pygame.draw.polygon(surface, color, [[0, size], [0, half], [half, size]])
    elif code == '1111':
        pygame.draw.polygon(surface, color, [[0, 0], [0, size], [size, size], [size, 0]])
