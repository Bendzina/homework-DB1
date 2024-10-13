import sqlite3

# Book კლასის განსაზღვრა
class Book:
    def __init__(self, title, author, release_year, isbn):
        self.title = title
        self.author = author
        self.release_year = release_year
        self.isbn = isbn

# მონაცემთა ბაზის ფუნქციონალი
class BookDatabase:
    def __init__(self, db_name="books.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS books
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT,
                            author TEXT,
                            release_year INTEGER,
                            isbn TEXT UNIQUE)''')
        self.conn.commit()

    def add_book(self, book):
        try:
            self.cursor.execute('''INSERT INTO books (title, author, release_year, isbn)
                                   VALUES (?, ?, ?, ?)''',
                                   (book.title, book.author, book.release_year, book.isbn))
            self.conn.commit()
            print("წიგნი წარმატებით დაემატა")
        except sqlite3.IntegrityError:
            print("წიგნი მსგავსი ISBN-ით უკვე არსებობს")

    def get_all_books(self):
        self.cursor.execute("SELECT * FROM books")
        return self.cursor.fetchall()

    def search_book(self, isbn):
        self.cursor.execute("SELECT * FROM books WHERE isbn = ?", (isbn,))
        return self.cursor.fetchone()

    def update_book(self, isbn, new_title=None, new_author=None, new_release_year=None):
        book = self.search_book(isbn)
        if book:
            updated_title = new_title if new_title else book[1]
            updated_author = new_author if new_author else book[2]
            updated_release_year = new_release_year if new_release_year else book[3]
            self.cursor.execute('''UPDATE books
                                   SET title = ?, author = ?, release_year = ?
                                   WHERE isbn = ?''',
                                   (updated_title, updated_author, updated_release_year, isbn))
            self.conn.commit()
            print("წიგნის დეტალები განახლდა")
        else:
            print("წიგნი ვერ მოიძებნა")

    def delete_book(self, isbn):
        self.cursor.execute("DELETE FROM books WHERE isbn = ?", (isbn,))
        self.conn.commit()
        print("წიგნი წარმატებით წაიშალა")

# მენიუზე ორიენტირებული ინტერფეისი
def menu():
    db = BookDatabase()

    while True:
        print("\n--- მენიუ ---")
        print("1. ახალი წიგნის დამატება")
        print("2. ყველა წიგნის წაკითხვა")
        print("3. წიგნის ძიება ISBN-ის მიხედვით")
        print("4. წიგნის დეტალების განახლება")
        print("5. წიგნის წაშლა")
        print("6. პროგრამიდან გასვლა")
        
        choice = input("აირჩიეთ მოქმედება (1-6): ")

        if choice == '1':
            title = input("შეიყვანეთ წიგნის სათაური: ")
            author = input("შეიყვანეთ ავტორი: ")
            release_year = int(input("შეიყვანეთ გამოშვების წელი: "))
            isbn = input("შეიყვანეთ ISBN: ")
            new_book = Book(title, author, release_year, isbn)
            db.add_book(new_book)

        elif choice == '2':
            books = db.get_all_books()
            for book in books:
                print(book)

        elif choice == '3':
            isbn = input("შეიყვანეთ ISBN: ")
            book = db.search_book(isbn)
            if book:
                print(book)
            else:
                print("წიგნი ვერ მოიძებნა")

        elif choice == '4':
            isbn = input("შეიყვანეთ განსახლებელი წიგნის ISBN: ")
            title = input("შეიყვანეთ ახალი სათაური (თუ არ გსურთ შეცვლა, დატოვეთ ცარიელი): ")
            author = input("შეიყვანეთ ახალი ავტორი (თუ არ გსურთ შეცვლა, დატოვეთ ცარიელი): ")
            release_year = input("შეიყვანეთ ახალი გამოშვების წელი (თუ არ გსურთ შეცვლა, დატოვეთ ცარიელი): ")
            db.update_book(isbn, new_title=title, new_author=author, new_release_year=release_year)

        elif choice == '5':
            isbn = input("შეიყვანეთ წასაშლელი წიგნის ISBN: ")
            db.delete_book(isbn)

        elif choice == '6':
            print("პროგრამიდან გასვლა...")
            break

        else:
            print("არასწორი არჩევანი, გთხოვთ სცადოთ თავიდან")

# პროგრამის გაშვება
if __name__ == "__main__":
    menu()
