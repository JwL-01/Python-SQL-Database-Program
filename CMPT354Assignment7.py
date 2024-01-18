import pyodbc
import uuid # Library for creating custom unique id

## Helper function for login function
def verifyLogin(userid):
    query="SELECT user_id, name FROM user_yelp WHERE user_id=?"
    cur.execute(query, (userid,))
    user = cur.fetchone()
    if user:
        return user
    else:
        return False

# Function 1: Login
def Login():
    print ("")
    print(" -----------== Welcome to the Yelp Database! ==----------- ")
    while True:
        print ("")
        user_id = input("Please type your Yelp userID or type quit to exit: ")
        if user_id.lower() == "quit":
            break
        user = verifyLogin(user_id)
        if user:
            print ("")
            print(f"Hello {user[1]}!")
            global curr_user
            curr_user = user[0]
            print ("")
            print(f"System Tracking - The Current userID is: {user[0]}")
            return user[0]
        else:
            print ("")
            print("Invalid userID! Please provide a valid userID.")

# Function 2: Search Business
def SearchBusiness():
    print ("")
    min_star_valid = False
    max_star_valid = False
    # Iniitialize the minimum star value from all businesses
    min_star_query = "SELECT MIN(stars) FROM business"
    cur.execute(min_star_query)
    default_min = cur.fetchone()[0]
    # Iniitialize the maximum star value from all businesses
    max_star_query = "SELECT MAX(stars) FROM business"
    cur.execute(max_star_query)
    default_max = cur.fetchone()[0]
    while not min_star_valid:
        min_star_input = input('Please enter the minimal stars for the business search: ')
        if not min_star_input:
            min_star_query = "SELECT MIN(stars) FROM business"
            cur.execute(min_star_query)
            min_star_input= cur.fetchone()[0]
        else:
            if (not min_star_input.isnumeric()) or (int(min_star_input) < 1) or (int(min_star_input) > 5):
                print("Error: The stars must be a valid number from 1 to 5")
            else:
                min_star_valid = True
    print("")
    while not max_star_valid:
        max_star_input = input('Please enter the maximum stars for the business search: ')
        if not max_star_input:
            max_star_query= "SELECT MAX(stars) FROM business"
            cur.execute(max_star_query)
            max_star_input= cur.fetchone()[0]
        else:
            if (not max_star_input.isnumeric()) or (int(max_star_input) > 5) or (int(max_star_input) < 1):
                print("Error: The stars must be a valid number from 1 to 5")
            else:
                max_star_valid = True
    print("")
    city = input('Please enter the name of the city, or hit enter to skip: ')
    if not city:
        city = "%"
    else:
        city = '%' + city + '%'
    print ("")
    name = input('Please enter the name of the business, or hit enter to skip: ')
    if not name:
        name = '%'
    else:
        name = '%' + name + '%'
    query = "SELECT business_id, name, address, city, stars FROM business WHERE city LIKE ? AND name LIKE ? AND stars <=? AND stars >=? ORDER BY name;"
    cur.execute(query, (city, name, max_star_input, min_star_input))
    all_businesses = cur.fetchall()
    if not all_businesses:
        print ("")
        print("No businesses was found.")
        return "Search Complete."
    for row in all_businesses:
        print(f"Business ID: {row[0]}")
        print(f"Name: {row[1]}")
        print(f"Address: {row[2]}")
        print(f"City: {row[3]}")
        print(f"Stars: {row[4]}\n")
    return "Search Complete!"

## Helper function for Seach User function
def attribute(attribute_name):
    valid = False
    while not valid:
        print ("")
        attribute_value = input(f"Filter result for if user is: {attribute_name} (Enter Yes/No)")
        try:
            attr_value = str(attribute_value)
            attribute_value = attribute_value.strip().lower()
            if attribute_value.lower() == 'yes':
                valid = True
                return f"{attribute_name} > 0"
            elif attribute_value == 'no':
                valid = True
                return f"{attribute_name} = 0"
            else:
                print("Invalid input. Please enter 'Yes' or 'No'.")
        except ValueError:
            if not attribute_value:
                return f"{attribute_name} = 0"
            print(f"Invalid input. Please enter 'Yes' or 'No'.")

