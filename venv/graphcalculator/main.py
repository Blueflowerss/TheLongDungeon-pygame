
x1 = input("X1 -->")
y1 = input("Y1 -- >")
x2 = input("X2 -->")
y2 = input("Y2 -->")
def convertToVector(x,y):
    if x != "" and y != "":
        return (float(x),float(y))


XY1 = convertToVector(x1,y1)
XY2 = convertToVector(x2,y2)
#y=ax+b
if XY1 != XY2 and (XY1[0] != XY2[0] and XY1[1] != XY2[1]):
    a = (XY1[1] - XY2[1]) / (XY1[0] - XY2[0])
    b = XY1[1] - a * XY1[0]
    print("Result --> y="+str(a)+"x+"+str(b))
else:
    print("Error, coordinates are the same.")