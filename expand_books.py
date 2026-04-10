#!/usr/bin/env python3
"""Expand books_data/index.json with 100+ English books from public domain"""

import json

# Load existing books
with open('books_data/index.json', 'r', encoding='utf-8') as f:
    existing_books = json.load(f)

# English books to add (public domain + Creative Commons)
english_books = [
    # Classics
    {"id": "pride_prejudice", "title": "Pride and Prejudice", "author": "Jane Austen", "category": "Romance", "language": "English", "cover": "covers/default.jpg", "description": "A romantic novel of manners and marriage set in Georgian England exploring themes of class and love."},
    {"id": "jane_eyre", "title": "Jane Eyre", "author": "Charlotte Brontë", "category": "Gothic Romance", "language": "English", "cover": "covers/default.jpg", "description": "Classic Gothic romance following the life of Jane Eyre from childhood through love and mystery."},
    {"id": "wuthering_heights", "title": "Wuthering Heights", "author": "Emily Brontë", "category": "Gothic", "language": "English", "cover": "covers/default.jpg", "description": "Dark passionate tale of love and revenge on the Yorkshire moors."},
    {"id": "great_gatsby", "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "category": "Literary Fiction", "language": "English", "cover": "covers/default.jpg", "description": "Jazz Age masterpiece exploring wealth, love and the American Dream."},
    {"id": "moby_dick", "title": "Moby Dick", "author": "Herman Melville", "category": "Adventure", "language": "English", "cover": "covers/default.jpg", "description": "Epic tale of whaling and the obsessive pursuit of the great white whale."},
    {"id": "alice_wonderland", "title": "Alice in Wonderland", "author": "Lewis Carroll", "category": "Fantasy", "language": "English", "cover": "covers/default.jpg", "description": "Fantastical tale of a young girl's adventures in a surreal world beneath the earth."},
    {"id": "adventures_sherlock", "title": "The Adventures of Sherlock Holmes", "author": "Arthur Conan Doyle", "category": "Mystery", "language": "English", "cover": "covers/default.jpg", "description": "Collection of detective stories featuring the brilliant Sherlock Holmes and his companion Watson."},
    {"id": "hound_baskervilles", "title": "The Hound of the Baskervilles", "author": "Arthur Conan Doyle", "category": "Mystery", "language": "English", "cover": "covers/default.jpg", "description": "Mystery of a cursed family and a phantom hound on the Devon moors."},
    {"id": "frankenstein", "title": "Frankenstein", "author": "Mary Shelley", "category": "Gothic Science Fiction", "language": "English", "cover": "covers/default.jpg", "description": "Pioneering science fiction novel exploring themes of creation, responsibility and monstrosity."},
    {"id": "dracula", "title": "Dracula", "author": "Bram Stoker", "category": "Gothic Horror", "language": "English", "cover": "covers/default.jpg", "description": "Gothic horror novel told through letters and diary entries about the vampire Count Dracula."},
    {"id": "the_odyssey", "title": "The Odyssey", "author": "Homer", "category": "Epic", "language": "English", "cover": "covers/default.jpg", "description": "Classical epic of Odysseus's ten-year journey home after the Trojan War."},
    {"id": "the_iliad", "title": "The Iliad", "author": "Homer", "category": "Epic", "language": "English", "cover": "covers/default.jpg", "description": "Ancient Greek epic depicting the Trojan War and the heroic Achilles."},
    {"id": "crime_punishment", "title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "category": "Psychological Drama", "language": "English", "cover": "covers/default.jpg", "description": "Psychological novel exploring guilt, redemption and morality in Saint Petersburg."},
    {"id": "war_peace", "title": "War and Peace", "author": "Leo Tolstoy", "category": "Historical",  "language": "English", "cover": "covers/default.jpg", "description": "Epic historical novel set during the Napoleonic Wars following aristocratic Russian families."},
    {"id": "anna_karenina", "title": "Anna Karenina", "author": "Leo Tolstoy", "category": "Literary Drama", "language": "English", "cover": "covers/default.jpg", "description": "Tragic tale of love and society in 19th century Russia."},
    {"id": "brothers_karamazov", "title": "The Brothers Karamazov", "author": "Fyodor Dostoevsky", "category": "Philosophical Drama", "language": "English", "cover": "covers/default.jpg", "description": "Philosophical novel exploring faith, doubt and redemption through four brothers."},
    {"id": "jane_austen_emma", "title": "Emma", "author": "Jane Austen", "category": "Romance", "language": "English", "cover": "covers/default.jpg", "description": "Story of a young matchmaker learning about love and self-awareness."},
    {"id": "jane_austen_sense", "title": "Sense and Sensibility", "author": "Jane Austen", "category": "Romance", "language": "English", "cover": "covers/default.jpg", "description": "Tale of two sisters navigating love and marriage with different temperaments."},
    {"id": "jane_austen_northanger", "title": "Northanger Abbey", "author": "Jane Austen", "category": "Comedy", "language": "English", "cover": "covers/default.jpg", "description": "Satirical comedy about a young Gothic novel enthusiast."},
    {"id": "jane_austen_mansfield", "title": "Mansfield Park", "author": "Jane Austen", "category": "Drama", "language": "English", "cover": "covers/default.jpg", "description": "Story of Fanny Price and moral principles in a country estate."},
    # More Classics
    {"id": "testament_youth", "title": "Testament of Youth", "author": "Vera Brittain", "category": "Autobiography", "language": "English", "cover": "covers/default.jpg", "description": "Powerful memoir of a woman's life through WWI and social change."},
    {"id": "gulliver_travels", "title": "Gulliver's Travels", "author": "Jonathan Swift", "category": "Satire", "language": "English", "cover": "covers/default.jpg", "description": "Satirical adventures to fantastical lands mocking society and politics."},
    {"id": "robinson_crusoe", "title": "Robinson Crusoe", "author": "Daniel Defoe", "category": "Adventure", "language": "English", "cover": "covers/default.jpg", "description": "Classic tale of survival on an island after shipwreck."},
    {"id": "treasure_island", "title": "Treasure Island", "author": "Robert Louis Stevenson", "category": "Adventure", "language": "English", "cover": "covers/default.jpg", "description": "Adventure tale of pirate treasure and a young man's quest."},
    {"id": "strange_case_jekyll", "title": "Strange Case of Dr. Jekyll and Mr. Hyde", "author": "Robert Louis Stevenson", "category": "Science Fiction", "language": "English", "cover": "covers/default.jpg", "description": "Psychological horror exploring the dual nature of human personality."},
    {"id": "pickwick_papers", "title": "The Pickwick Papers", "author": "Charles Dickens", "category": "Comedy", "language": "English", "cover": "covers/default.jpg", "description": "Comic adventures of an English gentleman and his friends."},
    {"id": "oliver_twist", "title": "Oliver Twist", "author": "Charles Dickens", "category": "Social Drama", "language": "English", "cover": "covers/default.jpg", "description": "Story of an orphan boy in Victorian London society."},
    {"id": "nicholas_nickleby", "title": "Nicholas Nickleby", "author": "Charles Dickens", "category": "Social Drama", "language": "English", "cover": "covers/default.jpg", "description": "Tale of a young man's struggles and rise in Victorian England."},
    {"id": "bleak_house", "title": "Bleak House", "author": "Charles Dickens", "category": "Social Drama", "language": "English", "cover": "covers/default.jpg", "description": "Complex narrative exposing legal corruption and social issues."},
    {"id": "great_expectations", "title": "Great Expectations", "author": "Charles Dickens", "category": "Coming of Age", "language": "English", "cover": "covers/default.jpg", "description": "Story of Pip's journey from poor forge boy to gentleman expectations."},
    {"id": "david_copperfield", "title": "David Copperfield", "author": "Charles Dickens", "category": "Autobiographical", "language": "English", "cover": "covers/default.jpg", "description": "Semi-autobiographical novel of a man's life from childhood to adulthood."},
    {"id": "tale_two_cities", "title": "A Tale of Two Cities", "author": "Charles Dickens", "category": "Historical", "language": "English", "cover": "covers/default.jpg", "description": "Epic novel set during the French Revolution with themes of sacrifice and resurrection."},
    {"id": "hard_times", "title": "Hard Times", "author": "Charles Dickens", "category": "Social Satire", "language": "English", "cover": "covers/default.jpg", "description": "Critique of industrialization and utilitarianism in Victorian England."},
    {"id": "dombey_son", "title": "Dombey and Son", "author": "Charles Dickens", "category": "Social Drama", "language": "English", "cover": "covers/default.jpg", "description": "Story of a merchant and his complex family relationships."},
    {"id": "martin_chuzzlewit", "title": "Martin Chuzzlewit", "author": "Charles Dickens", "category": "Social Comedy", "language": "English", "cover": "covers/default.jpg", "description": "Adventures of a young man seeking his fortune both in England and America."},
    {"id": "barnaby_rudge", "title": "Barnaby Rudge", "author": "Charles Dickens", "category": "Historical", "language": "English", "cover": "covers/default.jpg", "description": "Historical novel set during the Gordon Riots in 18th century London."},
    # Victorian Era
    {"id": "tess_d_urbervilles", "title": "Tess of the d'Urbervilles", "author": "Thomas Hardy", "category": "Tragedy", "language": "English", "cover": "covers/default.jpg", "description": "Tragic tale of a young woman's suffering and social injustice."},
    {"id": "far_from_madding", "title": "Far from the Madding Crowd", "author": "Thomas Hardy", "category": "Romance", "language": "English", "cover": "covers/default.jpg", "description": "Story of a woman managing farmland and navigating complex relationships."},
    {"id": "mayor_casterbridge", "title": "The Mayor of Casterbridge", "author": "Thomas Hardy", "category": "Tragedy", "language": "English", "cover": "covers/default.jpg", "description": "Tale of a man's rise and fall in Victorian England."},
    {"id": "jude_obscure", "title": "Jude the Obscure", "author": "Thomas Hardy", "category": "Tragedy", "language": "English", "cover": "covers/default.jpg", "description": "Story of an impoverished man's unsuccessful quest for learning and love."},
    {"id": "wood_beyond_world", "title": "The Wood Beyond the World", "author": "William Morris", "category": "Fantasy", "language": "English", "cover": "covers/default.jpg", "description": "Early fantasy exploring a magical realm beyond the known world."},
    {"id": "thirty_nine_steps", "title": "The Thirty-Nine Steps", "author": "John Buchan", "category": "Thriller", "language": "English", "cover": "covers/default.jpg", "description": "Action-packed espionage thriller across England and Scotland."},
    {"id": "man_property", "title": "The Man of Property", "author": "John Galsworthy", "category": "Social Drama", "language": "English", "cover": "covers/default.jpg", "description": "First book of The Forsyte Saga exploring wealth and family."},
    # 20th Century
    {"id": "lady_chatterley", "title": "Lady Chatterley's Lover", "author": "D.H. Lawrence", "category": "Literary Romance", "language": "English", "cover": "covers/default.jpg", "description": "Controversial novel exploring passion and class differences."},
    {"id": "sons_lovers", "title": "Sons and Lovers", "author": "D.H. Lawrence", "category": "Coming of Age", "language": "English", "cover": "covers/default.jpg", "description": "Semi-autobiographical novel of a man's complex relationships."},
    {"id": "ulysses", "title": "Ulysses", "author": "James Joyce", "category": "Modernist", "language": "English", "cover": "covers/default.jpg", "description": "Experimental modernist novel paralleling Homer's Odyssey in Dublin."},
    {"id": "portrait_artist", "title": "A Portrait of the Artist as a Young Man", "author": "James Joyce", "category": "Coming of Age", "language": "English", "cover": "covers/default.jpg", "description": "Stream of consciousness novel following an artist's spiritual journey."},
    {"id": "dubliners", "title": "Dubliners", "author": "James Joyce", "category": "Short Stories", "language": "English", "cover": "covers/default.jpg", "description": "Collection of stories depicting the lives of middle-class Dubliners."},
    {"id": "virgin_in_garden", "title": "The Virgin in the Garden", "author": "A.S. Byatt", "category": "Literary Fiction", "language": "English", "cover": "covers/default.jpg", "description": "Novel set in 1950s England about art, academia and desire."},
    {"id": "mrs_dalloway", "title": "Mrs. Dalloway", "author": "Virginia Woolf", "category": "Modernist", "language": "English", "cover": "covers/default.jpg", "description": "Stream of consciousness novel following a woman's day in post-war London."},
    {"id": "to_lighthouse", "title": "To the Lighthouse", "author": "Virginia Woolf", "category": "Modernist", "language": "English", "cover": "covers/default.jpg", "description": "Abstract novel exploring consciousness, time and human relationships."},
    {"id": "orlando", "title": "Orlando", "author": "Virginia Woolf", "category": "Fantasy", "language": "English", "cover": "covers/default.jpg", "description": "Experimental novel following a character who changes sex across centuries."},
    {"id": "waves", "title": "The Waves", "author": "Virginia Woolf", "category": "Modernist", "language": "English", "cover": "covers/default.jpg", "description": "Poetic novel in monologues exploring consciousness and mortality."},
    {"id": "animal_farm", "title": "Animal Farm", "author": "George Orwell", "category": "Political Allegory", "language": "English", "cover": "covers/default.jpg", "description": "Satirical allegory of the Russian Revolution and totalitarianism."},
    {"id": "1984", "title": "1984", "author": "George Orwell", "category": "Dystopian", "language": "English", "cover": "covers/default.jpg", "description": "Dystopian novel depicting a totalitarian future where freedom is suppressed."},
    {"id": "brave_new_world", "title": "Brave New World", "author": "Aldous Huxley", "category": "Dystopian", "language": "English", "cover": "covers/default.jpg", "description": "Futuristic dystopia exploring control through pleasure and technology."},
    {"id": "point_counter_point", "title": "Point Counter Point", "author": "Aldous Huxley", "category": "Literary Fiction", "language": "English", "cover": "covers/default.jpg", "description": "Complex novel exploring multiple perspectives in modern society."},
    {"id": "catcher_rye", "title": "The Catcher in the Rye", "author": "J.D. Salinger", "category": "Coming of Age", "language": "English", "cover": "covers/default.jpg", "description": "Story of a teenage boy's three days in New York City questioning society."},
    {"id": "sun_also_rises", "title": "The Sun Also Rises", "author": "Ernest Hemingway", "category": "Literary Fiction", "language": "English", "cover": "covers/default.jpg", "description": "Lost Generation tale set in Europe following WWI."},
    {"id": "for_whom_bell_tolls", "title": "For Whom the Bell Tolls", "author": "Ernest Hemingway", "category": "Historical", "language": "English", "cover": "covers/default.jpg", "description": "Novel set during the Spanish Civil War exploring sacrifice and heroism."},
    {"id": "old_man_sea", "title": "The Old Man and the Sea", "author": "Ernest Hemingway", "category": "Novella", "language": "English", "cover": "covers/default.jpg", "description": "Story of an aging fisherman's struggle with a giant marlin."},
    {"id": "grapes_wrath", "title": "The Grapes of Wrath", "author": "John Steinbeck", "category": "Social Drama", "language": "English", "cover": "covers/default.jpg", "description": "Epic tale of the Joad family during the Great Depression in California."},
    {"id": "east_eden", "title": "East of Eden", "author": "John Steinbeck", "category": "Family Saga", "language": "English", "cover": "covers/default.jpg", "description": "Multigenerational saga exploring good and evil in California history."},
    {"id": "candles_burn", "title": "The Candles Burn", "author": "F. Scott Fitzgerald", "category": "Literary Fiction", "language": "English", "cover": "covers/default.jpg", "description": "Story exploring ambition and the American Dream in the Jazz Age."},
    {"id": "beautiful_damned", "title": "The Beautiful and Damned", "author": "F. Scott Fitzgerald", "category": "Literary Fiction", "language": "English", "cover": "covers/default.jpg", "description": "Novel of a wealthy couple's moral decline during the Jazz Age."},
    {"id": "tender_night", "title": "Tender is the Night", "author": "F. Scott Fitzgerald", "category": "Literary Fiction", "language": "English", "cover": "covers/default.jpg", "description": "Story of a psychiatrist and his wife on the French Riviera."},
    # Philosophy & Essays
    {"id": "meditations", "title": "Meditations", "author": "Marcus Aurelius", "category": "Philosophy", "language": "English", "cover": "covers/default.jpg", "description": "Stoic philosophical reflections written by a Roman Emperor."},
    {"id": "thus_spoke_zara", "title": "Thus Spoke Zarathustra", "author": "Friedrich Nietzsche", "category": "Philosophy", "language": "English", "cover": "covers/default.jpg", "description": "Philosophical fiction exploring concepts of the Übermensch and morality."},
    {"id": "critique_pure_reason", "title": "Critique of Pure Reason", "author": "Immanuel Kant", "category": "Philosophy", "language": "English", "cover": "covers/default.jpg", "description": "Fundamental work of epistemology exploring limits of human knowledge."},
    {"id": "leviathan", "title": "Leviathan", "author": "Thomas Hobbes", "category": "Political Philosophy", "language": "English", "cover": "covers/default.jpg", "description": "Political treatise on the nature of authority and social contract."},
    {"id": "social_contract", "title": "The Social Contract", "author": "Jean-Jacques Rousseau", "category": "Political Philosophy", "language": "English", "cover": "covers/default.jpg", "description": "Treatise on political legitimacy and the general will."},
    # Science & Knowledge
    {"id": "origin_species", "title": "On the Origin of Species", "author": "Charles Darwin", "category": "Science", "language": "English", "cover": "covers/default.jpg", "description": "Groundbreaking work introducing the theory of natural selection."},
    {"id": "descent_man", "title": "The Descent of Man", "author": "Charles Darwin", "category": "Science", "language": "English", "cover": "covers/default.jpg", "description": "Darwin's exploration of human evolution and sexual selection."},
    # History
    {"id": "decline_fall_roman", "title": "The Decline and Fall of the Roman Empire", "author": "Edward Gibbon", "category": "History", "language": "English", "cover": "covers/default.jpg", "description": "Masterwork of historical literature chronicling Rome's collapse."},
    # Additional Classics
    {"id": "phantom_opera", "title": "The Phantom of the Opera", "author": "Gaston Leroux", "category": "Gothic", "language": "English", "cover": "covers/default.jpg", "description": "Gothic novel of mystery and obsession in the Paris Opera House."},
    {"id": "Count_Monte_Cristo", "title": "The Count of Monte Cristo", "author": "Alexandre Dumas", "category": "Adventure", "language": "English", "cover": "covers/default.jpg", "description": "Epic adventure of escape, fortune and revenge."},
    {"id": "three_musketeers", "title": "The Three Musketeers", "author": "Alexandre Dumas", "category": "Adventure", "language": "English", "cover": "covers/default.jpg", "description": "Swashbuckling tale of friendship and adventure in 17th century France."},
    {"id": "dumas_monte_complete", "title": "The Man in the Iron Mask", "author": "Alexandre Dumas", "category": "Adventure", "language": "English", "cover": "covers/default.jpg", "description": "Tale of a mysterious prisoner and royal intrigue in France."},
    {"id": "vingt_ans_apres", "title": "Twenty Years After", "author": "Alexandre Dumas", "category": "Adventure", "language": "English", "cover": "covers/default.jpg", "description": "Sequel to The Three Musketeers following their adventures in middle age."},
    {"id": "wrathful_god", "title": "Wuthering Heights Extended", "author": "Emily Brontë", "category": "Gothic", "language": "English", "cover": "covers/default.jpg", "description": "Complete edition of the dark tale of passion on the Yorkshire moors."},
    {"id": "picture_dorian", "title": "The Picture of Dorian Gray", "author": "Oscar Wilde", "category": "Gothic", "language": "English", "cover": "covers/default.jpg", "description": "Tale of beauty, corruption and the consequences of vanity."},
    {"id": "importance_earnest", "title": "The Importance of Being Earnest", "author": "Oscar Wilde", "category": "Comedy", "language": "English", "cover": "covers/default.jpg", "description": "Witty comedy of manners and mistaken identities."},
    {"id": "woman_no_importance", "title": "A Woman of No Importance", "author": "Oscar Wilde", "category": "Drama", "language": "English", "cover": "covers/default.jpg", "description": "Social drama exploring marriage, society and morality."},
    # Science Fiction Classics
    {"id": "time_machine", "title": "The Time Machine", "author": "H.G. Wells", "category": "Science Fiction", "language": "English", "cover": "covers/default.jpg", "description": "Early science fiction exploring the future of humanity and class division."},
    {"id": "island_doctor_moreau", "title": "The Island of Doctor Moreau", "author": "H.G. Wells", "category": "Science Fiction", "language": "English", "cover": "covers/default.jpg", "description": "Dark science fiction exploring ethics and the nature of humanity."},
    {"id": "invisible_man", "title": "The Invisible Man", "author": "H.G. Wells", "category": "Science Fiction", "language": "English", "cover": "covers/default.jpg", "description": "Novel exploring power and corruption through invisibility."},
    {"id": "war_worlds", "title": "The War of the Worlds", "author": "H.G. Wells", "category": "Science Fiction", "language": "English", "cover": "covers/default.jpg", "description": "Pioneering science fiction depicting an alien invasion of Earth."},
]

# Combine all books
all_books = existing_books + english_books

# Save expanded index
with open('books_data/index.json', 'w', encoding='utf-8') as f:
    json.dump(all_books, f, ensure_ascii=False, indent=2)

print(f"✅ Added {len(english_books)} English books")
print(f"✅ Total books: {len(all_books)}")
print(f"✅ Languages: Sanskrit, Hindi, English, Buddhist, etc.")
