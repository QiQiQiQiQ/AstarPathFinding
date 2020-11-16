# Visuliszing A* path finding with pygame
import numpy as np
import pygame
import sys
import time
#from pygame.locals import *

FPS = 30

BLOCKSIZE = 20
WINDOW_HEIGHT = 30  # number of blocks in a column
WINDOW_WIDTH = 40  # number of blocks in a row
BORDER = 1

BLACK = (0, 0, 0)  # border color
WHITE = (230, 230, 230)  # background color
YELLOW_START = (255, 255, 0)  # start point
YELLOW_END = (255, 128, 0)  # end point
BLUE = (0, 0, 255)  # yet to visit node
GREEN = (50, 205, 50)  # path
YELLOW = (255, 255, 0)  # visited node
RED = (255, 0, 0)

NODETYPE_BACKGROUND = 0
NODETYPE_OBSTACLE = 1
NODETYPE_START = 2
NODETYPE_END = 3
NODETYPE_NOTVISITED = 4
NODETYPE_VISITED = 5
NODETYPE_PATH = 6


# an array to store rectangle and their color and border property
all_rects = []

#initialize algorithm related variables
maze = [[0 for i in range(WINDOW_WIDTH)] for j in range(WINDOW_HEIGHT)] # the maze matrix, 0 for allowed path, -1 for obstacle
start = [3, 1]  #initial start point
end = [25, 18]  #end start point
cost = 1    #cost for every move

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

class pygameNode:
    def __init__(self, rect=None, nodeType=NODETYPE_BACKGROUND):
        self.rect = rect
        self.nodeType = nodeType    # 0 = background, 1 = obstacle, 2 = startnode, 3 = endnode

    def setType(self, nodeType):
        self.nodeType = nodeType

def return_path(current_node):
    path = []
    no_rows, no_columns = np.shape(maze)

    result = [[-1 for i in range(no_columns)] for j in range(no_rows)]
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent

    path = path[::-1]
    # set pygame rectangles on the path according to the path
    #start_value = 0
    '''
    for i in range(len(path)):
        result[path[i][0]][path[i][1]] = start_value
        start_value += 1
    return result
    '''
    return path

