import re
import datetime
from time import sleep
from sys import argv, exit

# List to save data dictionaries inputs from menu(),

purchase_list= []

# Main Function to call the file with arguments (registration with username & password) 
def start():
    if len(argv) == 1 or len(argv) == 2:
        print("\n*** Please call file with user name and password ***\n")
        print("** User name should be at least 3 characters ")
        print("** Password should contain:")
        print("one uppercase and one lowercase character\nShould have at least one special symbol\nShould be between 6 to 20 characters long\n")
        exit()
    if len(argv[1])<3:
        print("\n** User name should be at least 3 characters **\n")
        exit()
    elif len(argv) == 3:
        name= argv[1]
        password= argv[2]
        pattern_password= re.match(r"^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[^\w\d\s:])([^\s]){6,20}$", password)
        if pattern_password is None:
            print("\n**** Invalid password ****\n** Please try again with a valid password **")
            print("** Password should contain:")
            print("one uppercase and one lowercase character\nShould have at least one special symbol\nShould be between 6 to 20 characters long\n")
            exit()
        else:
            status= True
            print("\n** Registration successful! **")
            print(2*"\n",15*" ", 25*"-", "\n", 15*" ", "| Amazon Expense Report |", 
                    "\n", 15*" ", 25*"-")
            while status:
                phone_num= input("\nPlease enter your phone number (ex.: +4912345678): ")
                pattern_phone= re.match(r"\+49\d{8,11}", phone_num)
                if pattern_phone is None:
                    print("\n**** Invalid phone number ****\n** Please enter a valid phone number **")
                else:
                    status= False
                    login(name, password, phone_num)
                    
# Login with username and password function 
def login(name, password, phone_num):
    print("\n**** Please login ****")
    for i in range(3):
        login_name= input("Enter your username: ")
        login_pass= input("Enter your Password: ")
        if login_name == name and login_pass == password:
            print (f"\n*** Hello {name.capitalize()} ***\nWelcome to the Amazon Expense Tracker!")
            menu(name, password, phone_num)
            break
        else:
           print ("\n*** Wrong username or password ***\n** Pleas try to login again **\n") 
    
    print("*** You have reached 3 login attempts ***\n** Please register again **")
                
# Menu Function with 3 options to choose from
def menu(name, password, phone_num):
    print("\nWhat would you like to do?\n")
    print("1. Enter a purchase\n2. Generate a report\n3. Quit\n")
    
    choice= input("Enter your choice (1/2/3): ")
    # Displaying menu input options (1)
    if choice == "1":
        date= date_match()
        item= item_input()
        cost= weight_cost_input(text= "Enter the cost of the item in Euro: ", limit= 0)
        weight= weight_cost_input(text= "Enter the weight of the item in kg: ", limit= cost)
        quantity= quantity_input()
        # Calculating the final weight and cost, incase more than 1 quantity of same item per purchase
        final_weight= quantity * weight
        final_cost= cost * quantity
        # Saving purchase inputs in a dictionary 
        data_dic= {}
        data_dic["date"]= date
        data_dic["item"]= item
        data_dic["cost"]= cost
        data_dic["weight"]= weight
        data_dic["quantity"]= quantity
        data_dic["final_weight"]= final_weight
        data_dic["final_cost"]= final_cost
        # Adding data dictionary to purchase_list[] in global scope 
        purchase_list.append(data_dic)
        
        print("\n\nSaving Purchase...\n")
        for i in range(0,3):
            print("...", end=" ", flush=True)
            sleep(1)
        print("\n\nPurchase inputs saved!\n")
        # Reload menu after saving purchase inputs    
        menu(name, password, phone_num)
        
    # Displaying purchase report (2)
    elif choice == "2":
        if len(purchase_list) == 0:
            print("\n**** List is empty ****\n** Enter at least one purchase **\n")
            menu(name, password, phone_num)
        else:
            print("\n\nGenerating Report...")
            for i in range(0,3):
                print("...", end=" ", flush=True)
                sleep(1)
            print("\n\nReport has been generated!\n")
            report(name, password, phone_num)
            print("\n\nLoading Menu...")
            for i in range(0,3):
                print("...", end=" ", flush=True)
                sleep(1)
            menu(name, password, phone_num)
        
    # Quit option (3)
    elif choice == "3":
        print(f"\nThank you for your visit, {name.capitalize()}. Goodbye!\n"), sleep(2)
        # Quitting program using exit() from sys
        exit()
        
    # Repeat menu when user input is invalid 
    else:
        print("\n**** Invalid choice ****\n** Please enter a valid option number **")
        menu(name, password, phone_num)
        
