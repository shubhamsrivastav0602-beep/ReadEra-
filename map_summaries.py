import json
import os
import re

def create_summary_mapping():
    books_data_path = 'books_data/index.json'
    summaries_root = 'summaries'
    mapping = {}

    if not os.path.exists(books_data_path):
        print("index.json not found")
        return

    with open(books_data_path, 'r', encoding='utf-8') as f:
        books = json.load(f)

    # Get all summary files
    summary_files = []
    for root, dirs, files in os.walk(summaries_root):
        for file in files:
            if file.endswith('.md'):
                summary_files.append(os.path.join(root, file))

    print(f"Found {len(summary_files)} summary files.")

    for book in books:
        book_title = book.get('title', '').lower()
        book_id = book.get('id', '').lower()
        
        # Try to find a matching summary
        match = None
        for summary_path in summary_files:
            summary_name = os.path.basename(summary_path).lower()
            # Clean summary name (remove index 01_, extension .md, and special chars)
            clean_name = re.sub(r'^\d+_', '', summary_name)
            clean_name = clean_name.replace('.md', '').replace('_', ' ')
            
            # Check for matches
            if clean_name in book_title or book_id in summary_name or book_title in clean_name:
                match = summary_path
                break
        
        if match:
            # Store relative path
            mapping[book['id']] = match.replace('\\', '/')

    with open('summaries/mapping.json', 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    print(f"Successfully mapped {len(mapping)} books to summaries.")

if __name__ == "__main__":
    create_summary_mapping()
