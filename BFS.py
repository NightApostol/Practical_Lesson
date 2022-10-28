import pygame as pg
from random import random
from collections import deque


def get_rect(x, y): # создание квадрата
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2


def get_next_nodes(x, y): # проверяем наличие соседа
    check_next_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows and not grid[y][x] else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]
    return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]


cols, rows = 5,5 # определяем кол-во ячеек
TILE = 50 # задаем размер ячейке

pg.init()
sc = pg.display.set_mode([cols * TILE, rows * TILE])
clock = pg.time.Clock()

grid = [[True if random() < 0.2 else False for col in range(cols)] for row in range(rows)] #определяем создание препятствий(стен)
graph = {}

for y, row in enumerate(grid): # проверяем наличие соседей для каждого элемента  и составляем из этого массив
    for x, col in enumerate(row):
        if not col:
            graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)

# начальные переменные для алгоритма
start = (0, 0)
end = (4,4)
next_tile = deque([start])
visited = {start: None}
cur_node = start

max_tile = 0
max_vertex = 0
check_win = 0

while True:
    # зальем весь фон и закрасим наши препятствия 
    sc.fill(pg.Color('black'))
    [[pg.draw.rect(sc, pg.Color('darkorange'), get_rect(x, y), border_radius=TILE // 5) for x, col in enumerate(row) if col] for y, row in enumerate(grid)]
    

    # отобразим работу BFS алгоритма, а точнее раскрасим клетки находящиеся в очереди или уже посещенные алгоритмом
    [pg.draw.rect(sc, pg.Color('forestgreen'), get_rect(x, y)) for x, y in visited]
    [pg.draw.rect(sc, pg.Color('darkslategray'), get_rect(x, y)) for x, y in next_tile]

    # сохраним максимальное количество вершин графа ей пришлось одновременно удерживать в памяти
    if len(next_tile) > max_tile:
        max_tile = len(next_tile)
    
    # сохраним количество вершин графа ей пришлось раскрыть
    if len(visited) > max_vertex:
        max_vertex = len(visited)

    # Логика алгоритма BFS
    if next_tile:
        cur_node = next_tile.popleft()
        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            if next_node not in visited:
                next_tile.append(next_node)
                visited[next_node] = cur_node

    path_head = cur_node

    pg.draw.rect(sc, pg.Color('red'), get_rect(*end), border_radius=TILE // 3)
    pg.draw.rect(sc, pg.Color('blue'), get_rect(*start), border_radius=TILE // 3)
    pg.draw.rect(sc, pg.Color('magenta'), get_rect(*path_head), border_radius=TILE // 3)

    if get_rect(*path_head) == get_rect(*end):
        break

    if check_win == get_rect(*path_head):
        check_win = True
        break
    else:
        check_win = get_rect(*path_head)

    [exit() for event in pg.event.get() if event.type == pg.QUIT]

    pg.display.flip()
    clock.tick(10)

if check_win == True:
    print('\nИгру невозможно пройти!')
else:
    print('\nИгра пройдена, алгоритм - молодец!')
    
print('Максимальное количество вершин графа ей пришлось одновременно удерживать в памяти:' + str(max_tile))
print('Количество вершин графа ей пришлось раскрыть:' + str(max_vertex))
print('Мы ходим туть:', visited.keys())

