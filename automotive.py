import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

def init():
    pygame.init()
    display = (500, 500)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluOrtho2D(-20.0, 20.0, -20.0, 20.0)
    

vertexes = [(0,0,0),(-5,0,0),(-5,2,0),(0,2,0),(6.88,4,0),(1.88,4,0),(6.88,8,0),(1.88,8,0),(1.72,5,0),(-3.28,5,0)]
edges = [(0,1),(1,2),(2,3),(0,3),(0,4),(4,5),(5,1),(4,6),(6,7),(7,5),(3,8),(8,9),(9,2),(9,7),(8,6)]

def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 0.0, 1.0)
    glLineWidth(2)
    glBegin(GL_LINES)

    for edge in edges:
        for i in edge:
            glVertex3fv(vertexes[i])


    glEnd()
    glFlush()

def main():
    init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(4, (display[1] / display[0]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -30)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glRotatef(1,3,1,1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw()
        pygame.display.flip()
        pygame.time.wait(10)

main()
