import glfw
from OpenGL.GL import *
import numpy as np

keyInput = 4
primitiveType = {
    1: GL_POINTS,
    2: GL_LINES,
    3: GL_LINE_STRIP,
    4: GL_LINE_LOOP,
    5: GL_TRIANGLES,
    6: GL_TRIANGLE_STRIP,
    7: GL_TRIANGLE_FAN,
    8: GL_QUADS,
    9: GL_QUAD_STRIP,
    0: GL_POLYGON
}

def render():
    global primitiveType
    global keyInput
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(primitiveType[keyInput])
    p = np.linspace(0.0, 6.28, 13, True)
    for x in np.nditer(p):
        glVertex2fv(np.array([np.cos(x),np.sin(x)]))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global keyInput
    if action == glfw.PRESS and (key > 47 and key < 58):
        keyInput = key - 48

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"CG_weekly_practice_03-1_2017069598", None,None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        render()

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()