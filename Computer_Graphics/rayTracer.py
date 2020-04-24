#!/usr/bin/env python3
# -*- coding: utf-8 -*
# sample_python aims to allow seamless integration with lua.
# see examples below

import os
import sys
import pdb  # use pdb.set_trace() for debugging
import code # or use code.interact(local=dict(globals(), **locals()))  for debugging.
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image 

INT_MAX = sys.maxsize

class Color:
    def __init__(self, R, G, B):
        self.color = np.array([R, G, B]).astype(np.float)
    
    # Gamma corrects this color.
    # @param gamma the gamma value to use (2.2 is generally used).
    def gammaCorrect(self, gamma):
        inverseGamma = 1.0 / gamma;
        self.color = np.power(self.color, inverseGamma)

    def toUINT8(self):
        return (np.clip(self.color, 0, 1) * 255).astype(np.uint8)


class Shader:
    def __init__(self, type):
        self.t = type


class Shader_Phg(Shader):
    def __init__(self, diffuse, specular, exponent):
        self.d = diffuse
        self.s = specular
        self.e = exponent


class Shader_lbt(Shader):
    def __init__(self, diffuse):
        self.d = diffuse


class Sphere:
    def __init__(self, center, radius, shader):
        self.c = center
        self.r = radius
        self.s = shader


class Box:
    def __init__(self, minPt, maxPt, shader, normals):
        self.minPt = minPt
        self.maxPt = maxPt
        self.s = shader
        self.n = normals


class View:
    def __init__(self, viewPoint, viewDir, viewUp, viewProjNormal, viewWidth, viewHeight, projDistance, intensity):
        self.vPt = viewPoint
        self.vD = viewDir
        self.vU = viewUp
        self.vProjN = viewProjNormal
        self.vWth = viewWidth
        self.vHght = viewHeight
        self.projDist = projDistance
        self.intensity = intensity

class Light:
    def __init__(self, position, intensity):
        self.pst = position
        self.intensity = intensity

def raytrace(list, ray, viewPoint):
    global INT_MAX
    m = INT_MAX

    # idx is the index of the closest sphere or box
    idx = -1
    cnt = 0

    for i in list:
        if i.__class__.__name__ == 'Sphere':

            x = np.sum(ray * ray)
            y = np.sum((viewPoint - i.c) * ray)
            z = np.sum((viewPoint - i.c) ** 2) - i.r ** 2

            if y ** 2 - x * z >= 0:
                if -y + np.sqrt(y ** 2 - x * z) >= 0:
                    if m >= (-y + np.sqrt(y ** 2 - x * z)) / x:
                        m = (-y + np.sqrt(y ** 2 - x * z)) / x
                        idx = cnt

                if -y - np.sqrt(y ** 2 - x * z) >= 0:
                    if m >= (-y - np.sqrt(y ** 2 - x * z)) / x:
                        m = (-y - np.sqrt(y ** 2 - x * z)) / x
                        idx = cnt

        elif i.__class__.__name__ == 'Box':
            result = 1

            tx_min = (i.minPt[0]-viewPoint[0])/ray[0]
            tx_max = (i.maxPt[0]-viewPoint[0])/ray[0]

            if tx_min > tx_max:
                tx_min, tx_max = tx_max, tx_min

            ty_min = (i.minPt[1]-viewPoint[1])/ray[1]
            ty_max = (i.maxPt[1]-viewPoint[1])/ray[1]

            if ty_min > ty_max:
                ty_min, ty_max = ty_max, ty_min

            if tx_min > ty_max or ty_min > tx_max:
                result = 0

            if ty_min > tx_min:
                tx_min = ty_min
            if ty_max < tx_max:
                tx_max = ty_max

            tz_min = (i.minPt[2]-viewPoint[2])/ray[2]
            tz_max = (i.maxPt[2]-viewPoint[2])/ray[2]

            if tz_min > tz_max:
                tz_min, tz_max = tz_max, tz_min

            if tx_min > tz_max or tz_min > tx_max:
                result = 0

            if tz_min >= tx_min:
                tx_min = tz_min
            if tz_max < tx_max:
                tx_max = tz_max

            if result == 1:
                if m >= tx_min:
                    m = tx_min
                    idx = cnt

        cnt = cnt + 1

    # return gamma and index of closest figure in list
    return [m, idx]


