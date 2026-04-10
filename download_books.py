# ============================================
# READERA - DOWNLOAD CC HINDI BOOKS
# ============================================

import requests
import json
import os
import time

# ============================================
# CONFIGURATION
# ============================================

# Folder where books will be saved
BOOKS_FOLDER = "books_data"
os.makedirs(BOOKS_FOLDER, exist_ok=True)

# Collection URL (Hindi books)
COLLECTION_URL = "https://archive.org/details/booksbylanguage_hindi"

# How many books to download (pehle 5 test ke liye)
MAX_BOOKS = 5

# ============================================
# FUNCTIONS
# ============================================

def get_collection_books(collection_name, limit=20):
    """Collection se books ki list fetch karo"""
    url = f"https://archive.org/advancedsearch.php?q=collection:{collection_name} AND mediatype:texts&fl[]=identifier,title,creator,description,licenseurl&rows={limit}&output=json"
    
    print(f"📚 Fetching book list from: {collection_name}")
    response = requests.get(url)
    data = response.json()
    docs = data.get('response', {}).get('docs', [])
    
    # Sirf Creative Commons wali books
    cc_books = []
    for book in docs:
        license_url = book.get('licenseurl', '')
        if 'creativecommons' in license_url.lower() or 'cc0' in license_url.lower():
            cc_books.append({
                'id': book['identifier'],
                'title': book.get('title', 'Untitled'),
                'author': book.get('creator', 'Unknown'),
                'description': book.get('description', 'No description'),
                'license': license_url
            })
    
    return cc_books

def download_book_text(book_id):
    """Book ka full text download karo"""
    # Try different text URLs
    urls = [
        f"https://archive.org/stream/{book_id}/{book_id}_djvu.txt",
        f"https://archive.org/download/{book_id}/{book_id}.txt",
        f"https://archive.org/download/{book_id}/{book_id}_text.txt"
    ]
    
    for url in urls:
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                return response.text
        except:
            continue
    
    return None

def download_cover(book_id):
    """Cover image download karo"""
    urls = [
        f"https://archive.org/services/img/{book_id}",
        f"https://archive.org/download/{book_id}/{book_id}.jpg",
        f"https://archive.org/download/{book_id}/{book_id}_cover.jpg"
    ]
    
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Save cover image
                cover_path = os.path.join(BOOKS_FOLDER, f"{book_id}_cover.jpg")
                with open(cover_path, 'wb') as f:
                    f.write(response.content)
                return cover_path
        except:
            continue
    
    return None

