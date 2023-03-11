import pygame
import math
pygame.init()
screen = pygame.display.set_mode((800, 800))

def drawRect(x,y,color):
    x, y = x*Size, y*Size
    pygame.draw.rect(
        surface=screen,
        color=color,
        rect=pygame.Rect(x, y, Size, Size)
    )

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

showPathfindinng = True

def astar(maze, start, end):

    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    open_list = [start_node]
    closed_list = []


    while len(open_list) > 0:

        closest = math.inf
        closestIndex = 0
        for index,node in enumerate(open_list):
            if node.f < closest:
                closestIndex = index
                closest = node.f

        current_node = open_list[closestIndex]

        if showPathfindinng:
            drawRect(current_node.position[0], current_node.position[1], (130, 148, 96))
            pygame.display.update()

        open_list.pop(closestIndex)
        for offset in ((1,0), (0,1), (-1, 0), (0, -1)):
            position = current_node.position
            position = (position[0] + offset[0], position[1] + offset[1])
            child = Node(current_node, position)
            if len(maze[0]) > position[0] >= 0 and len(maze[1]) > position[1] >= 0 and not child in open_list and not child in closed_list and maze[position[0]][position[1]] != 1:
                child.g = child.parent.g + 1
                xDistance = end[0] - child.position[0] 
                yDistance = end[1] - child.position[1] 
                estimatedDistance = xDistance**2 + yDistance**2

                child.h = estimatedDistance
                child.f = child.g + child.h

                open_list.append(child)
                closed_list.append(child)
        if current_node == end_node:
            path = []
            current = current_node
            while current.parent:
                path.append(current.position)
                current = current.parent
            print("path found")
            return path


def getMousePos(pos):
    return pos[0] // Size, pos[1] // Size
def getThing(table):
    string = ""
    for i in table:
        string+=str(i)
    return string


COLORS = {
    "WALL": (10, 38, 71),
    "BACKGROUND": (20, 66, 114),
    "LIGHT": (32, 82, 149),
    "ULTRALIGHT": (44, 116, 179),
    "START": (255, 139, 19),
    "END": (255, 0, 50),
    "PATH": (111, 26, 182)
}

gridSize = 100
drawAt = []

start = (-1, -1)
end = (-1, -1)
grid = [[0 for _ in range(gridSize)] for _ in range(gridSize)]
# grid = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
for x in range(len(grid)):
    for y in range(len(grid[x])):
        if grid[x][y] == 1:
            drawAt.append((x, y, COLORS["LIGHT"]))

size = screen.get_size()
Size = size[0] // gridSize
stop = False
lastThing = ""
while not stop:

    events = pygame.event.get()
    mouse = pygame.mouse.get_pressed(5)
    screen.fill(COLORS["BACKGROUND"])
    for pos in drawAt:
        drawRect(pos[0], pos[1], pos[2])
    if start != (-1, -1):
        x, y = start[0] * Size, start[1] * Size
        pygame.draw.rect(
            surface=screen,
            color=COLORS["START"],
            rect=(x, y, Size, Size)
        )
    if end != (-1, -1):
        x, y = end[0] * Size, end[1] * Size
        pygame.draw.rect(
            surface=screen,
            color=COLORS["END"],
            rect=(x, y, Size, Size)
        )

    for x in range(gridSize):
        x = size[0] / gridSize * x
        pygame.draw.line(screen, COLORS["WALL"], (x, 0), (x, size[1]))
        y = x
        pygame.draw.line(screen, COLORS["WALL"], (0, y), (size[0], y))
    for event in events:
        if event.type == pygame.QUIT:
            stop = True
        elif event.type == pygame.KEYDOWN:
            if event.unicode == "c":
                for pos in drawAt:
                    grid[pos[0]][pos[1]] = 0
                drawAt = []
                start = (-1, -1)
                end = (-1, -1)
            elif event.unicode == "s":
                pos = getMousePos(pygame.mouse.get_pos())
                start = pos
                grid[pos[0]][pos[1]] = 2
            elif event.unicode == "e":
                pos = getMousePos(pygame.mouse.get_pos())
                end = pos
                grid[pos[0]][pos[1]] = 3
            elif event.unicode == "p":
                savedList = []
                for drawing in range(len(drawAt) - 1):
                    color = drawAt[drawing][2]
                    if color != COLORS["PATH"]:
                        savedList.append(drawAt[drawing])
                drawAt = savedList

                path = astar(grid, start, end)
                if path:
                    for point in path:
                        x, y = point[0], point[1]
                        drawAt.append((x, y, COLORS["PATH"]))


    if mouse[0]:
        currentPos = pygame.mouse.get_pos()
        x,y = getMousePos(currentPos)
        if grid[x][y] == 0:
            drawAt.append((x, y, COLORS["LIGHT"]))
            grid[x][y] = 1
    elif mouse[2]:
        currentPos = pygame.mouse.get_pos()
        x,y = getMousePos(currentPos)
        grid[x][y] = 0
        for i in range(len(drawAt) - 1):
            pos = drawAt[i]
            if pos[0] == x and pos[1] == y:
                drawAt.pop(i)


    pygame.display.update()