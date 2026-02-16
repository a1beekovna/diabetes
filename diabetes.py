
import tkinter as tk
from tkinter import messagebox
import csv
import math
#window for a message about an error or diabetic percentage
additional_window = None


#to display an error message if invalid data is entered 
def show_error_message(message):
    additional_window = tk.Toplevel()
    additional_window.title("Error")
    additional_window.geometry("350x150+580+400")
    tk.Label(additional_window, text=message, padx=50, pady=20).pack()
    tk.Button(additional_window, text="OK", command=additional_window.destroy).pack(pady=10)
#to show the diabetic percentage
def show_message(message, entries):
    global additional_window  # Declare additional_window as global

    if additional_window and additional_window.winfo_exists():
        return
     
    additional_window = tk.Toplevel()
    additional_window.title("Diabetes")
    additional_window.geometry("350x150+580+400")
    tk.Label(additional_window, text=message, padx=50, pady=20).pack()
    tk.Button(additional_window, text="OK", command=lambda: clear_entries(additional_window, entries)).pack(pady=10)
   

#after the output is given to erase old data 
def clear_entries(window, entries):
    window.destroy()
    for entry in entries:
        entry.delete(0, tk.END)    
#to check if an error occured while user is entering the data
def display_text(entries):
    for entry in entries:
        text = entry.get()
        if not text: 
            show_error_message(f"Some values are not valid please enter again")
            break
        else:
            try:
                float_value = float(text)
            except ValueError:
                show_error_message(f"Some values are not valid please enter again")
                break
                
            normalize_data(entries)
    

def normalize_data(entries):
    data=[]
    temp = []
    newData = [[] for _ in range(9)]
    #to read a given file
    with open('diabetes.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            data.append(lines)
        #to allocate the data which user was entered
        for i, entry in enumerate(entries):
            text=entry.get()
            temp.append(text)
    temp.append(0)
    data.append(temp)


    for column_index in range(9):
        max_value = float('-inf')  
        min_value = float('inf')   
        for row_index in range(1, len(data)):
            # to access the value in the first column of each row as float
            value = float(data[row_index][column_index])  
            # to update max and min values
            if value > max_value:
                max_value = value
            if value < min_value:
                min_value = value


        for row_index in range(1, len(data)):
            value = float(data[row_index][column_index]) 
            # to calculate new value of the data according to the min and max values
            n_new=(value-min_value)/(max_value-min_value)
            n_new=round(n_new,9)
            # to put that data into a new array
            newData[column_index].append(n_new)


    #to properly put the data into the new csv file
    transposed_temp = list(zip(*newData))
    #to delete the last row as it contains the user's data
    del transposed_temp[len(transposed_temp)-1]
    # to create a new csv file
    new_file = "diabetes_preprocessed.csv"

    # to write the transposed array to the CSV file
    with open(new_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        for row in transposed_temp:
            writer.writerow(row)

    transposed_temp = list(zip(*newData))
    distance_points(transposed_temp[len(transposed_temp)-1], entries)

def main():
    #to create as main window
    win = tk.Tk()
    win.title("Medical Care")
    
    win.geometry("1100x700+200+10")
    line = " "
    #to get headings of the data 
    with open('diabetes.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            line = lines
            break

    #to display headings on the window        
    for i in range(8):
        label = tk.Label(win, text = line[i])
        label.grid(row=0, column=i, padx=10, pady=50)

    #to display text boxes
    entries = []
    for i in range(8):
        entry = tk.Entry(win, width=15)
        entry.grid(row=1, column=i, padx=20)
        entries.append(entry)

    #to create a button to send the data and with the help of display_text function enterred data will be checked
    button = tk.Button(win, text="Submit", width=20, command=lambda: display_text(entries))
    button.grid(row=2, columnspan=8, pady=100) 
    
    # to run the window
    win.mainloop()


#to find 5 nearest data to our user's data and compire them
def distance_points(value, entries):
    new_datas=[]
    outcome = []
    with open('diabetes_preprocessed.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            new_datas.append((lines))
    for i in new_datas:
        sum = 0
        for data in range(8):
            sum += math.pow((float(i[data])- value[data]),2)
        sum = math.sqrt(sum)
        outcome.append([sum, i[8]])
    del outcome[len(outcome)-1]
    nearest = []
    for i in range(5):
        min = float('inf') 
        outMin = -1
        temp=0
        count = 0
        for out in outcome:
            for i in range(2):
                if (out[0] < min):
                    min = out[0]
                    outMin=out[1]
                    count = temp
            temp+=1
        nearest.append(outMin)
        del outcome[count]
    probability(nearest, entries)

#to calculate the probability of being a diabetic
def  probability(nearest, entries):
    count_positive = 0
    for i in nearest:
        if (float(i) == 1.0):
            count_positive +=1
    diabetes = count_positive * 20
    #to show the probability for the user on the window
    show_message(f" The probability of diabetes for your inputted patient is {diabetes}%.", entries)

#main function
if __name__ == '__main__':
    main()