### Functions for purchase inputs ##################################################################

# Function to match the input date of purchase in menu()
def date_match():
    while True:
        date_input= str(input("\nEnter the date of the purchase (MM/DD/YYYY or MM-DD-YYYY): "))
        # Matching date from user's input with regex
        date_match= re.match(r"^(0[1-9]|[12][0-9]|3[01])(-|/)(0[1-9]|1[0-2])(-|/)20[2-9][0-9]$", date_input)
        if date_match is None:
            print("\n**** Invalid date format ****\n** Please enter date again **")
        else:
            False
            # Converting date to the needed format with regex
            date_result=re.sub("-|/","/",date_match.group())
            return date_result

# Function to check item input in menu()
def item_input():
    while True:
        text= str(input("Enter the item purchased: "))
        if len(text)<3 : 
            print("\n**** Invalid input ****\n** Item name should be at least 3 characters **\n")
        else:
            False
            return text
        
# Function to check if the input is less than a limit, 
# used in cost and weight inputs in menu()
def weight_cost_input(text: str, limit=0):
    while True:
        num=input(text)
        try:
            num=float(num)
        
            if limit == 0 and num < limit :
                print(f"\n**** Invalid input ****\n** Input should be more than {limit} **\n")
            elif limit > 0 and (num > limit or num <= 0):
                print(f"\n**** Invalid input ****\n** Input should be more than 0 and less than {limit} **\n** Delivery cost is 1 EUR per 1 Kg **\n")
            else:
                False
                return num

        except ValueError:
            print("*** Please Enter a float value ! ***")
        
# Function to check item quantity in menu()
def quantity_input():
    while True:
        num= input("Enter the quantity purchased: ")
        try:
            num=int(num)
            if num < 1 :
                print(f"\n**** Invalid input ****\n** Quantity should be 1 or more **\n")
            else:
                False
                return num
        except ValueError:
            print("*** Please Enter a number value ! ***")
######################################################################################################

# Function to print the Expense Report
def report(name, password, phone_num):
    # Printing the head of the report
    print(2 * "\n", 15 * " ", 25 * "-", "\n", 15 * " ", "| Amazon Expense Report |",
          "\n", 15 * " ", 25 * '-')
    print(f"\nName: {name.capitalize()} {2 * ' '} Password: *** {2 * ' '} Tel: {phone_num} {2 * ' '}",
          f"Date: {datetime.date.today().strftime('%d/%m/%Y')}\n{70 * '-'}")

    # Calling the sum of total items cost, weight and quantity from the dictionary list

    final_cost_sum = sum(item["final_cost"] for item in purchase_list)

    final_weight_sum = sum(item["final_weight"] for item in purchase_list)

    quantity_sum = sum(item["quantity"] for item in purchase_list)

    # Calling max. and min. date of item purchase dictionaries in purchase_list[]
    most_recent_item = max(purchase_list, key=lambda item: item["date"])
    least_recent_item = min(purchase_list, key=lambda item: item["date"])

    # Calling max. and min. cost of item purchase dictionaries in purchase_list[]
    most_expensive_item = max(purchase_list, key=lambda item: item["cost"])
    least_expensive_item = min(purchase_list, key=lambda item: item["cost"])

    # printing the body of the report

    print("DELIVERY CHARGES", 10 * " ", "TOTAL ITEM COST")
    print(3 * " ", final_weight_sum, "EURO", 16 * " ",
          (final_cost_sum - final_weight_sum), "EURO")
    print(f"\nMOST EXPENSIVE:", 10 * " ", "LEAST EXPENSIVE:")
    print(f"Name:{most_expensive_item['item']} {16 * ' '} Name: {least_expensive_item['item']}")
    print(f"Cost: {most_expensive_item['cost']} {17 * ' '} Cost: {least_expensive_item['cost']}")
    print(f"\nAVERAGE COST OF ITEM PER ORDER: {final_cost_sum/quantity_sum} EURO\n")
    print(f"PURCHASE DATE RANGE: {least_recent_item['date']} - {most_recent_item['date']}")
    print(10 * "-")
    if final_cost_sum < 500:
        print("Note: You have NOT exceeded the spending limit of 500 EURO\n")
    elif final_cost_sum == 500:
        print("Note: You have reached the spending limit of 500 EURO\n")
    else:
        print("Note: You have exceeded the spending limit of 500 EURO\n")
    

# Calling main function to start   
if __name__=="__main__":
    start()
