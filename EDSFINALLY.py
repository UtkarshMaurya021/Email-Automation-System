import pandas as pd
import smtplib as sm
import mysql.connector as sql
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass

# Prompt user for MySQL server details

conn = sql.connect(host='localhost', user='root', passwd='1234', database="ECE")
cur = conn.cursor()
if conn.is_connected:
    print("""

                      =================================================================================
             
                                                    WELCOME  TO  EMAIL AUTOMATION SYSTEM

                                                        MADE BY : UTKARSH KUMAR MAURYA  
                                                                            AYUSH GHOSH
                                                                            ANSHUMAN
                                            DEPARTMENT : ELECTRONICS AND COMMUNICATION

                                                BHARTI VIDYAPEETH COLLEGE OF ENGINEERING

                      =================================================================================
            """)
cur.execute("create table if not exists Students(Name varchar(50), Gmail varchar(50) primary key,Phone_Number bigint(10)) ")

# Read data from MySQL table
cur.execute("SELECT * FROM Students")
rows = cur.fetchall()
df = pd.DataFrame(rows, columns=["Name", "Gmail", "Phone_Number"])
email_col = df["Gmail"]

# Display number of emails in database
print("Total number of emails in database: ", len(email_col))

# Prompt user to select specific member or send email to all members
choice = input("Do you want to send email to a specific member? (y/n): ")
if choice.lower() == 'y':
    name = input("Enter name of member: ")
    # Filter data by member name
    member_data = df[df['Name'] == name]
    email_col = member_data["Gmail"]
    # Display number of emails for the selected member
    print("Total number of emails for member ", name, ": ", len(email_col))

# SMTP email setup
try:
    server = sm.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("mauryautkarshk@gmail.com","qpfgaluahazksnvx")
    from_="mauryautkarshk@gmail.com"
    to_ = list(email_col)
    message = MIMEMultipart("alternative")
    message['Subject'] = "Important update about PBL project"
    message["From"] ="mauryautkarshk@gmail.com"

    # Create HTML message body
    html = '''
    <html>
    <head>
    </head>
    <body>
    <h1>PBL</h1>
    <h2>Check the PBL</h2>
    <p>This is just a testing message from group 3.</p>
    <button style="padding:20px;background:green;color:white">Verify</button>
    <h2>Ignore this message if you have already received one</h2>
    <h2>If it's the first time, please verify.</h2>
    <a href="https://www.example.com">Click here to visit our website</a>
    </body>
    </html>
    
        '''
    

    text = MIMEText(html, "html")
    message.attach(text)

    # Send email
    server.sendmail(from_, to_, message.as_string())
    print("Email sent successfully.")

except sm.SMTPException as e:
    print("Error: ", e)

finally:
    server.quit()
    conn.close()