# Function 3: Search Users
def SearchUsers():
    print ("")
    name = input('Please enter a users name:').strip()
    name = f"%{name.lower()}%" if name else '%'
    query = f"""SELECT user_id, name, useful, funny, cool, yelping_since FROM user_yelp WHERE name LIKE ? and {attribute('useful')}
                and {attribute('funny')} and {attribute('cool')} ORDER BY name;"""
    cur.execute(query, [name,])
    global all_user
    all_user = cur.fetchall()
    if len(all_user) == 0:
        print ("")
        print("No user was found.")
        return 'Search Complete.'
    else:
        print('-' * 80)
        for row in all_user:
            print(f"User ID: {row[0]}")
            print(f"Name: {row[1]}")
            print(f"Useful: {row[2]}")
            print(f"Funny: {row[3]}")
            print(f"Cool: {row[4]}")
            print(f"Yelping_Since: {row[5]}\n")
        print ("")
        return 'Search Complete!'

# Function 4: Make friend
def MakeFriend():
    print ("")
    while True:
        print ("")
        friend = input('Enter your friends userID: ')
        if not friend:
            print ("")
            print('Invalid input. Please enter a valid userID.')
            continue
        query_user = "SELECT user_id FROM user_yelp WHERE user_id=?"
        cur.execute(query_user, (friend,))
        if not cur.fetchone():
            print ("")
            print(f'No such user was found. Please enter a valid userID.')
            continue
        query = "INSERT INTO friendship VALUES (?, (SELECT user_id FROM user_yelp WHERE user_id=?))"
        query2 = "SELECT name FROM user_yelp WHERE user_id = ?"
        try:
            cur.execute(query, (curr_user, friend))
            conn.commit()
            cur.execute(query2, (friend))
            friend_name = cur.fetchone()
            friend_name = str(friend_name).replace("(", "")
            friend_name = str(friend_name).replace(")", "")
            friend_name = str(friend_name).replace(",", "")
            print ("")
            return f'You have added {friend_name} as your friend!'
        except Exception as e:
            print ("")
            return 'You are already friends with this user!'

# Funciton 5: Write Review
def WriteReview():
    while True:
        print ("")
        business_id = input('Please enter the business ID of the business you want to review for:')
        if business_id:
            # Check if business_id is valid
            query = "SELECT COUNT(*) FROM business WHERE business_id = ?"
            cur.execute(query, [business_id])
            row = cur.fetchone()[0]
            if not row:
                print ("")
                print('Invalid business_id. Please try again.')
            else:
                break
        else:
            print ("")
            print('Must enter a business_id for review. Please try again.')
    while True:
        print ("")
        stars = input('Please give a star rating, range from 1 to 5: ')
        try:
            stars = float(stars)
            if 0 < stars <= 5:
                break
            else:
                print ("")
                print('Star rating must be between 1 and 5. Please try again.')
        except ValueError:
            print('Invalid input. Please enter a number between 1 and 5 for rating.')
    review_id = ''
    while len(review_id) == 0:
        temp =  str(uuid.uuid4())[:22]
        query = "SELECT review_id FROM review WHERE review_id=?"
        cur.execute(query, [temp])
        row = cur.fetchone()
        if not row:
            review_id = temp
            break
    query = "INSERT INTO review (review_id, business_id, user_id, stars) values ('{0}', '{1}', '{2}', {3})".format(review_id,business_id,curr_user,stars)
    cur.execute(query)
    conn.commit()
    print ("")
    return 'Review inserted succussfully!'

def main():
    if not Login():
        print ("")
        print("Goodbye!")
        return
    running = True
    while running:
        print("")
        print('Please select one of the following actions')
        print("")
        print('1. Search Business')
        print('2. Search for a User')
        print('3. Make a Friend')
        print('4. Review a Business')
        print("")
        user_input = input('Choose from options 1 to 4: ')
        print('You selected option: '+ user_input)
        if int(user_input) == 1:
            print("")
            print('Search for a business and filter results with star count, city and name.')
            SearchBusiness()
        elif int(user_input) == 2:
            print("")
            print('Search for a user and filter results with name, review count and average stars.')
            SearchUsers()
        elif int(user_input) == 3:
            print("")
            print('Make a friend by entering the userID of the user.')
            MakeFriend()
        elif int(user_input) == 4:
            print("")
            print('Create a review for a business by rating them stars.')
            WriteReview()
        else:
            print("")
            print('Invalid input, please enter digits 1-4.')

conn = pyodbc.connect ('driver={SQL Server};Server=cypress.csil.sfu.ca;user=s_lijackyl;password=77bLjtyRQmjgJeNR;Trusted_Connection=yes;')
cur = conn.cursor()

print ("")
print("Connection to Yelp Database Successful!")
main()
conn.close()