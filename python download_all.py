# ============================================
# READERA - COMPLETE BOOK DOWNLOADER
# INTERNET ARCHIVE SE HINDI CC BOOKS
# ============================================

import requests
import json
import os
import time
from urllib.parse import urlparse
import re

# ============================================
# SETUP
# ============================================

print("="*60)
print("📚 READERA - HINDI CC BOOKS DOWNLOADER")
print("="*60)

# Create folders
os.makedirs("books_data", exist_ok=True)
os.makedirs("covers", exist_ok=True)
os.makedirs("texts", exist_ok=True)

# ============================================
# CONFIGURATION - YAHAN BADAL SAKTA HAI
# ============================================

# Collection URLs (multiple sources)
COLLECTIONS = [
    "booksbylanguage_hindi",
    "hindibooks",
    "hindiliterature",
    "hindipoetry",
    "hindi_novel",
]

# Total books to download
TOTAL_BOOKS = 50

# ============================================
# FUNCTION 1: GET BOOKS FROM COLLECTION
# ============================================

def get_books_from_collection(collection_name, limit=100):
    """Collection se saari books ki list le aao"""
    url = f"https://archive.org/advancedsearch.php?q=collection:{collection_name} AND mediatype:texts&fl[]=identifier,title,creator,description,licenseurl,date&rows={limit}&output=json"
    
    try:
        response = requests.get(url, timeout=30)
        data = response.json()
        docs = data.get('response', {}).get('docs', [])
        
        books = []
        for doc in docs:
            license_url = doc.get('licenseurl', '').lower()
            # Sirf CC books
            if 'creativecommons' in license_url or 'cc0' in license_url or 'cc-by' in license_url:
                books.append({
                    'id': doc['identifier'],
                    'title': doc.get('title', 'Untitled'),
                    'author': doc.get('creator', 'Unknown'),
                    'description': doc.get('description', 'No description'),
                    'date': doc.get('date', 'Unknown'),
                    'license': license_url
                })
        
        return books
    except Exception as e:
        print(f"Error fetching {collection_name}: {e}")
        return []

# ============================================
# FUNCTION 2: GET TEXT FROM DIFFERENT SOURCES
# ============================================

def get_book_text(book_id):
    """Book ka text nikaalo - multiple methods"""
    
    # Method 1: DjVu text file
    urls = [
        f"https://archive.org/stream/{book_id}/{book_id}_djvu.txt",
        f"https://archive.org/download/{book_id}/{book_id}.txt",
        f"https://archive.org/download/{book_id}/{book_id}_text.txt",
        f"https://archive.org/stream/{book_id}/{book_id}.txt",
        f"https://archive.org/download/{book_id}/text.txt"
    ]
    
    for url in urls:
        try:
            print(f"      Trying: {url}")
            resp = requests.get(url, timeout=45)
            if resp.status_code == 200:
                text = resp.text
                if len(text) > 500:
                    return text
        except:
            continue
    
    # Method 2: If text not found, try to get from PDF (advanced)
    try:
        pdf_url = f"https://archive.org/download/{book_id}/{book_id}.pdf"
        print(f"      Trying PDF extraction...")
        # Simple PDF text extraction using PyPDF2 (if installed)
        try:
            import PyPDF2
            import io
            pdf_resp = requests.get(pdf_url, timeout=60)
            if pdf_resp.status_code == 200:
                pdf_file = io.BytesIO(pdf_resp.content)
                reader = PyPDF2.PdfReader(pdf_file)
                text = ""
                for page in reader.pages[:20]:  # Pehle 20 pages
                    text += page.extract_text()
                if len(text) > 500:
                    return text
        except:
            pass
    except:
        pass
    
    return None

# ============================================
# FUNCTION 3: GET COVER IMAGE
# ============================================

def get_cover_image(book_id):
    """Cover image download karo"""
    cover_urls = [
        f"https://archive.org/services/img/{book_id}",
        f"https://archive.org/download/{book_id}/{book_id}.jpg",
        f"https://archive.org/download/{book_id}/{book_id}_cover.jpg",
        f"https://archive.org/download/{book_id}/cover.jpg",
        f"https://archive.org/download/{book_id}/item_image.jpg"
    ]
    
    for url in cover_urls:
        try:
            resp = requests.get(url, timeout=20)
            if resp.status_code == 200 and len(resp.content) > 1000:
                content_type = resp.headers.get('content-type', '')
                if 'image' in content_type:
                    ext = 'jpg'
                    if 'png' in content_type:
                        ext = 'png'
                    elif 'jpeg' in content_type:
                        ext = 'jpg'
                    
                    cover_path = f"covers/{book_id}.{ext}"
                    with open(cover_path, 'wb') as f:
                        f.write(resp.content)
                    return cover_path
        except:
            continue
    
    return None

