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

def drawStar(canvas, points, color):
    for i in range(points.shape[0]-1):
        r = i+1
        while True:
            drawLine(canvas, points[i][0], points[i][1],
                             points[r][0], points[r][1], color)
            r += 1
            if r == points.shape[0]: break
    drawPolygon(canvas, points, (0,0,0))
    return

def makingStar(canvas, ngon, size, T, R, color):
        #star
        points = getRegularNGon(ngon)
        points *= size
        points[:, 2] = 1
        T1 = makeTmat(T[0], T[1])
        R1 = makeRmat(R)

        pT = T1 @ R1 @ points.T
        points = pT.T
        points = points.astype('int')
        drawStar(canvas, points, color)


def main():
    width, height = 800, 800
    canvas = np.zeros((height, width, 3), dtype='uint8')

    ngonList = []
    sizeList = []
    locationList = []
    angleList = []

    for i in range(20):
        ngonList.append(np.random.randint(5, 7))
        sizeList.append(np.random.randint(20, 70))
        locationList.append(np.random.randint(100, 700, size=2))
        angleList.append(np.random.randint(0, 360))

    while True:
        colorList = []
        for i in range(20):
            colorList.append(np.random.randint(0, 256, size=3))
        
        for i in range(20):
            makingStar(canvas, ngonList[i], sizeList[i],
                       locationList[i], angleList[i], colorList[i])

        cv2.imshow("starry_sky", canvas)
        if cv2.waitKey(500) == 27: break


if __name__ == "__main__":
    main()