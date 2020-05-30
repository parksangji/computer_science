import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import *
import ctypes

GRID_SIZE = 30

camState = 0
target = [0., 0., 0. ]
camAng = [0., 9.]
camDist = 10
camHeight = 3.

upVector = [0, 1, 0]
prevPos = [0., 0.]
speedAng = [0.1, 0.1]
speedZoom = 0.5
speedPan = 0.001

isObj = 0
flag = 1
shadowFlag = 1
GRID_SIZE = 30

vertexArray, normalArray, faceArray = [], [], []
varr, narr, iarr, nnarr = None, None, None, None

def drawGrid():
	glLineWidth(1)
	glColor3ub(255, 255, 255)
	for x in range(-GRID_SIZE, GRID_SIZE):
		glBegin(GL_LINE_LOOP)
		glVertex3f(-GRID_SIZE, 0., x)
		glVertex3f( GRID_SIZE, 0., x)
		glEnd()

	for z in range(-GRID_SIZE, GRID_SIZE):
		glBegin(GL_LINE_LOOP)
		glVertex3f(z, 0., -GRID_SIZE)
		glVertex3f(z, 0.,  GRID_SIZE)
		glEnd()

def getShadow() :
	global varr, nnarr, iarr, faceArray
	nnarr = [[0.0] * 3] * len(varr)
	nnarr = np.array(nnarr)

	for i in range(len(iarr)):

		tmpArr1 = np.subtract(varr[faceArray[i][1]], varr[faceArray[i][0]])
		tmpArr2 = np.subtract(varr[faceArray[i][2]], varr[faceArray[i][0]])

		nv = np.cross(tmpArr1, tmpArr2)
		nv = nv / np.sqrt(np.dot(nv, nv))

		nnarr[faceArray[i][0]] += nv
		nnarr[faceArray[i][1]] += nv
		nnarr[faceArray[i][2]] += nv

	for i in range(len(varr)):
		nnarr[i] = nnarr[i] / np.sqrt(np.dot(nnarr[i], nnarr[i]))
	faceArray = []

def arraySetting():
	global varr, narr, iarr, normalArray, faceArray, vertexArray

	narr = [[0.0] * 3] * len(vertexArray)
	tfaceArray = []
	for i in range(len(faceArray)):
		tface = []
		for j in range(3):
			k = faceArray[i][j].split('/')
			tface.append(int(k[0]) - 1)
			narr[int(k[0]) - 1] = normalArray[int(k[2]) - 1]
		tfaceArray.append(tface)
	
	iarr = np.array(tfaceArray, np.int32)
	narr = np.array(narr)
	varr = np.array(vertexArray, 'float32')
	vertexArray, normalArray, faceArray = [], [], tfaceArray

def drawObject():
	global varr, narr, iarr, nnarr, shadowFlag

	glEnableClientState(GL_VERTEX_ARRAY)
	glEnableClientState(GL_NORMAL_ARRAY)
	
	if shadowFlag == 1: 
		glNormalPointer(GL_FLOAT, 3*varr.itemsize, narr)
	else :
		glNormalPointer(GL_FLOAT, 3*varr.itemsize, nnarr)
	
	glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
	glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

def calculateEye():
	global camAng, camDist, target
	tmpEye = [  target[0] + camDist * np.cos(np.radians(camAng[1])) * np.cos(np.radians(camAng[0])), 
				target[1] + camDist * np.sin(np.radians(camAng[1])), 
				target[2] + camDist * np.cos(np.radians(camAng[1])) * np.sin(np.radians(camAng[0]))   ]
	return tmpEye

def drop_callback(window, paths):
	global vertexArray, normalArray, faceArray, isObj
	isObj = 1
	face = [0] * 6
	print("File name: " + paths[0])
	file = open(paths[0], "r")

	while(True):
		tmp = []
		line = file.readline()
		if not line:
			break
		parse = line.split()
		subParse = parse[1:]
		if len(parse) == 0:
			continue

		# v: Geometric vertex
		elif parse[0] == 'v':
			for i in subParse:
				tmp.append(float(i))
			vertexArray.append(tmp)

		# vn : vertex normal
		elif parse[0] == 'vn':
			for i in subParse:
				tmp.append(float(i))
			normalArray.append(tmp)

		# f : face : how to get texture on the surface
		elif parse[0] == 'f':
			# check number of vertices
			if len(subParse) == 3: face[3] += 1
			elif len(subParse) == 4: face[4] += 1
			else: face[5] += 1
			faceArray.append(subParse)
	
	file.close()
	print("Total number of faces: " + str(face[3] + face[4] + face[5]))
	print("Number of faces with 3 vertices: " + str(face[3]))
	print("Number of faces with 4 vertices: " + str(face[4]))
	print("Number of faces with more than 4 vertices: " + str(face[5]))

	arraySetting()
	getShadow()