def save_book_data(book_info, text_content):
    """Book data ko JSON file mein save karo"""
    book_data = {
        'id': book_info['id'],
        'title': book_info['title'],
        'author': book_info['author'],
        'description': book_info['description'][:2000] if book_info['description'] else 'No description',
        'text': text_content[:5000] if text_content else 'No text available',
        'license': book_info['license'],
        'downloaded_at': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Save as JSON
    json_path = os.path.join(BOOKS_FOLDER, f"{book_info['id']}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(book_data, f, ensure_ascii=False, indent=2)
    
    # Also save text file separately
    txt_path = os.path.join(BOOKS_FOLDER, f"{book_info['id']}.txt")
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(text_content if text_content else 'No text available')
    
    return json_path

def generate_html_page(books_data):
    """Browse page ke liye HTML generate karo"""
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ReadEra - Hindi Books</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: system-ui; background: #f5f7fa; padding: 2rem; }
        h1 { color: #8B4513; margin-bottom: 0.5rem; }
        .sub { color: #64748b; margin-bottom: 2rem; }
        .books-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; }
        .book-card { background: white; border-radius: 12px; overflow: hidden; cursor: pointer; transition: transform 0.2s; border: 1px solid #eef2f7; }
        .book-card:hover { transform: translateY(-4px); box-shadow: 0 12px 24px rgba(0,0,0,0.1); }
        .book-cover { height: 200px; background: linear-gradient(135deg, #8B4513, #c17a3a); display: flex; align-items: center; justify-content: center; color: white; font-size: 3rem; }
        .book-info { padding: 1rem; }
        .book-title { font-weight: 700; margin-bottom: 0.25rem; }
        .book-author { font-size: 0.8rem; color: #64748b; }
        .read-btn { display: inline-block; margin-top: 0.5rem; padding: 0.3rem 0.8rem; background: #8B4513; color: white; border-radius: 6px; font-size: 0.7rem; }
    </style>
</head>
<body>
    <h1>📚 ReadEra - Hindi Books Library</h1>
    <div class="sub">Creative Commons Books from Internet Archive</div>
    <div class="books-grid" id="booksGrid"></div>

    <script>
        const books = ''' + json.dumps(books_data, ensure_ascii=False) + ''';

        function viewBook(bookId) {
            window.location.href = `reader.html?id=${bookId}`;
        }

        function renderBooks() {
            const grid = document.getElementById('booksGrid');
            grid.innerHTML = books.map(book => `
                <div class="book-card" onclick="viewBook('${book.id}')">
                    <div class="book-cover">📖</div>
                    <div class="book-info">
                        <div class="book-title">${book.title.substring(0, 60)}</div>
                        <div class="book-author">${book.author}</div>
                        <span class="read-btn">Read Now →</span>
                    </div>
                </div>
            `).join('');
        }

        renderBooks();
    </script>
</body>
</html>'''
    
    with open('browse.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("✅ browse.html created!")

def generate_reader_page(books_data):
    """Reader page banaye har book ke liye"""
    for book in books_data:
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{book['title']} - ReadEra</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: system-ui; background: #f5f7fa; }}
        .header {{ background: #8B4513; color: white; padding: 1rem; position: sticky; top: 0; }}
        .back-btn {{ background: none; border: none; color: white; font-size: 1rem; cursor: pointer; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 2rem; background: white; min-height: 100vh; }}
        .title {{ font-size: 2rem; margin-bottom: 0.5rem; }}
        .author {{ color: #64748b; margin-bottom: 1rem; }}
        .content {{ line-height: 1.8; font-size: 1.1rem; }}
    </style>
</head>
<body>
    <div class="header">
        <button class="back-btn" onclick="window.location.href='browse.html'">← Back to Library</button>
    </div>
    <div class="container">
        <h1 class="title">{book['title']}</h1>
        <div class="author">by {book['author']}</div>
        <div class="content">
            <p>{book['description']}</p>
            <hr style="margin: 1rem 0;">
            <p>{book['text'][:10000].replace(chr(10), '<br>')}</p>
        </div>
    </div>
</body>
</html>'''
        
        with open(f"reader_{book['id']}.html", 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    print(f"✅ Created {len(books_data)} reader pages")

# ============================================
# MAIN - RUN KARO
# ============================================

def main():
    print("="*50)
    print("📚 READERA - DOWNLOAD CC HINDI BOOKS")
    print("="*50)
    
    # Get collection name
    collection_name = COLLECTION_URL.split('/details/')[-1].split('?')[0]
    print(f"\n📖 Collection: {collection_name}")
    
    # Get books from collection
    books = get_collection_books(collection_name, limit=MAX_BOOKS)
    print(f"✅ Found {len(books)} Creative Commons books")
    
    if len(books) == 0:
        print("❌ No CC books found!")
        return
    
    downloaded_books = []
    
    for i, book in enumerate(books):
        print(f"\n📖 [{i+1}/{len(books)}] Downloading: {book['title'][:50]}...")
        
        # Download text
        text = download_book_text(book['id'])
        if text:
            print(f"   ✅ Text downloaded ({len(text)} chars)")
        else:
            print(f"   ⚠️ No text available")
            text = "Text not available for this book"
        
        # Download cover
        cover = download_cover(book['id'])
        if cover:
            print(f"   ✅ Cover downloaded")
        
        # Save book data
        save_book_data(book, text)
        print(f"   💾 Saved to {BOOKS_FOLDER}/")
        
        downloaded_books.append({
            'id': book['id'],
            'title': book['title'],
            'author': book['author'],
            'description': book['description'][:500] if book['description'] else 'No description',
            'text': text[:500] if text else 'No text'
        })
        
        # Wait to avoid rate limiting
        time.sleep(1)
    
    # Generate HTML pages
    print("\n" + "="*50)
    print("📄 Generating HTML pages...")
    generate_html_page(downloaded_books)
    generate_reader_page(downloaded_books)
    
    print("\n" + "="*50)
    print("🎉 COMPLETE!")
    print(f"✅ Downloaded {len(downloaded_books)} books")
    print(f"📁 Books saved in: {BOOKS_FOLDER}/")
    print(f"🌐 Open browse.html to see your library!")
    print("="*50)

if __name__ == "__main__":
    main()