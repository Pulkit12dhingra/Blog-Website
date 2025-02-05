import sqlite3
import os
import pandas as pd
import argparse

# Create a DataFrame
data = {
    "title": ["Sample"],
    "summary": ["This is a sample article entry"],
    "tag": ["Test"],
    "contributor": ["Pulkit"]
}

df = pd.DataFrame(data)
df.index.name = 'id'
df.reset_index(inplace=True)

# Function to initialize the database
def initialize_db():
    if os.path.exists("articles.db"):
        print("Database already exists.")
    else:
        conn = sqlite3.connect("articles.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                summary TEXT,
                tag TEXT,
                contributor TEXT
            )
        ''')
        df.to_sql("articles", conn, if_exists="replace", index=False)
        conn.commit()
        conn.close()
        print("Database initialized and data inserted.")

# Function to add an article
def add_article(title, summary, tag, contributor):
    conn = sqlite3.connect("articles.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO articles (title, summary, tag, contributor)
        VALUES (?, ?, ?, ?)
    ''', (title, summary, tag, contributor))
    conn.commit()
    conn.close()
    print("Article added successfully!")

# Function to delete an article by title
def delete_article(title):
    conn = sqlite3.connect("articles.db")
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM articles WHERE title = ?
    ''', (title,))
    conn.commit()
    conn.close()
    print("Article deleted successfully!")

# Function to display all articles
def display_articles():
    conn = sqlite3.connect("articles.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM articles')
    rows = cursor.fetchall()
    conn.close()
    
    if rows:
        for row in rows:
            print(f" Title: {row[0]}, Summary: {row[1]}, Tag: {row[2]}, Contributor: {row[3]}")
    else:
        print("No articles found.")

# Argument parser setup
parser = argparse.ArgumentParser(description="Manage articles in the database.")
parser.add_argument("operation", choices=["initialize", "add", "delete", "display"], help="Operation to perform")
parser.add_argument("--title", help="Title of the article")
parser.add_argument("--summary", help="Summary of the article")
parser.add_argument("--tag", help="Tag of the article")
parser.add_argument("--contributor", help="Contributor of the article")

args = parser.parse_args()

# Perform the requested operation
if args.operation == "initialize":
    initialize_db()
else:
    if not os.path.exists("articles.db"):
        print("Database does not exist. Please initialize the database first.")
    elif args.operation == "add":
        if args.title and args.summary and args.tag and args.contributor:
            add_article(args.title, args.summary, args.tag, args.contributor)
        else:
            print("For 'add' operation, please provide title, summary, tag, and contributor.")
    elif args.operation == "delete":
        if args.title:
            delete_article(args.title)
        else:
            print("For 'delete' operation, please provide the title of the article to delete.")
    elif args.operation == "display":
        display_articles()

# Sample usage:
# Initialize the database
# python /Users/pulkit/Desktop/projects/blog-website/contribue.py initialize

# Add an article
# python /Users/pulkit/Desktop/projects/blog-website/contribue.py add --title "New Article" --summary "This is a new article" --tag "News" --contributor "John Doe"

# Delete an article
# python /Users/pulkit/Desktop/projects/blog-website/contribue.py delete --title "New Article"

# Display all articles
# python /Users/pulkit/Desktop/projects/blog-website/contribue.py display
