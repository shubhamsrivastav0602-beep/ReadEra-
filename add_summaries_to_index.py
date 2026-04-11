import os
import json
import re
from pathlib import Path

# Load existing books
index_path = os.path.join(os.path.dirname(__file__), 'public', 'books_data', 'index.json')
with open(index_path, 'r', encoding='utf-8') as f:
    books = json.load(f)

# Map to track existing IDs
existing_ids = {book.get('id') for book in books}

# Scan summaries and add them
summaries_base = os.path.join(os.path.dirname(__file__), 'summaries')
category_map = {
    'Finance': 'Finance',
    'Fiction': 'Fiction', 
    'Biography': 'Biography',
    'Biography_Autobiography': 'Biography',
    'Classic_Hindi': 'Classic Hindi',
    'Non-Fiction': 'Non-Fiction',
    'Religious_Spiritual': 'Religious & Spiritual',
    'Romance': 'Romance',
    'Sci-Fi': 'Science Fiction',
    'Self-Help': 'Self Help',
    'Tech_Programming': 'Technology & Programming'
}

for category_dir in os.listdir(summaries_base):
    category_path = os.path.join(summaries_base, category_dir)
    if not os.path.isdir(category_path):
        continue
    
    category_name = category_map.get(category_dir, category_dir)
    
    for filename in sorted(os.listdir(category_path)):
        if filename.endswith('.md'):
            filepath = os.path.join(category_path, filename)
            
            # Generate ID
            base_name = filename.replace('.md', '')
            book_id = re.sub(r'^\d+_', '', base_name).lower().replace(' ', '_')
            
            # Skip if already exists
            if book_id in existing_ids:
                continue
            
            # Extract title from filename
            title = re.sub(r'^\d+_', '', base_name).replace('_', ' ')
            
            # Read first few  lines to extract author if available
            try:
                with open(filepath, 'r', encoding='utf-8') as mf:
                    content = mf.read(500)
                    # Try to extract author
                    author_match = re.search(r'[Bb]y\s+([^<\n]+)', content)
                    author = author_match.group(1).strip() if author_match else 'Unknown Author'
                    
                    # Try to extract description
                    desc_match = re.search(r'(?:Summary|Overview|Description)[:\s]+([^<\n]+)', content, re.IGNORECASE)
                    description = desc_match.group(1).strip() if desc_match else f"Summary of {title}"
            except:
                author = 'Unknown Author'
                description = f"Summary of {title}"
            
            # Create book entry
            book_entry = {
                'id': book_id,
                'title': title,
                'author': author,
                'category': category_name,
                'language': 'English',
                'description': description,
                'is_summary': True,
                'summary_path': f'summaries/{category_dir}/{filename}'
            }
            
            books.append(book_entry)
            existing_ids.add(book_id)
            print(f"Added: {title} ({book_id})")

# Save updated index
with open(index_path, 'w', encoding='utf-8') as f:
    json.dump(books, f, indent=2, ensure_ascii=False)

print(f"\nTotal books: {len(books)}")
print(f"Saved to {index_path}")
