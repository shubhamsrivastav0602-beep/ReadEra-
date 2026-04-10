#!/usr/bin/env python3
import requests

# Test Google Books API directly
api_key = 'AIzaSyDIbBQPqj_dY5R5Y-kBjrEaUZYAvSCbVD4'
search_url = 'https://www.googleapis.com/books/v1/volumes'
params = {
    'q': 'Great Gatsby',
    'key': api_key,
    'maxResults': 1
}

try:
    response = requests.get(search_url, params=params, timeout=5)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        items = data.get('items', [])
        print(f"Books found: {len(items)}")
        
        if items:
            book = items[0]
            volume_info = book.get('volumeInfo', {})
            image_links = volume_info.get('imageLinks', {})
            print(f"Title: {volume_info.get('title')}")
            print(f"Thumbnail: {image_links.get('thumbnail')}")
            print(f"Large: {image_links.get('large')}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Exception: {e}")
