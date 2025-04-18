import json
import os
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Book:
    title: str
    author: str
    isbn: str
    genre: str
    year_published: int
    date_added: str
    status: str  # "read", "reading", "to_read"

class LibraryManager:
    def __init__(self, data_file: str = "library_data.json"):
        self.data_file = data_file
        self.books: List[Book] = []
        self.load_library()

    def load_library(self) -> None:
        """Load the library data from the JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.books = [Book(**book) for book in data]
            except json.JSONDecodeError:
                print("Error: Invalid JSON file. Starting with empty library.")
                self.books = []
        else:
            self.books = []

    def save_library(self) -> None:
        """Save the library data to the JSON file."""
        with open(self.data_file, 'w') as f:
            json.dump([book.__dict__ for book in self.books], f, indent=4)

    def add_book(self, title: str, author: str, isbn: str, genre: str, 
                year_published: int, status: str = "to_read") -> None:
        """Add a new book to the library."""
        # Check if book with same ISBN already exists
        if any(book.isbn == isbn for book in self.books):
            print(f"Error: Book with ISBN {isbn} already exists in the library.")
            return

        new_book = Book(
            title=title,
            author=author,
            isbn=isbn,
            genre=genre,
            year_published=year_published,
            date_added=datetime.now().strftime("%Y-%m-%d"),
            status=status
        )
        self.books.append(new_book)
        self.save_library()
        print(f"Book '{title}' added successfully!")

    def remove_book(self, isbn: str) -> None:
        """Remove a book from the library by ISBN."""
        for i, book in enumerate(self.books):
            if book.isbn == isbn:
                removed_book = self.books.pop(i)
                self.save_library()
                print(f"Book '{removed_book.title}' removed successfully!")
                return
        print(f"Error: Book with ISBN {isbn} not found in the library.")

    def search_books(self, query: str) -> List[Book]:
        """Search for books by title, author, or ISBN."""
        query = query.lower()
        return [
            book for book in self.books
            if query in book.title.lower() or
               query in book.author.lower() or
               query in book.isbn.lower() or
               query in book.genre.lower()
        ]

    def list_books(self) -> None:
        """Display all books in the library."""
        if not self.books:
            print("The library is empty.")
            return

        print("\nLibrary Contents:")
        print("-" * 80)
        for i, book in enumerate(self.books, 1):
            print(f"{i}. {book.title} by {book.author}")
            print(f"   ISBN: {book.isbn}, Genre: {book.genre}")
            print(f"   Published: {book.year_published}, Status: {book.status}")
            print(f"   Added: {book.date_added}")
            print("-" * 80)

    def update_book_status(self, isbn: str, new_status: str) -> None:
        """Update the status of a book."""
        for book in self.books:
            if book.isbn == isbn:
                book.status = new_status
                self.save_library()
                print(f"Status updated successfully for '{book.title}'!")
                return
        print(f"Error: Book with ISBN {isbn} not found in the library.")

def main():
    library = LibraryManager()
    
    while True:
        print("\nPersonal Library Manager")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Search books")
        print("4. List all books")
        print("5. Update book status")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter author: ")
            isbn = input("Enter ISBN: ")
            genre = input("Enter genre: ")
            year = int(input("Enter year published: "))
            status = input("Enter status (read/reading/to_read): ")
            library.add_book(title, author, isbn, genre, year, status)
            
        elif choice == "2":
            isbn = input("Enter ISBN of the book to remove: ")
            library.remove_book(isbn)
            
        elif choice == "3":
            query = input("Enter search query: ")
            results = library.search_books(query)
            if results:
                print("\nSearch Results:")
                for book in results:
                    print(f"- {book.title} by {book.author} (ISBN: {book.isbn})")
            else:
                print("No books found matching your search.")
                
        elif choice == "4":
            library.list_books()
            
        elif choice == "5":
            isbn = input("Enter ISBN of the book to update: ")
            new_status = input("Enter new status (read/reading/to_read): ")
            library.update_book_status(isbn, new_status)
            
        elif choice == "6":
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
    library = LibraryManager()
    book = Book(
        title="The Great Gatsby",
        author="F. Scott Fitzgerald", 
        isbn="9780743273565",
        genre="Fiction",
        year_published=1925,
        date_added=datetime.now().strftime("%Y-%m-%d"),
        status="to_read"
    )
    library.add_book(
        title=book.title,
        author=book.author,
        isbn=book.isbn,
        genre=book.genre,
        year_published=book.year_published,
        status=book.status
    )
    print(f"Added test book: {book.title}")
