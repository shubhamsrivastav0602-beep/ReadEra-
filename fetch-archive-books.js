// ============================================
// READERA - INTERNET ARCHIVE BOOKS FETCHER
// ============================================

class ArchiveBookFetcher {
    constructor() {
        // Open Library API endpoints
        this.olBase = 'https://openlibrary.org';
        this.iaBase = 'https://archive.org';
    }

    // Step 1: Search books by genre/subject
    async searchBySubject(subject, limit = 20, offset = 0) {
        const url = `${this.olBase}/subjects/${encodeURIComponent(subject)}.json?limit=${limit}&offset=${offset}`;
        const response = await fetch(url);
        const data = await response.json();

        return {
            books: data.works || [],
            total: data.work_count || 0,
            offset: offset,
            limit: limit
        };
    }

    // Step 2: Search books (general query)
    async searchBooks(query, limit = 20, page = 1) {
        const url = `${this.olBase}/search.json?q=${encodeURIComponent(query)}&limit=${limit}&page=${page}`;
        const response = await fetch(url);
        const data = await response.json();

        return {
            books: data.docs || [],
            total: data.num_found || 0,
            page: page,
            limit: limit
        };
    }

    // Step 3: Get full book details by Open Library ID
    async getBookDetails(olId) {
        // Try work ID first
        let workId = olId;
        if (!olId.startsWith('/works/')) {
            workId = `/works/${olId}`;
        }

        const url = `${this.olBase}${workId}.json`;
        const response = await fetch(url);
        const data = await response.json();

        return {
            title: data.title,
            description: this.extractDescription(data),
            authors: data.authors || [],
            covers: data.covers || [],
            subjects: data.subjects || [],
            first_publish_date: data.first_publish_date,
            ia_id: data.ia || null  // Internet Archive identifier
        };
    }

    // Step 4: Get book by ISBN (most reliable)
    async getByISBN(isbn) {
        const url = `${this.olBase}/api/books?bibkeys=ISBN:${isbn}&format=json&jscmd=data`;
        const response = await fetch(url);
        const data = await response.json();
        const bookData = data[`ISBN:${isbn}`];

        if (!bookData) return null;

        return {
            title: bookData.title,
            authors: bookData.authors?.map(a => a.name) || [],
            description: bookData.description || null,
            publish_date: bookData.publish_date,
            number_of_pages: bookData.number_of_pages,
            covers: bookData.covers || [],
            isbn_10: isbn
        };
    }

    // Step 5: Get Internet Archive book text (full book content)
    async getIAText(iaId) {
        // Get book data from IA
        const metadataUrl = `${this.iaBase}/metadata/${iaId}`;
        const metadataResp = await fetch(metadataUrl);
        const metadata = await metadataResp.json();

        // Get text file URL
        const files = metadata?.result?.files || [];
        const textFile = files.find(f => f.format === 'Text' || f.name?.endsWith('.txt') || f.name?.endsWith('_djvu.txt'));

        if (textFile) {
            const textUrl = `${this.iaBase}/download/${iaId}/${textFile.name}`;
            const textResp = await fetch(textUrl);
            const text = await textResp.text();
            return text.substring(0, 10000); // First 10k chars
        }

        return null;
    }

    // Step 6: Get IA Book Manifest (page-by-page)
    async getIAManifest(iaId) {
        const url = `https://api.archivelab.org/books/${iaId}/ia_manifest`;
        const response = await fetch(url);
        return await response.json();
    }

    // Helper: Extract description from OL response
    extractDescription(data) {
        if (typeof data.description === 'string') return data.description;
        if (data.description && typeof data.description === 'object') return data.description.value;
        return null;
    }

    // ============ COMPLETE WORKFLOWS ============

    // Workflow 1: Get books by genre with IA text
    async getGenreBooksWithText(genre, limit = 10) {
        console.log(`🔍 Searching genre: ${genre}`);
        const result = await this.searchBySubject(genre, limit);

        const booksWithText = [];

        for (const work of result.books) {
            console.log(`📖 Processing: ${work.title}`);

            try {
                const details = await this.getBookDetails(work.key);

                let iaText = null;
                if (details.ia_id) {
                    console.log(`   📥 Fetching from IA: ${details.ia_id}`);
                    iaText = await this.getIAText(details.ia_id);
                }

                booksWithText.push({
                    title: details.title,
                    authors: details.authors?.map(a => a.name) || work.authors?.map(a => a.name) || [],
                    description: details.description,
                    genre: genre,
                    ia_id: details.ia_id,
                    ia_text_preview: iaText,
                    openlibrary_key: work.key
                });

            } catch (e) {
                console.log(`   ❌ Error: ${e.message}`);
            }

            // Rate limiting
            await this.sleep(500);
        }

        return booksWithText;
    }

