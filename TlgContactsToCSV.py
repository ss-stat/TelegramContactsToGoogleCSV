import json
import csv

# Open the result.json in the current directory
with open('result.json') as f:
    data = json.loads(f.read())

# Find and combine the phones of one person 
contacts = dict()
for contact in data['contacts']['list']:
    Name = contact['first_name']+' '+contact['last_name']
    if Name in contacts:
        contacts[Name]['phones'].append(contact['phone_number'])
    else:
        contacts[Name] = {
            'Given Name' : contact['first_name'],
            'Family Name' : contact['last_name'],
            'phones': []}
        contacts[Name]['phones'].append(contact['phone_number'])

# Form the list of dicts with keys corresponding to the google csv-file headers
# Telegram doesn't give phone's type, so default 'Phone N - Type' is 'Work'
csv_list = list()
for k, v in contacts.items():
    row_dict = {}
    row_dict['Name'] = k
    row_dict['Given Name'] = v['Given Name']
    row_dict['Family Name'] = v['Family Name']
    if len(v['phones']) > 0:
        for i in range(1, len(v['phones'])+1):
            key = 'Phone '+str(i)+' - Type'
            row_dict[key] = 'Work' # можно попробовать пустую строку, не вполне понятно обязательно ли определять тип       
            key = 'Phone '+str(i)+' - Value'
            row_dict[key] = v['phones'][i-1].strip()
            if row_dict[key].startswith('00'): row_dict[key] = '+'+row_dict[key][2:]     
            if i == 4:
                break 
                
    csv_list.append(row_dict)   
    
# List of all standart headers for google contacts csv-file - ref: http://www.scsb.org/google-csv-import.html      
headers = 'Name,Given Name,Additional Name,Family Name,Yomi Name,Given Name Yomi,Additional Name Yomi,Family Name Yomi,Name Prefix,Name Suffix,Initials,Nickname,Short Name,Maiden Name,Birthday,Gender,Location,Billing Information,Directory Server,Mileage,Occupation,Hobby,Sensitivity,Priority,Subject,Notes,Group Membership,E-mail 1 - Type,E-mail 1 - Value,E-mail 2 - Type,E-mail 2 - Value,Phone 1 - Type,Phone 1 - Value,Phone 2 - Type,Phone 2 - Value,Phone 3 - Type,Phone 3 - Value,Phone 4 - Type,Phone 4 - Value,Address 1 - Type,Address 1 - Formatted,Address 1 - Street,Address 1 - City,Address 1 - PO Box,Address 1 - Region,Address 1 - Postal Code,Address 1 - Country,Address 1 - Extended Address,Organization 1 - Type,Organization 1 - Name,Organization 1 - Yomi Name,Organization 1 - Title,Organization 1 - Department,Organization 1 - Symbol,Organization 1 - Location,Organization 1 - Job Description,Website 1 - Type,Website 1 - Value'

# Write the contacts.csv file to the current directory
keys = {key:'' for key in headers.split(',')}.keys()
with open('contacts.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames=keys)
    dict_writer.writeheader()
    dict_writer.writerows(csv_list)    
        
