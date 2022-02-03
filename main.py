import os
from re import A
import sys

os.chdir(sys.path[0])
sys.path.insert(1, "P://Python Projects/assets/")

from GUI import *


class Image:
	def __init__(self, size, rect):
		self.size = size
		self.rect = pg.Rect(rect)

		self.CreateGrid(100)

	def GetPosFromIndex(self, i, j):
		return self.rect.x + (i * self.size), self.rect.y + (j * self.size)

	def GetState(self, a, b, c, d):
		return (a * 8) + (b * 4) + (c * 2) + (d * 1)

	def CreateGrid(self, m=1):
		m = max(1, m)
		interpolate = m != 1

		self.grid = [[randint(0, m) / m for x in range(self.rect.w // self.size)] for y in range(self.rect.h // self.size)]

		self.lines = []

		threshold = 0.5

		for j in range(len(self.grid) - 1):
			for i in range(len(self.grid) - 1):
				x, y = self.GetPosFromIndex(i, j)

				c1 = self.grid[j][i] < threshold
				c2 = self.grid[j][i + 1] < threshold
				c3 = self.grid[j + 1][i + 1] < threshold
				c4 = self.grid[j + 1][i] < threshold

				state = self.GetState(int(c1), int(c2), int(c3), int(c4))
				
				aVal = self.grid[j][i]
				bVal = self.grid[j][i + 1]
				cVal = self.grid[j + 1][i + 1]
				dVal = self.grid[j + 1][i]

				if interpolate:
					a = Vec2(Lerp(x, x + self.size, (1 - aVal) / max((bVal - aVal), 1)), y)
					b = Vec2(x + self.size, Lerp(y, y + self.size, (1 - bVal) / max((cVal - bVal), 1)))
					c = Vec2(Lerp(x, x + self.size, (1 - dVal) / max((cVal - dVal), 1)), y + self.size)
					d = Vec2(x, Lerp(y, y + self.size, (1 - aVal) / max((dVal - aVal), 1)))
				else:
					a = Vec2(x + self.size // 2, y)
					b = Vec2(x + self.size, y + self.size // 2)
					c = Vec2(x + self.size // 2, y + self.size)
					d = Vec2(x, y + self.size // 2)

				aa = True

				match int(state):
						case 1:
							self.lines.append(Line((c.x, c.y), (d.x, d.y), white, 0, 0, aa))
						case 2:
							self.lines.append(Line((b.x, b.y), (c.x, c.y), white, 0, 0, aa))
						case 3:
							self.lines.append(Line((b.x, b.y), (d.x, d.y), white, 0, 0, aa))
						case 4:
							self.lines.append(Line((a.x, a.y), (b.x, b.y), white, 0, 0, aa))
						case 5:
							self.lines.append(Line((a.x, a.y), (d.x, d.y), white, 0, 0, aa))
							self.lines.append(Line((b.x, b.y), (c.x, c.y), white, 0, 0, aa))
						case 6:
							self.lines.append(Line((a.x, a.y), (c.x, c.y), white, 0, 0, aa))
						case 7:
							self.lines.append(Line((a.x, a.y), (d.x, d.y), white, 0, 0, aa))
						case 8:
							self.lines.append(Line((a.x, a.y), (d.x, d.y), white, 0, 0, aa))
						case 9:
							self.lines.append(Line((a.x, a.y), (c.x, c.y), white, 0, 0, aa))
						case 10:
							self.lines.append(Line((a.x, a.y), (b.x, b.y), white, 0, 0, aa))
							self.lines.append(Line((c.x, c.y), (d.x, d.y), white, 0, 0, aa))
						case 11:
							self.lines.append(Line((a.x, a.y), (b.x, b.y), white, 0, 0, aa))
						case 12:
							self.lines.append(Line((b.x, b.y), (d.x, d.y), white, 0, 0, aa))
						case 13:
							self.lines.append(Line((b.x, b.y), (c.x, c.y), white, 0, 0, aa))
						case 14:
							self.lines.append(Line((c.x, c.y), (d.x, d.y), white, 0, 0, aa))			

	def Draw(self, r):
		DrawRectOutline(white, (self.rect.x, self.rect.y, self.rect.w - (self.rect.w % self.size) - self.size + 1, self.rect.h - (self.rect.h % self.size) - self.size + 1))
		
		for j, row in enumerate(self.grid):
			for i, value in enumerate(row):
				pg.draw.circle(screen, ((1 - value) * 255, (1 - value) * 255, (1 - value) * 255), self.GetPosFromIndex(i, j), r)

		for line in self.lines:
			line.Draw()



cellSize = 40
gridSize = height - 50

i = Image(cellSize, ((width // 2) - (gridSize // 2), (height // 2) - (gridSize // 2) + cellSize, gridSize, gridSize))


def DrawLoop():
	screen.fill(darkGray)

	DrawAllGUIObjects()
 
	i.Draw(0)

	pg.display.update()


def HandleEvents(event):
	HandleGui(event)


def Update():
	pass


while running:
	clock.tick_busy_loop(fps)
	deltaTime = clock.get_time()
	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				running = False

		HandleEvents(event)

	Update()

	DrawLoop()
