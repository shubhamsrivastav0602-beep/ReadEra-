#!/usr/bin/env python3
"""Generate cover URLs using Open Library API for English books"""

import json
import urllib.parse

# Load books
with open('books_data/index.json', 'r', encoding='utf-8') as f:
    books = json.load(f)

# Create covers mapping
covers_map = {}

# Map of book titles to Open Library keys (for books where title search might be tricky)
OPEN_LIBRARY_MAPPINGS = {
    "pride_prejudice": {"author": "Jane Austen", "title": "Pride and Prejudice"},
    "jane_eyre": {"author": "Charlotte Brontë", "title": "Jane Eyre"},
    "wuthering_heights": {"author": "Emily Brontë", "title": "Wuthering Heights"},
    "great_gatsby": {"author": "F. Scott Fitzgerald", "title": "The Great Gatsby"},
    "moby_dick": {"author": "Herman Melville", "title": "Moby Dick"},
    "alice_wonderland": {"author": "Lewis Carroll", "title": "Alice's Adventures in Wonderland"},
    "adventures_sherlock": {"author": "Arthur Conan Doyle", "title": "The Adventures of Sherlock Holmes"},
    "hound_baskervilles": {"author": "Arthur Conan Doyle", "title": "The Hound of the Baskervilles"},
    "frankenstein": {"author": "Mary Shelley", "title": "Frankenstein"},
    "dracula": {"author": "Bram Stoker", "title": "Dracula"},
    "the_odyssey": {"author": "Homer", "title": "The Odyssey"},
    "the_iliad": {"author": "Homer", "title": "The Iliad"},
    "crime_punishment": {"author": "Fyodor Dostoevsky", "title": "Crime and Punishment"},
    "war_peace": {"author": "Leo Tolstoy", "title": "War and Peace"},
    "anna_karenina": {"author": "Leo Tolstoy", "title": "Anna Karenina"},
    "brothers_karamazov": {"author": "Fyodor Dostoevsky", "title": "The Brothers Karamazov"},
    "jane_austen_emma": {"author": "Jane Austen", "title": "Emma"},
    "jane_austen_sense": {"author": "Jane Austen", "title": "Sense and Sensibility"},
    "jane_austen_northanger": {"author": "Jane Austen", "title": "Northanger Abbey"},
    "jane_austen_mansfield": {"author": "Jane Austen", "title": "Mansfield Park"},
    "testament_youth": {"author": "Vera Brittain", "title": "Testament of Youth"},
    "gulliver_travels": {"author": "Jonathan Swift", "title": "Gulliver's Travels"},
    "robinson_crusoe": {"author": "Daniel Defoe", "title": "Robinson Crusoe"},
    "treasure_island": {"author": "Robert Louis Stevenson", "title": "Treasure Island"},
    "strange_case_jekyll": {"author": "Robert Louis Stevenson", "title": "Strange Case of Dr. Jekyll and Mr. Hyde"},
    "pickwick_papers": {"author": "Charles Dickens", "title": "The Pickwick Papers"},
    "oliver_twist": {"author": "Charles Dickens", "title": "Oliver Twist"},
    "nicholas_nickleby": {"author": "Charles Dickens", "title": "Nicholas Nickleby"},
    "bleak_house": {"author": "Charles Dickens", "title": "Bleak House"},
    "great_expectations": {"author": "Charles Dickens", "title": "Great Expectations"},
    "david_copperfield": {"author": "Charles Dickens", "title": "David Copperfield"},
    "tale_two_cities": {"author": "Charles Dickens", "title": "A Tale of Two Cities"},
    "hard_times": {"author": "Charles Dickens", "title": "Hard Times"},
    "dombey_son": {"author": "Charles Dickens", "title": "Dombey and Son"},
    "martin_chuzzlewit": {"author": "Charles Dickens", "title": "Martin Chuzzlewit"},
    "barnaby_rudge": {"author": "Charles Dickens", "title": "Barnaby Rudge"},
    "tess_d_urbervilles": {"author": "Thomas Hardy", "title": "Tess of the d'Urbervilles"},
    "far_from_madding": {"author": "Thomas Hardy", "title": "Far from the Madding Crowd"},
    "mayor_casterbridge": {"author": "Thomas Hardy", "title": "The Mayor of Casterbridge"},
    "jude_obscure": {"author": "Thomas Hardy", "title": "Jude the Obscure"},
    "wood_beyond_world": {"author": "William Morris", "title": "The Wood Beyond the World"},
    "thirty_nine_steps": {"author": "John Buchan", "title": "The Thirty-Nine Steps"},
    "man_property": {"author": "John Galsworthy", "title": "The Man of Property"},
    "lady_chatterley": {"author": "D.H. Lawrence", "title": "Lady Chatterley's Lover"},
    "sons_lovers": {"author": "D.H. Lawrence", "title": "Sons and Lovers"},
    "ulysses": {"author": "James Joyce", "title": "Ulysses"},
    "portrait_artist": {"author": "James Joyce", "title": "A Portrait of the Artist as a Young Man"},
    "dubliners": {"author": "James Joyce", "title": "Dubliners"},
    "virgin_in_garden": {"author": "A.S. Byatt", "title": "The Virgin in the Garden"},
    "mrs_dalloway": {"author": "Virginia Woolf", "title": "Mrs. Dalloway"},
    "to_lighthouse": {"author": "Virginia Woolf", "title": "To the Lighthouse"},
    "orlando": {"author": "Virginia Woolf", "title": "Orlando"},
    "waves": {"author": "Virginia Woolf", "title": "The Waves"},
    "animal_farm": {"author": "George Orwell", "title": "Animal Farm"},
    "1984": {"author": "George Orwell", "title": "1984"},
    "brave_new_world": {"author": "Aldous Huxley", "title": "Brave New World"},
    "point_counter_point": {"author": "Aldous Huxley", "title": "Point Counter Point"},
    "catcher_rye": {"author": "J.D. Salinger", "title": "The Catcher in the Rye"},
    "sun_also_rises": {"author": "Ernest Hemingway", "title": "The Sun Also Rises"},
    "for_whom_bell_tolls": {"author": "Ernest Hemingway", "title": "For Whom the Bell Tolls"},
    "old_man_sea": {"author": "Ernest Hemingway", "title": "The Old Man and the Sea"},
    "grapes_wrath": {"author": "John Steinbeck", "title": "The Grapes of Wrath"},
    "east_eden": {"author": "John Steinbeck", "title": "East of Eden"},
    "candles_burn": {"author": "F. Scott Fitzgerald", "title": "The Candles Burn"},
    "beautiful_damned": {"author": "F. Scott Fitzgerald", "title": "The Beautiful and Damned"},
    "tender_night": {"author": "F. Scott Fitzgerald", "title": "Tender is the Night"},
    "meditations": {"author": "Marcus Aurelius", "title": "Meditations"},
    "thus_spoke_zara": {"author": "Friedrich Nietzsche", "title": "Thus Spoke Zarathustra"},
    "critique_pure_reason": {"author": "Immanuel Kant", "title": "Critique of Pure Reason"},
    "leviathan": {"author": "Thomas Hobbes", "title": "Leviathan"},
    "social_contract": {"author": "Jean-Jacques Rousseau", "title": "The Social Contract"},
    "origin_species": {"author": "Charles Darwin", "title": "On the Origin of Species"},
    "descent_man": {"author": "Charles Darwin", "title": "The Descent of Man"},
    "decline_fall_roman": {"author": "Edward Gibbon", "title": "The Decline and Fall of the Roman Empire"},
    "phantom_opera": {"author": "Gaston Leroux", "title": "The Phantom of the Opera"},
    "Count_Monte_Cristo": {"author": "Alexandre Dumas", "title": "The Count of Monte Cristo"},
    "three_musketeers": {"author": "Alexandre Dumas", "title": "The Three Musketeers"},
    "dumas_monte_complete": {"author": "Alexandre Dumas", "title": "The Man in the Iron Mask"},
    "vingt_ans_apres": {"author": "Alexandre Dumas", "title": "Twenty Years After"},
    "wrathful_god": {"author": "Emily Brontë", "title": "Wuthering Heights"},
    "picture_dorian": {"author": "Oscar Wilde", "title": "The Picture of Dorian Gray"},
    "importance_earnest": {"author": "Oscar Wilde", "title": "The Importance of Being Earnest"},
    "woman_no_importance": {"author": "Oscar Wilde", "title": "A Woman of No Importance"},
    "time_machine": {"author": "H.G. Wells", "title": "The Time Machine"},
    "island_doctor_moreau": {"author": "H.G. Wells", "title": "The Island of Doctor Moreau"},
    "invisible_man": {"author": "H.G. Wells", "title": "The Invisible Man"},
    "war_worlds": {"author": "H.G. Wells", "title": "The War of the Worlds"},
}

