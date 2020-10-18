#Visuliszing A* path finding with pygame
import numpy as np
import pygame

FPS = 30

BLOCKSIZE = 20
WINDOW_HEIGHT = 30  # height in block
WINDOW_WIDTH = 40   #width in block
BORDER = 1

BLACK = (0,0,0) #border color
WHITE = (230, 230, 230) #background color
RED_START = (255, 0, 0)   #start point
RED_END = (200, 20, 20) #end point
BLUE = (0, 191, 255)    #yet to visit node
GREEN = (50, 205, 50)   #path
YELLOW = (240,230,140)  #visited node

NODETYPE_BACKGROUND = 0
NODETYPE_OBSTACLE = 1
NODETYPE_START = 2
NODETYPE_END = 3
NODETYPE_NOTVISITED = 4
NODETYPE_VISITED = 5
NODETYPE_PATH = 6

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
    def __init__(self, rect=None, nodeType=0):
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
    start_value = 0

    for i in range(len(path)):
        result[path[i][0]][path[i][1]] = start_value
        start_value += 1
    return result

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
            if maze[node_position[0]][node_position[1]] != 0:
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

def initWindow():
    global SCREEN, CLOCK
    global startNode_x, startNode_y, endNode_x, endNode_y
    global mouse_x_pre, mouse_y_pre
    startNode_x = 10
    startNode_y = 10
    endNode_x = 20
    endNode_y = 20
    mouse_x_pre = 0
    mouse_y_pre = 0
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH*BLOCKSIZE+200, WINDOW_HEIGHT*BLOCKSIZE+100))
    pygame.display.set_caption('A* Path Finding')
    clock = pygame.time.Clock()
    
    #an array to store rectangle and their color and border property
    global all_rects, bottom_rect, right_rect, button_rect
    all_rects = []
    bottom_rect = pygame.Rect(0, 600, 800, 100)
    right_rect = pygame.Rect(800, 0, 200, 700)


    #create all rectangles
    for x in range(WINDOW_WIDTH):
        column = []
        for y in range(WINDOW_HEIGHT):
            rect = pygame.Rect(x*BLOCKSIZE, y*BLOCKSIZE, BLOCKSIZE, BLOCKSIZE)
            column.append(pygameNode(rect, NODETYPE_BACKGROUND))
        all_rects.append(column)
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
    while True:
        # adjust rect color based on mouse clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                x = mouse_x // BLOCKSIZE
                y = mouse_y // BLOCKSIZE
                #check which rect was clicked and react to the click
                if x < WINDOW_WIDTH and y < WINDOW_HEIGHT:
                    if event.button == 1:
                        mouse_x_pre = x
                        mouse_y_pre = y
                        t = all_rects[x][y].nodeType
                        if  t == NODETYPE_START or t == NODETYPE_END:
                            drawObstacle = False
                            dragNode = True
                        elif t == NODETYPE_OBSTACLE or t == NODETYPE_BACKGROUND:
                            drawObstacle = True
                            dragNode = False
                            if t == NODETYPE_OBSTACLE:
                                all_rects[x][y].setType(NODETYPE_BACKGROUND)
                            elif t == NODETYPE_BACKGROUND:
                                all_rects[x][y].setType(NODETYPE_OBSTACLE)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawObstacle = False
                    dragNode = False

            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                x = mouse_x // BLOCKSIZE
                y = mouse_y // BLOCKSIZE
                if x < WINDOW_WIDTH and y < WINDOW_HEIGHT:
                    if drawObstacle:
                        if not (x == mouse_x_pre and y == mouse_y_pre):
                            if all_rects[x][y].nodeType == 1:
                                all_rects[x][y].setType(0)
                            elif all_rects[x][y].nodeType == 0:
                                all_rects[x][y].setType(1)
                            
                            path = AStarSearch(maze, cost, start, end)
                            
                    elif dragNode and (x < WINDOW_WIDTH and y < WINDOW_HEIGHT):
                        if not (x == mouse_x_pre and y == mouse_y_pre):
                            if all_rects[mouse_x_pre][mouse_y_pre].nodeType == NODETYPE_START:
                                start[0] = x
                                start[1] = y
                            else:
                                end[0] = x
                                end[1] = y
                            all_rects[x][y].setType(all_rects[mouse_x_pre][mouse_y_pre].nodeType)
                            all_rects[mouse_x_pre][mouse_y_pre].setType(NODETYPE_BACKGROUND)
                            
                            path = AStarSearch(maze, cost, start, end)
                    
                    mouse_x_pre = x
                    mouse_y_pre = y


        updateScreen()
        
        clock.tick(FPS)

def updateScreen():
    SCREEN.fill(WHITE)

    pygame.draw.rect(SCREEN, (200,200,200), bottom_rect, 0)
    pygame.draw.rect(SCREEN, (150, 150, 150), right_rect, 0)
    #draw all rectangles(update frame)
    for x in range(WINDOW_WIDTH):
        for y in range(WINDOW_HEIGHT):
            thisnode = all_rects[x][y]
            if thisnode.nodeType == NODETYPE_BACKGROUND:
                pygame.draw.rect(SCREEN, BLACK, thisnode.rect, BORDER)
            elif thisnode.nodeType == NODETYPE_OBSTACLE:
                pygame.draw.rect(SCREEN, BLACK, thisnode.rect, 0)
            elif thisnode.nodeType == NODETYPE_START:
                pygame.draw.rect(SCREEN, RED_START, thisnode.rect, 0)
            elif thisnode.nodeType == NODETYPE_END:
                pygame.draw.rect(SCREEN, RED_END, thisnode.rect, 0)
            elif thisnode.nodeType == NODETYPE_NOTVISITED:
                pygame.draw.rect(SCREEN, BLUE, thisnode.rect, 0)
            elif thisnode.nodeType == NODETYPE_VISITED:
                pygame.draw.rect(SCREEN, YELLOW, thisnode.rect, 0)
            elif thisnode.nodeType == NODETYPE_PATH:
                pygame.draw.rect(SCREEN, GREEN, thisnode.rect, 0)

    pygame.display.update()



if __name__ == '__main__':
    global maze, path
    maze = [[0 for i in range(WINDOW_WIDTH)] for j in range(WINDOW_HEIGHT)]
    global start, end
    start = [5, 5]
    end = [25, 18]
    cost = 1

    global path
    path = AStarSearch(maze, cost, start, end)
    #print(path)
    print('\n'.join([''.join(["{:" ">3d}".format(item) for item in row])
            for row in path]))

    initWindow()
