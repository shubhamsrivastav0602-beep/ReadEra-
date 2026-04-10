#!/usr/bin/env python3
"""Create text files for all books in index.json"""

import json
import os

# Load index
with open('books_data/index.json', 'r', encoding='utf-8') as f:
    books = json.load(f)

# Generate text files for books that don't have them
for book in books:
    text_file = f"books_data/{book['id']}.txt"
    
    # Skip if file already exists
    if os.path.exists(text_file):
        print(f"✅ {book['title']} - Already exists")
        continue
    
    # Create content
    content = f"""{book['title']}

By {book['author']}
Category: {book['category']}
Language: {book['language']}

{book['description']}

---

Chapter 1: Introduction

This is a digital copy of "{book['title']}" by {book['author']}.

{book['description']}

The work belongs to the category of {book['category']} and is written in {book['language']}.

Chapter 2: Content

[This is a sample text file. In a production environment, the complete content of the book would be stored here.]

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.

Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Chapter 3: Conclusion

Thank you for reading "{book['title']}" on ReadEra.

This book is part of our Creative Commons collection.

For more books, please visit our Browse page.

---

Total Pages: 50
Total Words: ~12,000
First Published: Ancient Times
Language: {book['language']}
Category: {book['category']}
"""
    
    # Write file
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Created: {book['title']}")

print(f"\n✅ Total books: {len(books)}")
print(f"✅ All text files created successfully!")
