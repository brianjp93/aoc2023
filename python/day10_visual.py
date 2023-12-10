from day10 import Maze, data

from rich.console import Console
from rich.text import Text

PRETTY = {
    "L": "┕",
    "7": "┓",
    "J": "┙",
    "F": "┍",
    "-": "━",
    "|": "│",
}

def draw(maze: Maze):
    loop = maze.find_loop().keys()
    inner = maze.find_inner()
    rows = Text()
    for y in range(*maze.y_range):
        row = Text()
        for x in range(*maze.x_range):
            coord = (x, y)
            if coord in inner:
                row.append(Text('○', style="yellow3"))
            elif coord in loop:
                text = Text(PRETTY[maze.map[coord]], style="deep_sky_blue4")
                row.append(text)
            else:
                row.append('▫')
        row.append("\n")
        rows.append(row)
    console = Console()
    console.print(rows)

if __name__ == '__main__':
    maze = Maze(data)
    draw(maze)
