import sys
from csv import DictReader


def main():
    # checks command for proper amount of args
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit()

# opens and reads database
    try:
        rawdata = open(sys.argv[1], newline='')
        data = DictReader(rawdata)
    except:
        print("couldnt open/read Database")
        sys.exit()

# opens and reads DNA
    try:
        dnaraw = open(sys.argv[2])
        dna = dnaraw.read()
    except:
        print("couldnt open/read DNA strip")
        sys.exit()

# initialises counter
    strcount = {}

# loops each STR and checks for it in DNA. if found it check for more consecutives and adds to temp count.
# when temp count is larger than max count it updates max count. and then makes a dictionary corrolating STR to max count
    for i in data.fieldnames[1:]:
        x = 0
        countmax = 0

        for j in range(len(dna) - len(i)):
            count = 0
            x = j
            while i in dna[x: len(i) + x]:
                count += 1
                if count > countmax:
                    countmax = count
                x += len(i)

        strcount[i] = countmax

# itterates over Database to find and print a match. if there is no match then print no match
    for row in data:
        count = 0

        for i in data.fieldnames[1:]:
            if f"{row[i]}" == f"{strcount[i]}":
                count += 1

            if count == len(data.fieldnames[1:]):
                print(f"{row[data.fieldnames[0]]}")
                sys.exit()

    print("No match")
    sys.exit()


main()
