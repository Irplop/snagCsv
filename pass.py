import csvparser
import sys



# print("===",sys.argv[1])


# fileName = "testFiles/edgeCases.csv"
# para = ["student=True"]
# csvparser.load(fileName, "LastName=Gold", "LastName=Tinuviel", "metadata=", "metadata=tolkien")

csvparser.load(sys.argv[1], *sys.argv[2:])
