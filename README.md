# IS211_BookCatalogue
Book Catalogue Web Application - Overview

The Book Catalogue Web Application which I titled "My Book Haven" is a simple and functional web-based solution designed to help users manage their personal book collection. Built using Flask and SQLite, the application allows users to log in, search for books using either ISBN or title, and save them to their personal collection. The application utilizes the Google Books API to fetch accurate and detailed book data, including the title, author, page count, average rating, and book cover thumbnails.

This application demonstrates a practical implementation of key web development concepts, including user authentication, database management, API integration, and dynamic rendering of web pages. The interface is user-friendly and provides essential functionality for managing books efficiently.

How It Works
User Authentication:

Users must log in to access their personal dashboard.
New users can register by creating a username and password. The application securely stores this information in the users table of the database.
Search for Books:

Search by ISBN: Users can input an ISBN to search for a specific book. The application queries the Google Books API and displays the result.
Search by Title: Users can input a book title, and the application will fetch multiple matching results from the API. The user can select the desired book from the list.
Adding Books:

Once a user selects a book, it is added to their personal collection and displayed on their dashboard.
The app stores the book's metadata, including the title, author, page count, average rating, and thumbnail URL, in the books table.
Viewing the Dashboard:

The dashboard displays a list of all books saved by the logged-in user. Each book is presented with its title, author, and cover thumbnail.
Deleting Books:

Users can remove books from their collection via the dashboard.

Solution Details
The Model
The application uses a simple relational database schema with two main tables:

1. Users Table:

Stores user credentials, including an auto-incremented id, username, and password.
Each user has a unique id that links them to their personal book collection in the books table.

2. Books Table:

Stores metadata about each book, including:
* id: Primary key for the book.
* user_id: Foreign key linking the book to a specific user.
* isbn: ISBN of the book.
* title: Book title.
* author: Author(s) of the book.
* page_count: Number of pages in the book.
* average_rating: Average rating of the book.
* thumbnail: URL to the book's cover image.

Key Features
* Database Integration: SQLite is used to manage user credentials and book data efficiently.
* API Integration: The Google Books API provides accurate and rich metadata about books.
* Dynamic Pages: HTML templates rendered using Flask's Jinja2 engine dynamically display user-specific data.
* User-Specific Data: Each user has their own dashboard, ensuring data isolation and personalized experience.