import pygame, sys, os
from pygame.locals import *
from random import randint
from math import cos
from math import sin
pygame.init()

MAXSPEED = 20
SIZE = 9
BASE_COLOR = (50, 100, 50)
COLOR_VARIANCE = 20
WINDOWSIZE = 1000
LENBRANCH = 20
TIMETICK = 1
MAXPART = 100
GRABCOLORMODE = 1
i = 0
AUTUMN = pygame.image.load("colors.jpg")
AUTUMN_DIMS = AUTUMN.get_rect().size

freeParticles = pygame.sprite.Group()
tree = pygame.sprite.Group()

window = pygame.display.set_mode((WINDOWSIZE, WINDOWSIZE))
pygame.display.set_caption("Brownian Tree")

screen = pygame.display.get_surface()


def color_grabber():
    if GRABCOLORMODE:
        x, y = (randint(0, AUTUMN_DIMS[0]-1), randint(0, AUTUMN_DIMS[1]-1))
        newcol = AUTUMN.get_at((x, y))
    else:
        cv = COLOR_VARIANCE
        newcol = (BASE_COLOR[0] + randint(-cv * 2, cv),
                  BASE_COLOR[1] + randint(-cv, cv),
                  BASE_COLOR[2] + randint(-cv, cv))
    return newcol


class Particle(pygame.sprite.Sprite):
    def __init__(self, vector, location, surface):
        pygame.sprite.Sprite.__init__(self)
        self.vector = vector
        self.surface = surface
        self.accelerate(vector)
        self.add(freeParticles)
        self.rect = pygame.Rect(location[0], location[1], SIZE, SIZE)
        newcol = color_grabber()
        self.surface.fill(newcol, self.rect)

    def onEdge(self):
        if self.rect.left <= 0:
            self.vector = (abs(self.vector[0]), self.vector[1])
        elif self.rect.top <= 0:
            self.vector = (self.vector[0], abs(self.vector[1]))
        elif self.rect.right >= WINDOWSIZE:
            self.vector = (-abs(self.vector[0]), self.vector[1])
        elif self.rect.bottom >= WINDOWSIZE:
            self.vector = (self.vector[0], -abs(self.vector[1]))

    def update(self):
        if freeParticles in self.groups():
            self.surface.fill((0, 0, 0), self.rect)
            self.remove(freeParticles)
            if pygame.sprite.spritecollideany(self, freeParticles):
                self.accelerate((randint(-MAXSPEED, MAXSPEED),
                                 randint(-MAXSPEED, MAXSPEED)))
                self.add(freeParticles)
            elif pygame.sprite.spritecollideany(self, tree):
                self.stop()
            else:
                self.add(freeParticles)

            self.onEdge()

            if (self.vector == (0, 0)) and tree not in self.groups():
                self.accelerate((randint(-MAXSPEED, MAXSPEED),
                                 randint(-MAXSPEED, MAXSPEED)))
            self.rect.move_ip(self.vector[0], self.vector[1])
        cv = COLOR_VARIANCE
        newcol = color_grabber()
        self.surface.fill(newcol, self.rect)

    def stop(self):
        self.vector = (0, 0)
        self.remove(freeParticles)
        self.add(tree)

    def accelerate(self, vector):
        self.vector = vector


NEW = USEREVENT + 1
TICK = USEREVENT + 2

pygame.time.set_timer(NEW, 50)
pygame.time.set_timer(TICK, TIMETICK)

def input(events):
    for event in events:
        if event.type == QUIT:
            sys.exit(0)
        elif event.type == NEW and (len(freeParticles) < MAXPART):
            Particle((randint(-MAXSPEED, MAXSPEED),
                      randint(-MAXSPEED, MAXSPEED)),
                     (randint(0, WINDOWSIZE), randint(0, WINDOWSIZE)),
                     screen)

        elif event.type == TICK:
            freeParticles.update()


center = WINDOWSIZE/2
if i == 0:
    for i in range(3):
        ang = i*3.14159/3
        for j in range(-LENBRANCH, LENBRANCH):
            root = Particle((0, 0),
                            (center + j*(cos(ang) * SIZE), center + j*(sin(ang) * SIZE)),
                            screen)
            root.stop()
    i = 1

while True:
    input(pygame.event.get())
    pygame.display.flip()
