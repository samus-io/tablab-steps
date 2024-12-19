import random
import string


# Function to generate a random password
def generate_random_password(length=12):
    """
    Generate a random password of specified length.
    - Password starts and ends with a letter (excluding 'O' and 'o').
    - Middle characters include letters, digits, and symbols.

    Args:
        length (int): Length of the password. Minimum value is 3.

    Returns:
        str: A randomly generated password.
    """
    if length < 3:
        raise ValueError("Password length must be at least 3 characters.")

    # Define character sets excluding 'O' and 'o'
    valid_letters = "".join(c for c in string.ascii_letters if c not in "Oo")
    symbols = "!@#$%^&*_+-=[]{}|:;<>?"
    password_charset = valid_letters + string.digits + symbols

    # Ensure the first and last characters are letters
    password = random.choice(valid_letters)  # Start with a letter
    password += "".join(random.choice(password_charset) for _ in range(length - 2))
    password += random.choice(valid_letters)  # End with a letter

    return password


# Function to generate a random address
def generate_random_address():
    streets = [
        "Ash Ln",
        "Aspen St",
        "Birch Dr",
        "Cedar Rd",
        "Chestnut Ct",
        "Dogwood Rd",
        "Elm Blvd",
        "Fir St",
        "Hickory Rd",
        "Juniper Ave",
        "Magnolia Blvd",
        "Main St",
        "Maple Ave",
        "Oak St",
        "Pine Ln",
        "Poplar Ave",
        "Redwood Dr",
        "Spruce Ct",
        "Sycamore Ln",
        "Willow St",
    ]
    cities = [
        "Bridgeport",
        "Brookfield",
        "Cedarwood",
        "Centerville",
        "Clearwater",
        "Elmwood",
        "Fairview",
        "Georgetown",
        "Greenwood",
        "Hillview",
        "Kingswood",
        "Lakeside",
        "Maplewood",
        "Meadowbrook",
        "Riverside",
        "Silverlake",
        "Springfield",
        "Sunnydale",
        "Westfield",
        "Woodland",
    ]
    states = [
        "AZ",
        "CA",
        "CO",
        "FL",
        "GA",
        "IL",
        "MI",
        "MN",
        "MO",
        "NC",
        "NV",
        "NY",
        "OH",
        "OR",
        "PA",
        "SC",
        "TX",
        "VA",
        "WA",
        "WI",
    ]

    return f"{random.randint(100, 999)} {random.choice(streets)}, {random.choice(cities)}, {random.choice(states)}"


# List of usernames
usernames = [
    "johndoe",
    "alice",
    "jackson01",
    "charlie2023",
    "dianak",
    "eve12",
    "frankie77",
    "gracelee",
    "henrym",
    "isabel23",
    "bobsmith77",
    "michaels",
    "linda22",
    "john87",
    "susan45",
    "chris33",
    "kelly90",
    "robert08",
    "patricia",
    "jennifer",
    "james44",
    "barbara56",
    "matthew88",
    "daniel07",
    "nancy65",
    "laura21",
    "mark76",
    "sandra54",
    "george32",
    "betty49",
    "donald17",
    "dorothy81",
    "joseph02",
    "karen23",
    "nancy66",
    "lisa98",
    "kevin72",
    "paul19",
    "brian64",
    "kimberly",
    "timothy",
    "jason57",
    "cynthia",
    "melissa",
    "jacob34",
    "rachel88",
    "jerry11",
    "jeffrey90",
    "amy77",
    "terry99",
    "donna44",
    "carl19",
    "judith35",
    "wayne67",
    "judy48",
    "sharon27",
    "steven92",
    "shawn88",
    "peter26",
    "dennis14",
    "catherine",
    "maria31",
    "janice52",
    "anthony",
    "walter",
    "rebecca",
    "brenda",
    "arthur23",
    "helen09",
    "sean11",
    "roger48",
    "katherine",
    "harold",
    "jessica",
    "philip",
    "ruth34",
    "andrew88",
    "carl17",
    "louis08",
    "janet42",
    "frances20",
    "craig10",
    "martha55",
    "ann12",
    "lori29",
]

# Generate user credentials with random passwords
user_credentials = [
    {"username": username, "password": generate_random_password(), "address": generate_random_address()}
    for username in usernames
]

# Generate SQL INSERT statements
sql_statements = [
    f'INSERT INTO User (username, password, address) VALUES ("{user["username"]}", "{user["password"]}", "{user["address"]}");'
    for user in user_credentials
]

# Print user credentials array
print("Generated user credentials:")
print(user_credentials)

# Print SQL statements
print("\nGenerated SQL statements:")
print("\n".join(sql_statements))
