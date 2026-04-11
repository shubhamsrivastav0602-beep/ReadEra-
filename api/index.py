import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
import json
from datetime import datetime
import requests

# Create Flask app with proper paths for Vercel
app = Flask(__name__, 
    template_folder=project_root,
    static_folder=project_root,
    static_url_path='/')
CORS(app)

# Configuration (served from /public to match static files)
BOOKS_DATA_PATH = os.path.join(project_root, 'public', 'books_data', 'index.json')
COVERS_DATA_PATH = os.path.join(project_root, 'public', 'books_data', 'covers.json')

# Google API Configuration
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', 'AIzaSyDIbBQPqj_dY5R5Y-kBjrEaUZYAvSCbVD4')
GOOGLE_BOOKS_API_URL = 'https://www.googleapis.com/books/v1/volumes'

# ============================================
# UTILITY FUNCTIONS
# ============================================

def load_books_data():
    """Load books from JSON file"""
    try:
        with open(BOOKS_DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def load_covers_data():
    """Load covers mapping"""
    try:
        with open(COVERS_DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def get_admin_credentials():
    """Get admin credentials from environment"""
    return {
        "admin_email": os.getenv('ADMIN_EMAIL', 'admin@readera.com'),
        "admin_password": os.getenv('ADMIN_PASSWORD', 'ReadEra@2024')
    }

def is_admin_authorized(request_data):
    """Check if admin credentials are valid"""
    admin_creds = get_admin_credentials()
    email = request_data.get('email', '')
    password = request_data.get('password', '')
    
    return (email == admin_creds['admin_email'] and 
            password == admin_creds['admin_password'])

# ============================================
# STATIC PAGES
# ============================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin.html')
def admin():
    return render_template('admin.html')

@app.route('/browse.html')
def browse():
    return render_template('browse.html')

@app.route('/book.html')
def book():
    return render_template('book.html')

@app.route('/auth.html')
def auth():
    return render_template('auth.html')

# ============================================
# AUTHENTICATION ENDPOINTS
# ============================================

@app.route('/api/admin/verify', methods=['POST'])
def verify_admin():
    """Verify admin credentials"""
    try:
        data = request.get_json()
        
        if is_admin_authorized(data):
            return jsonify({
                'success': True,
                'isAdmin': True,
                'message': 'Admin verified',
                'token': 'admin_session_' + datetime.now().isoformat()
            }), 200
        else:
            return jsonify({
                'success': False,
                'isAdmin': False,
                'message': 'Invalid credentials'
            }), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    """Logout admin"""
    return jsonify({
        'success': True,
        'message': 'Admin logged out'
    }), 200

# ============================================
# BOOKS ENDPOINTS
# ============================================

@app.route('/api/books', methods=['GET'])
def get_books():
    """Get paginated list of books"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        
        books = load_books_data()
        start = (page - 1) * limit
        end = start + limit
        
        return jsonify({
            'success': True,
            'books': books[start:end],
            'total': len(books),
            'page': page,
            'limit': limit,
            'pages': (len(books) + limit - 1) // limit
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/books/search', methods=['GET'])
def search_books():
    """Search books by query string"""
    try:
        query = request.args.get('q', '').lower()
        language = request.args.get('language', '').lower()
        category = request.args.get('category', '').lower()
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        
        books = load_books_data()
        results = []
        
        for book in books:
            matches_query = (not query or 
                           query in book.get('title', '').lower() or
                           query in book.get('author', '').lower() or
                           query in book.get('category', '').lower())
            
            matches_language = (not language or 
                              book.get('language', '').lower() == language)
            
            matches_category = (not category or 
                              book.get('category', '').lower() == category)
            
            if matches_query and matches_language and matches_category:
                results.append(book)
        
        start = (page - 1) * limit
        end = start + limit
        
        return jsonify({
            'success': True,
            'results': results[start:end],
            'total': len(results),
            'page': page,
            'limit': limit
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/books/<book_id>', methods=['GET'])
def get_book(book_id):
    """Get specific book by ID"""
    try:
        books = load_books_data()
        book = next((b for b in books if b.get('id') == book_id), None)
        
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        
        return jsonify({
            'success': True,
            'book': book
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# ADMIN ENDPOINTS
# ============================================

@app.route('/api/admin/stats', methods=['GET'])
def get_admin_stats():
    """Get admin dashboard statistics"""
    try:
        books = load_books_data()
        
        languages = {}
        categories = {}
        
        for book in books:
            lang = book.get('language', 'Unknown')
            cat = book.get('category', 'Unknown')
            
            languages[lang] = languages.get(lang, 0) + 1
            categories[cat] = categories.get(cat, 0) + 1
        
        return jsonify({
            'success': True,
            'stats': {
                'total_books': len(books),
                'languages': languages,
                'categories': categories,
                'total_languages': len(languages),
                'total_categories': len(categories),
                'recent_books': books[:5] if books else []
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/books/<book_id>/update', methods=['POST'])
def update_book(book_id):
    """Update book metadata"""
    try:
        data = request.get_json()
        books = load_books_data()
        
        book_index = next((i for i, b in enumerate(books) if b.get('id') == book_id), None)
        if book_index is None:
            return jsonify({'error': 'Book not found'}), 404
        
        if 'title' in data:
            books[book_index]['title'] = data['title']
        if 'author' in data:
            books[book_index]['author'] = data['author']
        if 'description' in data:
            books[book_index]['description'] = data['description']
        if 'category' in data:
            books[book_index]['category'] = data['category']
        
        return jsonify({
            'success': True,
            'message': 'Book updated',
            'book': books[book_index]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# COVERS ENDPOINTS
# ============================================

@app.route('/api/google-books/<book_title>', methods=['GET'])
def get_google_books_cover(book_title):
    """Fetch HD cover from Google Books API"""
    try:
        search_url = GOOGLE_BOOKS_API_URL
        params = {
            'q': book_title,
            'key': GOOGLE_API_KEY,
            'maxResults': 1
        }
        
        response = requests.get(search_url, params=params, timeout=5)
        
        if response.status_code != 200:
            return jsonify({
                'success': False,
                'message': 'Could not fetch from Google Books',
                'cover': None
            }), 200
        
        data = response.json()
        
        if data.get('items') and len(data['items']) > 0:
            book = data['items'][0]
            volume_info = book.get('volumeInfo', {})
            image_links = volume_info.get('imageLinks', {})
            thumbnail = image_links.get('thumbnail', '')
            large_image = image_links.get('large', '')
            
            cover_url = large_image or thumbnail
            
            return jsonify({
                'success': True,
                'cover_url': cover_url.replace('http://', 'https://') if cover_url else None,
                'title': volume_info.get('title', ''),
                'author': ', '.join(volume_info.get('authors', []))
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'No book found',
                'cover': None
            }), 200
            
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 200

# ============================================
# SUMMARIES ENDPOINTS
# ============================================

SUMMARIES_PATH = os.path.join(project_root, 'public', 'summaries', 'all_summaries.json')
SUMMARIES_METADATA_PATH = os.path.join(project_root, 'public', 'summaries', 'summaries_metadata.json')

def load_summaries_data():
    """Load all summaries from JSON file"""
    try:
        with open(SUMMARIES_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def load_summaries_metadata():
    """Load summaries metadata"""
    try:
        with open(SUMMARIES_METADATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

@app.route('/api/summaries/metadata', methods=['GET'])
def get_summaries_metadata():
    """Get metadata for all summaries"""
    try:
        metadata = load_summaries_metadata()
        return jsonify({
            'success': True,
            'summaries': metadata,
            'total': len(metadata)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/summaries/<book_title>', methods=['GET'])
def get_summary_by_title(book_title):
    """Get full summary content for a specific book"""
    try:
        # Decode URL-encoded title
        import urllib.parse
        decoded_title = urllib.parse.unquote(book_title)
        
        summaries = load_summaries_data()
        summary = summaries.get(decoded_title)
        
        if summary:
            return jsonify({
                'success': True,
                'summary': summary,
                'found': True
            }), 200
        else:
            return jsonify({
                'success': True,
                'summary': None,
                'found': False,
                'message': f'Summary not found for: {decoded_title}'
            }), 404
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/summaries/search', methods=['GET'])
def search_summaries():
    """Search summaries by keyword or category"""
    try:
        query = request.args.get('q', '').lower()
        category = request.args.get('category', '').lower()
        
        summaries = load_summaries_data()
        results = []
        
        for title, summary_data in summaries.items():
            # Check if summary matches filters
            matches_query = (not query or 
                           query in title.lower() or
                           query in summary_data.get('category', '').lower() or
                           query in summary_data.get('content', '').lower())
            
            matches_category = (not category or
                              summary_data.get('category', '').lower() == category)
            
            if matches_query and matches_category:
                # Return metadata only, not full content for search results
                results.append({
                    'title': title,
                    'id': summary_data.get('id'),
                    'category': summary_data.get('category'),
                    'word_count': summary_data.get('word_count')
                })
        
        return jsonify({
            'success': True,
            'results': results,
            'total': len(results)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

# Health check
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'ReadEra API is running'}), 200

# For Vercel serverless
if __name__ == '__main__':
    app.run(debug=False)
