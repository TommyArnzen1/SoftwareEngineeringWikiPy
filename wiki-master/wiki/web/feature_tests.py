# Feature tests.

# Feature One - PDF Coverter
import pypandoc
import os

# Feature Two - PDF Email
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders

# Feature Three - Login
import sqlite3
from flask import session
conn = sqlite3.connect('database.db')
cursor = conn.cursor()


# Feature One - PDF Converter
# Should display - "Feature One True".

# Convert the sample markdown file to a PDF file.
pypandoc.convert('../../content_test/test.md', 'pdf', outputfile="PDF_test/test.pdf", extra_args=['-V', 'geometry:margin=1.5cm'])

# Store the location where the converted file should be stored.
filename = "PDF_test/test.pdf"

# Check if the file was converted.
if os.path.exists(filename):

    # If the file was converted display a message.
    print("Feature One True")
else:

    # If the file was not converted display a message.
    print("Feature One False")





# Feature Two - PDF Email
# Should receive an email containing the test.pdf at the email address contained in the "to" variable.

# Convert the markdown file to a PDF file.
pypandoc.convert('../../content_test/test.md', 'pdf', outputfile="PDF_test/test.pdf", extra_args=['-V', 'geometry:margin=1.5cm'])

# Store the username and password for the email account to send the email.
username = 'updatewpy@gmail.com'
password = 'pass1pass1234'

# Store the email that will receive the email message.
to = 'arnzent1@mymail.nku.edu'

# Format the email.
message = MIMEMultipart()
message['From'] = username
message['To'] = "[" + to + "]"

# Add the subject.
message['Subject'] = "Check"

# Add the body message.
body = "Email sent from wikiPy."

body_send = MIMEText(body, 'plain')
message.attach(body_send)

# Store the location of the converted PDF file.
filename = "PDF_test/test.pdf"

# Add the PDF file to the email.
element = MIMEBase('application', "octet-stream")
element.set_payload(open(filename, "rb").read())
encoders.encode_base64(element)
element.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(filename))
message.attach(element)

# Send the email.
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.ehlo()
server.login(username, password)
server.sendmail(username, to, message.as_string())
server.close()





# Feature Three - Login
# Add "Check_User" to the database with password "Check".
# Check to see if the user was entered into the database.
# Result should be "Feature Three True" if the username and password are found to be in the database.

# Declare a variable to check if the feature three is executed.
check_three = 0

# Add the sample username and password to the database.
cursor.execute("DROP TABLE Users")
cursor.execute("CREATE TABLE Users(id INTEGER PRIMARY KEY AUTOINCREMENT , name TEXT, username TEXT, password TEXT)")
cursor.execute(("INSERT INTO Users('name', 'username', 'password') VALUES('name', 'Check_User', 'Check')"))

# Get the username and password entered by the user.
username = "Check_User"
password = "Check"

# Check to see if the username and password were added to the database.
find_user = ("SELECT * FROM users WHERE username = ? AND password = ?")
cursor.execute(find_user, [(username), (password)])
results = cursor.fetchall()

# Check to see if the username was found in the database.
if results:

    # If the username and password were found in the database display a message.
    print("Feature Three True")
else:

    # If the username and password were not found in the database display a message.
    print("Feature Three False")





# Feature Four - Add and Delete User
# Enter a user into the database, check if the user was entered, delete the user from the database,
# check if the user was deleted.
# Results should be "Feature Four True".

# Declare a check variable.
check_four = 0

# Add the user to the database.
cursor.execute("DROP TABLE Users")
cursor.execute("CREATE TABLE Users(id INTEGER PRIMARY KEY AUTOINCREMENT , name TEXT, username TEXT, password TEXT)")
cursor.execute(("INSERT INTO Users('name', 'username', 'password') VALUES('name', 'Check_User', 'Check')"))

# Get the username and password entered by the user.
username = "Check_User"
password = "Check"

# Check to see if the username and password were entered into the database.
find_user = ("SELECT * FROM users WHERE username = ? AND password = ?")
cursor.execute(find_user, [(username), (password)])
results = cursor.fetchall()

# Check to see if the user was added to the database.
if results:
    check_four = check_four + 1

# Remove the user from the database.
find_user = ("DELETE FROM users WHERE username = ? AND password = ?")
cursor.execute(find_user, [(username), (password)])
cursor.fetchall()

# Check to see if the username and password were removed from the database.
find_user = ("SELECT * FROM users WHERE username = ? AND password = ?")
cursor.execute(find_user, [(username), (password)])
results = cursor.fetchall()

# Check to see if the user was deleted from the database.
if results:

    # If the username and password were not deleted from the database display a message.
    print("Feature Four False")
else:
    check_four = check_four + 1

# Check if the username and password were deleted from the database.
if check_four is 2:

    # If the user was added and deleted from the database display a message.
    print("Feature Four True")
else:

    # If the username and password were not deleted from the database display a message.
    print("Feature Four False")