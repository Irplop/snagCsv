import re
import sys
import time


# NOTE: Using the RFC 4180 CSV Spec

def load(fileName, *para):
    start = time.time()
    print(" ========= QUERY RESULTS =========\n")

    with open(fileName) as csvFile:
        # NOTE: Spec does not require headers

        table = []
        row = []
        flag_continue = True
        previous_row_length = 0
        headers = []
        columned_query = []

        csv_str = csvFile.read()

        # get rid of new lines at the beginning of file
        csv_str = re.sub("\n*", "", csv_str, count=1)

        while flag_continue:
            # print(csv_str)
            # print(row)

            # check if start of new line
            if csv_str[0] == "\n":

                # get rid of empty newlines as per spec (ignore all empty lines)
                # this will work with 2+ new lines at the beginning and will loop thru until there is only one newline
                if csv_str[0:1] == "\n\n":
                    csv_str = csv_str[1:]

                # start new line
                else:

                    # check row length consistency
                    if previous_row_length != 0 and previous_row_length != row.__len__():
                        logError("Invalid row length on row " + str(row))

                    # load headers into array for the queries -- this assumes that the csv has headers
                    if table.__len__() == 0:
                        columned_query = loadHeaders(para, row)

                    # check and print queried rows
                    # this next statement returns duplicate rows when multiple matches occur
                    # [print(row) if row[q[0]] == q[1] else '' for q in columned_query]
                    # this next statement only returns one row when multiple matches occur
                    try:
                        next(print(row) for q in columned_query if row[q[0]] == q[1])
                    except StopIteration:
                        "" # do nothing if stop iteration occurs

                    previous_row_length = row.__len__()
                    table.append(row)
                    row = []
                    csv_str = re.sub("\n*", "", csv_str, count=1)


            # except for the beginning of a new line, the string should start with a comma
            if csv_str[0] == ",":
                flag = 1  # add padding for the beginning comma
            else:
                flag = 0  # dont add padding


            # PROCESS UNQUOTED FIELD
            # this also takes care of empty fields (a la ,,)
            if not csv_str[flag] == ('"'):
                comma_pos = csv_str[flag:].find(',').__pos__()
                newline_pos = csv_str.find("\n").__pos__()

                # last field in line, end the field at the newline
                if (comma_pos == -1 or comma_pos >= newline_pos) and newline_pos != -1:
                    row.append(csv_str[flag:newline_pos])
                    csv_str = csv_str[newline_pos + flag-1:]

                else:

                    # if last field then dont look for last comma
                    if comma_pos == -1:
                        row.append(csv_str[flag:])
                        csv_str = ''
                    else:
                        row.append(csv_str[flag: comma_pos+flag])
                        csv_str = csv_str[comma_pos+flag:]

                if row[-1].__contains__('"'):
                    logError("Unquoted field contains double-quotes in   " + row[-1])



            # PROCESS QUOTED FIELD
            elif csv_str[flag] == '"':

                # check for empty quoted string "",
                if csv_str[flag:3] == '"",':
                    row.append('')
                    csv_str = csv_str[flag + 3:]

                else:
                    # find the location of the next quote that is not escaped (not two double quotes - "")
                    match = re.search('(?<!")"(?!")', csv_str[flag+1:]).start()  # +1 for after the first quote

                    temp_field = csv_str[flag:match + flag + 2]  # 2 for one off plus next

                    # if there is a single quote here then its invalid
                    if re.search('(?<!")"(?!")', temp_field[1:-1]):
                        logError("invalid quotes in quoted field: " + temp_field)
                        print(temp_field, " HAS INVALID QUOTES")


                    # un-escape quotes
                    temp_field = re.sub('""', '"', temp_field)

                    # append and remove beginning and ending quotes
                    row.append(temp_field[1:-1])  # temp field already doesnt have beginning comma

                    # remove field from line (2 for each quote)
                    csv_str = csv_str[match + flag + 2:]


            if csv_str.__len__() == 0 or re.match("\n*\Z", csv_str):  # the regex checks if its just newlines until end
                table.append(row)

                # TODO: move this extra check so there is only one of these
                # hack - need to check the last row for queries
                # this next statement returns duplicate rows when multiple matches occur
                #[print(row) if row[q[0]] == q[1] else '' for q in columned_query]
                # this next statement only returns one row when multiple matches occur
                try:
                    next(print(row) for q in columned_query if row[q[0]] == q[1])
                except StopIteration:
                    ""  # do nothing if stop iteration occurs

                flag_continue = False


    # print(table)

    print("\n ======= END QUERY RESULTS =======\n")
    print("Successfully added", table.__len__(), "rows")
    # print("done in", time.time()-start, "seconds")



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
