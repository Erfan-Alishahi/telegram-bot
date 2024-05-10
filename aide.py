import json
import json

# Load the JSON data from the file
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract names from the "11000" key
names_11000 = [item['Name'] for item in data['11000']]



# Load the JSON file
with open('data-bot.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
print(data)
# Iterate through each dictionary element
for i, person in enumerate(data):
    name=person["Name"]
    print(f"Entering information for person {name}:")
    person["ID"] = 11001 + i+1
    person["Department"] = "Physics"
    person["DepartmentId"] = 11000
    person["NameFa"] = names_11000[i]

# Write the modified data back to the JSON file
with open('data-bot.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
