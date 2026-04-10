#!/usr/bin/env python3
import requests
import json
import os
import time
import re
from pathlib import Path

import sys

# Ensure UTF-8 output even on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Configuration
BOOKS_FOLDER = "books_data"
COVERS_FOLDER = "covers"
os.makedirs(BOOKS_FOLDER, exist_ok=True)
os.makedirs(COVERS_FOLDER, exist_ok=True)

class HindiBookFetcher:
    def __init__(self):
        self.books_index_path = os.path.join(BOOKS_FOLDER, "index.json")
        self.existing_books = self.load_existing_books()
        self.session = requests.Session()

    def load_existing_books(self):
        if os.path.exists(self.books_index_path):
            try:
                with open(self.books_index_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_books_index(self):
        with open(self.books_index_path, 'w', encoding='utf-8') as f:
            json.dump(self.existing_books, f, ensure_ascii=False, indent=2)
        print(f"[INFO] Updated index with {len(self.existing_books)} total books.")

    def book_exists(self, book_id):
        return any(b['id'] == book_id for b in self.existing_books)

    def fetch_hindi_books(self, limit=20):
        # Query for Hindi books with Creative Commons or Public Domain
        # We search specifically in the booksbylanguage_hindi collection
        search_url = "https://archive.org/advancedsearch.php"
        params = {
            'q': 'collection:booksbylanguage_hindi AND mediatype:texts AND (licenseurl:*creativecommons* OR licenseurl:*publicdomain*)',
            'fl[]': ['identifier', 'title', 'creator', 'description', 'licenseurl', 'date', 'subject'],
            'rows': limit,
            'page': 1,
            'output': 'json'
        }
        
        try:
            print(f"[SEARCH] Searching Internet Archive for Hindi Creative Commons books...")
            response = self.session.get(search_url, params=params, timeout=30)
            data = response.json()
            docs = data.get('response', {}).get('docs', [])
            print(f"[FOUND] Found {len(docs)} books matching criteria.")
            return docs
        except Exception as e:
            print(f"[ERROR] Error during search: {e}")
            return []

    def get_full_text(self, identifier):
        """Try multiple ways to get the full text content"""
        # First, check metadata for files
        meta_url = f"https://archive.org/metadata/{identifier}"
        try:
            resp = self.session.get(meta_url, timeout=20)
            meta_data = resp.json()
            files = meta_data.get('files', [])
            
            # Look for djvu.txt or similar text files
            text_files = [f['name'] for f in files if f['name'].endswith('_djvu.txt') or f['name'].endswith('_fulltext.txt')]
            if not text_files:
                text_files = [f['name'] for f in files if f['name'].endswith('.txt') and 'license' not in f['name'].lower()]

            for text_file in text_files:
                download_url = f"https://archive.org/download/{identifier}/{text_file}"
                print(f"   [DOWN] Downloading text from: {text_file}...")
                text_resp = self.session.get(download_url, timeout=60)
                if text_resp.status_code == 200:
                    content = text_resp.text
                    if len(content) > 1000: # Ensure it's not a stub
                        return content
        except Exception as e:
            print(f"   [WARN] Error getting text: {e}")
        
        return None

    def get_cover_image(self, identifier):
        """Find and download the best quality cover image"""
        # Try service img first
        service_url = f"https://archive.org/services/img/{identifier}"
        try:
            resp = self.session.get(service_url, timeout=20)
            if resp.status_code == 200 and 'image' in resp.headers.get('Content-Type', ''):
                cover_filename = f"{identifier}.jpg"
                cover_path = os.path.join(COVERS_FOLDER, cover_filename)
                with open(cover_path, 'wb') as f:
                    f.write(resp.content)
                return f"covers/{cover_filename}"
        except:
            pass
        return "covers/default.jpg"

    def clean_text(self, text):
        """Basic cleaning of OCR text if needed"""
        # Remove excessive whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

    def process_books(self, docs):
        newly_added = 0
        for doc in docs:
            identifier = doc['identifier']
            if self.book_exists(identifier):
                print(f"[SKIP] Book {identifier} already exists, skipping.")
                continue

            title = doc.get('title', 'Untitled Hindi Book')
            creator = doc.get('creator', 'Unknown Author')
            if isinstance(creator, list): creator = ", ".join(creator)
            
            description = doc.get('description', 'No description available.')
            # Clean HTML from description if any
            description = re.sub('<[^<]+?>', '', description)
            
            print(f"\n[BOOK] Processing: {title}")
            
            # Get full text
            full_text = self.get_full_text(identifier)
            if not full_text:
                print(f"   [FAIL] No full text found for {identifier}. Skipping.")
                continue
                
            full_text = self.clean_text(full_text)
            
            # Save text file
            text_filename = f"{identifier}.txt"
            with open(os.path.join(BOOKS_FOLDER, text_filename), 'w', encoding='utf-8') as f:
                f.write(full_text)
                
            # Get cover
            cover_path = self.get_cover_image(identifier)
            
            # Detect language (simplified)
            lang = "Hindi" if re.search('[\u0900-\u097F]', full_text) else "English"
            
            # Create book entry
            book_entry = {
                "id": identifier,
                "title": title,
                "author": creator,
                "category": "Hindi Literature",
                "language": lang,
                "cover": cover_path,
                "description": description,
                "featured": False,
                "source": "Internet Archive",
                "license": doc.get('licenseurl', 'Creative Commons'),
                "added_date": time.strftime("%Y-%m-%d")
            }
            
            self.existing_books.append(book_entry)
            newly_added += 1
            print(f"   [OK] Added successfully!")
            
            # Intermittent save
            self.save_books_index()
            
            # Small delay to be polite
            time.sleep(1)

        print(f"\n[DONE] Process complete. Added {newly_added} new books.")

if __name__ == "__main__":
    fetcher = HindiBookFetcher()
    docs = fetcher.fetch_hindi_books(limit=10) # Start with 10 books
    fetcher.process_books(docs)
