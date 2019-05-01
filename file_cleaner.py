import utils

def main():
    clean_poverty()
    clean_rent()
    clean_crime()
    combine_datasets()


def combine_datasets():
    poverty_table, _ = utils.read_table("poverty_data_clean.csv", True)
    crime_table, _ = utils.read_table("crime_data_clean.csv", True)
    rent_table, _ = utils.read_table("rent_data_no_dups.csv", True)
    combined_table = []
    combined_header = ["County", "State",\
        "Pov_Num_All","Pov_Pct_All","Median_Income", \
        "Crime_Rate_per_100000","Murder","Rape","Robbery","Aggravated_Assault","Burglary","Larceny","Vehicle_Theft","Arson",\
        "Population","Mean_Rent","Median_Rent"]
    for poverty_row in poverty_table:
        for crime_row in crime_table:
            for rent_row in rent_table:
                if poverty_row[2] == crime_row[0] and crime_row[0] == rent_row[3]:
                    new_add = [poverty_row[2], poverty_row[1],\
                        poverty_row[3], poverty_row[4], poverty_row[9],\
                        crime_row[2], crime_row[3], crime_row[4], crime_row[5], crime_row[6], crime_row[7], crime_row[8], crime_row[9], crime_row[10], \
                        crime_row[11], rent_row[9], rent_row[10]]
                    combined_table.append(new_add)
    
    no_dups = dict(((x[0],x[1]), x) for x in combined_table)
    new_table = list(no_dups.values())

    new_table.insert(0, combined_header)
    utils.write_table("combined_data.csv", new_table)



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
    no_dups = dict(((x[1],x[3]), x) for x in table)
    new_table = list(no_dups.values())
    utils.write_table("rent_data_no_dups.csv", new_table)
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