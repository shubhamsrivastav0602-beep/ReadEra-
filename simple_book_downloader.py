#!/usr/bin/env python3
"""
READERA - Simple Book Downloader
Download Creative Commons books from Archive.org
"""

import requests
import json
import os
import time
import sys

# Create folders
os.makedirs("books_data", exist_ok=True)
os.makedirs("covers", exist_ok=True)

# Hindi books list (tested, working sources)
BOOKS_TO_DOWNLOAD = [
    {
        "id": "Lakshay",
        "title": "Lakshay",
        "author": "Unknown",
        "url": "https://archive.org/download/Lakshay/Lakshay.txt"
    },
    {
        "id": "BhallataShatak",
        "title": "Bhallata Shatak",
        "author": "Bhallata",
        "url": "https://archive.org/download/BhallataShatakWithMaheshwariSanskritTikaVedKumariGhai/BhallataShatakWithMaheshwariSanskritTikaVedKumariGhai_djvu.txt"
    },
    {
        "id": "maa_haar_gayi",
        "title": "Maa Haar Gayi",
        "author": "Mannu Bandari",
        "url": "https://archive.org/download/cjbu_maa-haar-gayi-by-mannu-bandari-1956-delhi-prakashan-rajkamal-prakashan/cjbu_maa-haar-gayi-by-mannu-bandari-1956-delhi-prakashan-rajkamal-prakashan_djvu.txt"
    },
    {
        "id": "vakyarth_sangrah",
        "title": "Vakyarth Sangrah",
        "author": "Manu",
        "url": "https://archive.org/download/NvWl_vakyarth-sangrah-manu-03-02-713-lal-bahadur-shastri-sanskrit-university/NvWl_vakyarth-sangrah-manu-03-02-713-lal-bahadur-shastri-sanskrit-university_djvu.txt"
    },
    {
        "id": "book_of_psalms",
        "title": "The Book of Psalms",
        "author": "Sanskrit",
        "url": "https://archive.org/download/sanskrit-the-book-of-psalms/sanskrit-the-book-of-psalms_djvu.txt"
    },
]

all_books = []

def download_file(url, filename, max_retries=3):
    """Download file with retry logic"""
    for attempt in range(max_retries):
        try:
            print(f"      Attempting download... (Try {attempt+1}/{max_retries})")
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"      ✅ Downloaded successfully ({len(response.text)} chars)")
                return True
            else:
                print(f"      ⚠️ Status code: {response.status_code}")
        except Exception as e:
            print(f"      ❌ Error: {str(e)}")
        
        if attempt < max_retries - 1:
            print(f"      ⏳ Waiting 5 seconds before retry...")
            time.sleep(5)
    
    return False

def download_cover(book_id):
    """Download book cover"""
    urls = [
        f"https://archive.org/services/img/{book_id}",
        f"https://archive.org/download/{book_id}/{book_id}.jpg",
        f"https://archive.org/download/{book_id}/cover.jpg",
    ]
    
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200 and len(response.content) > 1000:
                cover_file = f"covers/{book_id}.jpg"
                with open(cover_file, 'wb') as f:
                    f.write(response.content)
                print(f"      🖼️ Cover saved: {cover_file}")
                return cover_file
        except:
            pass
    
    return None

def process_book(book_info):
    """Download and process one book"""
    book_id = book_info["id"]
    title = book_info["title"]
    author = book_info["author"]
    url = book_info["url"]
    
    print(f"\n📖 [{len(all_books)+1}] {title}")
    print(f"   Author: {author}")
    print(f"   📥 Downloading text...")
    
    # Download text
    text_file = f"books_data/{book_id}.txt"
    if not download_file(url, text_file):
        print(f"   ❌ Failed to download")
        return None
    
    # Get file size
    file_size = os.path.getsize(text_file)
    print(f"   📊 File size: {file_size} bytes")
    
    # Download cover
    print(f"   🖼️ Downloading cover...")
    cover = download_cover(book_id)
    
    # Create metadata
    book_data = {
        "id": book_id,
        "title": title,
        "author": author,
        "cover": cover if cover else "covers/default.jpg",
        "text_file": f"{book_id}.txt",
        "file_size": file_size,
        "category": "Literature",
        "language": "Hindi" if any(ord(c) > 127 for c in title) else "English"
    }
    
    # Save metadata
    meta_file = f"books_data/{book_id}.json"
    with open(meta_file, 'w', encoding='utf-8') as f:
        json.dump(book_data, f, ensure_ascii=False, indent=2)
    
    print(f"   ✅ Saved metadata: {meta_file}")
    return book_data

