# ============================================
# READERA - COMPLETE BOOK DOWNLOADER
# Cover + Full Text + Everything
# ============================================

import requests
import json
import os
import time
import base64

# ============================================
# CONFIGURATION
# ============================================

BOOKS_FOLDER = "books_data"
COVERS_FOLDER = "covers"
os.makedirs(BOOKS_FOLDER, exist_ok=True)
os.makedirs(COVERS_FOLDER, exist_ok=True)

# Collection URL (Hindi books)
COLLECTION_URL = "https://archive.org/details/booksbylanguage_hindi"

# Kitni books chahiye (pehle 10 test ke liye)
MAX_BOOKS = 10

# ============================================
# FUNCTIONS
# ============================================

def get_collection_books(collection_name, limit=30):
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
                'description': book.get('description', 'No description available.'),
                'license': license_url
            })
    
    return cc_books

def download_book_text(book_id):
    """Book ka full text download karo"""
    urls = [
        f"https://archive.org/stream/{book_id}/{book_id}_djvu.txt",
        f"https://archive.org/download/{book_id}/{book_id}.txt",
        f"https://archive.org/download/{book_id}/{book_id}_text.txt"
    ]
    
    for url in urls:
        try:
            print(f"      Trying: {url}")
            response = requests.get(url, timeout=60)
            if response.status_code == 200:
                text = response.text
                if len(text) > 500:  # Valid text hai
                    return text
        except Exception as e:
            print(f"      Failed: {e}")
            continue
    
    return None

def download_cover_image(book_id):
    """Cover image download karo aur save karo"""
    urls = [
        f"https://archive.org/services/img/{book_id}",
        f"https://archive.org/download/{book_id}/{book_id}.jpg",
        f"https://archive.org/download/{book_id}/{book_id}_cover.jpg",
        f"https://archive.org/download/{book_id}/cover.jpg"
    ]
    
    for url in urls:
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200 and len(response.content) > 1000:
                # Check if it's an image
                content_type = response.headers.get('content-type', '')
                if 'image' in content_type:
                    # Save cover image
                    cover_path = os.path.join(COVERS_FOLDER, f"{book_id}.jpg")
                    with open(cover_path, 'wb') as f:
                        f.write(response.content)
                    return f"covers/{book_id}.jpg"
        except:
            continue
    
    return None

def get_book_metadata(book_id):
    """Book ka metadata fetch karo (pages, date, etc.)"""
    url = f"https://archive.org/metadata/{book_id}"
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            metadata = data.get('metadata', {})
            return {
                'pages': metadata.get('pages', 0),
                'date': metadata.get('date', 'Unknown'),
                'publisher': metadata.get('publisher', 'Unknown'),
                'language': metadata.get('language', 'Hindi')
            }
    except:
        pass
    return {'pages': 0, 'date': 'Unknown', 'publisher': 'Unknown', 'language': 'Hindi'}

