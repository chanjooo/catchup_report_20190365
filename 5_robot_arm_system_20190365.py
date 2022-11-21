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

def getRectagle(width, height):
    points = [(0,0,1), (width,0,1), (width, height,1), (0,height,1)]
    points = np.array(points)
    return points

def wiper_moving(angle, area):
    if (angle // area) % 2 == 0:
        degree = area-(angle % area)
    else:
        degree = angle % area
    return degree


def main():
    width, height = 1000, 600
    canvas = np.zeros((height, width, 3), dtype='uint8')
    degree_2 = 0
    degree_3 = 0
    degree_4 = 0
    degree_5 = 0

    alpha = 0
    beta = 0
    gamma = 0
    delta = 0

    wid = 100
    hei = 30

    while True:
        canvas = np.zeros((height, width, 3), dtype='uint8')
        #color = np.random.randint(0, 256, size=3)

        #Rec1
        rec1 = getRectagle(wid, hei)
        rec1[:, 2] = 1

        rec1T1 = makeTmat(200, height-50)
        rec1R1 = makeRmat(-90)
        rec1T2 = makeTmat(0, -hei/2)

        Q1 = rec1T1 @ rec1R1 @ rec1T2
        qT1 = Q1 @ rec1.T
        points_1 = qT1.T
        points_1 = points_1.astype('int')
        drawPolygon(canvas, points_1, (255,155,155))

        #rec2
        rec2 = getRectagle(wid, hei)
        rec2[:, 2] = 1

        rec2T1 = makeTmat(wid, 0)
        rec2T2 = makeTmat(0, hei/2)
        rec2R1 = makeRmat(degree_2)
        rec2T3 = makeTmat(0, -hei/2)

        Q2 = rec2T1 @ rec2T2 @ rec2R1 @ rec2T3
        qT2 = Q1 @ Q2 @ rec2.T
        points_2 = qT2.T
        points_2 = points_2.astype('int')
        drawPolygon(canvas, points_2, (255,155,155))

        #rec3
        rec3 = getRectagle(wid, hei)
        rec3[:, 2] = 1

        rec3T1 = makeTmat(wid, 0)
        rec3T2 = makeTmat(0, hei/2)
        rec3R1 = makeRmat(-degree_3)
        rec3T3 = makeTmat(0, -hei/2)

        Q3 = rec3T1 @ rec3T2 @ rec3R1 @ rec3T3
        qT3 = Q1 @ Q2 @ Q3 @ rec3.T
        points_3 = qT3.T
        points_3 = points_3.astype('int')
        drawPolygon(canvas, points_3, (255,155,155))

        #rec4
        rec4 = getRectagle(wid, hei)
        rec4[:, 2] = 1

        rec4T1 = makeTmat(wid, 0)
        rec4T2 = makeTmat(0, hei/2)
        rec4R1 = makeRmat(degree_4)
        rec4T3 = makeTmat(0, -hei/2)

        Q4 = rec4T1 @ rec4T2 @ rec4R1 @ rec4T3
        qT4 = Q1 @ Q2 @ Q3 @ Q4 @ rec4.T
        points_4 = qT4.T
        points_4 = points_4.astype('int')
        drawPolygon(canvas, points_4, (255,155,155))

        #rec5
        rec5 = getRectagle(wid, hei)
        rec5[:, 2] = 1

        rec5T1 = makeTmat(wid, 0)
        rec5T2 = makeTmat(0, hei/2)
        rec5R1 = makeRmat(degree_5)
        rec5T3 = makeTmat(0, -hei/2)

        Q5 = rec5T1 @ rec5T2 @ rec5R1 @ rec5T3
        qT5 = Q1 @ Q2 @ Q3 @ Q4 @ Q5 @ rec5.T
        points_5 = qT5.T
        points_5 = points_5.astype('int')
        drawPolygon(canvas, points_5, (255,155,155))        

        #moving
        area = 90     #90, 180, 360 and so on

        alpha += 3  
        degree_2 = wiper_moving(alpha, area)
        beta += 5
        degree_3 = wiper_moving(beta, area)
        gamma += 7
        degree_4 = wiper_moving(gamma, area)
        delta += 1
        degree_5 = wiper_moving(delta, area)

        #showing
        cv2.imshow("window", canvas)
        if cv2.waitKey(10) == 27: break

#main
if __name__ == "__main__":
  main()
