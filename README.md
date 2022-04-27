## The Minefield

Challenge Description:
Can you find a safe way in such a short time?
Submit a series of moves that will get you from the top left corner of the minefield to the bottom right corner, without stepping on a mine.

Rules:
You can only move into white (empty) cells. If you step on a mine, you lose. You can't do more than 500 moves.

Solution Format:
The moves should be formatted as a simple string, with no spaces and using ONLY the following capital letters: U (up), D (down), L(left), R(right).

Files:

### Bomb Icon
![img](<https://github.com/rcung000/theminefield/blob/main/Bomb.png>)
### Space Icon
![img](<https://github.com/rcung000/theminefield/blob/main/Space.png>)
### Start Icon
![img](<https://github.com/rcung000/theminefield/blob/main/Start.png>)
### Finish Icon
![img](<https://github.com/rcung000/theminefield/blob/main/Finish.png>)
### Maze Image
![img](<https://github.com/rcung000/theminefield/blob/main/mazeImage.png>)

**Enter the flag that you receive after submitting a valid solution.**

### Approach 1
1. Gain access/read html files of the page. 
2. Find where the minefield is being stored and convert that to a matrix/2d array. 
3. Then solve using a tree-search algorithm.

### Concerns with Approach 1
* Can we guarantee that when "code" pulls the html of the minefield that it is specifically the same board that is being displayed on my end?
* Given the limited time of 7 seconds to find the path, can we download, process, and output the valid string in that time span?

### Approach 2
1. Take a screenshot of the minefield, whether its by manual capture or by image detection.
2. Convert the screenshot to a matrix/2d array.
3. Use a search algorithm to find the path and output the sequence.

### Concerns with Approach 2
* Given the limited time of 7 seconds to find the path, can we process, and output the valid string in that time span?

### Thoughts 1
I spent a fair bit of time thinking about pulling the html file of the page and then having it solved through that. The main concern is whether or not it'll pull the exact same minefield or pull a "refreshed" page. Given the time constraint of 7 seconds to process the data, whether it was through reading the html file or image detection it needed to be fast enough so that I had time to copy and paste the sequence. I ended up using the 2nd approach, mostly because I was familiaried with image detection from various assignments and my time at a hackathon.

### Code Snippet 1
```(python)
screenWidth, screenHeight = pyautogui.size()
print("Width: ", screenWidth, "\nHeight :", screenHeight)

# Calibration Debug
time.sleep(10)
currentMouseX1, currentMouseY1 = pyautogui.position()
print("Current xy position: ", currentMouseX1, ",", currentMouseY1)
time.sleep(10)
currentMouseX2, currentMouseY2 = pyautogui.position()
print("Current xy position: ", currentMouseX2, ",", currentMouseY2)

# Maze Image Capture, specific to 1920 x 1080 screensize, may differ from case to case
time.sleep(3)
mazeImage = pyautogui.screenshot(region=(440, 217, 485, 487))
# Local save file path
mazeImage.save(r'./mazeImage.png')
# 22 wide x 22 high, 484 cells
# start point is always [0][0] end point is always [21][21]
```

Always double checking to make sure the program is reading the correct screensize (1920 x 1080). I also implemented 2(10) second intervals where it'll check the position of your mouse. This was used to find the position of the maze image. It definitely would've been easier to have it detect the maze image itself, which would eliminate the following issues: (varying screensizes, different position than expected). But I was concerned with functionality over practicality at the time. (Definitely going to be an upgrade in the future.)

### Thoughts 2
Once I had gotten it calibrated enough and had it taking accurate screenshots of the maze image, it was time to move onto the next step. Converting the maze image to a matrix/2d array. I need to populate an array with every single cell of the maze image. After that, I can just run some sort of image detection and sort the rest out by assigning bombs with 1s and everything else with 0s. Since we just want to avoid the bombs, everything else is free real estate! Also extracted all of the relevant images from the maze image, regardless of whether or not I was going to use them at the end. (Better to have all of your bases covered!)

### Code Snippet 2
```(python)
# read the image and resize
img = cv2.imread('mazeImage.png')
resized = cv2.resize(img, (484, 484), cv2.INTER_LINEAR)

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
```

So I ran into a big uh-oh here. Why? Well the screenshot had a weird size, and did not play nice when trying to split up the grid into 484 individual cells. Solution? Trim! Truncate! So I resized it to a size of 484x484 so that each cell was give or take 22x22. Some of the cells were 21x21 and others were 22x23. So I went for the middle path and had it resized so that when split up, each cell was 21x21 giving extra allowance. (I'm looking at you grid lines.)

### Thoughts 3
Now comes the "slightly" easier part. Image detection. Colors are made from RGB, the three hues of light (red, green, blue) are mixed together to create different colors. When you look at a color on a screen (let it be a phone screen or computer monitor) there is a bunch of pixels with specific RGB values from 0-255. 0s across the board gives us white, and 255s gives us black. Why is this important? Image detection at its simplest, checks for differences in colors. I immediately thought of using grayscale here and then comparing them to valid examples (the images I extracted earlier) and the more closer it is to the original the more likely it is to be that image.

### Code Snippet 3
```(python)
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
```

Not too much to unpack here. I start by reading the images, and setting up the necessary grayscaled images to compare to the cells that are going into the maze array. Because I only need to find the "bombs" and mark their corresponding position as 1, everything else is considered 0. Because the start and finish icons have color and the space icon doesn't, the start and finish icons are going to be a lot "closer" to a bomb icon than a space icon. So I wrote a special case, since the start and finish icons are at fixed points and are exclusively always going to be on the top left and bottom right.

### Thoughts 4
Now that we have the matrix/2d array sorted out, we need to solve the maze without stepping on a mine and in less than 500 moves. We're going to use a Breadth-First search algorithm here because distance isn't an issue and we're going to find the minimum amount of steps to get to the goal. We're going to write into a matrix filled with 0s our path and then we can backtrack and put our steps into a string to be printed after.

### Code Snippet 4
```(python)
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
```

### Conclusion
It takes the code 4 seconds to process and output the string, leaving us 3 seconds to copy and paste it in.

<details>
    <summary>Spoiler!</summary>
keyring-heremit56
</details>