# Gradient colors for different categories (Sanskrit/Hindi books)
GRADIENT_COLORS = {
    "Sanskrit Poetry": {"start": "#8B4513", "end": "#D4AF74"},
    "Sanskrit Philosophy": {"start": "#7B3F00", "end": "#CD7F32"},
    "Sanskrit Epic": {"start": "#654321", "end": "#8B7355"},
    "Sanskrit Drama": {"start": "#6B4423", "end": "#A0826D"},
    "Hindi Literature": {"start": "#C41E3A", "end": "#FF6B6B"},
    "Hindi Fiction": {"start": "#D71A1A", "end": "#FF8A80"},
    "Hindi Poetry": {"start": "#B71C1C", "end": "#EF5350"},
    "Hindu Devotional": {"start": "#F57F17", "end": "#FBC02D"},
    "Buddhist Philosophy": {"start": "#F57C00", "end": "#FFB74D"},
    "Buddhist Literature": {"start": "#D84315", "end": "#FF7043"},
    "Sacred Texts": {"start": "#6D4C41", "end": "#A1887F"},
    "Political Philosophy": {"start": "#1565C0", "end": "#42A5F5"},
    "Medical Science": {"start": "#00695C", "end": "#4DB6AC"},
    "Music Theory": {"start": "#7B1FA2", "end": "#BA68C8"},
    "Architecture": {"start": "#C62828", "end": "#E53935"},
}

