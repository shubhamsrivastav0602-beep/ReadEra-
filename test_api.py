#!/usr/bin/env python3
"""
Quick test suite for ReadEra API endpoints
"""
import requests
import json

BASE_URL = 'http://localhost:5000'

def test_endpoints():
    print("🧪 Testing ReadEra API Endpoints...\n")
    
    # Test 1: Home page
    print("✓ Test 1: GET /")
    try:
        r = requests.get(f'{BASE_URL}/')
        print(f"  Status: {r.status_code} {'✓' if r.status_code == 200 else '✗'}\n")
    except Exception as e:
        print(f"  Error: {e}\n")
    
    # Test 2: Get books
    print("✓ Test 2: GET /api/books")
    try:
        r = requests.get(f'{BASE_URL}/api/books?page=1&limit=10')
        if r.status_code == 200:
            data = r.json()
            print(f"  Status: {r.status_code} ✓")
            print(f"  Total books: {data.get('total')}")
            print(f"  Returned: {len(data.get('books', []))} books\n")
        else:
            print(f"  Status: {r.status_code} ✗\n")
    except Exception as e:
        print(f"  Error: {e}\n")
    
    # Test 3: Search books
    print("✓ Test 3: GET /api/books/search?q=yoga")
    try:
        r = requests.get(f'{BASE_URL}/api/books/search?q=yoga&limit=5')
        if r.status_code == 200:
            data = r.json()
            print(f"  Status: {r.status_code} ✓")
            print(f"  Found: {data.get('total')} results")
            if data.get('results'):
                print(f"  First result: {data['results'][0].get('title')}\n")
        else:
            print(f"  Status: {r.status_code} ✗\n")
    except Exception as e:
        print(f"  Error: {e}\n")
    
    # Test 4: Admin verify
    print("✓ Test 4: POST /api/admin/verify")
    try:
        r = requests.post(f'{BASE_URL}/api/admin/verify', 
                         json={'email': 'admin@readera.com', 'password': 'ReadEra@2024'})
        if r.status_code == 200:
            data = r.json()
            print(f"  Status: {r.status_code} ✓")
            print(f"  Admin verified: {data.get('isAdmin')}\n")
        else:
            print(f"  Status: {r.status_code} - {r.json().get('message')}\n")
    except Exception as e:
        print(f"  Error: {e}\n")
    
    # Test 5: Admin stats
    print("✓ Test 5: GET /api/admin/stats")
    try:
        r = requests.get(f'{BASE_URL}/api/admin/stats')
        if r.status_code == 200:
            data = r.json()
            stats = data.get('stats', {})
            print(f"  Status: {r.status_code} ✓")
            print(f"  Total books: {stats.get('total_books')}")
            print(f"  Languages: {stats.get('total_languages')}")
            print(f"  Categories: {stats.get('total_categories')}\n")
        else:
            print(f"  Status: {r.status_code} ✗\n")
    except Exception as e:
        print(f"  Error: {e}\n")
    
    print("=" * 60)
    print("✅ All tests completed!")
    print("\n🌐 Access the application:")
    print(f"  Home:   {BASE_URL}/")
    print(f"  Browse: {BASE_URL}/browse.html")
    print(f"  Admin:  {BASE_URL}/admin.html")
    print("=" * 60)

if __name__ == '__main__':
    test_endpoints()
