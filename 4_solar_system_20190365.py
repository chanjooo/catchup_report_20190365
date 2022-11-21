#20190365 김찬주
import numpy as np
import cv2

def pos_neg(p0, p1):
    if p1 > p0: arrow = 1
    else: arrow = -1
    return arrow

def getline(x0, y0, x1, y1):
    points = []

    if np.absolute(y1-y0) < np.absolute(x1-x0):
        if x0 == x1:
            for y in range(y0, y1, pos_neg(y0, y1)):
                points.append((x0, y))
        else:
            for x in range(x0, x1, pos_neg(x0, x1)):
                y = (x - x0) * (y1 - y0) / (x1 - x0) + y0
                yint = int(y)
                points.append((x, yint))
    else:
        if y0 == y1:
            for x in range(x0, x1, pos_neg(x0, x1)):
                points.append((x, y0))
        else:
            for y in range(y0, y1, pos_neg(y0, y1)):
                x = (y - y0) * (x1 - x0) / (y1 - y0) + x0
                xint = int(x)
                points.append((xint, y))

    points.append((x1, y1))
    return points

def drawLine(canvas, x0, y0, x1, y1, color=(255, 255, 255)):
    xys = getline(x0, y0, x1, y1)
    for xy in xys:
        x, y = xy
        canvas[y, x, :] = color      
    return

def deg2rad(deg):
    rad = deg * np.pi / 180.
    return rad 

def getRegularNGon(ngon):
    delta = 360. / ngon
    points = []
    for i in range(ngon):
        degree = i * delta 
        radian = deg2rad(degree)
        x = np.cos(radian)
        y = np.sin(radian)
        points.append((x, y, 1))
    #
    points = np.array(points)
    return points 

def drawLinePQ(canvas, p, q, color):
    drawLine(canvas, p[0], p[1], q[0], q[1], color)
    return 

def drawPolygon(canvas, pts, color, axis=False):
    for k in range(pts.shape[0]-1):
        drawLine(canvas, pts[k,0], pts[k,1], 
                        pts[k+1,0], pts[k+1,1], color)
    drawLinePQ(canvas, pts[-1], pts[0], color)

    if axis == True: # center - pts[0]
        center = np.array([0., 0, 0])
        for p in pts:
            center += p 
        center = center / len(pts)
        center = center.astype('int')
        #print(center)
        drawLinePQ(canvas, center, pts[0], color=(255, 128, 128))
    return

def makeRmat(deg):
    rad = deg2rad(deg)
    c = np.cos(rad)
    s = np.sin(rad)
    Rmat = np.eye(3)
    Rmat[0,0] = c
    Rmat[0,1] = -s
    Rmat[1,0] = s
    Rmat[1,1] = c
    return Rmat

def makeTmat(a, b):
    Tmat = np.eye(3)
    Tmat[0,2] = a
    Tmat[1,2] = b
    return Tmat

def main():
    width, height = 900, 900
    canvas = np.zeros((height, width, 3), dtype='uint8')

    v_revolution = 0
    v_rotation = 0
    e_revolution = 0
    e_rotation = 0
    m_revolution = 0
    m_rotation = 0
    r_revolution = 0

    while True:
        canvas = np.zeros((height, width, 3), dtype='uint8')

        #sun
        sun = getRegularNGon(50)
        sun *= 50
        sun[:, 2] = 1

        sunT1 = makeTmat(height/2, width/2)  #center

        S = sunT1
        sun = (S @ sun.T).T
        sun = sun.astype('int')
        drawPolygon(canvas, sun, (0,0,255))

        #venus
        venus = getRegularNGon(20)
        venus *= 20
        venus[:, 2] = 1

        venusR1 = makeRmat(v_revolution)
        venusT1 = makeTmat(100, 0)
        venusR2 = makeRmat(v_rotation)

        V = venusR1 @ venusT1 @ venusR2
        venus = (S @ V @ venus.T).T
        venus = venus.astype('int')
        drawPolygon(canvas, venus, (255, 255, 255))

        #earth
        earth = getRegularNGon(20)
        earth *= 30
        earth[:, 2] = 1

        earthR1 = makeRmat(e_revolution)
        earthT1 = makeTmat(280, 0)
        earthR2 = makeRmat(-e_revolution)
        earthR3 = makeRmat(e_rotation)

        E = earthR1 @ earthT1 @ earthR2 @ earthR3
        earth = (S @ E @ earth.T).T
        earth = earth.astype('int')
        drawPolygon(canvas, earth, (255, 0, 0))

        #moon
        moon = getRegularNGon(20)
        moon *= 20
        moon[:, 2] = 1

        moonR1 = makeRmat(m_revolution)
        moonT1 = makeTmat(100, 0)
        moonR2 = makeRmat(-m_revolution)
        moonR3 = makeRmat(m_rotation)

        M = moonR1 @ moonT1 @ moonR2 @ moonR3
        moon = (S @ E @ M @ moon.T).T
        moon = moon.astype('int')
        drawPolygon(canvas, moon, (0, 120, 120))

        #rocket
        rocket = getRegularNGon(5)
        rocket *= 10
        rocket[:, 2] = 1

        rocketR1 = makeRmat(r_revolution)
        rocketT1 = makeTmat(40, 0)
        rocketR2 = makeRmat(-r_revolution)

        R = rocketR1 @ rocketT1 @ rocketR2
        rocket = (S @ E @ M @ R @ rocket.T).T
        rocket = rocket.astype('int')
        drawPolygon(canvas, rocket, (100, 100, 100))  

        v_revolution += (255/365)
        v_rotation += -(244/365)
        e_revolution += 1
        e_rotation += 30
        m_revolution += 12
        m_rotation += 12
        r_revolution += 3

        cv2.imshow("window", canvas)
        if cv2.waitKey(100) == 27: break

#main
if __name__ == "__main__":
  main()