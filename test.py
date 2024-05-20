def find_positions():
    
    positions = []

    keyword = ':'

    with open('ascii.txt', 'r') as file:
        content = file.read()

    pos = content.find(keyword)

    while pos != -1:
        positions.append(pos)
        pos = content.find(keyword, pos + 1)

    return positions


positions = find_positions()
print(positions)