def create_index():
    """Create books index"""
    print("\n" + "="*60)
    print("📋 Creating books index...")
    
    index_file = "books_data/index.json"
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(all_books, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Index created: {index_file}")
    print(f"   Total books: {len(all_books)}")

def create_browse_html():
    """Create simple browse.html"""
    print("\n" + "="*60)
    print("🌐 Creating browse.html...")
    
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Browse Books - ReadEra</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', sans-serif; background: #f5f7fa; min-height: 100vh; }
        .navbar { background: white; padding: 1rem 2rem; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        .navbar a { color: #8B4513; font-size: 1.5rem; font-weight: 700; text-decoration: none; }
        .container { max-width: 1200px; margin: 0 auto; padding: 2rem 1rem; }
        h1 { color: #1a2a3a; margin-bottom: 2rem; }
        .books-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 2rem; }
        .book-card { background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        .book-card:hover { transform: translateY(-5px); box-shadow: 0 8px 20px rgba(0,0,0,0.15); }
        .book-cover { width: 100%; height: 280px; object-fit: cover; background: #ddd; }
        .book-info { padding: 1rem; }
        .book-title { font-weight: 600; margin-bottom: 0.5rem; color: #1a2a3a; }
        .book-author { font-size: 0.9rem; color: #64748b; margin-bottom: 1rem; }
        .book-btn { display: block; width: 100%; padding: 0.7rem; background: #8B4513; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; }
        .book-btn:hover { background: #6b3410; }
    </style>
</head>
<body>
    <nav class="navbar">
        <a href="index.html">📚 ReadEra</a>
    </nav>

    <div class="container">
        <h1>📖 Browse Our Books</h1>
        <div id="booksContainer" class="books-grid"></div>
    </div>

    <script>
        async function loadBooks() {
            try {
                const response = await fetch('/books_data/index.json');
                const books = await response.json();
                
                const container = document.getElementById('booksContainer');
                container.innerHTML = books.map(book => `
                    <div class="book-card">
                        <img src="${book.cover}" alt="${book.title}" class="book-cover" onerror="this.src='covers/default.jpg'">
                        <div class="book-info">
                            <div class="book-title">${book.title}</div>
                            <div class="book-author">by ${book.author}</div>
                            <button class="book-btn" onclick="window.location='book.html?id=${book.id}'">Read Now</button>
                        </div>
                    </div>
                `).join('');
            } catch (error) {
                document.getElementById('booksContainer').innerHTML = '<p>Unable to load books. Run the downloader first.</p>';
            }
        }
        
        loadBooks();
    </script>
</body>
</html>'''
    
    with open('browse.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ browse.html created")

def main():
    """Main execution"""
    print("="*60)
    print("📚 READERA - Simple Book Downloader")
    print("="*60)
    print(f"\n📍 Downloading {len(BOOKS_TO_DOWNLOAD)} books...")
    
    # Download each book
    for book_info in BOOKS_TO_DOWNLOAD:
        try:
            book_data = process_book(book_info)
            if book_data:
                all_books.append(book_data)
            time.sleep(2)  # Wait between downloads
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    # Create index and HTML
    create_index()
    create_browse_html()
    
    # Final summary
    print("\n" + "="*60)
    print("✅ DONE!")
    print("="*60)
    print(f"\n📁 Downloaded {len(all_books)} books")
    print("\n📍 Files created:")
    print("   ✅ books_data/index.json")
    print("   ✅ books_data/*.txt (book texts)")
    print("   ✅ covers/*.jpg (book covers)")
    print("   ✅ browse.html")
    print("\n🌐 Visit browse.html to see all books!")
    print("="*60)

if __name__ == "__main__":
    main()