    // Workflow 2: Search and fetch
    async searchAndFetch(query, limit = 20) {
        console.log(`🔍 Searching: ${query}`);
        const result = await this.searchBooks(query, limit);

        const books = [];

        for (const doc of result.books) {
            books.push({
                title: doc.title,
                authors: doc.author_name || [],
                first_publish_year: doc.first_publish_year,
                isbn: doc.isbn?.[0] || null,
                cover_id: doc.cover_i,
                edition_count: doc.edition_count,
                openlibrary_key: doc.key,
                ia_collection: doc.ia_collection_s || null
            });
        }

        return books;
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// ============================================
// EXPORT AND USAGE EXAMPLES
// ============================================

const archiveFetcher = new ArchiveBookFetcher();

// Example 1: Get 20 Horror books from Open Library
async function fetchHorrorBooks() {
    console.log('📚 Fetching Horror books from Open Library...\n');

    const result = await archiveFetcher.searchBySubject('horror', 20);
    console.log(`✅ Found ${result.total} total books, showing ${result.books.length}\n`);

    result.books.forEach((book, i) => {
        console.log(`${i + 1}. ${book.title}`);
        console.log(`   Authors: ${book.authors?.map(a => a.name).join(', ') || 'Unknown'}`);
        console.log(`   First published: ${book.first_publish_year || 'N/A'}`);
        console.log(`   Key: ${book.key}\n`);
    });

    return result.books;
}

// Example 2: Search "machine learning" books
async function searchBooks() {
    const results = await archiveFetcher.searchAndFetch('machine learning', 10);
    console.table(results);
    return results;
}

// Example 3: Get full book details with IA text (if available)
async function getBookWithText(openlibraryKey) {
    console.log(`📖 Fetching: ${openlibraryKey}`);
    const details = await archiveFetcher.getBookDetails(openlibraryKey);

    console.log(`Title: ${details.title}`);
    console.log(`Description: ${details.description?.substring(0, 200)}...`);

    if (details.ia_id) {
        console.log(`IA ID: ${details.ia_id}`);
        const text = await archiveFetcher.getIAText(details.ia_id);
        if (text) {
            console.log(`Text preview: ${text.substring(0, 300)}...`);
        }
    }

    return details;
}

// Example 4: Get books by genre WITH full text (for your 10k books goal)
async function fetchBooksForYourLibrary() {
    const genres = ['fiction', 'science_fiction', 'fantasy', 'mystery', 'romance', 'history', 'biography', 'self_help'];
    let allBooks = [];

    for (const genre of genres) {
        console.log(`\n🔥 Processing genre: ${genre}`);
        const books = await archiveFetcher.getGenreBooksWithText(genre, 5);
        allBooks = [...allBooks, ...books];

        // Add to your Supabase here
        // await addToSupabase(books);
    }

    console.log(`\n✅ Total books fetched: ${allBooks.length}`);
    return allBooks;
}

// Example 5: Get book by ISBN (most reliable)
async function getBookByISBN(isbn) {
    const book = await archiveFetcher.getByISBN(isbn);
    if (book) {
        console.log(`Title: ${book.title}`);
        console.log(`Authors: ${book.authors.join(', ')}`);
        console.log(`Description: ${book.description?.substring(0, 200)}...`);
    }
    return book;
}

// ============================================
// PAGINATION EXAMPLE (for large collections)
// ============================================

async function fetchAllBooksBySubject(subject, totalNeeded = 100) {
    let allBooks = [];
    let offset = 0;
    const limit = 50;

    while (allBooks.length < totalNeeded) {
        const result = await archiveFetcher.searchBySubject(subject, limit, offset);

        if (result.books.length === 0) break;

        allBooks = [...allBooks, ...result.books];
        offset += limit;

        console.log(`Fetched ${allBooks.length} / ${Math.min(totalNeeded, result.total)} books`);

        if (offset >= result.total) break;
    }

    return allBooks.slice(0, totalNeeded);
}

// Make available globally
window.archiveFetcher = archiveFetcher;
window.fetchHorrorBooks = fetchHorrorBooks;
window.searchBooks = searchBooks;
window.getBookWithText = getBookWithText;
window.getBookByISBN = getBookByISBN;
window.fetchBooksForYourLibrary = fetchBooksForYourLibrary;
window.fetchAllBooksBySubject = fetchAllBooksBySubject;

console.log('✅ Archive Book Fetcher ready!');
console.log('📖 Available functions:');
console.log('   - fetchHorrorBooks()');
console.log('   - searchBooks()');
console.log('   - getBookWithText("key")');
console.log('   - getBookByISBN("9780451526538")');
console.log('   - fetchBooksForYourLibrary()');