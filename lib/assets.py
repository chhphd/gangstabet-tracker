from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.builder.call_builder import CallBuilder
import json

# Classes
class Blockchain:
    # Icon service
    icon_service = IconService(HTTPProvider("https://ctz.solidwallet.io", 3))

    # Contracts
    gangstabetMainContract = "cx384018e03aa8b739472c7a0645b70df97550e2c2"
    gangstabetToken = "cx6139a27c15f1653471ffba0b4b88dc15de7e3267"
    goldenKey = "cx5f1cc357f2304fb2646e20211adbe137ab5852dd"
    crownToken = "cx28b2ec885b50c8a93da752f2d0467a67127a70e8"

    def __init__(self):
        self.blockHeight = self.returnBlock()["height"]
 
    def returnBlock(self) -> dict:
        """
        Returns the latest block in full format.
        """
        block = self.icon_service.get_block("latest")
        return block

    def call(self, to: str,method: str, params: dict, height: int) -> dict:
        """
        Submits a read-only request to query data from the ICON blockchain using the CallBuilder function.

        Args:
            to: The contract address to query.
            method: The contract method to query.
            params: The parameters expected by the contract method.
            height: The block height to query (useful for fetching data about past state).

        Returns:
            A dictionary containing the result of the query.
        """
        call = CallBuilder().to(to)\
                            .method(method)\
                            .params(params)\
                            .height(height)\
                            .build()
        
        result = self.icon_service.call(call)
        return result

class Wallet:
  
    def __init__(self):
        self.addresses = self.get_addresses()     

    def get_addresses(self) -> list:
        with open("lib\\addresses.json") as json_data:
            address_list = json.load(json_data)
        return address_list
    
    def search_address(self) -> list:
        """
        Prompts the user to input the last 3 characters of an address and returns the one found

        Returns:
            list of str: A list with one address
        """
        while True:
            suffix = input("Input the last 3 characters of the address: ")
            matched_items = [item for item in self.addresses if item.endswith(suffix)]

            if matched_items:
                return matched_items
            else:
                print(f"No addresses ending in {suffix}. Please try again")

# Init
blockchain = Blockchain()
wallet = Wallet()                        