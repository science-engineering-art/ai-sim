# Python3 code to find all three angles
# of a triangle given coordinate
# of all three vertices
import math
 
# returns square of distance b/w two points
def lengthSquare(X, Y):
    xDiff = X[0] - Y[0]
    yDiff = X[1] - Y[1]
    return xDiff * xDiff + yDiff * yDiff
     
def printAngle(A, B, C):
     
    # Square of lengths be a2, b2, c2
    a2 = lengthSquare(B, C)
    b2 = lengthSquare(A, C)
    c2 = lengthSquare(A, B)
 
    # length of sides be a, b, c
    # a = math.sqrt(a2)
    b = math.sqrt(b2)
    c = math.sqrt(c2)
 
    # From Cosine law
    alpha = math.acos((b2 + c2 - a2) /
                         (2 * b * c))
    # betta = math.acos((a2 + c2 - b2) /
    #                      (2 * a * c))
    # gamma = math.acos((a2 + b2 - c2) /
    #                      (2 * a * b))
 
    # Converting to degree
    alpha = alpha * 180 / math.pi
    # betta = betta * 180 / math.pi
    # gamma = gamma * 180 / math.pi
 
    # printing all the angles
    print("alpha : %f" %(alpha))
    # print("betta : %f" %(betta))
    # print("gamma : %f" %(gamma))
         
# Driver code
A = (0, 0)
B = (0, 2)
C = (0, 0)
 
# printAngle(A, B, C)
 

def calculate_angle(x0, y0, x1, y1) -> float:

    if (x0**2 + y0**2) > (x1**2 + y1**2):
        tmp = x0, y0
        x0, y0 = x1, y1
        x1, y1 = tmp

    print(f'x0: {x0}, y0: {y0}, x1: {x1}, y1: {y1}')

    co = y1 - y0
    ca = x1 - x0

    if ca == 0 and co != 0:
        return 90.0

    h = (co**2 + ca**2)**0.5
    
    print(f'co: {co}, ca: {ca}, h: {h}')
    try: 
        angle = math.acos((co**2 + ca**2 - h**2) / (2 * co * ca))
        angle = math.degrees(angle)
    except:
        print('error 1')

    try: 
        angle = math.acos((co**2 + h**2 - ca**2) / (2 * co * h))
        angle = math.degrees(angle)
    except:
        print('error 2')

    try:
        angle = math.acos((h**2 + ca**2 - co**2) / (2 * h * ca))
        angle = math.degrees(angle)
    except:
        print('error 3')

    return angle

print(calculate_angle(0, 0, 0, 2))

# This code is contributed
# by ApurvaRaj