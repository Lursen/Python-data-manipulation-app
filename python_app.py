import csv
import json
import xml.etree.ElementTree as ET


def read_csv(file_name,array):
    try:
        with open(file_name) as csvfile:
            data = csv.DictReader(csvfile)
            for row in data:
                array.append(dict(row))
    except OSError:
        print ("Cannot open:", file_name)


def read_json(file_name,array):
    try:
        with open(file_name) as jsonfile:
            json_data = json.load(jsonfile)
            for dict in json_data.get('fields'):
                array.append(dict)
    except OSError:
        print ("Cannot open:", file_name)


def read_xml(file_name,array):
    try:
        open(file_name)
        xml_data = {}
        tree = ET.parse(file_name)
        root = tree.getroot()
        for child in root:
            for object in child:
                for value in object:
                    xml_data[(object.get('name'))] = value.text
        array.append(xml_data)
    except OSError:
        print ("Cannot open:", file_name)


def filter(old_data, new_data, keys):
    for odict in old_data:
        filterDict = {key:value for (key,value) in odict.items() 
                      if key in keys}
        newDict = {key:(value if key.startswith('D') else int(value)) 
                   for (key,value) in filterDict.items()}
        new_data.append(newDict)


def save_table(table, keys, file_name):
    with open(file_name, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys, delimiter=" ")
        dict_writer.writeheader()
        dict_writer.writerows(table)


def main():
    result_data = []
    # Getting files
    while True:
        print("Input file name:")
        file_name = input()
        more_files = False

        if (file_name.endswith('csv')):
            read_csv(file_name,result_data)
        elif (file_name.endswith('json')):
            read_json(file_name,result_data)
        elif (file_name.endswith('xml')):
            read_xml(file_name,result_data)
        else:
            print("Chosen file format is not supported!")

        proceed = False
        while (proceed == False):
            print("That's all? (yes/no)")
            response = input()
            if (response == 'yes'):
                proceed = True
                more_files = False
            elif (response == 'no'):
                proceed = True
                more_files = True
            else:
                proceed = False

        if (more_files == False):
            break

    # Getting keys
    print("Input value n for D:")
    Dn = int(input())
    keysD = []
    keysM = []
    for i in range(1, Dn+1):
        keysD.append(('D'+str(i)))

    print("Input value n for M:")
    Mn = int(input())
    for i in range(1, Mn+1):
        keysM.append(('M'+str(i)))
    
    keys = keysD + keysM

    # Filtering data
    filtered_data = []
    filter(result_data, filtered_data, keys)

    # Sorting data
    filtered_data = sorted(filtered_data, key = lambda k: k['D1'])
    
    # Saving data
    save_table(filtered_data, keys, 'basic_results.tsv')
    print("Data succesfully saved in basic_results.csv")

    # Advanced
    advanced_data = []
    advanced_data.append(filtered_data[0])

    for i in range(1, len(filtered_data)):
        current_dict = filtered_data[i]
        current_dict_Dval = [current_dict.get(key) for key in keys 
                             if key.startswith('D')]
        for k in range(0, len(advanced_data)):
            previous_dict = advanced_data[k]
            previous_dict_Dval = [previous_dict.get(key) for key in keys 
                                  if key.startswith('D')]
            if (current_dict_Dval == previous_dict_Dval):
                previous_dict_keys = [previous_dict]
                for key in keysM:
                    advanced_data[k][key] = (int(advanced_data[k].get(key) or 0) 
                                             + int(current_dict.get(key) or 0))
                break
        else:
            advanced_data.append(current_dict)

    save_table(advanced_data, keys, 'advanced_results.tsv')
    print("Data succesfully saved in advancedc_results.csv")


if __name__ == '__main__':
    main()
