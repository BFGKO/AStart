import math
import pygame

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


def astar(maze, start, end, screen):

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
        pygame.draw.rect(
            screen,
            (207, 77, 206),
            (current_node.position[0])
        )
        open_list.pop(closestIndex)
        for offset in ((1,0), (0,1), (-1, 0), (0, -1), (-1, -1), (1, 1), (-1, 1), (1, -1)):
            position = current_node.position
            position = (position[0] + offset[0], position[1] + offset[1])
            child = Node(current_node, position)
            if len(maze[0]) > position[0] >= 0 and len(maze[1]) > position[1] >= 0 and not child in open_list and not child in closed_list and maze[position[0]][position[1]] != 1:
                child.g = child.parent.g + 1
                estimatedDistance = int(math.sqrt((child.position[0] - end[0])**2 + (child.position[1] - end[1])**2))
                child.h = estimatedDistance
                child.f = child.g + child.h

                open_list.append(child)
                closed_list.append(child)
        if current_node.position == end_node.position:
            path = []
            current = current_node
            while current.parent:
                path.append(current.position)
                current = current.parent
            print("path found")
            return path




def main():

    maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = (0, 0)
    end = (7, 6)

    path = astar(maze, start, end)
    print(path)


if __name__ == '__main__':
    main()