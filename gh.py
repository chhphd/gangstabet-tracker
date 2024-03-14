from functions import output_rankings, output_singular_gangsta_list, output_total_holdings, output_singular_land_list
from datetime import datetime
import argparse
import re

def validate_string(input_string):
    regex_pattern = r'^hx[a-fA-F0-9]{40}$'
    return re.match(regex_pattern, input_string) is not None

def export_to_csv(df, filename):
    """
    Export a pandas DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to export.
        filename (str): The name of the file to export the data to.
    """

    # Prompt the user
    while True:
        choice = input("Do you want to export this to .csv? (y/n): ")

        if choice == "y":
            df.to_csv(filename, index=True)
            break
        elif choice == "n":
            break    
        else:
            print("Please input 'y' or 'n'.")

def export_to_txt(text, filename):
    """
    Export a pandas DataFrame to a TXT file.

    Args:
        df (pd.DataFrame): The DataFrame to export.
        filename (str): The name of the file to export the data to.
    """

    # Prompt the user
    choice = input("Do you want to export this to .txt? (y/n): ")

    if choice == "y":
        with open(filename, 'w') as f:
            f.write(text)
    elif choice == "n":
        pass    
    else:
        print("Please input 'y' or 'n'.")    

def parser() -> str:
    """
    Argparse implementation to input address when running the program
    Program should be run by:
    
    python gh.py --address=[your_address]
    
    """  
    # Init parser
    parser = argparse.ArgumentParser(prog='Gangstabet helper')
    
    # Parser arguments
    parser.add_argument('--address', dest='input_address', default='', required=True, help='address to be converted')
    
    args = parser.parse_args()
    # input_address = args.input_address

    return args.input_address

# Main menu
def menu():
    print("------------------------------------------")
    print("----------- GANGSTABET  HELPER -----------")
    print(f"{input_address}")
    print("------------------------------------------")
    print("1. Rankings")
    print("2. Total holdings")
    print("3. NFT list - detailed")
    print("4. Land list - detailed")
    print("0. Exit")

# Main menu options
def option1():
    # TODO: progress bar
    amounts = output_total_holdings(input_address)
    text = output_rankings(amounts, input_address)
    print(text)
    export_to_txt(text, f"output/rankings_{formatted_now}.txt")

def option2():
    # TODO: progress bar
    data = output_total_holdings(input_address)
    print(data)
    export_to_csv(data, f"output/total_holdings_{formatted_now}.csv")

def option3():
    data = output_singular_gangsta_list(input_address)
    print(data)
    export_to_csv(data, f"output/singular_nftlist_{formatted_now}.csv")

def option4():
    data = output_singular_land_list(input_address)
    print(data)
    export_to_csv(data, f"output/singular_landlist_{formatted_now}.csv")

def main():
    
    while True:    
        
        menu()

        choice = input("Enter your choice: ")
        if choice == "1":
            option1()
        elif choice == "2":
            option2()
        elif choice == "3":
            option3()
        elif choice == "4":
            option4()    
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please choose again.")

# Get the current date and time
now = datetime.now()
formatted_now = now.strftime("%Y%m%d_%H%M%S")

if __name__ == "__main__":
    input_address = parser()
    if validate_string(input_address):
        main()
    else:
        print("Please provide a valid ICX address")
        exit()
    