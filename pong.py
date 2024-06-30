import pygame
from pygame.locals import *
from enum import Enum
from collections import namedtuple
import random
import numpy as np
import base64
from io import BytesIO
from pong_agent import PongAgent

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 25)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 255, 0)


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60
BALL_SIZE = 10
BALL_SPEED = 7
PADDLE_SPEED = 7

class Direction(Enum):
    UP = 1
    DOWN = 2

Point = namedtuple('Point', 'x, y')

class PongGame:
    def __init__(self):
        self.w = SCREEN_WIDTH
        self.h = SCREEN_HEIGHT
        self.display = pygame.Surface((self.w, self.h))
        self.clock = pygame.time.Clock()
        self.agent = PongAgent()
        self.reset()

    def reset(self):
        self.paddle1 = pygame.Rect(10, (self.h - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.paddle2 = pygame.Rect(self.w - 20, (self.h - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball = pygame.Rect((self.w - BALL_SIZE) // 2, (self.h - BALL_SIZE) // 2, BALL_SIZE, BALL_SIZE)
        self.ball_dx = BALL_SPEED * random.choice((-1, 1))
        self.ball_dy = BALL_SPEED * random.choice((-1, 1))
        self.score1 = 0
        self.score2 = 0

    def play_step(self, action1):
        state_old = self.agent.get_state(self)
        action2 = self.agent.get_action(state_old)

        self.move_paddles(action1, action2)
        self.move_ball()
        self.check_collision()
        reward1, reward2 = self.update_score()

        state_new = self.agent.get_state(self)
        self.agent.train_short_memory(state_old, action2, reward2, state_new, False)
        self.agent.remember(state_old, action2, reward2, state_new, False)

        self.update_display()
        self.clock.tick(30)
        frame = self.get_image()  
        return reward1, self.score1, self.score2, frame
    
    def move_paddles(self, action1, action2):
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            self.paddle1.y -= PADDLE_SPEED
        elif keys[K_DOWN]:
            self.paddle1.y += PADDLE_SPEED

        if action2 == 0:
            self.paddle2.y -= PADDLE_SPEED
        elif action2 == 1:
            self.paddle2.y += PADDLE_SPEED

        if self.paddle1.y < 0:
            self.paddle1.y = 0
        if self.paddle1.y > self.h - PADDLE_HEIGHT:
            self.paddle1.y = self.h - PADDLE_HEIGHT

        if self.paddle2.y < 0:
            self.paddle2.y = 0
        if self.paddle2.y > self.h - PADDLE_HEIGHT:
            self.paddle2.y = self.h - PADDLE_HEIGHT

    def move_ball(self):
        self.ball.x += self.ball_dx
        self.ball.y += self.ball_dy

        if self.ball.y <= 0 or self.ball.y >= self.h - BALL_SIZE:
            self.ball_dy *= -1

    def check_collision(self):
        if self.ball.colliderect(self.paddle1) or self.ball.colliderect(self.paddle2):
            self.ball_dx *= -1

    def update_score(self):
        reward1, reward2 = 0, 0
        if self.ball.x <= 0:
            self.score2 += 1
            reward2 = 1
            self.reset()
        elif self.ball.x >= self.w - BALL_SIZE:
            self.score1 += 1
            reward1 = 1
            self.reset()
        return reward1, reward2

    def update_display(self):
        self.display.fill(BLACK)
        pygame.draw.rect(self.display, WHITE, self.paddle1)
        pygame.draw.rect(self.display, WHITE, self.paddle2)
        pygame.draw.ellipse(self.display, WHITE, self.ball)
        text = font.render(f"Score: {self.score1} - {self.score2}", True, WHITE)
        self.display.blit(text, (self.w // 2 - text.get_width() // 2, 10))

    def get_image(self):
        img_str = pygame.image.tostring(self.display, "RGB")
        img = pygame.image.fromstring(img_str, (self.w, self.h), "RGB")
        buf = BytesIO()
        pygame.image.save(img, buf)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return img_base64

if __name__ == '__main__':
    game = PongGame()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

        action1 = Direction.UP if pygame.key.get_pressed()[K_UP] else Direction.DOWN if pygame.key.get_pressed()[K_DOWN] else None
        _, _, _, frame = game.play_step(action1)

        # print(frame)