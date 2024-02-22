import pandas as pd
from lib.assets import wallet, blockchain

# Contract queries          
# Gangsta
def gangsta_getCharacterInfo(nftId: int) -> dict:
    """
    Query for one nft. 
    Contract name: GangstaBet.

    Args:
        nftId: the ID of the nft queried (in dec)

    Returns: 
        A list of all nft traits
    """
    # Call the contract
    balance = blockchain.call(
        to=blockchain.gangstabetMainContract, 
        method="getCharacterInfo", 
        params={"nftId": hex(nftId)}, 
        height=blockchain.blockHeight)    
    
    return balance

def gangsta_getAllNftOwned(address: str) -> list:
    """
    Query for one address.
    Contract name: GangstaBet.

    Args:
        address: the wallet addres for which to query

    Returns: 
        A list of all nfts owned
    """
    page = 1
    nftList = []

    # Call the contract
    balance = blockchain.call(
        to=blockchain.gangstabetMainContract, 
        method="getAllNftOwned", 
        params={"address": address, "page": page}, 
        height=blockchain.blockHeight)
    
    # Append the first page to the list
    nftList.append(balance["nftList"])

    # Loop until pages end if multiple
    while int(balance["totalPage"], 16) > page:
        page = page + 1
        balance = blockchain.call(
            to=blockchain.gangstabetMainContract, 
            method="getAllNftOwned", 
            params={"address": address, "page": page}, 
            height=blockchain.blockHeight)
        nftList.append(balance["nftList"])

    # Flatten the lists and convert to dec
    flatList = [int(item, 16) for sublist in nftList for item in sublist]

    return flatList

# GBET
def gbet_balanceOf(address: str) -> int:
    """
    Query for one address.
    Contract name: GangstaBet Token.

    Args:
        address: the wallet addres for which to query    
    
    Returns:
        GBET amount held by an address (claimed)
    """

    # Call the contract
    balance = blockchain.call(
        to=blockchain.gangstabetToken, 
        method="balanceOf", 
        params={"_owner": address}, 
        height=blockchain.blockHeight)
    
    amount = int(balance, 16) * 1e-18

    return round(amount, 2)

def gbet_totalSupply() -> int:
    """
    Query the total supply of GBET
    Returns:
        Total supply of GBET
    """
    # Call the contract
    balance = blockchain.call(
        to=blockchain.gangstabetToken, 
        method="totalSupply", 
        params=None, 
        height=blockchain.blockHeight)
    
    amount = int(balance, 16) * 1e-18

    return round(amount, 2)    

# Golden Key
def goldenkey_balanceOf(address: str) -> int:
    """
    Query for one address.
    Contract name: GangstaBet Golden Key.

    Args:
        address: the wallet addres for which to query    
    
    Returns:
        Goloen Key amount held by an address
    """

    # Call the contract
    balance = blockchain.call(
        to=blockchain.goldenKey, 
        method="balanceOf", 
        params={"_owner": address, "_id": 1}, 
        height=blockchain.blockHeight)
    
    amount = int(balance, 16)

    return amount   

def goldenkey_totalSupply() -> int:
    """
    Query the total supply of Golden Keys
    Returns:
        Total supply of Golden Keys
    """

    # Call the contract
    balance = blockchain.call(
        to=blockchain.goldenKey, 
        method="totalSupply", 
        params=None, 
        height=blockchain.blockHeight)
    
    amount = int(balance, 16)

    return amount 

# CROWN
def crown_balanceOf(address: str) -> int:
    """
    Query for one address.
    Contract name: CROWN.

    Args:
        address: the wallet addres for which to query    
    
    Returns:
        CROWN amount held by an address (claimed)
    """

    # Call the contract
    balance = blockchain.call(
        to=blockchain.crownToken, 
        method="balanceOf", 
        params={"_owner": address}, 
        height=blockchain.blockHeight)
    
    amount = int(balance, 16) * 1e-18

    return round(amount, 2)

def crown_totalSupply() -> int:
    """
    Query the total supply of CROWN
    Returns:
        Total supply of CROWN
    """

    # Call the contract
    balance = blockchain.call(
        to=blockchain.crownToken, 
        method="totalSupply", 
        params=None, 
        height=blockchain.blockHeight)
    
    amount = int(balance, 16) * 1e-18

    return round(amount, 2)

