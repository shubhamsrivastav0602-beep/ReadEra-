# ============================================
# READERA - SIMPLE WORKING DOWNLOADER
# ============================================

import requests
import json
import os
import time

print("="*50)
print("📚 READERA - BOOK DOWNLOADER")
print("="*50)

# Create folders
os.makedirs("books_data", exist_ok=True)
os.makedirs("covers", exist_ok=True)

# Get book list
print("\n📚 Fetching book list...")
url = "https://archive.org/advancedsearch.php?q=collection:booksbylanguage_hindi AND mediatype:texts&fl[]=identifier,title,creator&rows=10&output=json"
response = requests.get(url)
data = response.json()
books = data.get('response', {}).get('docs', [])

print(f"✅ Found {len(books)} books\n")

downloaded = []

for i, book in enumerate(books):
    print(f"[{i+1}/{len(books)}] {book.get('title', 'Untitled')[:50]}...")
    
    book_id = book['identifier']
    
    # Get cover
    cover_url = f"https://archive.org/services/img/{book_id}"
    cover_path = f"covers/{book_id}.jpg"
    try:
        cover_resp = requests.get(cover_url, timeout=10)
        if cover_resp.status_code == 200:
            with open(cover_path, 'wb') as f:
                f.write(cover_resp.content)
            print(f"   ✅ Cover saved")
        else:
            cover_path = ""
            print(f"   ⚠️ No cover")
    except:
        cover_path = ""
        print(f"   ⚠️ No cover")
    
    # Get text
    text = "No text available"
    text_url = f"https://archive.org/stream/{book_id}/{book_id}_djvu.txt"
    try:
        text_resp = requests.get(text_url, timeout=30)
        if text_resp.status_code == 200:
            text = text_resp.text[:5000]
            print(f"   ✅ Text saved ({len(text)} chars)")
    except:
        print(f"   ⚠️ No text")
    
    # Save data
    book_data = {
        'id': book_id,
        'title': book.get('title', 'Untitled'),
        'author': book.get('creator', 'Unknown'),
        'summary': text[:300] if text else 'No summary',
        'full_text': text,
        'cover_path': cover_path
    }
    
    # Save JSON
    with open(f"books_data/{book_id}.json", 'w', encoding='utf-8') as f:
        json.dump(book_data, f, ensure_ascii=False, indent=2)
    
    # Create reader HTML
    reader_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{book_data['title']} - ReadEra</title>
    <style>
        body {{ font-family: system-ui; max-width: 800px; margin: 0 auto; padding: 2rem; background: #f5f7fa; }}
        .cover {{ text-align: center; margin-bottom: 1rem; }}
        .cover img {{ max-width: 200px; border-radius: 12px; }}
        h1 {{ color: #8B4513; }}
        .content {{ background: white; padding: 2rem; border-radius: 12px; line-height: 1.6; }}
        .back {{ display: inline-block; margin-top: 1rem; color: #8B4513; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="cover">
        {f'<img src="{cover_path}">' if cover_path else '<div style="font-size: 3rem;">📖</div>'}
    </div>
    <h1>{book_data['title']}</h1>
    <p><strong>Author:</strong> {book_data['author']}</p>
    <div class="content">
        <h3>📖 Summary</h3>
        <p>{book_data['summary']}</p>
        <hr>
        <h3>📚 Full Text</h3>
        <p>{text.replace(chr(10), '<br>')}</p>
    </div>
    <a href="browse.html" class="back">← Back to Library</a>
</body>
</html>'''
    
    with open(f"reader_{book_id}.html", 'w', encoding='utf-8') as f:
        f.write(reader_html)
    
    downloaded.append(book_data)
    print(f"   ✅ Reader page created\n")
    
    time.sleep(1)

# Create browse.html
print("\n📄 Creating browse.html...")

browse_html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ReadEra - Hindi Library</title>
    <style>
        body { font-family: system-ui; background: #f5f7fa; padding: 2rem; }
        h1 { color: #8B4513; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; margin-top: 2rem; }
        .card { background: white; border-radius: 12px; overflow: hidden; cursor: pointer; transition: transform 0.2s; }
        .card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
        .cover { height: 200px; background: linear-gradient(135deg, #8B4513, #c17a3a); display: flex; align-items: center; justify-content: center; font-size: 3rem; color: white; }
        .cover img { width: 100%; height: 100%; object-fit: cover; }
        .info { padding: 1rem; }
        .title { font-weight: bold; }
        .author { color: #64748b; font-size: 0.8rem; margin-top: 0.25rem; }
        .btn { display: inline-block; margin-top: 0.5rem; padding: 0.3rem 0.8rem; background: #8B4513; color: white; border-radius: 6px; font-size: 0.7rem; }
    </style>
</head>
<body>
    <h1>📚 ReadEra - Hindi Books Library</h1>
    <p>Creative Commons Books from Internet Archive | ''' + str(len(downloaded)) + ''' books available</p>
    <div class="grid" id="booksGrid"></div>

    <script>
        const books = ''' + json.dumps([{'id': b['id'], 'title': b['title'], 'author': b['author'], 'cover': b['cover_path']} for b in downloaded], ensure_ascii=False) + ''';
        
        function viewBook(id) {
            window.location.href = `reader_${id}.html`;
        }
        
        function render() {
            const grid = document.getElementById('booksGrid');
            grid.innerHTML = books.map(book => `
                <div class="card" onclick="viewBook('${book.id}')">
                    <div class="cover">
                        ${book.cover ? `<img src="${book.cover}">` : '📖'}
                    </div>
                    <div class="info">
                        <div class="title">${book.title.substring(0, 60)}</div>
                        <div class="author">${book.author.substring(0, 50)}</div>
                        <span class="btn">Read Now →</span>
                    </div>
                </div>
            `).join('');
        }
        
        render();
    </script>
</body>
</html>'''

with open('browse.html', 'w', encoding='utf-8') as f:
    f.write(browse_html)

print("\n" + "="*50)
print(f"🎉 COMPLETE!")
print(f"✅ {len(downloaded)} books downloaded")
print(f"🌐 Open browse.html to read")
print("="*50)