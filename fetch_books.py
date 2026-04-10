#!/usr/bin/env python3
# ============================================
# READERA - INTELLIGENT BOOK FETCHER & UPDATER
# Creative Commons Books + Automatic HTML Update
# ============================================

import requests
import json
import os
import time
from pathlib import Path
import re

# ============================================
# CONFIGURATION
# ============================================

BOOKS_FOLDER = "books_data"
COVERS_FOLDER = "covers"
os.makedirs(BOOKS_FOLDER, exist_ok=True)
os.makedirs(COVERS_FOLDER, exist_ok=True)

# Creative Commons book sources
SOURCES = {
    "archive_hindi": "https://archive.org/advancedsearch.php?q=collection:booksbylanguage_hindi+AND+mediatype:texts&fl[]=identifier,title,creator,description,licenseurl,date,subject&rows=100&output=json",
    "archive_english": "https://archive.org/advancedsearch.php?q=collection:gutenberg&fl[]=identifier,title,creator,description,licenseurl&rows=50&output=json",
    "archive_sanskrit": "https://archive.org/advancedsearch.php?q=language:san+AND+mediatype:texts&fl[]=identifier,title,creator,description,licenseurl&rows=50&output=json",
}

# ============================================
# BOOK MANAGER CLASS
# ============================================

