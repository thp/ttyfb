# entirely cribbed from https://blog.bruce-hill.com/meandering-triangles

import collections
from itertools import product, tee, chain
import math
from time import time

from kinemacolor import Kinemacolor

demo = Kinemacolor()


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def elevation_function(x, y):
    t = time()

    cx = x + 0.5 * math.sin(t/5)
    cy = y + 0.5 * math.cos(t/3)
    v = math.sin(math.sqrt(100 * (cx**2 + cy**2) + 1) + t)

    cx = x + 0.5 * math.sin(t/2)
    cy = y + 0.5 * math.cos(t/7)
    v += math.sin(math.sqrt(100 * (cx**2 + cy**2) + 1) + t)

    return v


def find_contours(xmin, xmax, ymin, ymax, spacing=1, elevation=0.5):
    elevation_data = {
        (x, y): elevation_function(x/demo.w, y/demo.h)
        for x, y in product(
            range(xmin, xmax+spacing, spacing),
            range(ymin, ymax+spacing, spacing)
        )
    }

    triangles = chain(*zip(
        (((x, y), (x+spacing, y), (x, y+spacing))
            for x, y in product(
                range(xmin, xmax, spacing),
                range(ymin, ymax, spacing)
        )),
        (((x+spacing, y), (x, y+spacing), (x+spacing, y+spacing))
            for x, y in product(
                range(xmin, xmax, spacing),
                range(ymin, ymax, spacing)
        ))
    ))

    contour_segments = []
    for triangle in triangles:
        below = [v for v in triangle if elevation_data[v] < elevation]
        above = [v for v in triangle if elevation_data[v] >= elevation]
        # All above or all below means no contour line here
        if len(below) == 0 or len(above) == 0:
            continue
        # We have a contour line, let's find it
        minority = above if len(above) < len(below) else below
        majority = above if len(above) > len(below) else below

        contour_points = []
        crossed_edges = ((minority[0], majority[0]), (minority[0], majority[1]))
        for e1, e2 in crossed_edges:
            how_far = ((elevation - elevation_data[e2])
                       / (elevation_data[e1] - elevation_data[e2]))
            crossing_point = (
                how_far * e1[0] + (1-how_far) * e2[0],
                how_far * e1[1] + (1-how_far) * e2[1])
            contour_points.append(crossing_point)
        contour_segments.append((contour_points[0], contour_points[1]))

    unused_segments = set(contour_segments)
    segments_by_point = collections.defaultdict(set)
    for e1, e2 in contour_segments:
        segments_by_point[e1].add((e1, e2))
        segments_by_point[e2].add((e1, e2))

    contour_lines = []
    while unused_segments:
        # Start with a random segment
        line = collections.deque(unused_segments.pop())
        while True:
            tail_candidates = segments_by_point[line[-1]].intersection(unused_segments)
            if tail_candidates:
                tail = tail_candidates.pop()
                e1, e2 = tail
                line.append(e1 if e2 == line[-1] else e2)
                unused_segments.remove(tail)
            head_candidates = segments_by_point[line[0]].intersection(unused_segments)
            if head_candidates:
                head = head_candidates.pop()
                e1, e2 = head
                line.appendleft(e1 if e2 == line[0] else e2)
                unused_segments.remove(head)
            if not tail_candidates and not head_candidates:
                contour_lines.append(list(line))
                break

    return contour_lines


if __name__ == "__main__":
    while True:
        demo.clear()

        for el in [0.2, 0.5, 0.8]:
            lines = find_contours(0, demo.w-1, 0, demo.h-1, spacing=5, elevation=el)
            for segment in lines:
                for (x1, y1), (x2, y2) in pairwise(segment):
                    demo.line(x1, y1, x2, y2)

        demo.render()
