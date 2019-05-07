import utils

def main():
    #clean_poverty()
    # clean_rent()
    # clean_crime()
    # combine_datasets()
    normalize_combined()

def normalize_combined():
    combined_table, header = utils.read_table("combined_data.csv", True)
    columns = []
    new_header = []
    for x in range(len(header)):
        if x not in [2,6,7,8,9,10,11,12,13,16]:
            new_header.append(header[x])
            columns.append(utils.get_column(combined_table, x))
    columns.append([round(columns[6][i]*12*100/columns[3][i], 1) for i in range(len(columns[0]))])
    new_header.append("Pct_Income_as_Rent")

    columns[2] = normalize_data(columns[2], 3) # Poverty
    columns[3] = normalize_data(columns[3], 5) # Median Income
    columns[4] = normalize_data(columns[4], 5) # Crime Rate
    columns[5] = normalize_data(columns[5], 5) # Population
    columns[6] = normalize_data(columns[6], 5) # Rent
    columns[7] = normalize_data(columns[7], 5) # Rent as percent of income.
    
    new_table = []
    for x in range(len(columns[0])):
        buffer = []
        for column in columns:
            buffer.append(column[x])
        new_table.append(buffer)
    
    new_table.insert(0, new_header)
    utils.write_table("combined_data_normalized.csv", new_table)

def normalize_data(data, num_segs):
    groups = equal_width_bins(data, num_segs)
    rename_data(groups, data)
    return data

def rename_data(groups, data):
    if len(groups) == 3:
        for x in range(len(data)):
            if data[x] in groups[0]:
                data[x] = "Low"
            elif data[x] in groups[1]:
                data[x] = "Medium"
            elif data[x] in groups[2]:
                data[x] = "High"
    elif len(groups) == 5:
        for x in range(len(data)):
            if data[x] in groups[0]:
                    data[x] = "Very Low"
            elif data[x] in groups[1]:
                    data[x] = "Low"
            elif data[x] in groups[2]:
                    data[x] = "Medium"
            elif data[x] in groups[3]:
                    data[x] = "High"
            elif data[x] in groups[4]:
                    data[x] = "Very High"
    elif len(groups) == 10:
        for x in range(len(data)):
            for i in range(len(groups)):
                if data[x] in groups[i]:
                    data[x] = i+1
                    break


def equal_width_bins(data, num_segs):
    width = (max(data)-min(data))/num_segs #Finds width of bins.
    groups = []
    for x in range(num_segs):
        buffer = []
        for num in data:
            if num >= min(data)+(width*x) and num < min(data)+(width*(x+1)): #Apportions data to correct bin.
                buffer.append(num)
        groups.append(buffer)
    return groups


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