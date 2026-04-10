#!/usr/bin/env python3
"""
ReadEra - Auto Book Summary Generator
Internet Archive se books fetch karega aur Gemini se summary generate karega
"""

import os
import time
import requests
import json
from datetime import datetime

# ============================================
# 🔧 APNI VALUES YAHAN DALO 🔧
# ============================================

SUPABASE_URL = "https://ryzbikpzxphrsdctvqp.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_MPqGLh4Z15HdLuTRQ81SzA_Ssm9n"  # 👈 Check this
GEMINI_API_KEY = "AIzaSyBXjE5p5cE20rFkTnRP00530e5JZYfK5TLvs"  # 👈 Check this

# ============================================
# 🚀 CODE START - KUCH CHANGE MAT KARO
# ============================================

# Import libraries
try:
    import google.generativeai as genai
    from supabase import create_client, Client
    from tqdm import tqdm
except ImportError as e:
    print(f"❌ Libraries missing: {e}")
    print("Run: pip install -r requirements.txt")
    exit(1)

# Setup Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Setup Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Test Supabase connection
def test_supabase():
    try:
        result = supabase.table('books').select('count', count='exact').limit(1).execute()
        print("✅ Supabase connected!")
        return True
    except Exception as e:
        print(f"❌ Supabase error: {e}")
        return False

# Fetch books from Internet Archive
def fetch_books_from_archive(limit=10):
    """Internet Archive se books fetch karo"""
    url = "https://archive.org/advancedsearch.php"
    params = {
        "q": "mediatype:texts AND language:eng AND format:pdf",
        "fl": "identifier,title,creator,description,subject",
        "rows": limit,
        "page": 1,
        "output": "json"
    }
    
    print(f"📚 Fetching {limit} books from Internet Archive...")
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"❌ Failed to fetch: {response.status_code}")
        return []
    
    data = response.json()
    books = data.get("response", {}).get("docs", [])
    print(f"✅ Found {len(books)} books")
    return books

# Get full text of book from Internet Archive
def get_book_text(identifier):
    """Book ka full text fetch karo"""
    text_url = f"https://archive.org/stream/{identifier}/{identifier}_djvu.txt"
    
    try:
        response = requests.get(text_url, timeout=30)
        if response.status_code == 200:
            text = response.text
            if len(text) > 50000:
                text = text[:50000] + "...[truncated]"
            return text
        else:
            return None
    except Exception as e:
        print(f"  ⚠️ Failed to fetch text: {e}")
        return None

# Generate summary using Gemini
def generate_summary(title, author, genre, text):
    """Gemini se summary generate karo"""
    prompt = f"""
You are a professional book summarizer. Create a comprehensive summary of this book.

Book Title: {title}
Author: {author}
Genre: {genre}

Your summary MUST include:
1. Main theme and central idea of the book
2. Key concepts and important points (3-5 major points)
3. Practical takeaways for readers
4. Who should read this book (target audience)

Write in clear, engaging English. Keep the summary between 300-500 words.

Book text to summarize:
{text[:45000]}
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"  ❌ Gemini error: {e}")
        return None

# Check if book already exists in Supabase
def book_exists(title, author):
    """Book already hai kya database mein?"""
    try:
        result = supabase.table('books').select('id').eq('title', title).eq('author', author).execute()
        return len(result.data) > 0
    except:
        return False

# Save book to Supabase
def save_to_supabase(title, author, summary, genre):
    """Book ko Supabase mein save karo"""
    try:
        data = {
            "title": title[:200],
            "author": author[:100] if author else "Unknown",
            "summary": summary,
            "genre": genre[:50] if genre else "General",
            "subcategory": "Auto-Generated",
            "pdf_url": "",
            "cover_url": "",
            "total_pages": 0,
            "views": 0,
            "created_at": datetime.now().isoformat()
        }
        
        result = supabase.table('books').insert(data).execute()
        return True
    except Exception as e:
        print(f"  ❌ Save error: {e}")
        return False

# Main function
def main():
    print("\n" + "="*50)
    print("📚 READERA - AUTO BOOK SUMMARY GENERATOR")
    print("="*50 + "\n")
    
    # Test Supabase
    if not test_supabase():
        print("\n❌ Please fix Supabase credentials and try again!")
        return
    
    # Ask for number of books
    try:
        num_books = int(input("\n🔢 How many books to process? (1-100, default 10): ") or "10")
        num_books = min(num_books, 100)
    except:
        num_books = 10
    
    print(f"\n🚀 Starting to process {num_books} books...\n")
    
    # Fetch books
    books = fetch_books_from_archive(num_books)
    
    if not books:
        print("❌ No books found!")
        return
    
    # Process each book
    success_count = 0
    skip_count = 0
    fail_count = 0
    
    for i, book in enumerate(books):
        title = book.get("title", "Unknown")[:200]
        author = book.get("creator", "Unknown")[:100]
        identifier = book.get("identifier", "")
        genre = book.get("subject", "General")
        
        if isinstance(genre, list):
            genre = genre[0] if genre else "General"
        elif not genre:
            genre = "General"
        
        print(f"\n📖 [{i+1}/{len(books)}] Processing: {title[:60]}...")
        
        # Skip if already exists
        if book_exists(title, author):
            print(f"  ⏭️ Already exists in database - skipping")
            skip_count += 1
            continue
        
        # Get full text
        text = get_book_text(identifier)
        if not text or len(text) < 100:
            print(f"  ⚠️ No text available - skipping")
            fail_count += 1
            continue
        
        # Generate summary
        print(f"  🤖 Generating summary...")
        summary = generate_summary(title, author, genre, text)
        
        if not summary:
            print(f"  ❌ Summary generation failed")
            fail_count += 1
            continue
        
        # Save to Supabase
        if save_to_supabase(title, author, summary, genre):
            print(f"  ✅ Saved to database!")
            success_count += 1
        else:
            print(f"  ❌ Failed to save")
            fail_count += 1
        
        # Delay to avoid rate limits
        time.sleep(2)
    
    # Final summary
    print("\n" + "="*50)
    print("📊 FINAL SUMMARY")
    print("="*50)
    print(f"✅ Successfully added: {success_count}")
    print(f"⏭️ Skipped (already exist): {skip_count}")
    print(f"❌ Failed: {fail_count}")
    print(f"📚 Total processed: {success_count + skip_count + fail_count}")
    print("\n🎉 Done!")

if __name__ == "__main__":
    main()