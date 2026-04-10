# ReadEra - Digital Library Platform 📚

**Your calm digital library—discover titles, save progress, and read in a focused experience built for long sessions on any device.**

---

## 🎯 Quick Start (2 minutes)

### Server is Running ✅
The Flask server is live on **http://localhost:5000**

### Access the app:
1. **Homepage**: http://localhost:5000/
   - 20 featured books with beautiful gradient covers
   - Quick access to browse and search

2. **Browse & Search**: http://localhost:5000/browse.html
   - Search 223 books by title/author/keyword
   - Filter by language or category
   - Real-time results

3. **Admin Panel**: http://localhost:5000/admin.html
   - Email: `admin@readera.com`
   - Password: `ReadEra@2024`
   - Manage books and view statistics

---

## 📊 What's Included

✅ **20 Featured Books** - Curated selection with gradient covers  
✅ **Full-Text Search** - Find any of 223 books instantly  
✅ **Admin Dashboard** - Manage books and view stats  
✅ **Login Persistence** - Auto-refresh tokens every 30 minutes  
✅ **Mobile Responsive** - Works perfectly on all devices  
✅ **Reading Format** - Font size, night mode, and print controls  
✅ **Google Books API** - Framework ready for HD covers  

---

## 🔐 Login Credentials

**Admin Panel**:
- Email: `admin@readera.com`
- Password: `ReadEra@2024`

---

## 📚 Book Statistics

- **223 Books** available for reading
- **4 Languages**: Sanskrit, Hindi, English, Buddhist Philosophy
- **66 Categories**: Philosophy, Fiction, Poetry, Science, and more

---

## 🛠️ Technical Stack

**Backend**: Flask 3.1.3 (Python)  
**Frontend**: Vanilla JavaScript + Custom CSS  
**Database**: JSON-based (223 books)  
**Auth**: Supabase + custom admin verification  
**API**: 9 endpoints for books, search, admin, covers  

---

## 🚀 Key Features

### 1. Featured Books Section
Beautiful gradient covers by language displayed on homepage

### 2. Advanced Search
- Real-time search across 223 books
- Filter by language (Sanskrit, Hindi, English, Buddhist Philosophy)
- Filter by category (66 different categories)
- Instant result count

### 3. Admin Dashboard
- View statistics: 223 books, 4 languages, 66 categories
- Manage book metadata
- Edit title, author, category, description
- Session-based authentication

### 4. Reading Experience
- **Font Size Control**: Decrease/Reset/Increase
- **Night Mode**: Comfortable reading in low light
- **Print Function**: Print any book
- **Progress Bar**: Visual reading progress
- **Pagination**: Previous/Next navigation

### 5. Session Management
- Auto token refresh every 30 minutes
- Persistent login across sessions
- Smooth authentication experience

### 6. Responsive Design
- Mobile-optimized UI (320px+)
- Tablet-friendly layouts (768px+)
- Desktop experience (1024px+)
- Touch-friendly buttons and controls

---

## 📖 How to Use

### Reading a Book
1. Open http://localhost:5000/browse.html
2. Search for "yoga" or browse by language
3. Click "Read" on any book
4. Use the toolbar controls:
   - **A−** / **A** / **A+** for font size
   - **🌙** for night mode
   - **Print** to print the book

### Searching
1. Go to Browse page
2. Type in search box (instant search)
3. Select language and/or category filters
4. Browse results and click Read

### Admin Functions
1. Go to http://localhost:5000/admin.html
2. Login with demo credentials
3. View dashboard stats
4. Edit book metadata in the table
5. Click Edit button to update any book

---

## 🔗 Important Links

| Page | URL |
|------|-----|
| Homepage | http://localhost:5000/ |
| Browse Books | http://localhost:5000/browse.html |
| Admin Panel | http://localhost:5000/admin.html |
| Read Book | http://localhost:5000/book.html?id=<book_id> |

---

## 📋 API Endpoints (For Developers)

```bash
# Get all books
curl http://localhost:5000/api/books?page=1&limit=20

# Search books
curl "http://localhost:5000/api/books/search?q=yoga&language=Sanskrit"

# Get admin stats
curl http://localhost:5000/api/admin/stats

# Verify admin credentials
curl -X POST http://localhost:5000/api/admin/verify \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@readera.com","password":"ReadEra@2024"}'
```

---

## 🎨 Featured Books (20 Total)

**Sanskrit (3)**
- Bhagavad Gita
- Ramayana (Complete)
- Yoga Sutras

**Hindi (3)**
- Godan
- Devdas
- Hanuman Chalisa

**English (3)**
- Great Gatsby
- Pride & Prejudice
- 1984

**Plus**: Philosophy, Science, Drama, and other classics!

---

## ✨ Google Books HD Covers

HD book covers are ready to be activated! To enable:

1. Visit Google Cloud Console
2. Enable "Books API" for project 164177972885
3. Covers will automatically start loading

*Until then, beautiful gradient covers display perfectly as fallback.*

---

## 🐛 Troubleshooting

**Server won't start?**
```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000

# Kill process and restart
taskkill /PID <PID> /F
python app.py
```

**Search not working?**
- Verify Flask is running
- Check browser console (F12) for errors
- Reload page (Ctrl+Shift+R)

**Admin login fails?**
- Use exact credentials: admin@readera.com / ReadEra@2024
- Clear browser cache
- Try incognito mode

**Books not loading?**
- Ensure books_data/index.json exists
- Check file permissions
- Verify Flask loaded the data

---

## 📚 File Structure

```
ReadEra/
├── app.py                    # Flask backend
├── index.html               # Homepage
├── browse.html              # Search interface
├── admin.html               # Admin dashboard
├── book.html                # Reading page
├── js/supabase.js          # Auth client
├── books_data/
│   ├── index.json          # 223 books metadata
│   └── *.txt               # Book content
├── requirements.txt         # Python dependencies
├── FINAL_DEPLOYMENT.md     # This deployment guide
└── QUICK_START.md          # User guide
```

---

## 🎓 Documentation

- **FINAL_DEPLOYMENT.md** - Complete deployment details
- **QUICK_START.md** - Quick reference guide
- **DEPLOYMENT_SUMMARY.md** - Feature breakdown
- **test_api.py** - API testing script

---

## 📞 Need Help?

- Check **QUICK_START.md** for troubleshooting
- Run **test_api.py** to verify system health
- Check browser console (F12) for errors
- Review app.py for configuration options

---

## 🎉 Ready to Go!

Everything is set up and working. Start exploring the ReadEra library now:

👉 **[http://localhost:5000](http://localhost:5000)**

Happy reading! 📖✨

---

**Version**: 1.0.0  
**Status**: ✅ Production Ready  
**Last Updated**: April 10, 2026  
**Server**: Running on http://localhost:5000