def shade(m, ray, view, list, idx, light):
    if idx == -1:
        # No intersection point
        return np.array([0, 0, 0])
    else:
        a = 0
        b = 0
        c = 0
        n = np.array([0, 0, 0])
        v = -m*ray

        if list[idx].__class__.__name__ == 'Sphere':
            n = view.vPt + m*ray - list[idx].c

            if(abs(np.sqrt(np.sum(n*n)) - list[idx].r)>0.000001):
                print('check', abs(np.sqrt(np.sum(n*n)) - list[idx].r))

            n = n / np.sqrt(np.sum(n * n))

        elif list[idx].__class__.__name__ == 'Box':
            point_i = view.vPt + m*ray
            diff = INT_MAX
            i = -1
            cnt = 0

            for normal in list[idx].n:
                if abs(np.sum(normal[0:3] * point_i)-normal[3]) < diff:
                    diff = abs(np.sum(normal[0:3] * point_i)-normal[3])
                    i = cnt
                cnt = cnt + 1
            n = list[idx].n[i][0:3]
            n = n / np.sqrt(np.sum(n * n))

        for i in light:
            l_i = v + i.pst - view.vPt
            l_i = l_i / np.sqrt(np.sum(l_i * l_i))
            check = raytrace(list, -l_i, i.pst)

            if check[1] == idx:
                if list[idx].s.__class__.__name__ == "Shader_lbt":
                    a = a + list[idx].s.d[0] * i.intensity[0] * max(0, np.dot(l_i, n))
                    b = b + list[idx].s.d[1] * i.intensity[1] * max(0, np.dot(l_i, n))
                    c = c + list[idx].s.d[2] * i.intensity[2] * max(0, np.dot(l_i, n))
                elif list[idx].s.__class__.__name__ == 'Shader_Phg':
                    v_unit = v / np.sqrt(np.sum(v**2))
                    h = v_unit + l_i
                    h = h / np.sqrt(np.sum(h*h))
                    a = a + list[idx].s.d[0]*max(0,np.dot(n,l_i))*i.intensity[0] + list[idx].s.s[0] * i.intensity[0] * pow(max(0, np.dot(n, h)),list[idx].s.e[0])
                    b = b + list[idx].s.d[1]*max(0,np.dot(n,l_i))*i.intensity[1] + list[idx].s.s[1] * i.intensity[1] * pow(max(0, np.dot(n, h)),list[idx].s.e[0])
                    c = c + list[idx].s.d[2]*max(0,np.dot(n,l_i))*i.intensity[2] + list[idx].s.s[2] * i.intensity[2] * pow(max(0, np.dot(n, h)),list[idx].s.e[0])
        
        res = Color(a, b, c)
        res.gammaCorrect(2.2)
        return res.toUINT8()


def getNormal(a, b, c):
    dir = np.cross((b-a), (c-a))
    d = np.sum(dir*c)
    return np.array([dir[0], dir[1], dir[2], d])