def key_callback(window, key, scancode, action, mods):
	global camAng, camHeight, camDist, shadowFlag, flag

	if action == glfw.PRESS or action == glfw.REPEAT:
		if key == glfw.KEY_1:
			camAng += np.radians(-10)
		elif key == glfw.KEY_3:
			camAng += np.radians(10)
		elif key == glfw.KEY_2:
			camHeight += .1
		elif key == glfw.KEY_W:
			camHeight += -.1
		elif key == glfw.KEY_A:
			camDist -= .1
		# shading
		elif key == glfw.KEY_S:
			shadowFlag *= -1
		# changing mode
		elif key == glfw.KEY_Z:
			if flag == 1:
				glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
				flag *= -1
			else:
				glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
				flag *= -1

def mouse_callback(window, button, action, mods):
	global camState    
	# orbit
	# Rotate the camera around the target point by changing azimuth / elevation angles.
	if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
		camState = 1
	if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.RELEASE:
		camState = 0
	
	# panning
	# Move both the target point and camera in left, right, up and down direction of the camera
	if button == glfw.MOUSE_BUTTON_RIGHT and action == glfw.PRESS:
		camState = 2
	if button == glfw.MOUSE_BUTTON_RIGHT and action == glfw.RELEASE:
		camState = 0

def scroll_callback(window, xoffset, yoffset):
	global camDist
	# zooming
	camDist = camDist - yoffset * speedZoom
	if camDist < 1: 
		camDist = 1

def cursor_callback(window, xpos, ypos):
	global prevPos, camAng, camState, target, camDist, upVector
	# orbit
	xDistance = xpos - prevPos[0]
	yDistance = ypos - prevPos[1]

	if camState == 1: 
		camAng[1] += speedAng[0] * yDistance
		speed = speedAng[0]
		if camAng[1] < 0:
			camAng[1] += 360
		if camAng[1] >= 360:
			camAng[1] -= 360
		if camAng[1] >= 90 and camAng[1] < 270:
			upVector[1] = -1
		else:
			upVector[1] = 1
		camAng[0] += speed * xDistance
	
	# panning
	if camState == 2:
		tmpEye = calculateEye()
		eye = np.array(tmpEye)
		at = np.array(target)
		up = np.array(upVector)

		w = (eye - at) / np.sqrt(np.dot(eye - at, eye - at))
		u = np.cross(up, w) / np.sqrt(np.dot(np.cross(up, w), np.cross(up, w)))
		v = np.cross(w, u)

		target += xDistance * -u * speedPan * camDist
		target += yDistance *  v * speedPan * camDist

	prevPos[0] = xpos
	prevPos[1] = ypos

def render():
	global camAng, camHeight, camDist, tmpEye, target, upVector, isObj

	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	glEnable(GL_DEPTH_TEST)

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45, 1, 1, 1000)

	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	tmpEye = calculateEye()
	gluLookAt(  tmpEye[0], tmpEye[1], tmpEye[2],
				target[0], target[1], target[2],
				upVector[0], upVector[1], upVector[2])

	drawGrid()

	# lighting
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glEnable(GL_LIGHT1)
	# light 0
	glPushMatrix()
	lightPos = (3.,4.,5.,1.)
	glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
	glPopMatrix()
	# light 1
	glPushMatrix()
	glRotatef(120,0,1,0)
	lightPos = (-3.,-4.,5.,1.) 
	glLightfv(GL_LIGHT1, GL_POSITION, lightPos)
	glPopMatrix()
	
	ambientLightColor1 = (.1,.0,.0,1.)
	diffuseLightColor1 = (.6,.0,.0,1.)
	
	glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor1)
	glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLightColor1)
	ambientLightColor2 = (.0,.1,.0,1.)
	diffuseLightColor2 = (.0,.6,.0,1.)
	glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor2)
	glLightfv(GL_LIGHT1, GL_DIFFUSE, diffuseLightColor2)
	
	# material reflectance for each color channel
	objectColor = (1.,1.,1.,1.)
	specularObjectColor = (1.,1.,1.,1.)
	glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
	glMaterialfv(GL_FRONT, GL_SHININESS, 10)
	glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
	
	glPushMatrix()
	
	if isObj > 0: 
		drawObject()
	glPopMatrix()

	glDisable(GL_LIGHTING)

def main():
	global isObj, flag

	if not glfw.init():
		return
	window = glfw.create_window(640,640,'assignment2-2015004402', None,None)
	if not window:
		glfw.terminate()
		return
	glfw.make_context_current(window)
	glfw.set_mouse_button_callback(window, mouse_callback)
	glfw.set_cursor_pos_callback(window, cursor_callback)
	glfw.set_scroll_callback(window, scroll_callback)
	glfw.set_key_callback(window, key_callback)
	glfw.set_drop_callback(window, drop_callback)
	glfw.swap_interval(1)
	glfw.make_context_current(window)

	while not glfw.window_should_close(window):
		glfw.poll_events()
		render()
		glfw.swap_buffers(window)

	glfw.terminate()

if __name__ == "__main__":
	main()