def AStarSearch(maze, cost, start, end):
    start_node = Node(None, tuple(start))
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, tuple(end))
    end_node.g = end_node.h = end_node.f = 0

    yet_to_visit_list = []

    visited_list = []

    yet_to_visit_list.append(start_node)

    outer_iterations = 0
    max_iterations = (len(maze) // 2) ** 10
    move = [[-1, 0],
            [0, -1],
            [1, 0],
            [0, 1]]

    no_rows, no_columns = np.shape(maze)

    while len(yet_to_visit_list) > 0:
        outer_iterations += 1

        current_node = yet_to_visit_list[0]
        current_index = 0
        for index, item in enumerate(yet_to_visit_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        if outer_iterations > max_iterations:
            print("giving up on pathfinding, too many iterations")
            return return_path(current_node)

        yet_to_visit_list.pop(current_index)
        visited_list.append(current_node)
        if not(current_node == start_node or current_node == end_node):
            all_rects[current_node.position[0]
                      ][current_node.position[1]].setType(NODETYPE_VISITED)
            updateScreen(0.03)

        if current_node == end_node:
            return return_path(current_node)

        children = []

        for new_position in move:

            node_position = (current_node.position[0] + new_position[0],
                             current_node.position[1] + new_position[1])
            if(node_position[0] > (no_rows - 1) or
                    node_position[0] < 0 or
                    node_position[1] > (no_columns - 1) or
                    node_position[1] < 0):
                continue
            #if maze[node_position[0]][node_position[1]] == -1:
            if all_rects[node_position[0]][node_position[1]].nodeType == NODETYPE_OBSTACLE:
                continue
            new_node = Node(current_node, node_position)

            children.append(new_node)

        for child in children:
            if len([visited_child for visited_child in visited_list if visited_child == child]) > 0:
                continue

            child.g = current_node.g + cost

            child.h = ((child.position[0] - end_node.position[0]) ** 2 +
                       (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            if len([i for i in yet_to_visit_list if child == i and child.f > i.f]) > 0:
                continue
            yet_to_visit_list.append(child)
            if (child != start_node and child != end_node):
                all_rects[child.position[0]][child.position[1]
                                             ].setType(NODETYPE_NOTVISITED)
                updateScreen(0.04)

def initWindow():
    pygame.init()

    # pygame window and clock
    global SCREEN, CLOCK
    #
    #global startNode_x, startNode_y, endNode_x, endNode_y
    # two variable to help tracking mousemotion
    global mouse_x_pre, mouse_y_pre
    # additional surfaces in the pygame window
    global bottom_rect, right_rect, button_rect, start_button, clear_button

    SCREEN = pygame.display.set_mode(
        (WINDOW_WIDTH*BLOCKSIZE+200, WINDOW_HEIGHT*BLOCKSIZE+100))
    pygame.display.set_caption('A* Path Finding')
    clock = pygame.time.Clock()

    mouse_x_pre = 0
    mouse_y_pre = 0

    bottom_rect = pygame.Rect(0, 600, 800, 100)
    right_rect = pygame.Rect(800, 0, 200, 700)
    start_button = pygame.Rect(800+BLOCKSIZE, 0 + 2*BLOCKSIZE, 100, 50)
    clear_button = pygame.Rect(800+BLOCKSIZE, 80 + 2*BLOCKSIZE, 100, 50)

    # label for the rectangles
    global font, label_start_button, label_clear_button
    font = pygame.font.SysFont('Arial', 26)
    label_start_button = font.render("Start", True, (0, 0, 0))
    label_clear_button = font.render("Clear", True, (0, 0, 0))
    # create all rectangles
    for x in range(WINDOW_HEIGHT):
        row = []
        for y in range(WINDOW_WIDTH):
            rect = pygame.Rect(y*BLOCKSIZE, x*BLOCKSIZE, BLOCKSIZE, BLOCKSIZE)
            row.append(pygameNode(rect, NODETYPE_BACKGROUND))
        all_rects.append(row)
    # set initial position of start and end point
    x, y = start
    all_rects[x][y].setType(NODETYPE_START)
    x, y = end
    all_rects[x][y].setType(NODETYPE_END)

    # pygame start
    drawObstacle = False
    dragNode = False
    node_x_temp = 0  # x position of the node before drag
    node_y_temp = 0  # y position of the node before drag
    finding = False
    while True:
        # adjust rect color based on mouse clicks
        for event in pygame.event.get():
            # common part of a pygame program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.quit()

            # mouse clicked
            elif event.type == pygame.MOUSEBUTTONDOWN and not finding:
                mouse_y, mouse_x = event.pos
                x = mouse_x // BLOCKSIZE
                y = mouse_y // BLOCKSIZE
                # check which rect was clicked and react to the click
                # start button clicked, start finding
                if start_button.collidepoint(mouse_y, mouse_x) and event.button == 1:
                    print("start path finding")
                    finding = True
                    resetMaze(1)
                    initMaze()
                    updateScreen(0)
                    path = AStarSearch(maze, cost, start, end)
                    drawPath(path)
                    print('\n'.join(
                        [''.join(["{:" ">3d}".format(item) for item in row]) for row in path]))
                    finding = False
                elif clear_button.collidepoint(mouse_y, mouse_x) and event.button == 1:
                    resetMaze(0)
                # mouse clicked inside the board
                elif y < WINDOW_WIDTH and x < WINDOW_HEIGHT:
                    if event.button == 1:
                        mouse_x_pre = x
                        mouse_y_pre = y
                        t = all_rects[x][y].nodeType
                        if t == NODETYPE_START or t == NODETYPE_END:
                            drawObstacle = False
                            dragNode = True
                        elif t == NODETYPE_OBSTACLE or t == NODETYPE_BACKGROUND:
                            drawObstacle = True
                            dragNode = False
                            if t == NODETYPE_OBSTACLE:
                                all_rects[x][y].setType(NODETYPE_BACKGROUND)
                            elif t == NODETYPE_BACKGROUND:
                                all_rects[x][y].setType(NODETYPE_OBSTACLE)

            elif event.type == pygame.MOUSEBUTTONUP and not finding:
                if event.button == 1:
                    drawObstacle = False
                    dragNode = False

            elif event.type == pygame.MOUSEMOTION and not finding:
                mouse_y, mouse_x = event.pos
                x = mouse_x // BLOCKSIZE
                y = mouse_y // BLOCKSIZE
                if y < WINDOW_WIDTH and x < WINDOW_HEIGHT:
                    if drawObstacle:
                        if not (x == mouse_x_pre and y == mouse_y_pre):
                            if all_rects[x][y].nodeType == NODETYPE_BACKGROUND:
                                all_rects[x][y].setType(NODETYPE_OBSTACLE)
                            elif all_rects[x][y].nodeType == NODETYPE_OBSTACLE:
                                all_rects[x][y].setType(NODETYPE_BACKGROUND)

                    elif dragNode and (y < WINDOW_WIDTH and x < WINDOW_HEIGHT):
                        if not (x == mouse_x_pre and y == mouse_y_pre):
                            if all_rects[mouse_x_pre][mouse_y_pre].nodeType == NODETYPE_START:
                                start[0] = x
                                start[1] = y
                            else:
                                end[0] = x
                                end[1] = y
                            all_rects[x][y].setType(
                                all_rects[mouse_x_pre][mouse_y_pre].nodeType)
                            all_rects[mouse_x_pre][mouse_y_pre].setType(
                                NODETYPE_BACKGROUND)

                    mouse_x_pre = x
                    mouse_y_pre = y

        updateScreen(0)
        clock.tick(FPS)

def updateScreen(delay):
    SCREEN.fill(WHITE)

    # draw window elements
    # the area below board, displaying information about the game
    pygame.draw.rect(SCREEN, (200, 200, 200), bottom_rect, 0)
    # the area on the right with the start button inside it
    pygame.draw.rect(SCREEN, (150, 150, 150), right_rect, 0)
    # the button to start the path finding and the text in the button
    pygame.draw.rect(SCREEN, (180, 180, 180), start_button, 0)
    SCREEN.blit(label_start_button, (800+2.3*BLOCKSIZE, 0 + 2.5*BLOCKSIZE))
    pygame.draw.rect(SCREEN, (180, 180, 180), clear_button, 0)
    SCREEN.blit(label_clear_button, (800+2.3*BLOCKSIZE, 80 + 2.5*BLOCKSIZE))

    # draw all rectangles(update frame)
    for y in range(WINDOW_WIDTH):
        for x in range(WINDOW_HEIGHT):
            thisnode = all_rects[x][y]
            if thisnode.nodeType == NODETYPE_BACKGROUND:
                pygame.draw.rect(SCREEN, BLACK, thisnode.rect, BORDER)
            elif thisnode.nodeType == NODETYPE_OBSTACLE:
                pygame.draw.rect(SCREEN, BLACK, thisnode.rect, 0)
            elif thisnode.nodeType == NODETYPE_START:
                pygame.draw.rect(SCREEN, YELLOW_START, thisnode.rect, 0)
            elif thisnode.nodeType == NODETYPE_END:
                pygame.draw.rect(SCREEN, YELLOW_END, thisnode.rect, 0)
            elif thisnode.nodeType == NODETYPE_NOTVISITED:
                pygame.draw.rect(SCREEN, RED, thisnode.rect, 0)
            elif thisnode.nodeType == NODETYPE_VISITED:
                pygame.draw.rect(SCREEN, BLUE, thisnode.rect, 0)
            elif thisnode.nodeType == NODETYPE_PATH:
                pygame.draw.rect(SCREEN, GREEN, thisnode.rect, 0)

    pygame.display.update()
    if delay > 0:
        time.sleep(delay)

def initMaze():
    maze = [[0 for j in range(WINDOW_WIDTH)] for i in range(WINDOW_HEIGHT)]
    #maze = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH))
    for x in range(WINDOW_HEIGHT):
        for y in range(WINDOW_WIDTH):
            if all_rects[x][y].nodeType == NODETYPE_OBSTACLE:
                maze[x][y] = -1
            elif all_rects[x][y].nodeType == NODETYPE_START:
                start[0] = x
                start[1] = y
            elif all_rects[x][y].nodeType == NODETYPE_END:
                end[0] = x
                end[1] = y
    print('\n'.join([''.join(["{:" ">3d}".format(item) for item in row]) for row in maze]))

def resetMaze(flag):
    if flag == 0:   #reset to initial state, remove all nodes except for start and end node
        for y in range(WINDOW_WIDTH):
            for x in range(WINDOW_HEIGHT):
                if not ( (x==start[0] and y == start[1]) or ((x==end[0] and y == end[1])) ):
                    all_rects[x][y].setType(NODETYPE_BACKGROUND)
    elif flag == 1: #remove all path finding related nodes
        for y in range(WINDOW_WIDTH):
            for x in range(WINDOW_HEIGHT):
                if not ( (x==start[0] and y == start[1]) or ((x==end[0] and y == end[1])) or all_rects[x][y].nodeType == NODETYPE_OBSTACLE ):
                    all_rects[x][y].setType(NODETYPE_BACKGROUND)

def drawPath(path):
    for i in range(len(path)):
        x = path[i][0]
        y = path[i][1]
        if [x,y]==start or [x,y]==end:
            continue
        all_rects[x][y].setType(NODETYPE_PATH)
        updateScreen(0.1)

def logMsg():
    print('Start: '+start)
    print('End: '+end)

if __name__ == '__main__':
    initWindow()

    #global path
    #path = AStarSearch(maze, cost, start, end)
    #print('\n'.join([''.join(["{:" ">3d}".format(item) for item in row]) for row in path]))
    # print(path)
