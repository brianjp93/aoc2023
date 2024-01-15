from pathlib import Path
from typing import TypeAlias
from dataclasses import dataclass

Coord: TypeAlias = tuple[int, int]

data = (Path(__file__).parent.parent / "data" / "day23.txt").read_text()

#data = """#.#####################
##.......#########...###
########.#########.#.###
####.....#.>.>.###.#.###
####v#####.#v#.###.#.###
####.>...#.#.#.....#...#
####v###.#.#.#########.#
####...#.#.#.......#...#
######.#.#.#######.#.###
##.....#.#.#.......#...#
##.#####.#.#.#########v#
##.#...#...#...###...>.#
##.#.#v#######v###.###v#
##...#.>.#...>.>.#.###.#
######v#.#.###v#.#.###.#
##.....#...#...#.#.#...#
##.#########.###.#.#.###
##...###...#...#...#.###
####.###.#.###v#####v###
##...#...#.#.>.>.#.>.###
##.###.###.#.###.#.#v###
##.....###...###...#...#
######################.#"""


DIRS = {
    '^': (0, -1),
    '>': (1, 0),
    'v': (0, 1),
    '<': (-1, 0),
}


def get_adj(coord: Coord):
    for adj in DIRS.values():
        yield coord[0] + adj[0], coord[1] + adj[1]


@dataclass
class Edge:
    a: 'Node'
    b: 'Node'
    length: int


@dataclass
class Node:
    edges: list[Edge]
    coord: Coord

    def __hash__(self):
        return hash(self.coord)


@dataclass
class Maze:
    m: list[str]

    @classmethod
    def parse(cls, data):
        return cls(m=data.splitlines())

    def create_nodes(self):
        nodes: dict[Coord, Node] = {}
        visited: set[Coord] = set()
        node = Node(edges=[], coord=(1, 0))
        nodes[node.coord] = node
        queue: list[tuple[Coord, int, Node]] = [((1, 0), 0, node)]
        goal = (len(self.m[0]) - 2, len(self.m) - 1)
        while queue:
            coord, edge_length, node = queue.pop()
            count = 0
            if coord in visited:
                if end_node := nodes.get(coord):
                    edge = Edge(a=node, b=end_node, length=edge_length)
                    node.edges.append(edge)
                    end_node.edges.append(edge)
                continue
            visited.add(coord)
            if coord == goal:
                end_node = nodes.get(goal, Node(edges=[], coord=goal))
                edge = Edge(a=node, b=end_node, length=edge_length)
                node.edges.append(edge)
                end_node.edges.append(edge)
                nodes[end_node.coord] = end_node
                continue
            for adj in get_adj(coord):
                if self[adj] != '#':
                    count += 1
            if count > 2:
                # found a branch
                end_node = nodes.get(coord, Node(edges=[], coord=coord))
                nodes[coord] = end_node
                edge = Edge(a=node, b=end_node, length=edge_length)
                node.edges.append(edge)
                end_node.edges.append(edge)
                for adj in get_adj(coord):
                    if self[adj] != '#':
                        queue.append((adj, 1, end_node))
            else:
                for adj in get_adj(coord):
                    if self[adj] != '#':
                        queue.append((adj, edge_length + 1, node))
        return nodes

    def __getitem__(self, coord: Coord, default="#"):
        if coord[0] < 0 or coord[1] < 0:
            return default
        try:
            return self.m[coord[1]][coord[0]]
        except IndexError:
            return default

    def traverse_nodes(self):
        big = 0
        nodes = self.create_nodes()
        queue: list[tuple[Node, int, set[Coord]]] = []
        queue.append((nodes[(1, 0)], 0, set()))
        goal = (len(self.m[0]) - 2, len(self.m) - 1)
        i = 0
        number_of_solutions = 0
        while queue:
            i += 1
            if i % 100000 == 0:
                print(f"Looking at item {i=}, {len(queue)=}, {big=}, solutions found={number_of_solutions}")
            node, dist, seen = queue.pop()
            if node.coord in seen:
                continue
            seen.add(node.coord)
            if node.coord == goal:
                number_of_solutions += 1
                if dist > big:
                    big = dist
                continue

            for edge in node.edges:
                other = edge.b if edge.a == node else edge.a
                if other.coord not in seen:
                    queue.append((other, dist + edge.length, seen.copy()))
        print(f"Solutions found: {number_of_solutions}")
        return big

    def traverse(self, slippery=True):
        big = 0
        queue: list[tuple[Coord, int, set[Coord]]] = []
        queue.append(((1, 0), 0, set()))
        goal = (len(self.m[0]) - 2, len(self.m) - 1)
        i = 0
        while queue:
            i += 1
            if i % 10000 == 0:
                print(f"Looking at item {i=}, {len(queue)=}")
            coord, dist, seen = queue.pop()
            if coord == goal:
                if dist > big:
                    big = dist
                print(f"Found a solution at {dist=}, {big=}")
                continue

            val = self[coord]
            seen.add(coord)
            if slippery and val in DIRS.keys():
                vec = DIRS[val]
                valid_dirs = [(coord[0] + vec[0], coord[1] + vec[1])]
            else:
                valid_dirs = get_adj(coord)
            for ncoord in valid_dirs:
                if self[ncoord] != '#' and ncoord not in seen:
                    queue.append((ncoord, dist + 1, seen.copy()))
        return big


def part1():
    maze = Maze.parse(data)
    big = maze.traverse()
    return big


def part2():
    maze = Maze.parse(data)
    big = maze.traverse_nodes()
    return big


if __name__ == '__main__':
    print(f"{part1()=}")  # 1.35s
    print(f"{part2()=}")
