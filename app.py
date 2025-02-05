from flask import Flask,render_template,request
import sqlite3

app = Flask(__name__)

# Function to fetch all articles from the database
def get_articles():
    conn = sqlite3.connect("articles.db")  # Connect to SQLite database
    cursor = conn.cursor()
    cursor.execute("SELECT title, summary, tag, contributor FROM articles")  # Fetch all articles
    articles = cursor.fetchall()  # List of tuples
    conn.close()
    return articles


# Function to fetch articles by a specific tag
def get_articles_by_tag(tag):
    conn = sqlite3.connect("articles.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, summary, tag, contributor FROM articles WHERE tag=?", (tag,))
    articles = cursor.fetchall()
    conn.close()
    
    # Convert tuples to a list of dictionaries for JSON response
    return [
        {"title": row[0], "summary": row[1], "tag": row[2], "contributor": row[3]}
        for row in articles
    ]


@app.route("/")
def hello_world():
    #name = "Pulkt"
    return render_template('index.html')#, person=name)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/playlist')
def playlist():
    articles_data = get_articles()  # Fetch all articles from the database
    return render_template('playlist.html', articles=articles_data)

@app.route('/articles')
def articles():
    articles_data = get_articles()  # Fetch articles from DB
    return render_template('articles.html', articles=articles_data)

# Display article details from a separate logic (e.g., stored files)
@app.route('/article/<article_title>')
def display_article(article_title):
    # Logic to get article content from a separate file
    try:
        return render_template(f'Articles/{article_title}.html')  # Load dedicated HTML file
    except:
        return "Article Not Found", 404  # Handle missing files gracefully

@app.route('/contribute')
def contribute():
    return render_template('contribute.html')




if __name__ == '__main__':
    app.run(debug=True)