# Lands
def land_getLandInfo(nftId: int) -> dict:
    """
    Query for one nft. 
    Contract name: Emerald City Land.

    Args:
        nftId: the ID of the nft queried (in dec)

    Returns: 
        A list of all nft traits
    """
    # Call the contract
    balance = blockchain.call(
        to=blockchain.emeraldCityLand, 
        method="getLandInfo", 
        params={"nftId": hex(nftId)}, 
        height=blockchain.blockHeight)    
    
    return balance

def land_getOwnersNfts(address: str) -> list:
    """
    Query for one address.
    Contract name: Emerald City Land.

    Args:
        address: the wallet addres for which to query

    Returns: 
        A list of all nfts owned
    """
    page = 1
    nftList = []

    # Call the contract
    balance = blockchain.call(
        to=blockchain.emeraldCityLand, 
        method="getOwnersNfts", 
        params={"address": address, "page": page}, 
        height=blockchain.blockHeight)
    
    # Append the first page to the list
    nftList.append(balance["nftList"])

    # Loop until pages end if multiple
    while int(balance["totalPage"], 16) > page:
        page = page + 1
        balance = blockchain.call(
            to=blockchain.emeraldCityLand, 
            method="getOwnersNfts", 
            params={"address": address, "page": page}, 
            height=blockchain.blockHeight)
        nftList.append(balance["nftList"])

    # Flatten the lists and convert to dec
    flatList = [int(item, 16) for sublist in nftList for item in sublist]

    return flatList    

# Output functions
# Total holdings by address in a table
def output_total_holdings(addresses: list) -> pd.DataFrame:
    """
    Query to see how many nfts are in a wallet.

    Args:
        addresses: list of all addresses passed from wallet.addresses

    Returns:
        A pandas dataframe with multiple columns
    """
    
    # Init empty lists 
    nft_amounts = []
    gbet_amounts = []
    goldenkey_amounts = []
    crown_amounts = []
    land_amounts = []

    for address in addresses:

        # Query the blockchain for data
        nft_amount = len(gangsta_getAllNftOwned(address))
        gbet_amount = gbet_balanceOf(address)
        goldenkey_amount = goldenkey_balanceOf(address)
        crown_amount = crown_balanceOf(address)
        land_amount = len(land_getOwnersNfts(address))

        # Append to corresponding lists
        nft_amounts.append(nft_amount) 
        gbet_amounts.append(gbet_amount)
        goldenkey_amounts.append(goldenkey_amount)
        crown_amounts.append(crown_amount)
        land_amounts.append(land_amount)

    # Create dataframe
    data = {
        "address": addresses,
        "nft": nft_amounts,
        "gbet": gbet_amounts,
        "goldenkey": goldenkey_amounts,
        "crown": crown_amounts,
        "lands": land_amounts
    }    
    df = pd.DataFrame(data)

    return df    

# Rankings by showing % of supply owned.
def output_rankings(amounts: pd.DataFrame) -> str:
    """
    Query to show % of holdings compared to total supply.
    Can be used separately or inside the output_total_holdings functions

    Args:
        amounts: dataframe from output_total_holdings function

    Returns:
        A pandas dataframe with multiple columns 
    """

    # Sum the relevant columns
    nft_holdings = amounts["nft"].sum()
    gbet_holdings = amounts["gbet"].sum()
    goldenkey_holdings = amounts["goldenkey"].sum()
    crown_holdings = amounts["crown"].sum()

    # Get total supply for each item
    nft_supply = 5555
    gbet_supply = gbet_totalSupply()
    goldenkey_supply = goldenkey_totalSupply()
    crown_supply = crown_totalSupply()

    # Create message
    text = f"""
    Your rankings (holdings / supply)
    NFT: {nft_holdings} / {nft_supply} -> {nft_holdings/nft_supply*100:,.2f} %
    GBET: {gbet_holdings} / {gbet_supply} -> {gbet_holdings/gbet_supply*100:,.2f} %
    Golden Key: {goldenkey_holdings} / {goldenkey_supply} -> {goldenkey_holdings/goldenkey_supply*100:,.2f} %
    CROWN: {crown_holdings} / {crown_supply} -> {crown_holdings/crown_supply*100:,.2f} %
    """

    return text