def main():
    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    # set default values
    viewPoint = np.array([0, 0, 0]).astype(np.float)
    viewDir = np.array([0, 0, -1]).astype(np.float)
    viewUp = np.array([0, 1, 0]).astype(np.float)
    viewProjNormal = -1 * viewDir # you can safely assume this. (no examples will use shifted perspective camera)
    viewWidth = 1.0
    viewHeight = 1.0
    projDistance = 1.0
    intensity = np.array([1, 1, 1]).astype(np.float)  # how bright the light is.
    print(np.cross(viewDir, viewUp))

    imgSize = np.array(root.findtext('image').split()).astype(np.int)

    list = []
    light = []

    for c in root.findall('camera'):
        viewPoint = np.array(c.findtext('viewPoint').split()).astype(np.float)
        viewDir = np.array(c.findtext('viewDir').split()).astype(np.float)
        print('viewpoint', viewPoint)
        if (c.findtext('projNormal')):
            viewProjNormal = np.array(c.findtext('projNormal').split()).astype(np.float)
        viewUp = np.array(c.findtext('viewUp').split()).astype(np.float)
        if (c.findtext('projDistance')):
            projDistance = np.array(c.findtext('projDistance').split()).astype(np.float)
        viewWidth = np.array(c.findtext('viewWidth').split()).astype(np.float)
        viewHeight = np.array(c.findtext('viewHeight').split()).astype(np.float)

    view = View(viewPoint, viewDir, viewUp, viewProjNormal, viewWidth, viewHeight, projDistance, intensity)

    for c in root.findall('surface'):
        type_c = c.get('type')
        if type_c == 'Sphere':
            center_c = np.array(c.findtext('center').split()).astype(np.float)
            radius_c = np.array(c.findtext('radius')).astype(np.float)
            ref = ''
            for child in c:
                if child.tag == 'shader':
                    ref = child.get('ref')
            for d in root.findall('shader'):
                if d.get('name') == ref:
                    diffuse_d = np.array(d.findtext('diffuseColor').split()).astype(np.float)
                    print('name', d.get('name'))
                    print('diffuseColor', diffuse_d)
                    type_d = d.get('type')
                    if type_d == 'Lambertian':
                        shader = Shader_lbt(diffuse_d)
                        list.append(Sphere(center_c, radius_c, shader))
                    elif type_d == 'Phong':
                        exponent_d = np.array(d.findtext('exponent').split()).astype(np.float)
                        specular_d = np.array(d.findtext('specularColor').split()).astype(np.float)
                        shader = Shader_Phg(diffuse_d, specular_d, exponent_d)
                        list.append(Sphere(center_c, radius_c, shader))
        elif type_c == 'Box':
            minPt_c = np.array(c.findtext('minPt').split()).astype(np.float)
            maxPt_c = np.array(c.findtext('maxPt').split()).astype(np.float)

            normals = []

            point_a = np.array([minPt_c[0], minPt_c[1], maxPt_c[2]])
            point_b = np.array([minPt_c[0], maxPt_c[1], minPt_c[2]])
            point_c = np.array([maxPt_c[0], minPt_c[1], minPt_c[2]])
            point_d = np.array([minPt_c[0], maxPt_c[1], maxPt_c[2]])
            point_e = np.array([maxPt_c[0], minPt_c[1], maxPt_c[2]])
            point_f = np.array([maxPt_c[0], maxPt_c[1], minPt_c[2]])

            normals.append(getNormal(point_a, point_c, point_e))
            normals.append(getNormal(point_b, point_c, point_f))
            normals.append(getNormal(point_a, point_b, point_d))
            normals.append(getNormal(point_a, point_e, point_d))
            normals.append(getNormal(point_e, point_c, point_f))
            normals.append(getNormal(point_d, point_f, point_b))

            ref = ''
            for child in c:
                if child.tag == 'shader':
                    ref = child.get('ref')
            for d in root.findall('shader'):
                if d.get('name') == ref:
                    diffuse_d = np.array(d.findtext('diffuseColor').split()).astype(np.float)
                    print('name', d.get('name'))
                    print('diffuseColor', diffuse_d)
                    type_d = d.get('type')
                    if type_d == 'Lambertian':
                        shader = Shader_lbt(diffuse_d)
                        list.append(Box(minPt_c, maxPt_c, shader, normals))
                    elif type_d == 'Phong':
                        exponent_d = np.array(d.findtext('exponent').split()).astype(np.float)
                        specular_d = np.array(d.findtext('specularColor').split()).astype(np.float)
                        shader = Shader_Phg(diffuse_d, specular_d, exponent_d)
                        list.append(Box(minPt_c, maxPt_c, shader, normals))

    for c in root.findall('light'):
        position_c = np.array(c.findtext('position').split()).astype(np.float)
        intensity_c = np.array(c.findtext('intensity').split()).astype(np.float)
        light.append(Light(position_c, intensity_c))

    channels = 3
    img = np.zeros((imgSize[1], imgSize[0], channels), dtype=np.uint8)
    img[:, :] = 0

    pixel_x = view.vWth / imgSize[0]
    pixel_y = view.vHght / imgSize[1]

    w = view.vD
    u = np.cross(w, view.vU)
    v = np.cross(w, u)

    w_unit = w / np.sqrt(np.sum(w * w))
    u_unit = u / np.sqrt(np.sum(u * u))
    v_unit = v / np.sqrt(np.sum(v * v))

  
    start = w_unit * view.projDist - u_unit * pixel_x * ((imgSize[0]/2) + 1/2) - v_unit * pixel_y * ((imgSize[1]/2) + 1/2)

    for x in np.arange(imgSize[0]):
        for y in np.arange(imgSize[1]):
            ray = start + u_unit * x * pixel_x + pixel_y * y * v_unit
            tmp = raytrace(list, ray, view.vPt)
            img[y][x] = shade(tmp[0], ray, view, list, tmp[1], light)

    rawimg = Image.fromarray(img, 'RGB')
    #rawimg.save('out.png')
    rawimg.save(sys.argv[1] + '.png')


if __name__ == "__main__":
    main()