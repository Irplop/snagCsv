import time

def parse(fileName, *para):

    start = time.time()
    print(" ========= QUERY RESULTS =========\n")

    table = []
    row = []
    headers = []
    header_len = 0
    columned_query = []

    with open(fileName) as csv_file:

        for line in csv_file:

            row = line.split(",")

            # get rid of the newline at the end of the last field if there
            if row[-1][-1] == "\n":
                row[-1] = row[-1][:-1]

            # ignore empty newlines
            if row != [""] and len(row) == header_len:
                table.append(row)

            # load headers
            if len(table) == 0:
                table.append(row)
                columned_query = loadHeaders(para, row)
                header_len = len(row)

            # check queries
            try:
                next(print(row) for q in columned_query if row[q[0]] == q[1])
            except StopIteration:
                ""  # do nothing if stop iteration occurs



    # print(table)

    print("\n ======= END QUERY RESULTS =======\n")
    print("Successfully added", len(table), "rows")
    print("done in", time.time()-start, "seconds")




def loadHeaders(para, row):
    headers = row
    columned_query = []  # contains the column number of the query instead of the string

    # check if headers are unique
    if len(headers) != len(set(headers)):
        logError("Headers are not unique!")

    # query stuff
    for arg in para:
        key, val = arg.split("=")
        try:
            columned_query.append([list.index(headers, key), val])

        except ValueError:
            logError("given parameter of " + key + " is not a valid header in the csv")

    return columned_query


def logError(str):
    print("\033[1;31;40m===ERROR: ", str)
    sys.exit(0)