# ============================================
# FUNCTION 4: GET METADATA
# ============================================

def get_metadata(book_id):
    """Book metadata fetch karo"""
    url = f"https://archive.org/metadata/{book_id}"
    try:
        resp = requests.get(url, timeout=20)
        if resp.status_code == 200:
            data = resp.json()
            meta = data.get('metadata', {})
            return {
                'pages': meta.get('pages', 'Unknown'),
                'publisher': meta.get('publisher', 'Unknown'),
                'language': meta.get('language', 'Unknown'),
                'year': meta.get('year', 'Unknown'),
                'subject': meta.get('subject', 'Unknown')
            }
    except:
        pass
    return {'pages': 'Unknown', 'publisher': 'Unknown', 'language': 'Unknown', 'year': 'Unknown', 'subject': 'Unknown'}

# ============================================
# FUNCTION 5: SAVE ALL DATA
# ============================================

def save_book(book_info, text, cover_path, metadata):
    """Poori book ko save karo"""
    
    # Clean text
    if text:
        # Remove extra spaces
        text = re.sub(r'\n\s*\n', '\n\n', text)
        # Limit to 50000 chars for storage
        if len(text) > 50000:
            text = text[:50000] + "\n\n...[Text truncated due to length]..."
    
    book_data = {
        'id': book_info['id'],
        'title': book_info['title'],
        'author': book_info['author'],
        'description': book_info['description'][:2000] if book_info['description'] else '',
        'summary': (text[:800] if text else book_info['description'][:800]) if book_info['description'] else 'No summary available',
        'full_text': text if text else 'No text available',
        'cover_path': cover_path if cover_path else '',
        'pages': metadata['pages'],
        'publisher': metadata['publisher'],
        'language': metadata['language'],
        'year': metadata['year'],
        'subject': metadata['subject'],
        'date': book_info['date'],
        'license': book_info['license'],
        'downloaded_at': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Save JSON
    json_path = f"books_data/{book_info['id']}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(book_data, f, ensure_ascii=False, indent=2)
    
    # Save text separately
    if text:
        txt_path = f"texts/{book_info['id']}.txt"
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(text)
    
    return json_path

# ============================================
# FUNCTION 6: GENERATE BROWSE HTML
# ============================================

def generate_browse_html(books):
    """Beautiful browse page generate karo"""
    
    books_json = []
    for book in books:
        books_json.append({
            'id': book['id'],
            'title': book['title'],
            'author': book['author'],
            'summary': book.get('summary', '')[:150],
            'cover': book.get('cover_path', ''),
            'pages': book.get('pages', 'Unknown'),
            'year': book.get('year', 'Unknown')
        })
    
    html = '''<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ReadEra - Hindi Digital Library</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', sans-serif;
            background: #f5f7fa;
            color: #1a2a3a;
        }
        
        /* Navbar */
        .navbar {
            background: linear-gradient(135deg, #8B4513, #c17a3a);
            padding: 1rem 2rem;
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        .navbar h1 {
            color: white;
            font-size: 1.5rem;
        }
        .navbar p {
            color: rgba(255,255,255,0.8);
            font-size: 0.85rem;
            margin-top: 0.25rem;
        }
        
        /* Container */
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        /* Stats */
        .stats {
            background: white;
            padding: 1rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }
        .stats-count {
            color: #8B4513;
            font-weight: bold;
            font-size: 1.2rem;
        }
        .search-box input {
            padding: 0.5rem 1rem;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            width: 250px;
        }
        
        /* Books Grid */
        .books-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1.5rem;
        }
        
        /* Book Card */
        .book-card {
            background: white;
            border-radius: 16px;
            overflow: hidden;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 1px solid #eef2f7;
        }
        .book-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 30px -15px rgba(0,0,0,0.2);
        }
        
        /* Cover */
        .book-cover {
            height: 220px;
            background: linear-gradient(135deg, #8B4513, #c17a3a);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 3rem;
            overflow: hidden;
        }
        .book-cover img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        /* Info */
        .book-info {
            padding: 1.25rem;
        }
        .book-title {
            font-weight: 700;
            font-size: 1rem;
            margin-bottom: 0.25rem;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        .book-author {
            font-size: 0.8rem;
            color: #64748b;
            margin-bottom: 0.5rem;
        }
        .book-meta {
            font-size: 0.7rem;
            color: #8B4513;
            margin-bottom: 0.5rem;
        }
        .book-summary {
            font-size: 0.75rem;
            color: #475569;
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        .read-btn {
            display: inline-block;
            margin-top: 0.75rem;
            padding: 0.4rem 1rem;
            background: #8B4513;
            color: white;
            border-radius: 8px;
            font-size: 0.7rem;
            font-weight: 600;
            text-decoration: none;
        }
        
        /* Footer */
        .footer {
            background: #0c2744;
            color: #cbd5e1;
            text-align: center;
            padding: 1.5rem;
            margin-top: 2rem;
        }
        
        @media (max-width: 768px) {
            .container { padding: 1rem; }
            .books-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="navbar">
        <h1>📚 ReadEra - Hindi Digital Library</h1>
        <p>Creative Commons Books from Internet Archive | Free to Read</p>
    </div>
    
    <div class="container">
        <div class="stats">
            <div>📖 <span class="stats-count" id="bookCount">''' + str(len(books_json)) + '''</span> Hindi Books Available</div>
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="🔍 Search by title or author...">
            </div>
        </div>
        
        <div class="books-grid" id="booksGrid"></div>
    </div>
    
    <div class="footer">
        <p>© 2026 ReadEra | All books are Creative Commons licensed | Source: Internet Archive</p>
    </div>

    <script>
        const books = ''' + json.dumps(books_json, ensure_ascii=False) + ''';
        
        function viewBook(bookId) {
            window.location.href = `reader_${bookId}.html`;
        }
        
        function renderBooks(searchTerm = '') {
            const grid = document.getElementById('booksGrid');
            let filtered = books;
            
            if (searchTerm) {
                const term = searchTerm.toLowerCase();
                filtered = books.filter(book => 
                    book.title.toLowerCase().includes(term) || 
                    book.author.toLowerCase().includes(term)
                );
            }
            
            if (filtered.length === 0) {
                grid.innerHTML = '<div style="text-align:center; padding:3rem;">No books found</div>';
                return;
            }
            
            grid.innerHTML = filtered.map(book => `
                <div class="book-card" onclick="viewBook('${book.id}')">
                    <div class="book-cover">
                        ${book.cover ? `<img src="${book.cover}" alt="${book.title}">` : '📖'}
                    </div>
                    <div class="book-info">
                        <div class="book-title">${book.title.substring(0, 70)}${book.title.length > 70 ? '...' : ''}</div>
                        <div class="book-author">✍️ ${book.author.substring(0, 50)}</div>
                        <div class="book-meta">📄 ${book.pages} pages | 📅 ${book.year}</div>
                        <div class="book-summary">${book.summary.substring(0, 120)}${book.summary.length > 120 ? '...' : ''}</div>
                        <span class="read-btn">📖 Read Now →</span>
                    </div>
                </div>
            `).join('');
        }
        
        document.getElementById('searchInput').addEventListener('input', (e) => {
            renderBooks(e.target.value);
        });
        
        renderBooks();
    </script>
</body>
</html>'''
    
    with open('browse.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✅ browse.html generated!")

# ============================================
# FUNCTION 7: GENERATE READER HTML
# ============================================

def generate_reader_html(book):
    """Individual book reader page generate karo"""
    
    # Get cover HTML
    cover_html = ''
    if book.get('cover_path') and os.path.exists(book['cover_path']):
        cover_html = f'<div style="text-align:center; margin-bottom:2rem;"><img src="{book["cover_path"]}" style="max-width:250px; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.1);"></div>'
    
    # Get text
    text_content = book.get('full_text', 'No text available')
    text_html = text_content.replace('\n', '<br>').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    html = f'''<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{book['title']} - ReadEra</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', sans-serif;
            background: #f5f7fa;
        }}
        .header {{
            background: #8B4513;
            color: white;
            padding: 1rem 2rem;
            position: sticky;
            top: 0;
            z-index: 100;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
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
        .download-btn {{
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            font-size: 0.9rem;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
            background: white;
            min-height: 100vh;
        }}
        .title {{
            font-size: 2rem;
            margin-bottom: 0.5rem;
            color: #0a2540;
        }}
        .author {{
            color: #64748b;
            margin-bottom: 0.5rem;
            font-size: 1rem;
        }}
        .meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid #eef2f7;
            color: #8B4513;
            font-size: 0.85rem;
        }}
        .content {{
            line-height: 1.8;
            font-size: 1rem;
            color: #334155;
        }}
        .content p {{ margin-bottom: 1rem; }}
        .footer {{
            background: #0c2744;
            color: #cbd5e1;
            text-align: center;
            padding: 1rem;
        }}
        @media (max-width: 768px) {{
            .container {{ padding: 1rem; }}
            .title {{ font-size: 1.5rem; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <button class="back-btn" onclick="window.location.href='browse.html'">← Back to Library</button>
        <div>
            <a href="texts/{book['id']}.txt" download class="download-btn">📥 Download Text</a>
        </div>
    </div>
    <div class="container">
        {cover_html}
        <h1 class="title">{book['title']}</h1>
        <div class="author">by {book['author']}</div>
        <div class="meta">
            <span>📄 {book.get('pages', 'Unknown')} pages</span>
            <span>📅 {book.get('year', 'Unknown')}</span>
            <span>🔖 {book.get('language', 'Unknown')}</span>
            <span>🏛️ {book.get('publisher', 'Unknown')}</span>
        </div>
        <div class="content">
            <h3>📖 About this book</h3>
            <p>{book.get('description', 'No description available')[:500]}</p>
            <hr style="margin: 1.5rem 0;">
            <h3>📚 Read Online</h3>
            {text_html}
        </div>
    </div>
    <div class="footer">
        <p>Creative Commons Book from Internet Archive | Free to Read and Share</p>
    </div>
</body>
</html>'''
    
    with open(f"reader_{book['id']}.html", 'w', encoding='utf-8') as f:
        f.write(html)
    return f"reader_{book['id']}.html"

# ============================================
# MAIN EXECUTION
# ============================================

def main():
    all_books = []
    seen_ids = set()
    
    # Step 1: Get books from all collections
    print("\n📚 STEP 1: Fetching book list from collections...")
    print("-"*40)
    
    for collection in COLLECTIONS:
        print(f"\n🔍 Collection: {collection}")
        books = get_books_from_collection(collection, limit=50)
        print(f"   Found {len(books)} CC books")
        
        for book in books:
            if book['id'] not in seen_ids:
                seen_ids.add(book['id'])
                all_books.append(book)
        
        print(f"   Total unique books so far: {len(all_books)}")
    
    # Limit to TOTAL_BOOKS
    all_books = all_books[:TOTAL_BOOKS]
    print(f"\n📊 Total unique CC books to download: {len(all_books)}")
    
    # Step 2: Download each book
    print("\n📥 STEP 2: Downloading books...")
    print("-"*40)
    
    downloaded_books = []
    
    for i, book in enumerate(all_books):
        print(f"\n{'='*50}")
        print(f"📖 [{i+1}/{len(all_books)}] {book['title'][:60]}...")
        print(f"   ID: {book['id']}")
        print(f"   Author: {book['author']}")
        
        # Get cover
        print(f"   🖼️ Downloading cover...")
        cover_path = get_cover_image(book['id'])
        if cover_path:
            print(f"   ✅ Cover saved")
        else:
            print(f"   ⚠️ No cover available")
        
        # Get text
        print(f"   📥 Downloading text (may take 10-30 seconds)...")
        text = get_book_text(book['id'])
        if text:
            print(f"   ✅ Text downloaded ({len(text)} chars)")
        else:
            print(f"   ❌ No text available")
        
        # Get metadata
        print(f"   📊 Fetching metadata...")
        metadata = get_metadata(book['id'])
        
        # Save
        print(f"   💾 Saving data...")
        save_book(book, text, cover_path, metadata)
        
        # Store for HTML
        book_data = {
            'id': book['id'],
            'title': book['title'],
            'author': book['author'],
            'description': book['description'][:500] if book['description'] else '',
            'summary': (text[:800] if text else book['description'][:800]) if book['description'] else 'No summary',
            'full_text': text if text else 'No text available',
            'cover_path': cover_path,
            'pages': metadata['pages'],
            'publisher': metadata['publisher'],
            'language': metadata['language'],
            'year': metadata['year']
        }
        
        downloaded_books.append(book_data)
        
        # Generate reader page
        print(f"   📄 Generating reader page...")
        generate_reader_html(book_data)
        
        # Wait to avoid rate limits
        time.sleep(2)
    
    # Step 3: Generate browse page
    print("\n" + "="*50)
    print("📄 STEP 3: Generating browse page...")
    generate_browse_html(downloaded_books)
    
    # Final summary
    print("\n" + "="*50)
    print("🎉 COMPLETE!")
    print("="*50)
    print(f"✅ Books downloaded: {len(downloaded_books)}")
    print(f"📁 Books data: books_data/ folder")
    print(f"🖼️ Covers: covers/ folder")
    print(f"📝 Texts: texts/ folder")
    print(f"🌐 Open browse.html to see your library!")
    print("="*50)

if __name__ == "__main__":
    main()