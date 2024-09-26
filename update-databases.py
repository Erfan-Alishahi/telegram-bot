import os
import json

def convert(path_of_data_bot, path_of_txt_file, path_of_second_data, department_id, department_name):
    # load and convert text file to json
    with open(path_of_txt_file, 'r', encoding='utf-8') as f:
        first_data = f.readlines()

    Lst = list()
    Dict = dict()
    for line in first_data:
        if line[0] == '#':
            Lst.append(Dict)
            Dict = dict()
        elif line[0] == '%':
            Lst.append(Dict)
            break
        else:
            part1, part2 = line.split('^')
            Dict[part1] = part2[:-1]

    # add ID, Position to data
    ID = department_id + 1 # id of first people
    for element in Lst:
        element['ID'] = ID
        ID += 1
        element['Position'] = 'Faculty'
    # Now, Lst is list of dict's which are data of faculties

    # add Lst to data-bot
    with open(path_of_data_bot, 'r', encoding='utf-8') as f:
        f = f.read()
        data_bot_dict = json.loads(f)
    ID = department_id # id of department
    data_bot_dict[ID] = Lst
    with open(path_of_data_bot, 'w') as f:
        json.dump(data_bot_dict, f)
    # Now data-bot updated

    # Now let's update second data
    Lst2 = list()
    Dict = dict()
    for element in Lst:
        Dict['ID'] = element['ID']
        Dict['Department'] = department_name # enter department name
        Dict['Name'] = element['Name']
        Lst2.append(Dict)
        Dict = dict()
    # Now Lst2 is list of dict's which are second data of faculties

    # add Lst2 to second database
    with open(path_of_second_data, 'r', encoding='utf-8') as f:
        f = f.read()
        second_data_dict = json.loads(f)

    second_data_dict[ID] = Lst2

    with open(path_of_second_data, 'w') as f:
        json.dump(second_data_dict, f)
    # Now second database updated


department_id = int(input('Department ID: '))
department_name = input('Department Name: ')
path_of_data_bot = os.getcwd()+'/data-bot.json'
path_of_txt_file = os.getcwd()+'/basic-info.txt'
path_of_second_data = os.getcwd()+'/data.json'

convert(path_of_data_bot, path_of_txt_file, path_of_second_data, department_id, department_name)
print('Done.')
