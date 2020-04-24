import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

gComposedM = np.identity(3)

def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1] )
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global gComposedM
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_Q:
            newM = np.identity(3)
            newM[0][2] = -0.1
            gComposedM = newM @ gComposedM   
        elif key == glfw.KEY_E:
            newM = np.identity(3)
            newM[0][2] = 0.1
            gComposedM = newM @ gComposedM
        elif key == glfw.KEY_A:
            th = np.radians(10)
            newM = np.array([[np.cos(th), -np.sin(th),0.],
                          [np.sin(th), np.cos(th),0.],
                          [0.,         0.,        1.]])
            gComposedM = gComposedM @ newM
        elif key == glfw.KEY_D:
            th = np.radians(-10)
            newM = np.array([[np.cos(th), -np.sin(th),0.],
                          [np.sin(th), np.cos(th),0.],
                          [0.,         0.,        1.]])
            gComposedM = gComposedM @ newM
        elif key == glfw.KEY_1:
            newM = np.identity(3)
            gComposedM = newM
        elif key == glfw.KEY_W:
            newM = np.array([[0.9,0.,0.],
                            [0.,0.9,0.],
                            [0.,0.,0.9]])
            gComposedM = newM @ gComposedM
        elif key == glfw.KEY_S:
            th = np.radians(10)
            newM = np.array([[np.cos(th), -np.sin(th),0.],
                          [np.sin(th), np.cos(th),0.],
                          [0.,         0.,        1.]])
            gComposedM = newM @ gComposedM


def main():
    global gComposedM
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"CG_weekly_practice_04_2017069598", None,None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(gComposedM)
        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__":
    main()