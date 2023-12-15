'''import pygame
import creature_parts

# Инициализация Pygame
pygame.init()

# Определение цветов
WHITE = (255, 255, 255)

# Создание класса-родителя для всех живых существ
x = SCREEN_WIDTH // 2
y = SCREEN_HEIGHT // 2

class Entity:
    pass
class Characters(Entity):
    def __init__(self, x, y, radius, health):
        self.x = x
        self.y = y
        self.radius = radius
        self.health=health

    def draw(self, screen):
        pygame.draw.ellipse(screen, WHITE, (self.x, self.y, self.width, self.height)

#Задание класса главного героя
class Main_Character(Characters):
    """
    """
    Main_Character_Color = (255, 7, 230)
    FONT_COLOR = (50, 50, 50)

    def __init__(self, surface, camera, name=""):
        super().__init__(surface, camera)
        self.x = random.randint(100, 400)
        self.y = random.randint(100, 400)
        self.mass = 20
        self.speed = 4
        self.color = col = Main_Character_Color

        if name:
            self.name = name
        else:
            self.name = "Anonymous"
        self.pieces = []

    def collisionDetection(self, edibles):
        """Detects cells being inside the radius of current player.
        Those cells are eaten.
        """
        pass

    def move(self):
        """Updates players current position depending on player's mouse relative position.
        """

        dX, dY = pygame.mouse.get_pos()
        # Find the angle from the center of the screen to the mouse in radians [-Pi, Pi]
        rotation = math.atan2(dY - float(SCREEN_HEIGHT) / 2, dX - float(SCREEN_WIDTH) / 2)
        # Convert radians to degrees [-180, 180]
        rotation *= 180 / math.pi
        # Normalize to [-1, 1]
        # First project the point from unit circle to X-axis
        # Then map resulting interval to [-1, 1]
        normalized = (90 - math.fabs(rotation)) / 90
        vx = self.speed * normalized
        vy = 0
        if rotation < 0:
            vy = -self.speed + math.fabs(vx)
        else:
            vy = self.speed - math.fabs(vx)
        tmpX = self.x + vx
        tmpY = self.y + vy
        self.x = tmpX
        self.y = tmpY

    def feed(self):
        """Unsupported feature.
        """
        pass


    def draw(self):
        """Draws the player as an outlined circle.
        """
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        center = (int(self.x * zoom + x), int(self.y * zoom + y))

        # Draw the ouline of the player as a darker, bigger circle
        pygame.draw.circle(self.surface, self.outlineColor, center, int((self.mass / 2 + 3) * zoom))
        # Draw the actual player as a circle
        pygame.draw.circle(self.surface, self.color, center, int(self.mass / 2 * zoom))
        # Draw player's name
        fw, fh = font.size(self.name)
        drawText(self.name, (self.x * zoom + x - int(fw / 2), self.y * zoom + y - int(fh / 2)),
                 Player.FONT_COLOR)

#Задание класса врагов
class Enemies(Characters):
    pass


class Camera:
    """Создание обьекта камеры, которая следует за игроком
    """

    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.zoom = 0.5

    def centre(self, blobOrPos):
        """Makes sure that the given object will be at the center of player's view.
        Zoom is taken into account as well.
        """
        if isinstance(blobOrPos, Player):
            x, y = blobOrPos.x, blobOrPos.y
            self.x = (x - (x * self.zoom)) - x + (SCREEN_WIDTH / 2)
            self.y = (y - (y * self.zoom)) - y + (SCREEN_HEIGHT / 2)
        elif type(blobOrPos) == tuple:
            self.x, self.y = blobOrPos

    def update(self, target):
        #self.zoom = 100 / (target.mass) + 0.3
        self.centre(blob)

Player = Main_Character(200,200,100)
# Задание размеров окна
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Овал-персонаж")

main_character = MainCharacter(WIDTH // 2, HEIGHT // 2)

# Основной игровой цикл
running = True
while running:
    screen.fill((0, 0, 0))  # Очистка экрана

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Рисование главного персонажа
    main_character.draw(screen)

    pygame.display.flip()  # Обновление экрана

# Завершение игры
pygame.quit()
'''