import mysql.connector

# Database connection
myDb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="kenya_news"
)
myCursor = myDb.cursor()

# Create table if it doesn't exist
myCursor.execute("""
    CREATE TABLE IF NOT EXISTS Images (
        id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        Photo LONGBLOB NOT NULL
    )
""")

# Function to insert blob into the database
def InsertBlob(FilePath):
    with open(FilePath, "rb") as File:
        BinaryData = File.read()
        sqlStatement = "INSERT INTO Images (Photo) VALUES (%s)"
        myCursor.execute(sqlStatement, (BinaryData,))
        myDb.commit()

# Function to retrieve blob from the database
def RetrieveBlob(ID):
    sqlStatement2 = "SELECT Photo FROM Images WHERE id = %s"
    myCursor.execute(sqlStatement2, (ID,))
    myResult = myCursor.fetchone()
    if myResult:
        storeFilePath = "imageOutputs/img{0}.jpg".format(str(ID))
        with open(storeFilePath, "wb") as File:
            File.write(myResult[0])
        print(f"Image retrieved and saved to {storeFilePath}")
    else:
        print(f"No image found with ID {ID}")

# Main menu
print("1. Insert image\n2. Read Image\n")
menuInput = input("Choose an option: ")
if int(menuInput) == 1:
    UserFilePath = input("Enter file path: ")
    InsertBlob(UserFilePath)
elif int(menuInput) == 2:
    userIDChoice = input("Enter ID: ")
    RetrieveBlob(userIDChoice)
else:
    print("Invalid option selected")

# Close the cursor and the connection
myCursor.close()
myDb.close()
