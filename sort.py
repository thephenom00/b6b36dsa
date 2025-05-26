import sys
 
sequence = []
 
maxValue = None
type = None #Hodnota 1 odpovídá vzestupně a hodnota 2 sestupně seřazené posloupnosti. Pokud posloupnost seřazena není, je tato hodnota 0
virus = None #Napadení virem (hodnota 1) či nikoliv (hodnota 0)
size = None
 
def isArrangedAscending(sequence):
    n = len(sequence)
    for i in range(n - 1):
        if sequence[i] > sequence[i + 1]:
            return False
    return True
 
if __name__ == "__main__":
    sequence = []
 
    first_row = sys.stdin.readline().strip().split()
    settings = list(map(int, first_row))
 
    maxValue = settings[0]
    type = settings[1]
    virus = settings[2]
 
    # maximum prvků posloupnosti je menší než 1
    if maxValue < 1:
        print("Error: Maximum neni kladne!", file=sys.stderr)
        sys.exit(1)
 
    #typ řazení posloupnosti není z množiny {0,1,2}
    if type not in {0, 1, 2}:
        print("Error: Neznamy typ razeni posloupnosti!", file=sys.stderr)
        sys.exit(1)
 
    #chybí informace o napadení virem nebo je zadaná chybně (mimo množinu {0,1})
    if virus not in {0, 1}:
        print("Error: Nelze urcit, zda posloupnost napadl virus!", file=sys.stderr)
        sys.exit(1)
 
    sequence = [int(row) if int(row) <= maxValue else (print("Error: Prvek posloupnosti je mimo rozsah!", file=sys.stderr) or sys.exit(1)) for row in sys.stdin]
 
    # Every descending will be reversed
    if type == 2:
        sequence = sequence[::-1]
 
    if type in {1, 2} and virus == 0:
        if not isArrangedAscending(sequence):
            print("Error: Posloupnost neni usporadana!", file=sys.stderr)
            sys.exit(1)
 
    size = len(sequence)
    if size < 1000:
        print("Error: Posloupnost ma mene nez 1000 prvku!", file=sys.stderr)
        sys.exit(1)
     
    if size > 2000000:
        print("Error: Posloupnost ma vic nez 2000000 prvku!", file=sys.stderr)
        sys.exit(1)
 
########### ARRANGE ###########
def countingArranger(sequence):
    biggestValue = max(sequence)
 
    count = [0] * (biggestValue + 1)
     
    for num in sequence:
        count[num] += 1
     
    for i in range(1, len(count)):
        count[i] += count[i - 1]
     
    output = [0] * len(sequence)
     
    for num in sequence[::-1]:
        output[count[num] - 1] = num
        count[num] -= 1
     
    for i in range(len(sequence)):
        sequence[i] = output[i]
 
def insertionArranger(sequence):
    for i in range(1, len(sequence)):
        temp = sequence[i]
        j = i - 1
 
        while (j >= 0 and sequence[j] > temp):
            sequence[j+1] = sequence[j]
            j -= 1
        sequence[j+1] = temp
 
def partition(list, start, end):
    pivot = list[end]
    i = start - 1
 
    for j in range(start, end):
        if list[j] < pivot:
            i += 1
            list[i], list[j] = list[j], list[i]
    i+=1
 
    list[i], list[end] = list[end], list[i]
    return i
 
def quickArranger(list, start, end):
    if start >= end:
        return
     
    pivot = partition(list, start, end)
    quickArranger(list, start, pivot - 1)
    quickArranger(list, pivot+1, end)
 
########### REST ###########
if (virus == 1 and maxValue == 100):
    countingArranger(sequence)
elif (virus == 1):
    insertionArranger(sequence)
elif type in {1, 2} and virus == 0:
    None
elif (maxValue <= 1000):
    countingArranger(sequence)
else:
    quickArranger(sequence, 0, len(sequence) - 1)
 
sequence_as_string = '\n'.join(map(str, sequence))
print(sequence_as_string)
 
# hihi_3_09 - 1000000 elements, numbers up to 100, VIRUS THIS IS OKAY -> COUNTING WAS USED
# hihi_3_07 - 1500000 elements, descending, VIRUS -> I NEED INSERTION, BUT QUICK WAS USED
# hihi_3_06 - 2000000 elements, ascending, VIRUS -> I NEED INSERTION, BUT QUICK WAS USED
# hihi_3_05 - 1000000 elements, descending, VIRUS -> I NEED INSERTION, BUT QUICK WAS USED
# hihi_3_04 - 1000000 elements, ascending, VIRUS