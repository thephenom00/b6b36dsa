import sys
from typing import List, Optional
from collections import deque
 
class Bod:
    def __init__(self, vyska, radek, sloupec):
        self.vyska = vyska  # Výška bodu
        self.radek = radek  # Souřadnice řádku (x)
        self.sloupec = sloupec  # Souřadnice sloupce (y)
        self.rodic_nahoru = None  # Rodičovský bod pro cestu nahoru
        self.rodic_dolu = None  # Rodičovský bod pro cestu dolů
        self.max_sklon_nahoru = 0  # Úhel pro cestu nahoru
        self.max_sklon_dolu = 0  # Úhel pro cestu dolů
        self.delka_nahoru = 0  # Délka cesty nahoru
        self.delka_dolu = 0  # Délka cesty dolů
 
    def __str__(self):
        return f"Heigth: {self.vyska}, Path: {self.delka_dolu + self.delka_nahoru}, MaxUp: {self.max_sklon_nahoru}, MaxDown: {self.max_sklon_dolu} \n Row: {self.radek}, Column: {self.sloupec} \n ParentUp: {self.rodic_nahoru.vyska} \n "
     
 
class Route():
    def __init__(self, radky, sloupce):
        self.radky = radky  # Anzahl der Reihen
        self.sloupce = sloupce  # Anzahl der Spalten
        self.lanovka = [[None]*sloupce for _ in range(radky)]  # Initialisierung der Matrix für die Seilbahn mit None-Werten
     
    def fillRoute(self, matrix):
        for radek in range(self.radky):
            for sloupec in range(self.sloupce):
                vyska = matrix[radek][sloupec]
                self.lanovka[radek][sloupec] = Bod(vyska, radek, sloupec)
     
    def resetRoute(self):
        for radek in range(self.radky):
            for sloupec in range(self.sloupce):
                bod = self.lanovka[radek][sloupec]
                self.lanovka[radek][sloupec] = Bod(bod.vyska, radek, sloupec)
 
    def processLift(self):
        queue = deque()
        queue.append(self.lanovka[0][0])
        dead_ends = set()
        highest_points = []
 
        while queue:
            current = queue.popleft()
            neigbours = self.steigen(current)
            if neigbours:
                queue.extend(neigbours)
            else:
                dead_ends.add(current)
         
        queue.append(self.lanovka[self.radky - 1][self.sloupce - 1]) # Start from and end and go up
 
        while queue:
            current = queue.popleft()
            neigbours = self.absteigen(current)
            if neigbours:
                queue.extend(neigbours)
            if current in dead_ends:
                highest_points.append(current)
 
        nejvyssiBod = self.najitNejvyssiBod(highest_points)
        self.vypisCestu(nejvyssiBod)
         
    def najitNejvyssiBod(self, nejvyssi_body):
        if len(nejvyssi_body) == 0:
            print("Error: Cesta neexistuje!", file=sys.stderr)
            sys.exit(1)
 
        if len(nejvyssi_body) == 1:
            return nejvyssi_body[0]
 
        nejvyssi_vyska = max(bod.vyska for bod in nejvyssi_body)
        body_s_nejvyssi_vyskou = [bod for bod in nejvyssi_body if bod.vyska == nejvyssi_vyska]
        nejvetsi_radek = max(bod.radek for bod in body_s_nejvyssi_vyskou)
         
        for bod in body_s_nejvyssi_vyskou:
            if bod.radek == nejvetsi_radek:
                return bod
 
     
    def vypisCestu(self, nejvyssiBod):
        path = []
        current = nejvyssiBod
 
        while current != None:
            path.append(current)
            current = current.rodic_nahoru
        path.reverse()
 
        current = nejvyssiBod.rodic_dolu
        while current != None:
            path.append(current)
            current = current.rodic_dolu
 
        final_str = f"{nejvyssiBod.delka_nahoru + nejvyssiBod.delka_dolu + 1}\n"
        for point in path:
            final_str += f"{point.vyska} "
 
        print(final_str.strip())
         
 
    def steigen(self, bod):
        radek = bod.radek
        sloupec = bod.sloupec
        neighbours = deque()
 
        down = self.lanovka[radek + 1][sloupec] if radek + 1 < self.radky else None
        right = self.lanovka[radek][sloupec + 1] if sloupec + 1 < self.sloupce else None
 
        if down != None and self.najdiCestuStoupat(down, bod):
            neighbours.append(down)
        if right != None and self.najdiCestuStoupat(right, bod):
            neighbours.append(right)
         
        return list(neighbours)
     
    def absteigen(self, bod):
        radek = bod.radek
        sloupec = bod.sloupec
        neighbours = deque()
 
        up = self.lanovka[radek - 1][sloupec] if radek - 1 >= 0 else None
        left = self.lanovka[radek][sloupec - 1] if sloupec - 1 >= 0 else None
 
        if up != None and self.najdiCestuKlesat(up, bod):
            neighbours.append(up)
        if left != None and self.najdiCestuKlesat(left, bod):
            neighbours.append(left)
         
        return list(neighbours)
 
    def najdiCestuStoupat(self, bod, predchozi):
        sklon = bod.vyska - predchozi.vyska
 
        if sklon <= 0:
            return False
         
        sklon = max(sklon, predchozi.max_sklon_nahoru)
 
        if bod.max_sklon_nahoru != 0 and bod.max_sklon_nahoru >= sklon:
            return False
         
        bod.max_sklon_nahoru = sklon
        bod.delka_nahoru = predchozi.delka_nahoru + 1
        bod.rodic_nahoru = predchozi
 
        return True
     
    def najdiCestuKlesat(self, bod, predchozi):
        sklon = bod.vyska - predchozi.vyska
 
        if sklon <= 0:
            return False
         
        sklon = max(sklon, predchozi.max_sklon_dolu)
 
        if bod.max_sklon_dolu >= sklon and bod.max_sklon_dolu != 0:
            return False
         
        bod.max_sklon_dolu = sklon
        bod.delka_dolu = predchozi.delka_dolu + 1
        bod.rodic_dolu = predchozi
 
        return True
     
    ################################################################################################################################################################################################################################################
     
    def processPiste(self):
        # breakpoint()
        queue = deque()
        queue.append(self.lanovka[0][0])
        dead_ends = set()
        highest_points = []
 
        while queue:
            current = queue.popleft()
            neigbours = self.ascendingPiste(current)
            if neigbours:
                queue.extend(neigbours)
            else:
                if current not in dead_ends:
                    dead_ends.add(current)
 
        queue.append(self.lanovka[self.radky - 1][self.sloupce - 1]) 
 
        while queue:
            current = queue.popleft()
            neigbours = self.ascendingPiste(current, True)
            if neigbours:
                queue.extend(neigbours)
            else:
                if current in dead_ends and current not in highest_points:
                    highest_points.append(current)
 
        suitable_point = self.findSuitablePoint(highest_points)
 
        self.vypisCestu(suitable_point)
 
    def findSuitablePoint(self, highest_points):
        if not highest_points:
            print("Error: Cesta neexistuje!", file=sys.stderr)
            sys.exit(1)
         
        longest_path = max(bod.delka_dolu + bod.delka_nahoru for bod in highest_points)
        points_with_longest_paths = [bod for bod in highest_points if bod.delka_dolu + bod.delka_nahoru == longest_path]
         
        if len(points_with_longest_paths) == 1:
            return points_with_longest_paths[0]
         
        highest_point_value = max(point.vyska for point in points_with_longest_paths)
        points_with_longest_paths_and_max_height = [point for point in points_with_longest_paths if point.vyska == highest_point_value]
 
        if len(points_with_longest_paths_and_max_height) == 1:
            return points_with_longest_paths_and_max_height[0]
         
        min_slope_value = min(max(point.max_sklon_nahoru, point.max_sklon_dolu) for point in points_with_longest_paths_and_max_height)
        points_with_longest_paths_max_height_and_min_slope = [point for point in points_with_longest_paths_and_max_height if max(point.max_sklon_nahoru, point.max_sklon_dolu) == min_slope_value]
        return points_with_longest_paths_max_height_and_min_slope[0]
 
    def ascendingPiste(self, bod, last = False):
        radek = bod.radek
        sloupec = bod.sloupec
        height = bod.vyska
        neighbours = deque()
     
        up = self.lanovka[radek - 1][sloupec] if radek - 1 >= 0 else None
        left = self.lanovka[radek][sloupec - 1] if sloupec - 1 >= 0 else None
        down = self.lanovka[radek + 1][sloupec] if radek + 1 < self.radky else None
        right = self.lanovka[radek][sloupec + 1] if sloupec + 1 < self.sloupce else None
 
        if last:
            if up != None and self.findPathPiste(up, bod, last):
                neighbours.append(up)
            if left != None and self.findPathPiste(left, bod, last):
                neighbours.append(left)
            if down != None and self.findPathPiste(down, bod, last):
                neighbours.append(down)
            if right != None and self.findPathPiste(right, bod, last):
                neighbours.append(right)
        else: 
            if up != None and self.findPathPiste(up, bod):
                neighbours.append(up)
            if left != None and self.findPathPiste(left, bod):
                neighbours.append(left)
            if down != None and self.findPathPiste(down, bod):
                neighbours.append(down)
            if right != None and self.findPathPiste(right, bod):
                neighbours.append(right)
 
        return list(neighbours)
     
    def findPathPiste(self, current, previous, last = False): # previous = current, current = neighbour
        angle = current.vyska - previous.vyska
 
        if angle > 0:
            if last:
                angle = max(angle, previous.max_sklon_dolu)
                if previous.delka_dolu + 1 > current.delka_dolu:
                    current.delka_dolu = previous.delka_dolu + 1
                    current.max_sklon_dolu = angle
                    current.rodic_dolu = previous
                    return True
                elif previous.delka_dolu + 1 == current.delka_dolu and angle < current.max_sklon_dolu:
                    current.delka_dolu = previous.delka_dolu + 1
                    current.max_sklon_dolu = angle
                    current.rodic_dolu = previous
            else:
                angle = max(angle, previous.max_sklon_nahoru)
                if previous.delka_nahoru + 1 > current.delka_nahoru:
                    current.delka_nahoru = previous.delka_nahoru + 1
                    current.max_sklon_nahoru = angle
                    current.rodic_nahoru = previous
                    return True
                elif previous.delka_nahoru + 1 == current.delka_nahoru and angle < current.max_sklon_nahoru:
                    current.delka_nahoru = previous.delka_nahoru + 1
                    current.max_sklon_nahoru = angle
                    current.rodic_nahoru = previous
        return False
 
if __name__ == "__main__":
    matrix = []
  
    first_row = sys.stdin.readline().strip().split()
    settings = list(map(int, first_row))
  
    if len(settings) != 2:
        print("Error: Chybny vstup!", file=sys.stderr)
        sys.exit(1)
      
    n, m = settings
  
    for i in range(n):
        row = sys.stdin.readline().strip().split()
        if len(row) != m:
            print("Error: Chybny vstup!", file=sys.stderr) 
            sys.exit(1)
        matrix.append(list(map(int, row)))
 
    route = Route(n, m)
    route.fillRoute(matrix)
 
    if len(sys.argv) > 1:
        if sys.argv[1] == "piste":
            route.processPiste()
            route.resetRoute()
        elif sys.argv[1] == "lift":
            route.processLift()
            route.resetRoute()
        else:
            print("Error: Chybny vstup!", file=sys.stderr)
            sys.exit(1)
    else:
        route.processLift()
        route.resetRoute()
        route.processPiste()
        route.resetRoute()