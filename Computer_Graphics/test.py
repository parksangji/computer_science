import glfw
from OpenGL.GL import *
import numpy as np

def render() :
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    width = 0.3
    glRotatef(-45,0,0,1)
    drawBox(width)
    glFlush()


def drawBox(height) :
    glBegin(GL_POLYGON)
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(0, height,0)
    glVertex3f(0, 0, 0)
    glVertex3f(height,0,0)
    glVertex3f(height,height,0)
    glEnd()


def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"CG_weekly_practice_03-1_2017069598", None,None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        render()

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()