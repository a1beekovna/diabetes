import csv
import json
import re

def fileRead():
    students = []
    with open("students.csv") as file:
        csvRead = csv.reader(file, delimiter=';')
        header = next(csvRead)
        for row in csvRead:
            if row:  # Check if row is not empty
                id = int(row[0])
                list_dict = {
                    header[0]: id,
                    header[1]: row[1],
                    header[2]: row[2],
                    header[3]: row[3],
                    header[4]: row[4]
                }
                students.append(list_dict)
    return students

def printJson(std_list):
    with open("student.json", "w") as outJSON:
        json.dump(std_list, outJSON, indent=4)

def commandSet(input, students):
    students = sorted(students, key=lambda x: int(x['id']))
    splitedInput = input.split()
    if splitedInput[0].upper() == "INSERT":
        insertCommand(input, students)
    elif splitedInput[0].upper() == "SELECT":
        selectCommand(input, students)
    elif splitedInput[0].upper() == "DELETE":
        deleteCommand(input, students)
    elif splitedInput[0].lower() == "exit":
        print("Exited")
    else:
        print("Invalid command!")

def selectCommand(input, students):
    splitedInput = input.split()
    if len(splitedInput) < 4:
        print("Invalid command!")
        return
    
    returnValues = splitedInput[1]
    listSelect = []

    if "where" in splitedInput:
        whereIndex = splitedInput.index("where")
        orderIndex = splitedInput.index("order") if "order" in splitedInput else len(splitedInput)
        listSelect = findRequests(students, splitedInput[whereIndex+1:orderIndex])
    else:
        listSelect = students

    if "order" in splitedInput:
        orderBy = splitedInput[orderIndex + 2]
        if orderBy.lower() == "asc":
            listSelect = sorted(listSelect, key=lambda i: i['id'])
        elif orderBy.lower() == "desc":
            listSelect = sorted(listSelect, key=lambda i: i['id'], reverse=True)

    if returnValues.lower() == "all":
        printJson(listSelect)
    else:
        columns = returnValues.split(',')
        selection = [{key: record[key] for key in columns} for record in listSelect]
        printJson(selection)

def findRequests(students, conditions):
    # This function needs to parse the conditions and return the matching records
    if not conditions:
        return students
    
    column_name = conditions[0]
    operator = conditions[1]
    parameter = conditions[2]
    #iterator
    return [student for student in students if evaluateCondition(student[column_name], operator, parameter)]

def evaluateCondition(value, operator, parameter):
    if operator == "=":
        return value == parameter
    elif operator == "!=":
        return value != parameter
    elif operator == "<":
        return value < parameter
    elif operator == ">":
        return value > parameter
    elif operator == "<=":
        return value <= parameter
    elif operator == ">=":
        return value >= parameter
    return False

def insertCommand(input, students):
    given = input.split()
    if given[1].lower() == "into" and given[2].lower() == "students" and given[3].lower().startswith("values"):
        values = re.findall(r'\((.*?)\)', input)[0].split(',') #gets text inside bracets 
        list_dict = {
            "id": int(values[0].strip()),
            "name": values[1].strip(),
            "lastname": values[2].strip(),
            "email": values[3].strip(),
            "grade": values[4].strip()
        }
        if any(student["id"] == list_dict["id"] for student in students):
            print("This id is already in the list.")
        else:
            students.append(list_dict)
    else:
        print("Invalid command!")

def deleteCommand(input, students):
    splitedInput = input.split()
    if "where" in splitedInput:
        whereIndex = splitedInput.index("where")
        conditions = splitedInput[whereIndex + 1:]
        listRemove = findRequests(students, conditions)
        for item in listRemove:
            students.remove(item)
        print("done")
    else:
        print("Invalid command!")
        print(splitedInput)

def main():
    students = fileRead()
    user_input = ''
    while user_input.lower() != 'exit':
        user_input = input('Enter command set: ')
        commandSet(user_input, students)

if __name__ == '__main__':
    main()