class BookManager:
    def __init__(self):
        self.books = []
        self.load_existing_books()
    
    def load_existing_books(self):
        """Load already downloaded books"""
        books_index = os.path.join(BOOKS_FOLDER, "index.json")
        if os.path.exists(books_index):
            with open(books_index, 'r', encoding='utf-8') as f:
                self.books = json.load(f)
            print(f"✅ Loaded {len(self.books)} existing books")
    
    def book_exists(self, book_id):
        """Check if book already exists"""
        return any(b['id'] == book_id for b in self.books)
    
    def fetch_from_source(self, source_url, source_name):
        """Fetch books from Creative Commons sources"""
        try:
            print(f"\n📚 Fetching from {source_name}...")
            response = requests.get(source_url, timeout=30)
            data = response.json()
            docs = data.get('response', {}).get('docs', [])
            
            cc_books = []
            for book in docs:
                license_url = book.get('licenseurl', '')
                # Filter for Creative Commons or CC0 licenses
                if 'creativecommons' in license_url.lower() or 'cc0' in license_url.lower() or 'public domain' in license_url.lower():
                    book_id = book['identifier']
                    
                    # Skip if already exists
                    if self.book_exists(book_id):
                        continue
                    
                    cc_books.append({
                        'id': book_id,
                        'title': book.get('title', 'Untitled'),
                        'author': book.get('creator', 'Unknown'),
                        'description': book.get('description', 'No description available.'),
                        'license': license_url,
                        'date': book.get('date', ''),
                        'subject': book.get('subject', []) if isinstance(book.get('subject', []), list) else [book.get('subject', '')],
                        'source': source_name
                    })
            
            print(f"✅ Found {len(cc_books)} new Creative Commons books")
            return cc_books
        except Exception as e:
            print(f"❌ Error fetching from {source_name}: {e}")
            return []
    
    def download_book_text(self, book_id, max_retries=3):
        """Download book text content"""
        urls = [
            f"https://archive.org/stream/{book_id}/{book_id}_djvu.txt",
            f"https://archive.org/download/{book_id}/{book_id}.txt",
            f"https://archive.org/download/{book_id}/{book_id}_text.txt",
            f"https://archive.org/download/{book_id}/page_numbers.json",
        ]
        
        for attempt in range(max_retries):
            for url in urls:
                try:
                    response = requests.get(url, timeout=60)
                    if response.status_code == 200:
                        text = response.text
                        if len(text) > 500:  # Valid text
                            return text
                except:
                    continue
            time.sleep(2)  # Wait before retry
        
        return None
    
    def download_cover_image(self, book_id):
        """Download cover image"""
        urls = [
            f"https://archive.org/services/img/{book_id}",
            f"https://archive.org/download/{book_id}/{book_id}_cover.jpg",
            f"https://archive.org/download/{book_id}/cover.jpg",
            f"https://archive.org/download/{book_id}/{book_id}.jpg",
        ]
        
        for url in urls:
            try:
                response = requests.get(url, timeout=30)
                if response.status_code == 200 and len(response.content) > 1000:
                    content_type = response.headers.get('content-type', '')
                    if 'image' in content_type:
                        cover_path = os.path.join(COVERS_FOLDER, f"{book_id}.jpg")
                        with open(cover_path, 'wb') as f:
                            f.write(response.content)
                        return f"covers/{book_id}.jpg"
            except:
                continue
        
        return "covers/default.jpg"
    
    def process_book(self, book_info):
        """Download and process a single book"""
        book_id = book_info['id']
        
        print(f"\n📖 Processing: {book_info['title'][:50]}...")
        
        # Download text
        print(f"   📥 Downloading text...")
        text_content = self.download_book_text(book_id)
        if not text_content:
            print(f"   ⚠️  Could not download text, skipping...")
            return None
        
        # Download cover
        print(f"   🖼️  Downloading cover...")
        cover_path = self.download_cover_image(book_id)
        
        # Save text file
        text_file = os.path.join(BOOKS_FOLDER, f"{book_id}.txt")
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(text_content)
        
        # Create book record
        book_data = {
            'id': book_id,
            'title': book_info['title'],
            'author': book_info['author'],
            'description': book_info['description'][:500],  # Limit description
            'cover': cover_path,
            'text_file': f"{book_id}.txt",
            'license': book_info['license'],
            'date': book_info.get('date', ''),
            'category': self.extract_category(book_info.get('subject', [])),
            'language': self.detect_language(text_content),
            'text_length': len(text_content),
            'downloaded_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Save metadata
        meta_file = os.path.join(BOOKS_FOLDER, f"{book_id}.json")
        with open(meta_file, 'w', encoding='utf-8') as f:
            json.dump(book_data, f, ensure_ascii=False, indent=2)
        
        print(f"   ✅ Saved: {book_info['title']}")
        return book_data
    
    def extract_category(self, subjects):
        """Extract main category from subjects"""
        if not subjects:
            return "General"
        if isinstance(subjects, list) and len(subjects) > 0:
            return subjects[0]
        return "General"
    
    def detect_language(self, text):
        """Simple language detection"""
        # Check for Hindi characters
        if re.search('[\u0900-\u097F]', text):
            return "Hindi"
        # Check for Sanskrit characters
        if re.search('[\u0900-\u097F]', text):
            return "Sanskrit"
        return "English"
    
    def save_books_index(self):
        """Save all books to index"""
        index_file = os.path.join(BOOKS_FOLDER, "index.json")
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(self.books, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Saved index with {len(self.books)} books")
    
    def generate_browse_html(self):
        """Generate browse.html with all books"""
        html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Browse Books - ReadEra</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', sans-serif; background: #f5f7fa; color: #1a2a3a; }
        .navbar { background: white; padding: 0.75rem 1.5rem; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        .nav-container { max-width: 1400px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; gap: 1rem; }
        .logo a { color: #8B4513; font-size: 1.65rem; font-weight: 700; text-decoration: none; }
        .nav-primary { display: flex; gap: 1rem; list-style: none; }
        .nav-primary a { color: #334155; text-decoration: none; font-weight: 500; padding: 0.5rem 0.75rem; transition: all 0.2s; }
        .nav-primary a:hover { color: #8B4513; background: rgba(139,69,19,0.08); border-radius: 8px; }
        .btn { display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.55rem 1rem; border-radius: 10px; cursor: pointer; border: 2px solid transparent; text-decoration: none; font-weight: 600; }
        .btn-solid { background: #8B4513; color: white; }
        .btn-solid:hover { background: #6b3410; }
        .container { max-width: 1400px; margin: 0 auto; padding: 2rem 1.5rem; }
        .header { margin-bottom: 3rem; }
        .header h1 { font-size: 2.5rem; margin-bottom: 0.5rem; }
        .header p { color: #64748b; font-size: 1.1rem; }
        .filters { display: flex; gap: 1rem; margin-bottom: 2rem; flex-wrap: wrap; }
        .filter-btn { padding: 0.5rem 1rem; border: 2px solid #e2e8f0; background: white; border-radius: 8px; cursor: pointer; transition: all 0.2s; }
        .filter-btn.active { background: #8B4513; color: white; border-color: #8B4513; }
        .books-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 2rem; }
        .book-card { background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.08); transition: all 0.3s; cursor: pointer; }
        .book-card:hover { transform: translateY(-8px); box-shadow: 0 12px 24px rgba(0,0,0,0.15); }
        .book-cover { width: 100%; height: 300px; object-fit: cover; background: #f1f5f9; }
        .book-info { padding: 1.5rem; }
        .book-title { font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem; color: #1a2a3a; }
        .book-author { font-size: 0.9rem; color: #64748b; margin-bottom: 0.75rem; }
        .book-category { display: inline-block; background: rgba(139,69,19,0.1); color: #8B4513; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }
        .book-desc { font-size: 0.85rem; color: #64748b; margin-top: 0.75rem; line-height: 1.4; }
        .book-footer { display: flex; gap: 0.5rem; margin-top: 1rem; }
        .book-btn { flex: 1; padding: 0.5rem; border: none; border-radius: 8px; cursor: pointer; font-size: 0.85rem; font-weight: 600; }
        .read-btn { background: #8B4513; color: white; }
        .read-btn:hover { background: #6b3410; }
        .footer { background: linear-gradient(180deg, #0c2744 0%, #061526 100%); color: #cbd5e1; padding: 2rem 1.5rem; text-align: center; }
        .empty { text-align: center; padding: 3rem; color: #64748b; }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="logo"><a href="index.html">ReadEra</a></div>
            <ul class="nav-primary">
                <li><a href="index.html">Home</a></li>
                <li><a href="browse.html" style="color: #8B4513; font-weight: 700;">Browse</a></li>
                <li><a href="contact.html">Contact</a></li>
                <li><a href="about.html">About</a></li>
            </ul>
            <div>
                <a href="auth.html" class="btn btn-solid"><i class="fas fa-sign-in-alt"></i> Login</a>
            </div>
        </div>
    </nav>

    <div class="container">
        <div class="header">
            <h1>📚 Browse Our Collection</h1>
            <p>Discover thousands of free Creative Commons books</p>
        </div>

        <div class="filters">
            <button class="filter-btn active" onclick="filterBooks('all')">All Books</button>
            <button class="filter-btn" onclick="filterBooks('hindi')">हिंदी</button>
            <button class="filter-btn" onclick="filterBooks('english')">English</button>
            <button class="filter-btn" onclick="filterBooks('sanskrit')">Sanskrit</button>
        </div>

        <div id="booksContainer" class="books-grid"></div>
    </div>

    <footer class="footer">
        <p>&copy; 2026 ReadEra. All Creative Commons books.</p>
    </footer>

    <script>
        let allBooks = [];

        // Load books data
        async function loadBooks() {
            try {
                const response = await fetch('books_data/index.json');
                allBooks = await response.json();
                renderBooks(allBooks);
            } catch (error) {
                document.getElementById('booksContainer').innerHTML = '<div class="empty"><p>No books available yet. Please run the book fetcher script.</p></div>';
            }
        }

        function renderBooks(books) {
            const container = document.getElementById('booksContainer');
            if (books.length === 0) {
                container.innerHTML = '<div class="empty"><p>No books found.</p></div>';
                return;
            }
            
            container.innerHTML = books.map(book => `
                <div class="book-card">
                    <img src="${book.cover}" alt="${book.title}" class="book-cover" onerror="this.src='covers/default.jpg'">
                    <div class="book-info">
                        <div class="book-title">${book.title}</div>
                        <div class="book-author">by ${book.author}</div>
                        <div class="book-category">${book.category}</div>
                        <div class="book-desc">${book.description.substring(0, 100)}...</div>
                        <div class="book-footer">
                            <button class="book-btn read-btn" onclick="readBook('${book.id}')">Read Now</button>
                        </div>
                    </div>
                </div>
            `).join('');
        }

        function filterBooks(language) {
            if (language === 'all') {
                renderBooks(allBooks);
            } else {
                renderBooks(allBooks.filter(b => b.language.toLowerCase() === language));
            }
        }

        function readBook(bookId) {
            window.location.href = `book.html?id=${bookId}`;
        }

        loadBooks();
    </script>
</body>
</html>
'''
        
        with open('browse.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("✅ Generated browse.html")
    
    def run(self, max_books=50):
        """Main execution"""
        print("=" * 60)
        print("📚 READERA BOOK FETCHER - Starting...")
        print("=" * 60)
        
        # Fetch from all sources
        new_books = []
        for source_name, source_url in SOURCES.items():
            books = self.fetch_from_source(source_url, source_name)
            new_books.extend(books[:max_books // len(SOURCES)])  # Distribute evenly
        
        print(f"\n📥 Processing {len(new_books)} new books...")
        
        for i, book_info in enumerate(new_books, 1):
            print(f"\n[{i}/{len(new_books)}]")
            book_data = self.process_book(book_info)
            if book_data:
                self.books.append(book_data)
            time.sleep(1)  # Rate limiting
        
        # Save and update
        self.save_books_index()
        self.generate_browse_html()
        
        print("\n" + "=" * 60)
        print(f"✅ COMPLETE! Downloaded {len(self.books)} books total")
        print("=" * 60)
        print("\n📍 Files created:")
        print(f"   - books_data/index.json (all book metadata)")
        print(f"   - books_data/*.txt (book content)")
        print(f"   - covers/*.jpg (book covers)")
        print(f"   - browse.html (updated book browser)")

# ============================================
# RUN AUTOMATION
# ============================================

if __name__ == "__main__":
    manager = BookManager()
    manager.run(max_books=50)  # Fetch 50 new books
    print("\n✅ You can now visit browse.html to see all books!")
