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

def drawTriangle(canvas, pts, color, fill=False):
    for k in range(pts.shape[0]-1):
        drawLine(canvas, pts[k,0], pts[k,1], 
                        pts[k+1,0], pts[k+1,1], color)
    drawLinePQ(canvas, pts[-1], pts[0], color)

    if fill == True:
        p0p1Line = getline(pts[0][0], pts[0][1], pts[1][0], pts[1][1])
        p1p2Line = getline(pts[1][0], pts[1][1], pts[2][0], pts[2][1])
        p2p0Line = getline(pts[2][0], pts[2][1], pts[0][0], pts[0][1])

        for i in p0p1Line:   #p2 ~ line
            drawLine(canvas, pts[2][0], pts[2][1], i[0], i[1], color)
        for i in p1p2Line:   #p0 ~ line
            drawLine(canvas, pts[0][0], pts[0][1], i[0], i[1], color)
        for i in p2p0Line:   #p1 ~ line
            drawLine(canvas, pts[1][0], pts[1][1], i[0], i[1], color)

    return

def main():
    width, height = 800, 800
    canvas = np.zeros((height, width, 3), dtype='uint8')
    
    angle = 0

    while True:
        canvas = np.zeros((height, width, 3), dtype='uint8')
        #color = np.random.randint(0, 256, size=3)

        rec_wid = 50
        rec_hei = 200

        wing_wid = 80
        wing_hei = 120

        rec = np.array([(0,0,1), (rec_wid,0,1), (rec_wid,rec_hei,1), (0,rec_hei,1)])
        centerT1 = makeTmat(400,400)
        recT2 = makeTmat(-rec_wid/2,0)

        R = centerT1 @ recT2
        rT = R @ rec.T
        rec = rT.T
        rec = rec.astype('int')
        drawPolygon(canvas, rec, (255,0,0))

        #first
        first = np.array([(0,0,1), (wing_hei,-wing_wid/2,1), (wing_hei,wing_wid/2,1)])
        firstR1 = makeRmat(angle)

        pT1 = centerT1 @ firstR1 @ first.T
        first = pT1.T
        first = first.astype('int')
        drawTriangle(canvas, first, (255,255,255), fill=True)

        #second
        second = np.array([(0,0,1), (wing_hei,-wing_wid/2,1), (wing_hei,wing_wid/2,1)])
        secondR1 = makeRmat(angle+90)

        pT2 = centerT1 @ secondR1 @ second.T
        second = pT2.T
        second = second.astype('int')
        drawTriangle(canvas, second, (255,255,255), fill=True)

        #third
        third = np.array([(0,0,1), (wing_hei,-wing_wid/2,1), (wing_hei,wing_wid/2,1)])
        thirdR1 = makeRmat(angle+180)

        pT3 = centerT1 @ thirdR1 @ third.T
        third = pT3.T
        third = third.astype('int')
        drawTriangle(canvas, third, (255,255,255), fill=True)

        #fourth
        fourth = np.array([(0,0,1), (wing_hei,-wing_wid/2,1), (wing_hei,wing_wid/2,1)])
        fourthR1 = makeRmat(angle+270)

        pT4 = centerT1 @ fourthR1 @ fourth.T
        fourth = pT4.T
        fourth = fourth.astype('int')
        drawTriangle(canvas, fourth, (255,255,255), fill=True)       

        angle += 5

        #showing
        cv2.imshow("window", canvas)
        if cv2.waitKey(10) == 27: break

#main
if __name__ == "__main__":
  main()