def save_book_data(book_info, text_content, cover_path, metadata):
    """Book data ko JSON file mein save karo"""
    
    # Generate a proper summary from text
    summary = book_info['description']
    if (not summary or summary == 'No description available.') and text_content:
        # Extract first 500 chars as summary
        summary = text_content[:500].replace('\n', ' ').strip()
        if len(summary) < 50:
            summary = "This is a Creative Commons book from Internet Archive. Download and read the full text."
    
    book_data = {
        'id': book_info['id'],
        'title': book_info['title'],
        'author': book_info['author'],
        'summary': summary[:1000],
        'full_text': text_content if text_content else 'No text available',
        'cover_path': cover_path if cover_path else '',
        'pages': metadata['pages'],
        'date': metadata['date'],
        'publisher': metadata['publisher'],
        'language': metadata['language'],
        'license': book_info['license'],
        'downloaded_at': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Save as JSON
    json_path = os.path.join(BOOKS_FOLDER, f"{book_info['id']}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(book_data, f, ensure_ascii=False, indent=2)
    
    # Also save text file separately
    if text_content:
        txt_path = os.path.join(BOOKS_FOLDER, f"{book_info['id']}.txt")
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
    
    return json_path

def generate_browse_page(books_data):
    """Beautiful browse page generate karo with covers"""
    
    # Create books array for JavaScript
    books_js = []
    for book in books_data:
        books_js.append({
            'id': book['id'],
            'title': book['title'],
            'author': book['author'],
            'summary': book['summary'][:200],
            'cover': book['cover_path'] if book['cover_path'] else '',
            'has_text': book['has_text']
        })
    
    html_content = f'''<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ReadEra - Hindi Books Library</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', system-ui; background: #f5f7fa; }}
        
        /* Navbar */
        .navbar {{
            background: linear-gradient(135deg, #8B4513, #c17a3a);
            color: white;
            padding: 1rem 2rem;
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        .navbar h1 {{ font-size: 1.5rem; }}
        
        /* Container */
        .container {{ max-width: 1400px; margin: 0 auto; padding: 2rem; }}
        
        /* Stats */
        .stats {{
            background: white;
            padding: 1rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            text-align: center;
        }}
        .stats span {{ color: #8B4513; font-weight: bold; }}
        
        /* Books Grid */
        .books-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1.5rem;
        }}
        
        /* Book Card */
        .book-card {{
            background: white;
            border-radius: 16px;
            overflow: hidden;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            border: 1px solid #eef2f7;
        }}
        .book-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 28px rgba(0,0,0,0.15);
        }}
        
        /* Book Cover */
        .book-cover {{
            height: 220px;
            background: linear-gradient(135deg, #8B4513, #c17a3a);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 3rem;
            overflow: hidden;
        }}
        .book-cover img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        
        /* Book Info */
        .book-info {{ padding: 1rem; }}
        .book-title {{
            font-weight: 700;
            font-size: 1rem;
            margin-bottom: 0.25rem;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        .book-author {{
            font-size: 0.8rem;
            color: #64748b;
            margin-bottom: 0.5rem;
        }}
        .book-summary {{
            font-size: 0.75rem;
            color: #475569;
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        .read-btn {{
            display: inline-block;
            margin-top: 0.75rem;
            padding: 0.3rem 0.8rem;
            background: #8B4513;
            color: white;
            border-radius: 6px;
            font-size: 0.7rem;
            font-weight: 600;
        }}
        
        /* Footer */
        .footer {{
            background: #0c2744;
            color: #cbd5e1;
            text-align: center;
            padding: 1.5rem;
            margin-top: 2rem;
        }}
        
        @media (max-width: 768px) {{
            .container {{ padding: 1rem; }}
            .books-grid {{ grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); }}
        }}
    </style>
</head>
<body>
    <div class="navbar">
        <h1>📚 ReadEra - Hindi Digital Library</h1>
    </div>
    
    <div class="container">
        <div class="stats">
            📖 <span id="bookCount">{len(books_data)}</span> Creative Commons Hindi Books | 
            🆓 Free to Read | 
            📥 Download Available
        </div>
        
        <div class="books-grid" id="booksGrid"></div>
    </div>
    
    <div class="footer">
        <p>© 2026 ReadEra | All books are Creative Commons licensed from Internet Archive</p>
    </div>

    <script>
        const booksData = {json.dumps(books_js, ensure_ascii=False)};
        
        function viewBook(bookId) {{
            window.location.href = `reader.html?id=${{bookId}}`;
        }}
        
        function renderBooks() {{
            const grid = document.getElementById('booksGrid');
            
            if (booksData.length === 0) {{
                grid.innerHTML = '<div style="text-align:center; padding:3rem;">No books found. Please run download_books.py again.</div>';
                return;
            }}
            
            grid.innerHTML = booksData.map(book => `
                <div class="book-card" onclick="viewBook('${{book.id}}')">
                    <div class="book-cover">
                        ${{book.cover ? `<img src="${{book.cover}}" alt="${{book.title}}">` : '📖'}}
                    </div>
                    <div class="book-info">
                        <div class="book-title">${{book.title.substring(0, 60)}}${{book.title.length > 60 ? '...' : ''}}</div>
                        <div class="book-author">✍️ ${{book.author.substring(0, 50)}}</div>
                        <div class="book-summary">${{book.summary.substring(0, 120)}}${{book.summary.length > 120 ? '...' : ''}}</div>
                        <span class="read-btn">📖 Read Now →</span>
                    </div>
                </div>
            `).join('');
        }}
        
        renderBooks();
    </script>
</body>
</html>'''
    
    with open('browse.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("✅ browse.html created with covers!")

def generate_reader_page(book):
    """Individual reader page banaye"""
    
    # Get cover HTML
    cover_html = ''
    if book['cover_path'] and os.path.exists(book['cover_path']):
        cover_html = f'<div style="text-align:center; margin-bottom:2rem;"><img src="{book["cover_path"]}" style="max-width:200px; border-radius:12px;"></div>'
    
    # Format text for HTML
    text_content = book.get('full_text', 'No text available')
    text_html = text_content.replace('\n', '<br>') if text_content else 'No text available'
    
    html_content = f'''<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{book['title']} - ReadEra</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', system-ui; background: #f5f7fa; }}
        .header {{
            background: #8B4513;
            color: white;
            padding: 1rem;
            position: sticky;
            top: 0;
            z-index: 100;
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        .back-btn {{
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.9rem;
        }}
        .back-btn:hover {{ background: rgba(255,255,255,0.3); }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 2rem; background: white; min-height: 100vh; }}
        .title {{ font-size: 2rem; margin-bottom: 0.5rem; color: #0a2540; }}
        .author {{ color: #64748b; margin-bottom: 1rem; font-size: 1.1rem; }}
        .meta {{ display: flex; gap: 1rem; margin-bottom: 2rem; color: #8B4513; font-size: 0.85rem; }}
        .content {{ line-height: 1.8; font-size: 1.05rem; }}
        .content p {{ margin-bottom: 1rem; }}
        .footer {{ background: #0c2744; color: #cbd5e1; text-align: center; padding: 1rem; margin-top: 2rem; }}
        @media (max-width: 768px) {{
            .container {{ padding: 1rem; }}
            .title {{ font-size: 1.5rem; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <button class="back-btn" onclick="window.location.href='browse.html'">← Back to Library</button>
        <span>📖 Reading Mode</span>
    </div>
    <div class="container">
        {cover_html}
        <h1 class="title">{book['title']}</h1>
        <div class="author">by {book['author']}</div>
        <div class="meta">
            <span>📄 {book.get('pages', 0)} pages</span>
            <span>📅 {book.get('date', 'Unknown')}</span>
            <span>🔖 {book.get('language', 'Hindi')}</span>
        </div>
        <div class="content">
            <h3>📖 Summary</h3>
            <p>{book.get('summary', 'No summary available')}</p>
            <hr style="margin: 1.5rem 0;">
            <h3>📚 Full Text</h3>
            {text_html}
        </div>
    </div>
    <div class="footer">
        <p>Creative Commons Book from Internet Archive | Free to Read</p>
    </div>
</body>
</html>'''
    
    reader_path = f"reader_{book['id']}.html"
    with open(reader_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    return reader_path

# ============================================
# MAIN FUNCTION
# ============================================

def main():
    print("="*60)
    print("📚 READERA - COMPLETE HINDI BOOKS DOWNLOADER")
    print("="*60)
    
    # Get collection name
    collection_name = COLLECTION_URL.split('/details/')[-1].split('?')[0]
    print(f"\n📖 Collection: {collection_name}")
    print(f"📚 Max books: {MAX_BOOKS}\n")
    
    # Get books from collection
    books = get_collection_books(collection_name, limit=MAX_BOOKS + 10)
    print(f"\n✅ Found {len(books)} Creative Commons books")
    
    if len(books) == 0:
        print("❌ No CC books found!")
        return
    
    downloaded_books = []
    
    for i, book in enumerate(books[:MAX_BOOKS]):
        print(f"\n{'='*50}")
        print(f"📖 [{i+1}/{MAX_BOOKS}] {book['title'][:60]}...")
        print(f"   ID: {book['id']}")
        print(f"   Author: {book['author']}")
        
        # Download cover
        print(f"   🖼️ Downloading cover...")
        cover_path = download_cover_image(book['id'])
        if cover_path:
            print(f"   ✅ Cover saved: {cover_path}")
        else:
            print(f"   ⚠️ No cover available")
        
        # Download full text
        print(f"   📥 Downloading text...")
        text_content = download_book_text(book['id'])
        if text_content:
            print(f"   ✅ Text downloaded ({len(text_content)} characters)")
        else:
            print(f"   ⚠️ No text available")
            text_content = "Full text not available for this book. Please read online at Internet Archive."
        
        # Get metadata
        print(f"   📊 Fetching metadata...")
        metadata = get_book_metadata(book['id'])
        print(f"   ✅ Pages: {metadata['pages']}, Language: {metadata['language']}")
        
        # Save everything
        print(f"   💾 Saving data...")
        save_book_data(book, text_content, cover_path, metadata)
        
        # Store for HTML generation
        downloaded_books.append({
            'id': book['id'],
            'title': book['title'],
            'author': book['author'],
            'summary': book['description'][:500] if book['description'] and len(book['description']) > 50 else (text_content[:500] if text_content else 'No summary'),
            'full_text': text_content if text_content else 'No text available',
            'cover_path': cover_path,
            'has_text': text_content is not None,
            'pages': metadata['pages'],
            'date': metadata['date'],
            'publisher': metadata['publisher'],
            'language': metadata['language']
        })
        
        # Generate reader page immediately
        print(f"   📄 Generating reader page...")
        generate_reader_page(downloaded_books[-1])
        print(f"   ✅ Reader page created")
        
        # Wait to avoid rate limiting
        time.sleep(2)
    
    # Generate main browse page
    print("\n" + "="*60)
    print("📄 Generating main browse page...")
    generate_browse_page(downloaded_books)
    
    # Final summary
    print("\n" + "="*60)
    print("🎉 COMPLETE!")
    print("="*60)
    print(f"✅ Books downloaded: {len(downloaded_books)}")
    print(f"📁 Books folder: {BOOKS_FOLDER}/")
    print(f"🖼️ Covers folder: {COVERS_FOLDER}/")
    print(f"🌐 Open browse.html to see your library with covers!")
    print("="*60)

if __name__ == "__main__":
    main()