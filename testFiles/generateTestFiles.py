import random
import string

str = ""

f = open("70000x10.csv", "w")


for i in range(70000):
    row = ""
    for j in range(10):
        a = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        row = row + a + ","

    row = row[:-1]  # get rid of the last comma
    f.write(row)
    f.write("\n")


f.close()
