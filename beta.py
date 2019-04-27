

#TODO: display errors when too few parameters

def load(fileName, para):

    # NOTE: Using the RFC 4180 CSV Spec

    with open(fileName) as csvFile:

        # NOTE: Spec does not require headers


        for line in csvFile:

            if line.__contains__("\""):
                print("line contains double quotes")

                processQuotedLine(line)


            else:
                print("not quotes in line")

                rows = line.split(",")
                print(rows)
                print(rows.__len__())








    # TODO: check column length after loading



    print("para = ", para)




    # start parsing lines
    # make sure to NOT trim spaces out
    # make sure to
    # count lines
    # check for quotes as per spec
    # check for escaped quotes as per spec



    # TODO: error checking
    #   too many or too few columns (commas)
    #   make sure windows and unix style new lines are accepted (new line delimination)


# Check if each line has the same number of columns by ______
# def checkValidColumnLength(csvFile):
    # by checking number of commas in each line?
    #  but this might ignore escaped commas

    # OR

def processQuotedLine(line):
    while line.__len__() > 0:

        # field starts with
        if line[0] == "\"":
            next_quote = line.find("\"")
            print(next_quote,1)

            # find next quote

            # check if escaped quote
            # if yes, then find next and get rid of the escaped ones recursively then save field
            # if no then save field

        # detect valid quotes
        # detect escaped quotes and replace
        # detect escaped commas


def logError(str):
    print("ERROR: ", logError)
    exit()
