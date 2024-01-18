# Python SQL Database Program
The Database Application is designed to interact with a Yelp databse using the pyodbc library for ODBC integration. This application is a simple terminal interface to access and manage information stored in the Yelp database.

**Introduction**
---
Key Features:

Login
1. This function allows the user to log in the interface to have access to all other
functionalities. The user must be remembered by the system for further operations in the
same session.
2. The user must enter a valid user ID.
3. If the user ID is invalid, an appropriate message should be shown to the user.
   
Search Business
1. This function allows the user to search for businesses that satisfy certain criteria.
2. A user should be able to set the following filters as their search criteria: minimum number
of stars, city, and name (or part of the name). The search is not case-sensitive. It means that
the search for upper or lower case must return the same results.
3. The user can choose one of the following three orderings of the results: by name, by city,
or by number of stars.
4. After the search is complete, a list of search results must be shown to the user. The list
must include the following information for each business: id, name, address, city and
number of stars. The results must be ordered according to the chosen attribute. The results
can be shown on the terminal or in a GUI.
5. If the search result is empty, an appropriate message should be shown to the user.
Search Users
6. This function allows the user to search for users that satisfy certain criteria.
7. A user should be able to set the following filters as their search criteria: name (or a part of
the name), review count, average stars. The search is not case-sensitive.
8. After the search is complete, a list of search results must be shown to the user. The list
must include the following information for each user: id, name, review count, useful,
funny, cool, average stars, and the date when the user was registered at Yelp. The results
must be ordered by name. The results can be shown on the terminal or in a GUI.
9. If the search result is empty, an appropriate message should be shown to the user.
    
Make Friend
1. A user must be able to select another user from the results of the function Search Users and
create a friendship. This can be done by entering the user’s ID in a terminal or by clicking
on a user in a GUI. The selected user will be a friend of the user that is logged in to the
database.
2. The friendship should be recorded in the Friendship table

Review Business
1. A user should be able to review a business.
2. To make a review, a user must enter the business’s ID in a terminal or click on a business
returned by Search Business in a GUI.
3. The user must provide the number of stars (integer between 1 and 5).
4. The review should be recorded in the Review table. Consider the ID of the logged user and
the current date.
5. The program should update the number of stars and the count of reviews for the reviewed
business. You need to make sure that the triggers you implemented in assignment 4 are
working properly with your application program.

![image](https://github.com/JwL-01/Python-SQL-Database-Program/blob/main/login.jpg)
