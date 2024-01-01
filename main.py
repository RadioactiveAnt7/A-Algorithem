
import pygame
import math
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (238, 130, 238)
pygame.init()
width = 1200
hight = 900
startNode = None
endNode = None
SCREEN = pygame.display.set_mode((width, hight), pygame.DOUBLEBUF)
DIAGDIST = 2 ** 0.5
visitedNodes = [startNode]
grid = []


class node:
   def __init__(self, pos, h_cost, g_cost, f_cost, Color):
       self.x = pos[0]
       self.y = pos[1]
       self.parent = None
       self.f_cost = f_cost
       self.g_cost = g_cost
       self.h_cost = h_cost
       self.pos = pos
       self.Color = Color

   def __lt__(self, other):
       return self.f_cost < other.f_cost

   def TraceBack(self):
       if self.parent != None:
           self.parent.Color = "BLUE"
           self.parent.TraceBack()

   def minDistance(self, other):
       dx = abs(self.x - other.x)
       dy = abs(self.y - other.y)
       return math.sqrt(dx ** 2 + dy ** 2)

   def calF_cost(self):
       self.f_cost = self.g_cost + self.h_cost

   def expandParent(self, grid, endnode):
       self.Color = "PURPLE"
       visitedNodes.pop(0)
       for i in range(self.x - 1, self.x + 2):
           for j in range(self.y - 1, self.y + 2):
               if (i >= 0 and i < len(grid)) and (j >= 0 and j < len(grid[0])):  #
                   if grid[i][j] != self and grid[i][j].Color == "":
                       grid[i][j].parent = self
                       grid[i][j].g_cost = self.g_cost + grid[i][j].minDistance(self)
                       grid[i][j].h_cost = grid[i][j].minDistance(endnode)
                       grid[i][j].calF_cost()
                       grid[i][j].Color = "GREEN"
                       visitedNodes.append(grid[i][j])
                   elif grid[i][j].Color == "GREEN" and grid[i][j].parent.g_cost > self.g_cost:
                       grid[i][j].parent = self
                       grid[i][j].g_cost = self.g_cost + grid[i][j].minDistance(self)
                       grid[i][j].calF_cost()

       visitedNodes.sort()


def checkIfDone(endNode):
   for i in range(endNode.x - 1, endNode.x + 2):
       for j in range(endNode.y - 1, endNode.y + 2):
           if (i >= 0 and i < len(grid)) and (j >= 0 and j < len(grid[0])):
               if grid[i][j].Color == "PURPLE":
                   return True
   return False


def GenerateGrid():
   for x in range(100):
       grid.append([])
       for y in range(100):
           grid[x].append("")

   for y in range(len(grid[0])):
       for x in range(len(grid)):
           grid[x][y] = node((x, y), 0, 0, 0, "")


def paint():
   for y in range(len(grid[0]) - 1):
       for x in range(len(grid) - 1):
           if grid[x][y].Color == "PURPLE":
               pygame.draw.rect(SCREEN, PURPLE, (grid[x][y].x * 20, grid[x][y].y * 20, 20, 20))
           if grid[x][y].Color == "GREEN":
               pygame.draw.rect(SCREEN, (0, 255, 0), (grid[x][y].x * 20, grid[x][y].y * 20, 20, 20))
           if grid[x][y].Color == "RED":
               pygame.draw.rect(SCREEN, (255, 0, 0), (grid[x][y].x * 20, grid[x][y].y * 20, 20, 20))
           if grid[x][y].Color == "BLUE":
               pygame.draw.rect(SCREEN, (0, 0, 255), (grid[x][y].x * 20, grid[x][y].y * 20, 20, 20))
           if grid[x][y].Color == "BLACK":
               pygame.draw.rect(SCREEN, (0, 0, 0), (grid[x][y].x * 20, grid[x][y].y * 20, 20, 20))
           if grid[x][y].Color == "CYAN":
               pygame.draw.rect(SCREEN, (0, 100, 100), (grid[x][y].x * 20, grid[x][y].y * 20, 20, 20))


def find_pos():
   mouseX_pos, mouseY_pos = pygame.mouse.get_pos()
   temp = mouseX_pos % 20
   mouseX_pos -= temp
   temp = mouseY_pos % 20
   mouseY_pos -= temp
   return grid[mouseX_pos // 20][mouseY_pos // 20]


def draw_grid():
   for i in range(1, width // 20):
       pygame.draw.rect(SCREEN, BLACK, (i * 20, 0, 1, hight))
   for i in range(1, hight // 20):
       pygame.draw.rect(SCREEN, BLACK, (1, i * 20, width, 1))


def main():
   running = False
   quit_ = False
   GenerateGrid()

   while not running and not quit_:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               quit_ = True
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_RETURN:
                   running = True
               if event.key == pygame.K_ESCAPE:
                   quit_ = True

       pygame.display.update()

   go = False
   done_start = False
   done_end = False
   draw = False

   while running and not quit_ and not go:
       SCREEN.fill(WHITE)
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               quit_ = True
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_RETURN:
                   go = True
           if event.type == pygame.MOUSEBUTTONDOWN and not go:
               if event.button == 3 and not done_start:
                   startNode = find_pos()
                   startNode.Color = "BLUE"
                   done_start = True
               elif event.button == 3 and done_start and not done_end:
                   endNode = find_pos()
                   endNode.Color = "RED"
                   done_end = True
               else:
                   draw = True

           elif event.type == pygame.MOUSEBUTTONUP:
               draw = False
       if draw and done_start and done_end:
           if find_pos().Color == "":
               find_pos().Color = "BLACK"

       paint()
       draw_grid()
       pygame.display.update()

   done = False

   startNode.expandParent(grid, endNode)
   while running and not quit_ and go:
       SCREEN.fill(WHITE)
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               quit_ = True

       if not done:
           lowestFCostNode = visitedNodes[0]

           lowestFCostNode.expandParent(grid, endNode)
           done = checkIfDone(endNode)

       if done:
           lowestFCostNode.TraceBack()
           pass

       paint()
       draw_grid()
       pygame.display.update()


if __name__ == '__main__':
   main()




