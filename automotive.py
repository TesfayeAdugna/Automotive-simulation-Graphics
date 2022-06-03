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
    glClearColor(0.9, 0.9, 0.9, 0.0)
    
vertexes = [(0,0,0),(-5,0,0),(-5,2,0),(0,2,0),(6.88,0,8),(1.88,0,8),(6.88,4,8),(1.88,4,8),(1.72,4,2),(-3.28,4,2)]
edges = [(0,1),(1,2),(2,3),(0,3),(0,4),(4,5),(5,1),(4,6),(6,7),(7,5),(3,8),(8,9),(9,2),(9,7),(8,6)]

def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    
    glLineWidth(2)
    glBegin(GL_LINES)

    

    # glBegin(GL_POINTS)
    r = 2
    x = np.linspace(-0.2,0.2,1000)
    z = np.linspace(-2,2,100)
    y = np.sqrt(np.subtract(np.power(r,2),np.power(z,2)))
    
    glColor3f(0.0,0.0,0.0)
    for i,j,k in zip(x,y,z):
        # glVertex3fv((i+2.5-5,j,k+5.5))
        # glVertex3fv((i+2.5-5,-j,k+5.5))

        glVertex3fv((i+2.5-5,j,k))
        glVertex3fv((i+2.5-5,-j,k))

    glColor3f(1.0, 0.0, 1.0)
    for edge in edges:
        for i in edge:
            glVertex3fv(vertexes[i])


    # r = 2
    # x = np.linspace(-2,2,100)
    # y = np.sqrt(np.subtract(np.power(r,2),np.power(x,2)))
    # z = np.linspace(0,0,1000)
    # glColor3f(0.0,0.0,0.0)
    # for i,j,k in zip(x,y,z):
    #     glVertex3fv((i+2.5,j,k))
    #     glVertex3fv((i+2.5,-j,k))


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
        glRotatef(1,0,5,1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw()
        pygame.display.flip()
        pygame.time.wait(10)

main()
