import sys
 
codes = {
' ': 31, 'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10, 'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15, 'p': 16, 'q': 17, 'r': 18, 's': 19, 't': 20, 'u': 21, 'v': 22, 'w': 23, 'x': 24, 'y': 25, 'z': 26
}
 
class HashTable:
    def __init__(self, name, size=11):
        self.size = size
        self.table = [None] * size
        self.name = name
        self.getPowerOf32()
        self.num_of_taken_positions = 0
        self.removed = ["TOMB", 0]
 
    def getPowerOf32(self):
        self.power_of_32 = [1]
        for i in range(1, 50):
            self.power_of_32.append(self.power_of_32[-1] * 32)
 
    def hash(self, message):
        p = 32
        m = self.size
        hash_value = 0
        for i in range(len(message)):
            if message[i] in codes:
                hash_value += (codes[message[i]]) * self.power_of_32[i]
        return hash_value % m
     
    def getMessage(self, message):
        index = self.hash(message)
        for i in range (self.size):
            if self.table[index] is None:
                return -1, 0
            if self.table[index][0] == message:
                return index, self.table[index][1]
            index = (index + 1) % self.size
        return -1, 0
 
    # [a, b, REMOVED, c, REMOVED, d, REMOVED, REMOVED]
    def insert(self, message):
        potentional_index = None
        index = self.hash(message)
 
        if self.table[index] is None:
            self.table[index] = [message, 1]
            self.num_of_taken_positions += 1
        else:
            while True:
                if self.table[index] is None:
                    if potentional_index is not None:
                        self.table[potentional_index] = [message, 1]
                        self.num_of_taken_positions += 1
                        break
                    else:
                        self.table[index] = [message, 1]
                        self.num_of_taken_positions += 1
                        break
                 
                elif self.table[index] == self.removed:
                    if potentional_index is None:
                        potentional_index = index
 
                elif self.table[index][0] == message:
                    self.table[index][1] += 1
                    break
 
                index = (index + 1) % self.size
 
        if self.num_of_taken_positions/self.size > 0.7:
            self.resizeAndInsert(self.size * 2)
 
    def insertWithoutResizing(self, message):
        index = self.hash(message[0])
        if self.table[index] is None:
            self.table[index] = message
            self.num_of_taken_positions += 1
        else:
            found = False
            while not found:
                if self.table[index] is None:
                    self.table[index] = message
                    self.num_of_taken_positions += 1
                    found = True
                index = (index + 1) % self.size
     
    def resizeAndInsert(self, newSize):
        oldTable = self.table[:]
        self.table = [None] * newSize
        self.size = newSize
        self.num_of_taken_positions = 0
 
        for messages in oldTable:
            if messages not in (None, self.removed):
                self.insertWithoutResizing(messages)
 
    def remove(self, message):
        index = self.hash(message)
        if self.table[index] is None:
            return
        elif self.table[index][0] == message:
            if self.table[index][1] > 1:
                self.table[index][1] -= 1
            else: 
                self.table[index] = self.removed
                self.num_of_taken_positions -= 1
        else:
            while self.table[index] is not None:
                if self.table[index][0] == message:
                    if self.table[index][1] > 1:
                        self.table[index][1] -= 1
                    else: 
                        self.table[index] = self.removed
                        self.num_of_taken_positions -= 1
                index = (index + 1) % self.size
 
        if (self.num_of_taken_positions / self.size) < 0.3 and self.size > 11:
            self.resizeAndInsert(self.size // 2)
 
############################################################################################################
     
tables = [HashTable("Mirek"), HashTable("Jarka"), HashTable("Jindra"), HashTable("Rychlonozka"), HashTable("Cervenacek")]
 
def process_input():
    can_insert = False
    can_delete = False
    member = None
 
    for line in sys.stdin:
        line = line.strip()
 
        if line.startswith("#"):
            command = line[1]
            if command == 'i':
                table_sizes = line.split()[1:]
                for i, size in enumerate(table_sizes):
                    tables[i] = HashTable(tables[i].name, int(size))
 
            elif command == 'a':
                can_delete = False
                can_insert = True
                continue
 
            elif command.isdigit():
                if int(command) > 5:
                    print("Error: Chybny vstup!", file=sys.stderr)
                else:
                    can_insert = False
                    can_delete = False
                    member = int(command) - 1
                    continue
             
            elif command == 'p':
                if member is None:
                    print("Error: Chybny vstup!", file=sys.stderr)
                    continue
                 
                can_insert = False
                can_delete = False
                print(f"{tables[member].name}")
                print(f"\t{tables[member].size} {tables[member].num_of_taken_positions}")
                continue
             
            elif command == 'd' and member is not None:
                can_insert = False
                can_delete = True
                continue
 
        elif can_insert:
            for table in tables:
                table.insert(line)
         
        elif can_delete:
            tables[member].remove(line)
 
        elif member is not None:
            index, count = tables[member].getMessage(line)
            print(f"\t{line} {index} {count}")
            continue
 
if __name__ == "__main__":
    process_input()