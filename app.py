from flask import flash
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DATABASE = 'book_catalogue.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE username = ? AND password = ?',
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    books = conn.execute(
        'SELECT * FROM books WHERE user_id = ?',
        (session['user_id'],)
    ).fetchall()
    conn.close()

    return render_template('dashboard.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        isbn = request.form['isbn']
        response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}')
        data = response.json()

        if 'items' in data:
            books = []
            for item in data['items']:
                book_data = item['volumeInfo']
                books.append({
                    'title': book_data.get('title', 'N/A'),
                    'author': ', '.join(book_data.get('authors', ['N/A'])),
                    'page_count': book_data.get('pageCount', 0),
                    'average_rating': book_data.get('averageRating', 0),
                    'thumbnail': book_data.get('imageLinks', {}).get('thumbnail', ''),
                })
            # Save search results in the session
            session['search_results'] = books

            return render_template('choose_book.html', books=books, enumerate=enumerate)

        else:
            flash('Book not found')
    return render_template('add_book.html')


@app.route('/search_title', methods=['POST'])
def search_title():
    # Get the title input from the form
    title = request.form['title']
    response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=intitle:{title}')
    data = response.json()

    if 'items' in data:
        # Parse the search results
        books = []
        for item in data['items']:
            book_data = item['volumeInfo']
            books.append({
                'title': book_data.get('title', 'N/A'),
                'author': ', '.join(book_data.get('authors', ['N/A'])),
                'page_count': book_data.get('pageCount', 0),
                'average_rating': book_data.get('averageRating', 0),
                'thumbnail': book_data.get('imageLinks', {}).get('thumbnail', ''),
            })

        # Save the results in the session for use in /add_selected_book
        session['search_results'] = books

        # Debug: Print the stored search results to the console
        print(session.get('search_results'))

        return render_template('choose_book.html', books=books, enumerate=enumerate)


    flash('No books found with that title.')
    return redirect(url_for('add_book'))


@app.route('/add_selected_book', methods=['POST'])
def add_selected_book():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Debugging: Verify session search results
    print("Search Results in Session:", session.get('search_results'))

    selected_index = int(request.form['selected_book'])  # Get selected book index
    books = session.get('search_results', [])  # Retrieve search results from session

    if books and 0 <= selected_index < len(books):
        selected_book = books[selected_index]

        # Insert selected book into the database
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO books (user_id, isbn, title, author, page_count, average_rating, thumbnail) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (session['user_id'], '', selected_book['title'], selected_book['author'],
             selected_book['page_count'], selected_book['average_rating'], selected_book['thumbnail'])
        )
        conn.commit()
        conn.close()

        flash('Book added successfully!')
        return redirect(url_for('dashboard'))

    flash('Error adding book. Please try again.')
    return redirect(url_for('add_book'))

@app.route('/delete/<int:id>')
def delete_book(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    conn.execute('DELETE FROM books WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('dashboard'))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Insert new user into the database
        conn = get_db_connection()
        try:
            conn.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, password)
            )
            conn.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists. Please choose another one.')
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