# NFT list and traits for a single address, searched by the last 3 characters
def output_singular_gangsta_list() -> pd.DataFrame:
    """
    Queries the chain for NFTs in a wallet and traits for each NFT.
    The function inside prompts the user for the last 3 digits of the address to query so there's no need for args.

    Args:
        none

    Returns
        A dataframe containing the NFT list, their respective traits and link to craft.network
    """
    # Init empty lists for character attributes
    characterLevel_list = []
    characterName_list = []
    className_list = []
    currentExp_list = []
    currentExpPercent_list = []
    isGangster_list = []
    levelTitle_list = []

    # Query the contract and extract the NFT list for the wallet
    address = str(wallet.search_address()[0])
    nft_list = gangsta_getAllNftOwned(address)

    # Loop through every NFT in the NFT list and query the contract for stats
    for nft in nft_list:

        # Get NFT data
        data = gangsta_getCharacterInfo(nft)
        characterLevel = data["characterLevel"]
        characterName = data["characterName"]
        className = data["className"]
        currentExp = data["currentExp"]
        currentExpPercent = data["currentExpPercent"]
        isGangster = data["isGangster"]
        levelTitle = data["levelTitle"]

        # Append to lists for dataframe
        characterLevel_list.append(int(characterLevel, 16))
        characterName_list.append(characterName)
        className_list.append(className)
        currentExp_list.append(int(currentExp, 16))
        currentExpPercent_list.append(int(currentExpPercent, 16))
        isGangster_list.append(int(isGangster, 16))
        levelTitle_list.append(levelTitle)

    # Create list with craft.network links for every NFT
    craft_link_list = [f"https://craft.network/nft/gangstabet:{item}" for item in nft_list]

    # Compile the data into a dict for dataframe
    data = {
        "address": address,
        "nft_id": nft_list,
        "characterLevel": characterLevel_list,
        "characterName": characterName_list,
        "className": className_list,
        "currentExp": currentExp_list,
        "currentExpPercent": currentExpPercent_list,
        "isGangster": isGangster_list,
        "levelTitle": levelTitle_list,
        "craft_link": craft_link_list
        }

    df = pd.DataFrame(data)

    return df

def output_singular_land_list() -> pd.DataFrame:
    """
    Queries the chain for NFTs in a wallet and traits for each NFT.
    The function inside prompts the user for the last 3 digits of the address to query so there's no need for args.

    Args:
        none

    Returns
        A dataframe containing the NFT list, their respective traits and link to craft.network
    """

    # Init empty lists for character attributes
    id_list = []
    name_list = []
    xcoord_list = []
    ycoord_list = []
    zone_list = []
    zone_name_list = []

    # Query the contract and extract the NFT list for the wallet
    address = str(wallet.search_address()[0])
    nft_list = land_getOwnersNfts(address)

    # Loop through every NFT in the NFT list and query the contract for stats
    for nft in nft_list:

        # Get NFT data
        data = land_getLandInfo(nft)
        id = data["id"]
        name = data["name"]
        xcoord = data["orthogonalXCoordinate"]
        ycoord = data["orthogonalYCoordinate"]
        zone = data["zoneId"]

        # Append to lists for dataframe
        id_list.append(id)
        name_list.append(name)
        xcoord_list.append(xcoord)
        ycoord_list.append(ycoord)
        zone_list.append(zone)
        zone_name_list.append(get_zone(zone))

    # Create list with craft.network links for every NFT
    craft_link_list = [f"https://craft.network/nft/emerald-city-land:{item}" for item in nft_list]

    # Compile the data into a dict for dataframe
    data = {
        "id": id_list,
        "name": name_list,
        "xcoord": xcoord_list,
        "ycoord": ycoord_list,
        "zone": zone_list,
        "zone_name": zone_name_list,
        "craft_link": craft_link_list
    }

    df = pd.DataFrame(data)

    return df    

# Various helper functions
# Lookup function for zone id -> zone name
def get_zone(key: str) -> str:
    """
    Funtion to lookup the zoneId which is not provided onchain.
    There are 8 zones.

    Args:
        key: str

    Returns:
        A string containing the name of the zone.
    """

    # Create lookup dict
    zone_lookup = {
    "1": "recreational",
    "2": "airport",
    "3": "industrial",
    "4": "governmental",
    "5": "education",
    "6": "health",
    "7": "commercial",
    "8": "residential"
    }
    
    return zone_lookup.get(key)

