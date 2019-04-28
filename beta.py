import re

#TODO: display errors when too few parameters

def load(fileName, para):

    # NOTE: Using the RFC 4180 CSV Spec

    with open(fileName) as csvFile:

        # NOTE: Spec does not require headers

        table = []

        for line in csvFile:
            print("processing line: ", line)

            if line != "\n":

                if line.__contains__("\""):
                    table.append(process_quoted_line(line))

                else:
                    row = line[:-1].split(",")  # the -1 removes the ending line break
                    table.append(row)

    print(table)
    # TODO: check column length after loading


def process_quoted_line(line):
    row = []

    while line.__len__() != 0:

        # except for the beginning, the line here should start with a comma
        if line[0] == ",":
            flag = 1  # add padding for the beginning comma
        else:
            flag = 0  # dont add padding

        # check if current field is not quoted
        # this also takes care of empty fields (a la ,,)
        comma_pos = line[flag:].find(',').__pos__()
        if not line[:comma_pos].__contains__('"'):

            # if last field then dont look for last comma
            if comma_pos == -1:
                row.append(line[flag:])
                line = ''
            else:
                row.append(line[flag: comma_pos + 1])
                line = line[comma_pos + flag:]

        else:

            if line[0] == ",":
                line = line[1:]

            # check for empty quoted string "",
            if line[0:3] == '"",':
                row.append('')
                line = line[3:]

            else:
                # find the location of the next quote that is not escaped (not two double quotes - "")
                match = re.search('(?<!")"(?!")', line[1:]).start()

                temp_field = line[:match + 2]

                # un-escape quotes
                temp_field = re.sub('""', '"', temp_field)
                print(temp_field)

                # append and remove beginning and ending quotes
                row.append(temp_field[1:-1])

                # remove field from line
                line = line[match + 3:]

    return row


def logError(str):
    print("ERROR: ", logError)
    exit()
