import mysql.connector
import tkinter as tk
from tkinter import messagebox, filedialog, Listbox, Scrollbar
import os

# Database connection
myDb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="kenya_news"
)
myCursor = myDb.cursor()

# Create Articles table if it doesn't exist
myCursor.execute("""
    CREATE TABLE IF NOT EXISTS Articles (
        AuthorID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        Author VARCHAR(255) NOT NULL,
        Topic VARCHAR(255) NOT NULL,
        Catchword VARCHAR(255) NOT NULL,
        Office VARCHAR(255) NOT NULL,
        Date DATE NOT NULL,
        Photo LONGBLOB
    )
""")

# Function to insert data into the Articles table
def InsertArticle(Author, Topic, Catchword, Office, Date, FilePath):
    try:
        BinaryData = None
        if FilePath:
            with open(FilePath, "rb") as File:
                BinaryData = File.read()
        sqlStatement = """
            INSERT INTO Articles (Author, Topic, Catchword, Office, Date, Photo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        myCursor.execute(sqlStatement, (Author, Topic, Catchword, Office, Date, BinaryData))
        myDb.commit()
        print("Article inserted successfully.")
    except Exception as e:
        print(f"Error inserting article: {e}")


def RetrieveArticlesByAuthorID(AuthorID):
    try:
        sqlStatement = "SELECT AuthorID, Author, Topic, Catchword, Office, Date FROM Articles WHERE AuthorID = %s"
        myCursor.execute(sqlStatement, (AuthorID,))
        return myCursor.fetchall()
    except Exception as e:
        print(f"Error retrieving articles: {e}")
        return []


def RetrievePhoto(AuthorID):
    try:
        sqlStatement = "SELECT Photo FROM Articles WHERE AuthorID = %s"
        myCursor.execute(sqlStatement, (AuthorID,))
        myResult = myCursor.fetchone()
        if myResult and myResult[0]:
            if not os.path.exists('articleOutputs'):
                os.makedirs('articleOutputs')
            storeFilePath = f"articleOutputs/article{AuthorID}.jpg"
            with open(storeFilePath, "wb") as File:
                File.write(myResult[0])
            return storeFilePath
        else:
            return None
    except Exception as e:
        print(f"Error retrieving photo: {e}")
        return None


class ArticleFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Article Filter")

        # AuthorID filter
        self.authorid_label = tk.Label(root, text="Enter AuthorID to filter:")
        self.authorid_label.pack()

        self.authorid_entry = tk.Entry(root)
        self.authorid_entry.pack()

        self.filter_button = tk.Button(root, text="Filter Articles", command=self.filter_articles)
        self.filter_button.pack()

      
        self.articles_listbox = Listbox(root, width=100, height=20)
        self.articles_listbox.pack()

        self.articles_scrollbar = Scrollbar(self.articles_listbox)
        self.articles_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.articles_listbox.config(yscrollcommand=self.articles_scrollbar.set)
        self.articles_scrollbar.config(command=self.articles_listbox.yview)

        self.view_image_button = tk.Button(root, text="View Image", command=self.view_image)
        self.view_image_button.pack()

    def filter_articles(self):
        authorid = self.authorid_entry.get()
        if not authorid.isdigit():
            messagebox.showerror("Invalid input", "Please enter a valid numeric AuthorID")
            return
        articles = RetrieveArticlesByAuthorID(int(authorid))
        self.articles_listbox.delete(0, tk.END)
        for article in articles:
            self.articles_listbox.insert(tk.END, f"ID: {article[0]}, Author: {article[1]}, Topic: {article[2]}, Catchword: {article[3]}, Office: {article[4]}, Date: {article[5]}")

    def view_image(self):
        selected_article = self.articles_listbox.get(tk.ACTIVE)
        if selected_article:
            authorid = int(selected_article.split(",")[0].split(":")[1].strip())
            photo_path = RetrievePhoto(authorid)
            if photo_path:
                os.system(f"start {photo_path}")
            else:
                messagebox.showinfo("No Image", "No image found for this article.")
        else:
            messagebox.showerror("Selection Error", "Please select an article from the list.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ArticleFilterApp(root)
    root.mainloop()


myCursor.close()
myDb.close()
