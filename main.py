import pyautogui
import time
import cv2
import numpy as np

# Given a minefield.
# Solve for a series of moves that will get from the top left corner of the
# minefield to the bottom right without stepping on a mine.
# Step 1: Screenshot the minefield with pyautogui.
# Step 2: Convert the screenshot to an array.
# Step 3: Use a search algorithm to find the path and output the sequence.

# Screen Size Debug
# screenWidth, screenHeight = pyautogui.size()
# print("Width: ", screenWidth, "\nHeight :", screenHeight)

# Calibration Debug
# time.sleep(10)
# currentMouseX1, currentMouseY1 = pyautogui.position()
# print("Current xy position: ", currentMouseX1, ",", currentMouseY1)
# time.sleep(10)
# currentMouseX2, currentMouseY2 = pyautogui.position()
# print("Current xy position: ", currentMouseX2, ",", currentMouseY2)

# Maze Image Capture, specific to 1920 x 1080 screensize, may differ from case to case
# time.sleep(3)
mazeImage = pyautogui.screenshot(region=(440, 217, 485, 487))
# Local save file path
mazeImage.save(r'./mazeImage.png')
# 22 wide x 22 high, 484 cells
# start point is always [0][0] end point is always [21][21]

# read the image and resize
img = cv2.imread('mazeImage.png')
resized = cv2.resize(img, (484, 484), cv2.INTER_LINEAR)


# cv2.imshow("Resized Image", resized)
# cv2.waitKey(1)


# splits up the grid into 484 individual cells (22 rows x 22 columns)
def split_grid(grid):
    rows = np.vsplit(grid, 22)
    boxes = []
    for r in rows:
        cols = np.hsplit(r, 22)
        for box in cols:
            box = cv2.resize(box, (21, 21), cv2.INTER_LINEAR)
            # cv2.imshow("cell", box)
            # cv2.waitKey()
            boxes.append(box)
    return boxes


# Don't really need Start & Finish because they're at fixed points, 0,0 & 21,21
# Load up Space and Bomb for Image Comparison, compare with images in grid and output 0 or 1 to maze accordingly
Start = cv2.imread('Start.png')
Space = cv2.imread('Space.png')
Bomb = cv2.imread('Bomb.png')
Finish = cv2.imread('Finish.png')
gray_Bomb = cv2.cvtColor(Bomb, cv2.COLOR_BGR2GRAY)
gray_Space = cv2.cvtColor(Space, cv2.COLOR_BGR2GRAY)
gray_Start = cv2.cvtColor(Start, cv2.COLOR_BGR2GRAY)
gray_Finish = cv2.cvtColor(Finish, cv2.COLOR_BGR2GRAY)
histogram1 = cv2.calcHist([gray_Bomb], [0], None, [256], [0, 256])
histogram2 = cv2.calcHist([gray_Space], [0], None, [256], [0, 256])

maze = np.zeros((22, 22))
step = np.zeros((22, 22))
step[0][0] = 1

grid = split_grid(resized)
for x in range(22):
    for y in range(22):
        cell = grid[x * 22 + y]
        gray_cell = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
        histogram = cv2.calcHist([gray_cell], [0], None, [256], [0, 256])

        i = 0
        c1 = 0
        while i < len(histogram) and i < len(histogram1):
            c1 += (histogram[i] - histogram1[i]) ** 2
            i += 1
        c1 = c1 ** (1 / 2)

        i = 0
        c2 = 0
        while i < len(histogram) and i < len(histogram2):
            c2 += (histogram[i] - histogram2[i]) ** 2
            i += 1
        c2 = c2 ** (1 / 2)

        if (x == 0 and y == 0) or (x == 21 and y == 21):
            # print("All clear!")
            maze[x][y] = 0
        elif c1 < c2:
            # print("Looks like a bomb!")
            maze[x][y] = 1
        else:
            # print("All clear!")
            maze[x][y] = 0


def make_step(k):
    for i in range(len(step)):
        for j in range(len(step[i])):
            if step[i][j] == k:
                if i > 0 and step[i - 1][j] == 0 and maze[i - 1][j] == 0:
                    step[i - 1][j] = k + 1
                if j > 0 and step[i][j - 1] == 0 and maze[i][j - 1] == 0:
                    step[i][j - 1] = k + 1
                if i < len(step) - 1 and step[i + 1][j] == 0 and maze[i + 1][j] == 0:
                    step[i + 1][j] = k + 1
                if j < len(step[i]) - 1 and step[i][j + 1] == 0 and maze[i][j + 1] == 0:
                    step[i][j + 1] = k + 1


k = 0
while step[21][21] == 0:
    k += 1
    make_step(k)


def printMatrix(s):
    """Debug Purposes to check that everything is inputted correctly"""
    for i in range(len(s)):
        for j in range(len(s[0])):
            print("%5d " % (s[i][j]), end="")
        print('\n')


# printMatrix(step)

i = 21
j = 21
k = step[i][j]
the_path = ""
while k > 1:
    if i > 0 and step[i - 1][j] == k - 1:
        i, j = i - 1, j
        the_path = 'D' + the_path
        k -= 1
    elif j > 0 and step[i][j - 1] == k - 1:
        i, j = i, j - 1
        the_path = 'R' + the_path
        k -= 1
    elif i < len(step) - 1 and step[i + 1][j] == k - 1:
        i, j = i + 1, j
        the_path = 'U' + the_path
        k -= 1
    elif j < len(step[i]) - 1 and step[i][j + 1] == k - 1:
        i, j = i, j + 1
        the_path = 'L' + the_path
        k -= 1

print(the_path)
