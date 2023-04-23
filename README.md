
![](img_for_readme/HEADER.png)
_____
A joke database site with **45** categories of jokes, totaling over **130,000** jokes!
_____
## <span style='color:rgb(232, 204, 111)'> Possibilities. </span>
The site is implemented with pre-registration, in order to be able to:
+ joke ratings;
+ sending a new anecdote from the user for consideration by the administrator;
+ consideration of the joke by the administrator: 
  + to confirm the addition of a new joke;
  + to rejection the addition of a new joke.
_____

### <span style='color:rgb(232, 204, 111)'> 1. The first page of the site is the login.</span>
+ On this page, the user can log in, or go to the registration page
+ to go to the page use the direct path /
![](img_for_readme/0.login.jpg)
### <span style='color:rgb(232, 204, 111)'> 2. Registration page. </span>
+ Filling in information: login, email, password, first name, last name
+ to go to the page use the direct path /registration/
![](img_for_readme/1.registration.jpg)
### <span style='color:rgb(232, 204, 111)'> 3. Main page with anekdots from database. </span>
+ Contains jokes, with a choice of a category of jokes, 
with the ability to go to the page - adding a new joke, 
as well as a button to exit the profile;
+ With the ability to evaluate anecdote.
+ to go to the page use the direct path /anek/
![](img_for_readme/2.main.jpg)
### <span style='color:rgb(232, 204, 111)'> 4. Submission page for consideration of adding a new joke to the database. </span>
+ to go to the page use the direct path /new/
![](img_for_readme/3.new_anek.jpg)
### <span style='color:rgb(232, 204, 111)'> 5. Admin page. </span>
+ The page is designed to review new jokes from users, with confirmation of adding a new joke to the database, 
or rejecting it. When reviewing a new joke, the administrator sees the sender's name, 
mail, category of the joke, and the joke itself.
+ To be able to go to this page, you need to access it by changing the user status in the database 
(in the project folder - aneks.db - Users table - column "administrator")
+ to go to the page use the direct path /admin/
![](img_for_readme/4.admin.jpg)
## <span style='color:rgb(232, 204, 111)'> Used frameworks and libraries: </span>
+ Flask;
+ WTF;
+ SQLAlchemy;
+ Flask-login;
+ Werkzeug;
+ Jinja2.
