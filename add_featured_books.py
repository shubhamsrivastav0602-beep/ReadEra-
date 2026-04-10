import json

# Path to the books data file
BOOKS_FILE = 'books_data/index.json'

# List of 20 featured book IDs
FEATURED_BOOK_IDS = [
    # Sanskrit Classics (3)
    'bhagavad_gita',
    'ramayana_complete',
    'yoga_sutras',
    
    # Hindi Literature (3)
    'godan',
    'devdas',
    'hanuman_chalisa',
    
    # English Classics (3)
    'great_gatsby',
    'pride_prejudice',
    '1984',
    
    # Philosophy & Buddhism (3)
    'brahma_sutras',
    'samkhya_karika',
    'dhammapada',
    
    # Science & Medicine (3)
    'aryabhatiya',
    'ayurveda_samhita',
    'sushruta_samhita',
    
    # Drama & Poetry (3)
    'shakuntala',
    'kalidasa_kumara',
    'meghaduta',
    
    # Other Popular (2)
    'animal_farm',
    'frankenstein'
]

def add_featured_flag():
    """Add 'featured': True to the top 20 books"""
    try:
        # Read the current books data
        with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
            books = json.load(f)
        
        # Add featured flag
        featured_count = 0
        for book in books:
            if book['id'] in FEATURED_BOOK_IDS:
                book['featured'] = True
                featured_count += 1
            else:
                book['featured'] = False
        
        # Save the updated books
        with open(BOOKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(books, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Successfully marked {featured_count} books as featured")
        print(f"✓ Total books in library: {len(books)}")
        
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == '__main__':
    add_featured_flag()
