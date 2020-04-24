import glfw
import numpy as np
from OpenGL.GL import *

def polygon() :
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_LINE_LOOP)
    x = np.cos(np.array((0,30,60,90,120,150,180,210,240,270,300,330,360))*np.pi/180)
    y = np.sin(np.array((0,30,60,90,120,150,180,210,240,270,300,330,360))*np.pi/180)
    for i in range(12) :    
        glVertex2f(x[i],y[i])   
    glEnd()
def polygon_key_events(a) :
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity() 
    if a == 1 : glBegin(GL_POINTS)
    elif a == 2 : glBegin(GL_LINES)
    elif a == 3 : glBegin(GL_LINE_STRIP)
    elif a == 4 : glBegin(GL_LINE_LOOP)
    elif a == 5 : glBegin(GL_TRIANGLES)
    elif a == 6 : glBegin(GL_TRIANGLE_STRIP)
    elif a == 7 : glBegin(GL_TRIANGLE_FAN)
    elif a == 8 : glBegin(GL_QUADS)
    elif a == 9 : glBegin(GL_QUAD_STRIP)
    elif a == 10 : glBegin(GL_POLYGON)
    x = np.cos(np.array((0,30,60,90,120,150,180,210,240,270,300,330,360))*np.pi/180)
    y = np.sin(np.array((0,30,60,90,120,150,180,210,240,270,300,330,360))*np.pi/180)
    for i in range(12) :    
        glVertex2f(x[i],y[i])   
    glEnd()

def key_callback(window,key,scancode,action,mods) :
    if (key == glfw.KEY_ESCAPE and action == glfw.PRESS) :
        glfw.set_window_should_close(window, 1)
def main() :

    if not glfw.init() :
        return
    window = glfw.create_window(480,480,"CG_weekly_practice_03-1_2017069598",None,None)
    if not window:
        glfw.termiante()
        return
    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)

    while not glfw.window_should_close(window) :
        glfw.poll_events()
        polygon()
        if (glfw.get_key(window,glfw.KEY_1)==glfw.PRESS) : polygon_key_events(1)
        elif (glfw.get_key(window,glfw.KEY_2)==glfw.PRESS) : polygon_key_events(2)
        elif (glfw.get_key(window,glfw.KEY_3)==glfw.PRESS) : polygon_key_events(3)
        elif (glfw.get_key(window,glfw.KEY_4)==glfw.PRESS) : polygon_key_events(4)
        elif (glfw.get_key(window,glfw.KEY_5)==glfw.PRESS) : polygon_key_events(5)
        elif (glfw.get_key(window,glfw.KEY_6)==glfw.PRESS) : polygon_key_events(6)
        elif (glfw.get_key(window,glfw.KEY_7)==glfw.PRESS) : polygon_key_events(7)
        elif (glfw.get_key(window,glfw.KEY_8)==glfw.PRESS) : polygon_key_events(8)
        elif (glfw.get_key(window,glfw.KEY_9)==glfw.PRESS) : polygon_key_events(9)
        elif (glfw.get_key(window,glfw.KEY_0)==glfw.PRESS) : polygon_key_events(10)

        glfw.swap_buffers(window)

    glfw.termiante()

if __name__ == "__main__" :
    main()