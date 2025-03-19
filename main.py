import streamlit as st
import sqlite3
import time

# Database setup
def init_db():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        author TEXT,
                        year INTEGER,
                        genre TEXT,
                        read INTEGER)''')
    conn.commit()
    conn.close()

def add_book(title, author, year, genre, read):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, year, genre, read) VALUES (?, ?, ?, ?, ?)", 
                   (title, author, year, genre, int(read)))
    conn.commit()
    conn.close()

def remove_book(title):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE title = ?", (title,))
    conn.commit()
    conn.close()

def search_books(search_term):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", (f"%{search_term}%", f"%{search_term}%"))
    results = cursor.fetchall()
    conn.close()
    return results

def get_all_books():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return books

def get_library_stats():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), SUM(read) FROM books")
    total_books, books_read = cursor.fetchone()
    conn.close()
    return total_books or 0, books_read or 0

# Initialize Database
init_db()

st.title("📚 Personal Library Manager 📖")
st.write("Manage your personal book collection easily! 📔")

menu = st.sidebar.radio("📌 Select an Option", ["Add a Book 🆕", "Remove a Book ❌", "Search a Book 🔍", "Display All Books 📖", "View Library 📊"])

if menu == "Add a Book 🆕":
    st.header("📚 Add a New Book")
    title = st.text_input("📖 Enter Book Title")
    author = st.text_input("✍️ Enter Author Name")
    year = st.number_input("📅 Enter Publication Year", min_value=1000, max_value=2100, step=1)
    genre = st.text_input("📂 Enter Genre")
    read_status = st.checkbox("✅ Mark as Read")
    
    if st.button("➕ Add Book"):
        add_book(title, author, year, genre, read_status)
        st.success("🎉 Book Added Successfully! 📚")
        st.rerun()

elif menu == "Remove a Book ❌":
    st.header("🗑️ Remove a Book")
    books = get_all_books()
    book_titles = [book[1] for book in books]
    
    if book_titles:
        selected_book = st.selectbox("📖 Select a book to remove", book_titles, key="remove_book")
        
        if st.button("❌ Remove Book"):
            remove_book(selected_book)
            st.success("🚀 Book Removed Successfully! 📖")
            st.rerun()
    else:
        st.warning("📭 No books available to remove!")

elif menu == "Search a Book 🔍":
    st.header("🔍 Search for a Book")
    search_term = st.text_input("🔎 Enter title or author name to search")
    if st.button("🔍 Search"):
        results = search_books(search_term)
        if results:
            st.write("🎯 Matching Books:")
            st.table(results)
        else:
            st.warning("❌ No books found with this search term!")

elif menu == "Display All Books 📖":
    st.header("📖 Your Library")
    books = get_all_books()
    if books:
        st.table(books)
    else:
        st.warning("📭 Your library is empty! Start adding books! 📚")

elif menu == "View Library 📊":
    st.header("📊 Library Statistics")
    total_books, books_read = get_library_stats()
    percentage_read = (books_read / total_books * 100) if total_books > 0 else 0
    
    st.write(f"📚 Total Books: {total_books}")
    st.write(f"✅ Books Read: {books_read}")
    st.write(f"📊 Percentage Read: {percentage_read:.2f}%")