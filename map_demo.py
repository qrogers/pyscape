map = [[0,0],[5,5],[6,7],[7,2]]
links = [(0,1),(2,3)]

#o--\..
#....o.
#.o-/..
#......

draw = []

for x in range(10):
    draw.append([])
    for y in range(10):
        draw[x].append(".")

for point in map:
    draw[point[1]][point[0]] = "o"

for link in links:
    start = map[link[0]]
    end   = map[link[1]]
    for x in range(10):
        if start[0] > end[0]:
            start[0] -= 1
            if start[1] == end[1]:
                char = "-"
            else:
                char = "/"
            draw[start[1]][start[0]] = char
        elif start[0] < end[0]:
            start[0] += 1
            draw[start[1]][start[0]] = "-"
        if start[1] > end[1]:
            start[1] -= 1
            if start[0] == end[0]:
                char = "|"
            else:
                char = "/"
            draw[start[1]][start[0]] = char
        elif start[1] < end[1]:
            start[1] += 1
            if start[1] == end[1]:
                char = "|"
            else:
                char = '>'
            draw[start[1]][start[0]] = char

for point in map:
    draw[point[1]][point[0]] = "o"

for line in draw:
    print line