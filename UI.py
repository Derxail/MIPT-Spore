import pygame

class HealthBar:
    def __init__(
            self,
            value,
            max_value,
            length,
            height,
            color,
            outline_color = (0, 0, 0),
            back_color = (244, 164, 96),
            font_color = (255, 255, 255),
            outline_thickness = 2
    ):
        self.value = value
        self.max_value = max_value
        self.color = color
        self.outline_color = outline_color
        self.surface = pygame.Surface((length, height))
        self.length = length
        self.height = height
        self.ouline_thickness = outline_thickness
        self.back_color = back_color
        self.font_color = font_color
        self.font = font = pygame.font.SysFont('Comic Sans MS', int(self.height * 0.85))
        self.text = self.font.render(
            str(str(self.value)+"/"+str(self.max_value)), False, self.font_color)
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
        self.text = self.font.render(
            str(self.value) + "/" + str(self.max_value),
            False,
            self.font_color
        )
        self.surface.blit(self.text, (self.length / 2 - len(str(self.max_value))*0.8*self.height, -self.ouline_thickness))


    def set_value(self, value):
        self.value = value
        self.redraw()

    def set_max_value(self, max_value):
        self.max_value = max_value
        self.redraw()

