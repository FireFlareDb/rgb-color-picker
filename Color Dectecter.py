import cv2
import numpy as np
import pandas as pd
import argparse


# giving image path by using argparse
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help = "Image Path")
args = vars(ap.parse_args())
img_path = args['image']
# Reading Image With OpenCV
img = cv2.imread(img_path)


#declaring global variables (are used later on)
clicked = False
r = g = b = xpos = ypos = 0


# Now We Will Read The CSV File
index = ["color","color_name","hex","R","G","B"]
csv = pd.read_csv('colors.csv', names=index, header=None)




def draw_function(event, x, y, flages, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

# First, We'll Create A Windown Using OpenCV To Display The Image
# Second, We'll Set A CallBack Function Which Will Be Called When Mouse Event Happens
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)


# Now We Have The R,G,B Values. So We Need Another Function Which Will Return 
# The Name Of Color.
# To Get The Color Name, By Calculating The Minimun Distance From The Color In CSV

# Formula 👇
# d = abs(Red - ithRedColor) + (Green - ithGreenColor) + (Blue - ithBlueColor)

def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i, "G"])) + abs(B- int(csv.loc[i, "B"]))
        if (d<=minimum):
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname


while(1):
    cv2.imshow("image",img)
    if (clicked):
        # cv2.rectangle(image, startpoint, endoint, color, thickness) -1 thinkness fills recentangle entirely
        cv2.rectangle(img, (20,20), (750, 60), (b,g,r), -1)
        
        # Creating text string to display (color name and RGB values)
        text = getColorName(r,g,b) + ' R='+str(r) + ' G='+str(g) + ' B='+str(b)
        
        cv2.putText(img, text, (50, 50), 2,0.8,(255,255,255), 2, cv2.LINE_AA)
        
        # For Very Light Colors We Will Display Text In Balck Color
        if(r+g+b>=600):
            cv2.putText(img, text, (50,50), 2,0.8,(0,0,0),2,cv2.LINE_AA)
        clicked = False
        
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destoryAllwindows()