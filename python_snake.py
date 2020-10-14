import math
import random
import tkinter as tk
import pygame
import sys
from tkinter import messagebox

class cube(object):
    rows = 20 
    w = 500
    def __init__(self, start, dirnx=1, dirny=0, color=(255,0,0)):
        self.position = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.position = (self.position[0] + self.dirnx, self.position[1] + self.dirny)

    def draw(self, surface, eyes=False):
        distance = self.w // self.rows
        row = self.position[0]
        col = self.position[1]

        pygame.draw.rect(surface, self.color, (row * distance+1, col * distance + 1, distance-2, distance-2))

        if eyes:
            center = distance // 2
            radius = 3
            circleMiddle= (row*distance - radius , col * distance + 8)
            circleMiddle2 = (row * distance + distance - radius * 2, col * distance + 8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        # for event in pygame.event.get():
        #     if event.pygame == pygame.QUIT:
        #         pygame.quit()

        keys = pygame.key.get_pressed()

        for key in keys:
            if keys[pygame.K_LEFT]:
                self.dirnx = -1
                self.dirny = 0
                self.turns[self.head.position[:]] = [self.dirnx, self.dirny]

            elif keys[pygame.K_RIGHT]:
                self.dirnx = 1
                self.dirny = 0
                self.turns[self.head.position[:]] = [self.dirnx, self.dirny]

            elif keys[pygame.K_UP]:
                self.dirnx = 0
                self.dirny = -1
                self.turns[self.head.position[:]] = [self.dirnx, self.dirny]

            elif keys[pygame.K_DOWN]:
                self.dirnx = 0
                self.dirny = 1
                self.turns[self.head.position[:]] = [self.dirnx, self.dirny]
        
        for i, cube in enumerate(self.body):
            position = cube.position[:]
            if position in self.turns: 
                turn = self.turns[position]
                cube.move(turn[0], turn[1])
                if i == len(self.body) - 1: 
                    self.turns.pop(position)
            else:
                #checking for edges of the screen 
                if cube.dirnx == -1 and cube.position[0] <= 0: cube.position = (cube.rows-1, cube.position[1])
                elif cube.dirnx == 1 and cube.position[0] >= cube.rows-1: cube.position = (0, cube.position[1])
                elif cube.dirny == 1 and cube.position[1] >= cube.rows-1: cube.position = (cube.position[0], cube.rows-1)
                else: cube.move(cube.dirnx,cube.dirny)

    def reset(self, pos):
        pass

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.position[0]-1, tail.position[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.position[0]+1, tail.position[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.position[0], tail.position[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.position[0], tail.position[1]+1)))

    def draw(self, surface):
        for i, cube in enumerate(self.body):
            if i == 0:
                cube.draw(surface, True)
            else:
                cube.draw(surface)

def drawGrid(w, rows, surface):
    size_between = w // rows

    x = 0
    y = 0

    for l in range(rows):
        x += size_between
        y += size_between

        pygame.draw.line(surface, (255, 255, 255), (x,0), (x,w))
        pygame.draw.line(surface, (255, 255, 255), (0,y), (w,y))


def redrawWindow(surface):
    global rows, width, s
    surface.fill((0,0,0))
    s.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()

def randomSnack(rows, item):    
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda x:x.position == (x,y), positions))) > 0:
            continue
        else:
            break
    
    return (x,y)



def message_box(subject, content):
    pass

def main():
    global width, rows, s
    width = 500
    rows = 20
    window = pygame.display.set_mode((width, width))
    s = snake((255,0,0), (10,10))
    snack = cube(randomSnack(rows, s), color=(0,255,0))
    flag = True
    
    clock = pygame.time.Clock()

    while (flag):
        pygame.time.delay(50) #50 ms delay lower - faster
        clock.tick(10) #being able to run 10 blocks every second lower - slower
        redrawWindow(window)
        s.move()
        #add the snack to the snake if it hit it
        if s.body[0].position == snack.position:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0,255,0))

        redrawWindow(window)
        #code for pygame window not crashing
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit(0)


main()