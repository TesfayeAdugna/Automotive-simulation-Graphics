import random
import pygame
import numpy as np
import newtrial_points as p
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *


def init():
    pygame.init()
    display = (500, 500)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluOrtho2D(-10, 10.0, -10.0, 10.0)
    glClearColor(0.9, 0.9, 0.9, 0.0)
    
# Generating random colors.
def random_color():
    x = random.randint(0, 255) / 255
    y = random.randint(0, 255) / 255
    z = random.randint(0, 255) / 255
    color = (x, y, z)
    return color

colors_list= []
for n in range(len(p.chair_faces_vector4)):
    colors_list.append(random_color())


def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    
    # Arches start here.
    glBegin(GL_QUADS)
    for face in p.chair_faces_vector4:
        x = 0
        for vertex in face:
            x+=1
            glColor3fv(p.colors[x%12])
            glVertex3fv(p.chair_verticies_vector3[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in p.chair_edges_vector2:
        for i in edge:
            glVertex3fv(p.chair_verticies_vector3[i])

    glEnd()
    # Arches End here.

    # Body to be continued here...

    
    glFlush()

def main():
    init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(4, (display[1] / display[0]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -20)
    # glRotatef(1, 0, 0, 1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glRotatef(0, 0, 0, 90)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw()
        pygame.display.flip()
        pygame.time.wait(10)

main()
