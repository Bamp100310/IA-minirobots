import math
import random
import pygame


# ============================================================
# CONFIGURACIÓN
# ============================================================

WIDTH = 1000
HEIGHT = 700

NUM_OBSTACLES = 4

ROBOT_RADIUS = 18
OBSTACLE_RADIUS = 35

ROBOT_SPEED = 2.5

# Distancia máxima que pueden detectar los sensores
MAX_SENSOR_DISTANCE = 180

# Distancia a partir de la cual el robot empieza a evadir
SAFE_DISTANCE = 70

# Ángulo de los sensores laterales
SIDE_SENSOR_ANGLE = math.radians(45)

# Velocidad de giro
TURN_ANGLE = math.radians(4)


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def distance(x1, y1, x2, y2):
    """
    Calcula la distancia euclidiana entre dos puntos.
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def normalize_angle(angle):
    """
    Mantiene el ángulo entre 0 y 2*pi.
    """
    return angle % (2 * math.pi)


# ============================================================
# OBSTÁCULO
# ============================================================

class Obstacle:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = OBSTACLE_RADIUS

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (180, 60, 60),
            (int(self.x), int(self.y)),
            self.radius
        )


# ============================================================
# ROBOT
# ============================================================

class Robot:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        # Orientación inicial
        self.angle = 0

    # --------------------------------------------------------
    # DIRECCIÓN DE UN SENSOR
    # --------------------------------------------------------

    def get_sensor_angle(self, sensor):
        """
        Devuelve la orientación de cada sensor.

        frontal  -> 0°
        izquierda -> +45°
        derecha   -> -45°
        """

        if sensor == "frontal":
            return self.angle

        if sensor == "izquierda":
            return self.angle + SIDE_SENSOR_ANGLE

        if sensor == "derecha":
            return self.angle - SIDE_SENSOR_ANGLE

    # --------------------------------------------------------
    # CÁLCULO DE SENSOR
    # --------------------------------------------------------

    def sensor_distance(self, sensor, obstacles):

        sensor_angle = self.get_sensor_angle(sensor)

        # Dirección del sensor
        dx = math.cos(sensor_angle)
        dy = math.sin(sensor_angle)

        closest_distance = MAX_SENSOR_DISTANCE

        # Revisar todos los obstáculos
        for obstacle in obstacles:

            # Vector desde el robot hasta el obstáculo
            ox = obstacle.x - self.x
            oy = obstacle.y - self.y

            # Proyección del obstáculo sobre el sensor
            projection = ox * dx + oy * dy

            # Si está detrás del sensor, ignorarlo
            if projection < 0:
                continue

            # Distancia perpendicular del obstáculo al sensor
            perpendicular = abs(ox * dy - oy * dx)

            # El sensor solamente detecta el obstáculo
            # si el rayo pasa por su radio.
            if perpendicular <= obstacle.radius:

                # Distancia aproximada hasta la superficie
                hit_distance = projection - math.sqrt(
                    obstacle.radius ** 2 -
                    perpendicular ** 2
                )

                if 0 <= hit_distance < closest_distance:
                    closest_distance = hit_distance

        return closest_distance

    # --------------------------------------------------------
    # LECTURA DE LOS 3 SENSORES
    # --------------------------------------------------------

    def read_sensors(self, obstacles):

        return {
            "frontal": self.sensor_distance(
                "frontal",
                obstacles
            ),

            "izquierda": self.sensor_distance(
                "izquierda",
                obstacles
            ),

            "derecha": self.sensor_distance(
                "derecha",
                obstacles
            )
        }

    # --------------------------------------------------------
    # DECISIÓN DEL ROBOT
    # --------------------------------------------------------

    def decide_movement(self, sensors):

        frontal = sensors["frontal"]
        izquierda = sensors["izquierda"]
        derecha = sensors["derecha"]

        # ----------------------------------------------------
        # OBSTÁCULO FRONTAL
        # ----------------------------------------------------

        if frontal < SAFE_DISTANCE:

            # Girar hacia el lado que tenga más espacio
            if izquierda > derecha:
                self.angle += TURN_ANGLE
            else:
                self.angle -= TURN_ANGLE

        # ----------------------------------------------------
        # OBSTÁCULO A LA IZQUIERDA
        # ----------------------------------------------------

        elif izquierda < SAFE_DISTANCE:

            # Alejarse del obstáculo
            self.angle -= TURN_ANGLE

        # ----------------------------------------------------
        # OBSTÁCULO A LA DERECHA
        # ----------------------------------------------------

        elif derecha < SAFE_DISTANCE:

            # Alejarse del obstáculo
            self.angle += TURN_ANGLE

    # --------------------------------------------------------
    # MOVIMIENTO
    # --------------------------------------------------------

    def move(self):

        self.x += math.cos(self.angle) * ROBOT_SPEED
        self.y += math.sin(self.angle) * ROBOT_SPEED

    # --------------------------------------------------------
    # EVITAR SALIR DE LA PANTALLA
    # --------------------------------------------------------

    def keep_inside_screen(self):

        if self.x < ROBOT_RADIUS:
            self.x = ROBOT_RADIUS
            self.angle = math.pi - self.angle

        elif self.x > WIDTH - ROBOT_RADIUS:
            self.x = WIDTH - ROBOT_RADIUS
            self.angle = math.pi - self.angle

        if self.y < ROBOT_RADIUS:
            self.y = ROBOT_RADIUS
            self.angle = -self.angle

        elif self.y > HEIGHT - ROBOT_RADIUS:
            self.y = HEIGHT - ROBOT_RADIUS
            self.angle = -self.angle

    # --------------------------------------------------------
    # COMPROBAR COLISIÓN
    # --------------------------------------------------------

    def collision(self, obstacles):

        for obstacle in obstacles:

            d = distance(
                self.x,
                self.y,
                obstacle.x,
                obstacle.y
            )

            if d < ROBOT_RADIUS + obstacle.radius:
                return True

        return False

    # --------------------------------------------------------
    # DIBUJAR ROBOT
    # --------------------------------------------------------

    def draw(self, screen):

        # Cuerpo
        pygame.draw.circle(
            screen,
            (60, 120, 220),
            (int(self.x), int(self.y)),
            ROBOT_RADIUS
        )

        # Dirección del robot
        direction_x = (
            self.x +
            math.cos(self.angle) * ROBOT_RADIUS
        )

        direction_y = (
            self.y +
            math.sin(self.angle) * ROBOT_RADIUS
        )

        pygame.draw.line(
            screen,
            (255, 255, 255),
            (int(self.x), int(self.y)),
            (int(direction_x), int(direction_y)),
            3
        )

    # --------------------------------------------------------
    # DIBUJAR SENSORES
    # --------------------------------------------------------

    def draw_sensor(
        self,
        screen,
        sensor,
        sensor_distance,
        color
    ):

        angle = self.get_sensor_angle(sensor)

        end_x = (
            self.x +
            math.cos(angle) * sensor_distance
        )

        end_y = (
            self.y +
            math.sin(angle) * sensor_distance
        )

        pygame.draw.line(
            screen,
            color,
            (int(self.x), int(self.y)),
            (int(end_x), int(end_y)),
            2
        )


# ============================================================
# CREAR OBSTÁCULOS
# ============================================================

def create_obstacles():

    obstacles = []

    while len(obstacles) < NUM_OBSTACLES:

        x = random.randint(
            OBSTACLE_RADIUS,
            WIDTH - OBSTACLE_RADIUS
        )

        y = random.randint(
            OBSTACLE_RADIUS,
            HEIGHT - OBSTACLE_RADIUS
        )

        # Evitar colocar obstáculos demasiado cerca
        # del centro donde comienza el robot.
        if distance(
            x,
            y,
            WIDTH / 2,
            HEIGHT / 2
        ) < 150:
            continue

        # Evitar obstáculos demasiado juntos
        valid_position = True

        for obstacle in obstacles:

            if distance(
                x,
                y,
                obstacle.x,
                obstacle.y
            ) < OBSTACLE_RADIUS * 2 + 30:

                valid_position = False
                break

        if valid_position:
            obstacles.append(
                Obstacle(x, y)
            )

    return obstacles


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    pygame.init()

    screen = pygame.display.set_mode(
        (WIDTH, HEIGHT)
    )

    pygame.display.set_caption(
        "Simulación de Robot con 3 Sensores"
    )

    clock = pygame.time.Clock()

    font = pygame.font.SysFont(
        "Arial",
        18
    )

    # --------------------------------------------------------
    # CREAR ROBOT
    # --------------------------------------------------------

    robot = Robot(
        WIDTH / 2,
        HEIGHT / 2
    )

    # --------------------------------------------------------
    # CREAR OBSTÁCULOS ALEATORIOS
    # --------------------------------------------------------

    obstacles = create_obstacles()

    running = True

    step = 0

    while running:

        # ====================================================
        # EVENTOS
        # ====================================================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

        # ====================================================
        # SENSORES
        # ====================================================

        sensors = robot.read_sensors(
            obstacles
        )

        # ====================================================
        # DECISIÓN
        # ====================================================

        robot.decide_movement(
            sensors
        )

        # ====================================================
        # MOVIMIENTO
        # ====================================================

        robot.move()

        robot.keep_inside_screen()

        # ====================================================
        # SEGURIDAD CONTRA COLISIÓN
        # ====================================================

        if robot.collision(obstacles):

            # Retroceder
            robot.x -= (
                math.cos(robot.angle)
                * ROBOT_SPEED
                * 2
            )

            robot.y -= (
                math.sin(robot.angle)
                * ROBOT_SPEED
                * 2
            )

            # Cambiar dirección
            robot.angle += math.pi / 2

        step += 1

        # ====================================================
        # DIBUJAR
        # ====================================================

        screen.fill(
            (25, 25, 30)
        )

        # Obstáculos
        for obstacle in obstacles:
            obstacle.draw(screen)

        # Sensores
        robot.draw_sensor(
            screen,
            "frontal",
            sensors["frontal"],
            (255, 255, 0)
        )

        robot.draw_sensor(
            screen,
            "izquierda",
            sensors["izquierda"],
            (0, 255, 0)
        )

        robot.draw_sensor(
            screen,
            "derecha",
            sensors["derecha"],
            (0, 200, 255)
        )

        # Robot
        robot.draw(screen)

        # ====================================================
        # INFORMACIÓN
        # ====================================================

        text1 = font.render(
            f"Paso: {step}",
            True,
            (255, 255, 255)
        )

        text2 = font.render(
            f"Sensor frontal: {sensors['frontal']:.2f}",
            True,
            (255, 255, 0)
        )

        text3 = font.render(
            f"Sensor izquierda: {sensors['izquierda']:.2f}",
            True,
            (0, 255, 0)
        )

        text4 = font.render(
            f"Sensor derecha: {sensors['derecha']:.2f}",
            True,
            (0, 200, 255)
        )

        screen.blit(text1, (15, 15))
        screen.blit(text2, (15, 40))
        screen.blit(text3, (15, 65))
        screen.blit(text4, (15, 90))

        # ====================================================
        # ACTUALIZAR PANTALLA
        # ====================================================

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":
    main()