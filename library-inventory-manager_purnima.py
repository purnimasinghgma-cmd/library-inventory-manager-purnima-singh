import json
from pathlib import Path
import logging

logging.basicConfig(filename="library.log", level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def __str__(self):
        return f"{self.title} by {self.author}, ISBN: {self.isbn}, Status: {self.status}"

    def to_dict(self):
        return {"title": self.title, "author": self.author, "isbn": self.isbn, "status": self.status}

    def issue(self):
        if self.status == "available":
            self.status = "issued"
            return True
        return False

    def return_book(self):
        if self.status == "issued":
            self.status = "available"
            return True
        return False

    def is_available(self):
        return self.status == "available"

class LibraryInventory:
    def __init__(self, json_file="books.json"):
        self.books = []
        self.json_file = Path(json_file)
        self.load_books()

    def add_book(self, book):
        self.books.append(book)
        logging.info(f"Added book: {book.title}")
        self.save_books()

    def search_by_title(self, title):
        return [book for book in self.books if title.lower() in book.title.lower()]

    def search_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def display_all(self):
        if not self.books:
            print("No books in inventory.")
            return
        for book in self.books:
            print(book)

    def save_books(self):
        try:
            with open(self.json_file, "w") as f:
                json.dump([book.to_dict() for book in self.books], f, indent=4)
        except Exception as e:
            logging.error(f"Error saving books: {e}")

    def load_books(self):
        if not self.json_file.exists():
            self.books = []
            return
        try:
            with open(self.json_file, "r") as f:
                data = json.load(f)
                self.books = [Book(**item) for item in data]
        except Exception as e:
            logging.error(f"Error loading books: {e}")
            self.books = []

def main():
    inventory = LibraryInventory()

    while True:
        print("\nLibrary Inventory Menu:")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search by Title")
        print("6. Search by ISBN")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            title = input("Enter title: ").strip()
            author = input("Enter author: ").strip()
            isbn = input("Enter ISBN: ").strip()
            if inventory.search_by_isbn(isbn):
                print("Error: Book with this ISBN already exists.")
                continue
            book = Book(title, author, isbn)
            inventory.add_book(book)
            print("Book added successfully.")
        elif choice == "2":
            isbn = input("Enter ISBN of book to issue: ").strip()
            book = inventory.search_by_isbn(isbn)
            if not book:
                print("Book not found.")
            elif book.issue():
                inventory.save_books()
                print("Book issued successfully.")
            else:
                print("Book is already issued.")
        elif choice == "3":
            isbn = input("Enter ISBN of book to return: ").strip()
            book = inventory.search_by_isbn(isbn)
            if not book:
                print("Book not found.")
            elif book.return_book():
                inventory.save_books()
                print("Book returned successfully.")
            else:
                print("Book was not issued.")
        elif choice == "4":
            inventory.display_all()
        elif choice == "5":
            title = input("Enter title to search: ").strip()
            results = inventory.search_by_title(title)
            if results:
                for b in results:
                    print(b)
            else:
                print("No matching books found.")
        elif choice == "6":
            isbn = input("Enter ISBN to search: ").strip()
            book = inventory.search_by_isbn(isbn)
            if book:
                print(book)
            else:
                print("Book not found.")
        elif choice == "7":
            print("Exiting library inventory manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")

if __name__ == "__main__":
    main()
