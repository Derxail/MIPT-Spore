import pygame

class HealthBar:
    def __init__(
            self,
            value,
            max_value,
            position,
            length,
            height,
            color,
            outline_color = (0, 0, 0),
            back_color = (244, 164, 96),
            outline_thickness = 3
    ):
        self.value = value
        self.max_value = max_value
        self.position = position
        self.color = color
        self.outline_color = outline_color
        self.surface = pygame.Surface((length, height))
        self.length = length
        self.height = height
        self.ouline_thickness = outline_thickness
        self.back_color = back_color
        self.redraw()

    def redraw(self):
        pygame.draw.rect(
            self.surface,
            self.color,
            pygame.Rect(
                0,
                0,
                self.length * (float(self.value)/float(self.max_value)),
                self.height
            )
        )
        pygame.draw.rect(
            self.surface,
            self.back_color,
            pygame.Rect(
                self.length * (float(self.value)/float(self.max_value)),
                0,
                self.length,
                self.height
            )
        )
        pygame.draw.rect(
            self.surface,
            self.outline_color,
            pygame.Rect(
                0,
                0,
                self.length,
                self.height
            ),
            self.ouline_thickness
        )


    def set_value(self, value):
        self.value = value
        self.redraw()

    def set_max_value(self, max_value):
        self.max_value = max_value
        self.redraw()

