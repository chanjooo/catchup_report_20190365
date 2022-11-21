#20190365 김찬주
import numpy as np
import cv2
import time

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
    width, height = 700, 700
    canvas = np.zeros((height, width, 3), dtype='uint8')

    hour = 0
    hour_angle = 0
    minute_angle = 0

    while True:
        canvas = np.zeros((height, width, 3), dtype='uint8')

        #frame
        frame = getRegularNGon(100)
        frame *= 150
        frame[:,2] = 1
        centerT1 = makeTmat(height/2, width/2)  #center

        fT = centerT1 @ frame.T
        frame = fT.T
        frame = frame.astype('int')
        drawPolygon(canvas, frame, (255,255,255))

        for i in range(0,12):
            gap = np.array([(135,0,1), (145,0,1)])
            startR1 = makeRmat(-90)    #make polygon stand
            gapR2 = makeRmat(i*30)

            gT = centerT1 @ startR1 @ gapR2 @ gap.T
            gap = gT.T
            gap = gap.astype('int')
            drawLinePQ(canvas, gap[0], gap[1], (255,255,255))

        #a hour hand
        hourhand = np.array([(0,-4,1), (60,-4,1), (65,0,1), (60,4,1), (0,4,1)])
        hhR2 = makeRmat(hour_angle)

        hT = centerT1 @ startR1 @ hhR2 @ hourhand.T
        hourhand = hT.T
        hourhand = hourhand.astype('int')
        drawPolygon(canvas, hourhand, (255,80,80))

        #a minute hand
        minutehand = np.array([(0,-5,1), (100,-5,1), (105,0,1), (100,5,1), (0,5,1)])
        mhR2 = makeRmat(minute_angle)

        mT = centerT1 @ startR1 @ mhR2 @ minutehand.T
        minutehand = mT.T
        minutehand = minutehand.astype('int')
        drawPolygon(canvas, minutehand, (255,128,128))

        #time
        now = time.localtime(time.time())

        minute_angle = now.tm_min * 6
        if now.tm_hour > 12: hour = now.tm_hour - 12
        hour_angle = hour*30 + (now.tm_min / 60 * 30)

        #show
        cv2.imshow("window", canvas)
        if cv2.waitKey(10) == 27: break

#main
if __name__ == "__main__":
    main()




   