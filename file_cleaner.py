import utils

def main():
    clean_poverty()
    clean_rent()
    clean_crime()


def clean_crime():
    table = []
    infile = open("crime_data.csv", "r")

    lines = infile.readlines()
    header = lines.pop(0).strip().split(",")
    header.insert(1, "State_Name")
    table.insert(0, header)
    
    for line in lines:
        newline = remove_quotes(line)
        newline = newline.strip() #removes whitespace characters
        values = newline.split(",") #splits on comma
        values.insert(1, values[0][-2:])
        values[0] = values[0][:-3]
        #utils.convert_to_float(values)
        table.append(values)


    utils.write_table("crime_data_clean.csv", table)
    infile.close()


def clean_rent():
    table = []
    infile = open("rent_data.csv", "r")

    lines = infile.readlines()
    for line in lines:
        newline = line.strip() #removes whitespace characters
        values = newline.split(",") #splits on comma
        #utils.convert_to_float(values)
        table.append(values)

    utils.write_table("rent_data_clean.csv", table)
    infile.close()

def clean_poverty():
    table = []
    infile = open("poverty_data.csv", "r")

    lines = infile.readlines()
    for line in lines:
        newline = remove_quotes(line)
        newline = newline.strip() #removes whitespace characters
        values = newline.split(",") #splits on comma
        #utils.convert_to_float(values)
        table.append(values)

    header = table.pop(0)
    header[0] = header[0][3:]
    table.insert(0, header)
    utils.write_table("poverty_data_clean.csv", table)
    infile.close()


def remove_quotes(line):
    newline = ''
    count = 0
    for char in line:
        if count == 0:
            if char == '"':
                count = 1
            else:
                newline += char
        elif count == 1:
            if char == '"':
                count = 0
            elif char == ',':
                pass
            else:
                newline += char
    return newline

main()