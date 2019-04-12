import utils

def main():
    table, header = clean_poverty()
    header[0] = header[0][3:]
    table.insert(0, header)
    utils.write_table("poverty_data_clean.csv", table)


def clean_poverty():
    table = []
    infile = open("poverty_data.csv", "r")


    lines = infile.readlines()
    for line in lines:
        count = 0
        newline = ''
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
        newline = newline.strip() #removes whitespace characters
        values = newline.split(",") #splits on comma
        #utils.convert_to_float(values)
        table.append(values)
    header = table.pop(0)


    infile.close()
    return table, header

main()