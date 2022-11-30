import math
import pygame
from pygame.locals import *
from sys import exit
import os
import random

pygame.init()

MUSIC = 1   #change to 0 to remove music
WIDTH, HEIGHT = 1100, 700
PADDLE_LENGHT, PADDLE_HEIGHT = 120, 8
BALL_RADIUS = 12
DEFLECTION_ANGLE = 30

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hari Krishnan's PONG")
clock = pygame.time.Clock()
FONT1 = pygame.font.SysFont("comicsans", 50)
FONT2 = pygame.font.SysFont("comicsans", 28)
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("Assets","background.jpg")), (WIDTH, HEIGHT))
BALL_IMG = pygame.transform.scale(pygame.image.load(os.path.join("Assets","metal_ball.png")), (2 * BALL_RADIUS, 2 * BALL_RADIUS))
pygame.time.set_timer(USEREVENT, 1000)
collide = pygame.mixer.Sound(os.path.join("Assets","collision.wav"))
music0 = pygame.mixer.Sound(os.path.join("Assets","music0.mp3"))
music = pygame.mixer.Sound(os.path.join("Assets","music.mp3"))
collide.set_volume(0.4)
TEXT1 = FONT1.render("PRESS SPACEBAR", True, "white")
TEXT2 = FONT1.render("YOU LOST!", True, "red")
TEXT3 = FONT2.render("Timer : ", True, "green")
TEXT4 = FONT2.render("HIGHT SCORE : ", True, "green")

class Paddle:
    def __init__(self, x, y, width, height, vel, color):
        self.x = x
        self.y = y
        self.vel = vel
        self.width = width
        self.height = height
        self.color = color

    def draw_paddle(self):
        pygame.draw.rect(WIN, self.color, Rect(self.x + self.height, self.y, self.width - self.height, self.height))
        pygame.draw.circle(WIN, "red", [self.x + self.height, self.y + self.height / 2], self.height / 2)
        pygame.draw.circle(WIN, "red", [self.x + self.width, self.y + self.height / 2], self.height / 2)
        pygame.draw.rect(WIN, "red", Rect(self.x + self.height, self.y, self.width * 0.1, self.height))
        pygame.draw.rect(WIN, "red", Rect(self.x + self.width * 0.9, self.y, self.width * 0.1, self.height))

    def paddle_move(self):
        keys = pygame.key.get_pressed()
        if self.x > 0 and keys[K_LEFT]:
            self.x -= self.vel

        if self.x < WIDTH - self.width - self.vel and keys[K_RIGHT]:
            self.x += self.vel


class Circle:
    def __init__(self, x, y, r, vel):
        self.x = x
        self.y = y
        self.angle = random.choice([i + 90 - DEFLECTION_ANGLE for i in range(2 * DEFLECTION_ANGLE) if i != DEFLECTION_ANGLE])
        self.vel = vel
        self.r = r

    def draw_circle(self):
        WIN.blit(BALL_IMG, (self.x - self.r, self.y - self.r))

    def circle_move(self):
        if self.x > WIDTH - self.r:
            self.angle = 180 - self.angle
        if self.x < self.r:
            self.angle = 180 - self.angle
        if self.y < self.r:
            self.angle = 360 - self.angle
        self.angle = self.angle % 360

        if self.angle < 25:
            self.angle = 35
        elif self.angle > 335:
            self.angle = 345
        elif 155 < self.angle < 180:
            self.angle = 145
        elif 180 < self.angle < 205:
            self.angle = 215
        self.x += self.vel * math.cos(math.radians(self.angle))
        self.y += self.vel * math.sin(-math.radians(self.angle))

    def circle_paddle_collision(self, paddle):
        collision_tolerance = self.vel + 1 
        ball = Rect(self.x - self.r, self.y - self.r, 2 * self.r, 2 * self.r + 4)
        paddle_rect = Rect(paddle.x, paddle.y, paddle.width, paddle.height)
        if paddle_rect.colliderect(ball):
            length = paddle.x + paddle.width / 2 - self.x
            if abs(paddle.y - (self.y + self.r)) <= collision_tolerance and (0 > self.angle or 180 < self.angle):
                self.angle = (360 - self.angle + 40 * length / (paddle.width / 2 + self.r))
            elif abs(paddle.x - (self.x + self.r))  <= collision_tolerance and (90 > self.angle > -90 or 270 < self.angle):
                self.angle = 180 - self.angle
            elif abs(paddle.x + paddle.width - (self.x - self.r)) <= collision_tolerance and (90 < self.angle < 270 or self.angle < -90):
                self.angle = 180 - self.angle


def draw(image):
    WIN.blit(image, (0, 0))


def begin(paddle, circle):
    paddle.paddle_move()
    circle.x = paddle.x + paddle.width / 2
    keys = pygame.key.get_pressed()
    display_text(TEXT1, ((WIDTH - TEXT1.get_width()) / 2, (HEIGHT - TEXT1.get_height()) / 2))
    if keys[K_SPACE]:
        music0.stop()
        return 1
    else:
        return 0


def display_text(text, pos):
    WIN.blit(text, pos)
    pygame.display.update(Rect(pos[0], pos[1], text.get_width(), text.get_height()))

def score(time, high_score):
    display_text(TEXT3, (10, 10))
    display_text(FONT2.render(str(time), 1, "green"), (10 + TEXT3.get_width(), 10))
    display_text(TEXT4, (WIDTH - TEXT4.get_width() - high_score.get_width() - 10, 10))
    display_text(high_score, (WIDTH - high_score.get_width() - 10, 10))
    
def main():
    circle = Circle(WIDTH / 2, HEIGHT * 0.92 - BALL_RADIUS, BALL_RADIUS, 8)
    paddle = Paddle((WIDTH - PADDLE_LENGHT) / 2, HEIGHT * 0.92, PADDLE_LENGHT, PADDLE_HEIGHT, 10, (180, 180, 180))
    run = True
    run_once = 0
    time = 0
    sound1, sound2 = MUSIC, MUSIC
    if os.path.isfile(os.path.join("high_score.txt")):
        with open("high_score.txt", "r") as fobj:
            high_score = FONT2.render(fobj.read(), True, "green")
    else:
        with open("high_score.txt", "w") as fobj:
            fobj.write('1')
        with open("high_score.txt", "r") as fobj:
            high_score = FONT2.render(fobj.read(), True, "green")
    while run:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            elif event.type == USEREVENT and run_once == 1:
                time += 1

        vel_increment = time / 30
        circle.vel += int(vel_increment)
        draw(BACKGROUND)
        paddle.draw_paddle()
        circle.draw_circle()

        if not run_once:
            run_once = begin(paddle, circle)
            if sound2:
                music0.play(-1)
                sound2=0
        else:
            paddle.paddle_move()
            circle.circle_move()
            circle.circle_paddle_collision(paddle)
            if sound1:
                music.play(-1)
                sound1 = 0

        if circle.y > HEIGHT - circle.r:
            display_text(TEXT2, ((WIDTH - TEXT2.get_width()) / 2, (HEIGHT - TEXT2.get_height()) / 2))
            music.stop()
            music0.stop()
            pygame.time.delay(2000)
            with open("high_score.txt", "r") as fobj:
                w = fobj.read()
                if int(w) < time:
                    with open("high_score.txt", "w") as fobj:
                        fobj.write(str(time))
            main()
        score(time, high_score)
        circle.vel -= int(vel_increment)
        clock.tick(60)
    pygame.quit()
    exit()


if __name__ == "__main__":
    main()
