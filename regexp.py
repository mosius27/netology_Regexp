import re
from pprint import pprint
import csv

def fix_address_book(data):
    
    for i, elem in enumerate(data):
        parts =re.split(r'\s+', elem.strip())
        if len(parts) == 3:
            data[i] = parts[0]
            data[i + 1] = parts[1]
            data[i + 2] = parts[2]
        elif len(parts) == 2:
            data[i] = parts[0]
            data[i + 1] = parts[1]
        else:
            data[i] = parts[0]

    return data

def fix_phone_number(phone):
    pattern = r'^(\+7|8)[\s\-]?(\(?\d{3}\)?)[\s\-]?(\d{3})[\s\-]?(\d{2})[\s\-]?(\d{2})[\s\-]?(доб\.\s?\d+)?$'
    match = re.match(pattern, phone)
    if match:
        groups = match.groups()
        code = groups[1]
        first = groups[2]
        second = groups[3]
        third = groups[4]
        extension = groups[5]
        if code[0] == '(':
            code = code[1:-1]
        phone = f'+7({code}){first}-{second}-{third}'
        if extension:
            phone += f' {extension}'
    return phone


def merge_contacts(data):
    merge_list = []
    for compared in data:
        for employee in data:
            if compared[0:2] == employee[0:2]:
                list_employee = compared
                compared = list_employee[0:2]
                for i in range(2, 7):
                    if list_employee[i] == '':
                        compared.append(employee[i])
                    else:
                        compared.append(list_employee[i])
        if compared not in merge_list:
            merge_list.append(compared)

    return merge_list


if __name__ == "__main__":
    with open("phonebook_raw.csv", 'r', encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
        pprint(contacts_list)

    new_contact_list = []
    for i, contact in enumerate(contacts_list):
        if i != 0:
            fixed_contact = []
            fixed_contact += fix_address_book([contact[0], contact[1], contact[2]])
            fixed_contact += contact[3:5]
            fixed_contact.append(fix_phone_number(contact[5]))
            fixed_contact += (contact[6:])
            
            new_contact_list.append(fixed_contact)
        else:
            new_contact_list.append(contact)

    new_contact_list = merge_contacts(new_contact_list)

    # код для записи файла в формате CSV
    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(new_contact_list)