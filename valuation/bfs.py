from collections import deque

from structs import Grid, GridPath


def shortest_path_bfs(blocked: Grid, start: tuple[int, int], goal: tuple[int, int]) -> GridPath:
    sx, sy = start
    gx, gy = goal

    h, w = blocked.shape

    if blocked[sy, sx] or blocked[gy, gx]:
        return []

    prev: dict[tuple[int, int], tuple[int, int] | None] = {start: None}
    q = deque([start])

    while q:
        x, y = q.popleft()

        if (x, y) == goal:
            break

        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if (
                    0 <= nx < w
                    and 0 <= ny < h
                    and not blocked[ny, nx]
                    and (nx, ny) not in prev
            ):
                prev[(nx, ny)] = (x, y)
                q.append((nx, ny))

    if goal not in prev:
        return []

    path: GridPath = []
    cur: tuple[int, int] | None = goal

    while cur is not None:
        path.append(cur)
        cur = prev[cur]

    path.reverse()
    return path