def get_gradient_for_book(book):
    """Get gradient colors for a book based on category"""
    category = book.get('category', '')
    
    # Try exact match first
    if category in GRADIENT_COLORS:
        return GRADIENT_COLORS[category]
    
    # Try partial matches
    for key, value in GRADIENT_COLORS.items():
        if key.lower() in category.lower():
            return value
    
    # Default based on language
    lang = book.get('language', '')
    if lang == 'Sanskrit':
        return {"start": "#8B4513", "end": "#D4AF74"}
    elif lang == 'Hindi':
        return {"start": "#C41E3A", "end": "#FF6B6B"}
    else:
        return {"start": "#1e40af", "end": "#3b82f6"}

# Process each book
for book in books:
    book_id = book['id']
    
    if book['language'] == 'English':
        # Try to get Open Library cover
        if book_id in OPEN_LIBRARY_MAPPINGS:
            mapping = OPEN_LIBRARY_MAPPINGS[book_id]
            title = mapping['title']
            author = mapping['author']
            
            # Create Open Library search query
            query = f"{title} {author}".replace(" ", "+")
            
            # Open Library API endpoint for cover search
            ol_url = f"https://covers.openlibrary.org/b/title/{urllib.parse.quote(title)}-M.jpg"
            
            covers_map[book_id] = {
                "type": "openlib",
                "url": ol_url,
                "fallback_gradient": get_gradient_for_book(book)
            }
        else:
            # Fallback gradient
            covers_map[book_id] = {
                "type": "gradient",
                "gradient": get_gradient_for_book(book)
            }
    else:
        # Sanskrit, Hindi, etc. - use gradients
        covers_map[book_id] = {
            "type": "gradient",
            "gradient": get_gradient_for_book(book)
        }

# Save covers mapping
with open('books_data/covers.json', 'w', encoding='utf-8') as f:
    json.dump(covers_map, f, ensure_ascii=False, indent=2)

print(f"✅ Generated covers.json with {len(covers_map)} entries")
english_books = sum(1 for v in covers_map.values() if v.get('type') == 'openlib')
gradient_books = sum(1 for v in covers_map.values() if v.get('type') == 'gradient')
print(f"   📚 {english_books} English books with Open Library covers")
print(f"   🎨 {gradient_books} books with gradient covers")
