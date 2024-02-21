from lib.functions import output_rankings, output_singular_nft_list, output_total_holdings
from lib.assets import wallet
from datetime import datetime

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
    Export a pandas DataFrame to a CSV file.

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

def menu():
    print("# Gangstabet helper #")
    print("--------------------")
    print("1. Rankings")
    print("2. Total holdings")
    print("3. NFT list for an address")
    print("0. Exit")

def option1():
    amounts = output_total_holdings(wallet.addresses)
    text = output_rankings(amounts)
    print(text)
    export_to_txt(text, f"output/rankings_{formatted_now}.txt")

def option2():
    data = output_total_holdings(wallet.addresses)
    print(data)
    export_to_csv(data, f"output/total_holdings_{formatted_now}.csv")

def option3():
    data = output_singular_nft_list()
    print(data)
    export_to_csv(data, f"output/singular_nftlist_{formatted_now}.csv")

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
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please choose again.")

# Get the current date and time
now = datetime.now()

# Format the date and time
formatted_now = now.strftime("%Y%m%d_%H%M%S")

if __name__ == "__main__":
    main()