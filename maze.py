import sys
 
 
maze = []
 
if (__name__ == "__main__"):
    for row in sys.stdin:
        maze.append(row.strip())
              
def checkIfMazeIsValid(rows):
      if not checkRectangle(rows):
        sys.stderr.write("Error: Bludiste neni obdelnikove!\n")
        sys.exit(1)
      elif not checkEnterInLeftUpper(rows):
        sys.stderr.write("Error: Vstup neni vlevo nahore!\n")
        sys.exit(1)
      elif not checkExitInRightLower(rows):
        sys.stderr.write("Error: Vystup neni vpravo dole!\n")
        sys.exit(1)
      elif not checkWidth(rows):
        sys.stderr.write("Error: Sirka bludiste je mimo rozsah!\n")
        sys.exit(1)
      elif not checkLength(rows):
        sys.stderr.write("Error: Delka bludiste je mimo rozsah!\n")
        sys.exit(1)
      elif not checkUnknownChars(rows):
        sys.stderr.write("Error: Bludiste obsahuje nezname znaky!\n")
        sys.exit(1)
      elif not checkFence(rows):
         sys.stderr.write("Error: Bludiste neni oplocene!\n")
         sys.exit(1)
 
def checkRectangle(rows):
      for i in range(len(rows) - 1):
         if len(rows[i]) != len(rows[i+1]):
            return False
      return True
          
def checkEnterInLeftUpper(rows):
      if rows[0][1] != ".":
        return False
      return True
 
def checkExitInRightLower(rows):
      lastRow = rows[len(rows) - 1]
      if lastRow[len(lastRow) - 2] != ".":
        return False
      return True
 
def checkWidth(rows):
      for row in rows:
         stripped = row
         if len(stripped) - 1 < 5 or len(stripped) - 1 > 100:
            return False
      return True
 
def checkLength(rows):
       if len(rows) < 5 or len(rows) > 100:
          return False
       return True
 
def checkUnknownChars(rows):
       for line in rows:
          for char in line:
             if char != '.' and char != '#':
                return False
       return True
 
def checkFence(rows):
       for row_num in range(len(rows)):
          if row_num == 0:
             for char_index in range(len(rows[row_num])):
                if char_index != 1:
                   if rows[row_num][char_index].strip() != "#":
                      return False
          elif row_num == len(rows) - 1:
             for char_index in range(len(rows[row_num])):
                if char_index != len(rows[row_num]) - 2:
                   if rows[row_num][char_index].strip() != "#":
                      return False
          else:
             if rows[row_num][0] != "#" or rows[row_num][len(rows[row_num]) - 1] != "#":
                return False
              
       return True
 
checkIfMazeIsValid(maze)
 
start = [0,1]
end = [len(maze) - 1, len(maze[0]) - 2]
 
def getPath(maze, start, end, visited):
     
    path = [[start]]
 
    while path != []:
        currentPath = path.pop(0)
        lastPosition = currentPath[-1] # THE LAST ONE
 
        y = lastPosition[0]
        x = lastPosition[1]
 
        if (lastPosition == end):
            return currentPath
 
        for move in [[y, x-1], [y, x+1], [y-1, x], [y+1, x]]: # L, R, U, D
            possibleY = move[0]
            possibleX = move[1]
 
            if (possibleX < 0 or possibleX >= len(maze[0]) or possibleY < 0 or possibleY >= len(maze)):
                continue
            elif (maze[possibleY][possibleX] == "#"):
                continue
            elif [possibleY, possibleX] in visited:
                continue
 
            path.append(currentPath + [move])
            visited += [move]
 
    return None
 
path = getPath(maze, start, end, [start])
if path == None:
    sys.stderr.write("Error: Cesta neexistuje!\n")
    sys.exit(1)
 
obligatoryPath = path[:]
 
for coordinate in path:
    if (getPath(maze, start, end, [start, coordinate]) == None or coordinate == start):
        continue
    else:
        obligatoryPath.remove(coordinate)
 
 
for coordinate in obligatoryPath:
    y = coordinate[0]
    x = coordinate[1]
    maze[coordinate[0]] = maze[coordinate[0]][:x] + "!" + maze[coordinate[0]][x+1:]
 
for row in maze:
    print(row)