< !DOCTYPE html >
    <html lang="en">
        <head>
            <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Book Fetcher - ReadEra</title>
                    <style>
                        body {
                            font - family: system-ui;
                        max-width: 800px;
                        margin: 2rem auto;
                        padding: 1rem;
                        background: #f5f7fa;
        }
                        .card {
                            background: white;
                        padding: 1.5rem;
                        border-radius: 16px;
                        margin-bottom: 1rem;
        }
                        button {
                            background: #8B4513;
                        color: white;
                        padding: 0.8rem 1.5rem;
                        border: none;
                        border-radius: 12px;
                        cursor: pointer;
        }
                        pre {
                            background: #1e293b;
                        color: #e2e8f0;
                        padding: 1rem;
                        border-radius: 12px;
                        overflow-x: auto;
                        font-size: 0.8rem;
        }
                        .status {
                            margin - top: 1rem;
                        padding: 0.5rem;
                        border-radius: 8px;
        }
                        .success {background: #d1fae5; color: #065f46; }
                        .error {background: #fee2e2; color: #991b1b; }
                        .info {background: #dbeafe; color: #1e40af; }
                    </style>
                </head>
                <body>
                    <h1>📚 ReadEra - Book Fetcher</h1>
                    <p>Internet Archive se Creative Commons books fetch karo aur apni website pe save karo</p>

                    <div class="card">
                        <h3>🔗 Collection URL</h3>
                        <input type="text" id="collectionUrl" style="width: 100%; padding: 0.5rem; margin: 0.5rem 0;" value="https://archive.org/details/booksbylanguage_hindi">
                            <button id="fetchBtn">🚀 Fetch & Save Books</button>
                            <div id="status"></div>
                    </div>

                    <div class="card">
                        <h3>📊 Progress</h3>
                        <pre id="logs">Ready. Enter URL and click Fetch...</pre>
                    </div>

                    <div class="card">
                        <h3>📚 Saved Books</h3>
                        <div id="savedBooksList"></div>
                    </div>

                    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
                    <script>
        // ============================================
                        // READERA - BOOK FETCHER (LOCAL DOWNLOAD)
                        // ============================================

                        const SUPABASE_URL = "https://ryzbikpzxphrsdctvqp.supabase.co";
                        const SUPABASE_KEY = "sb_publishable_MPqGLh4Z15HdLuTRQ81SzA_Ssm9n";
                        const supabase = supabaseClient.createClient(SUPABASE_URL, SUPABASE_KEY);

                        const logsDiv = document.getElementById('logs');
                        const statusDiv = document.getElementById('status');
                        const savedBooksDiv = document.getElementById('savedBooksList');

                        function log(message, type = 'info') {
            const timestamp = new Date().toLocaleTimeString();
                        logsDiv.innerText += `\n[${timestamp}] ${message}`;
                        logsDiv.scrollTop = logsDiv.scrollHeight;

                        statusDiv.innerHTML = `<div class="status ${type}">${message}</div>`;
            setTimeout(() => {
                if (statusDiv.innerHTML.includes(message)) {
                            statusDiv.innerHTML = '';
                }
            }, 3000);
        }

                        async function fetchBookText(identifier) {
            // Try to get text from Internet Archive
            const txtUrl = `https://archive.org/stream/${identifier}/${identifier}_djvu.txt`;
                        try {
                const response = await fetch(txtUrl);
                        if (response.ok) {
                    const text = await response.text();
                        return text.substring(0, 10000); // First 10000 chars
                }
            } catch(e) { }

            // Try alternative text URL
                        const altUrl = `https://archive.org/download/${identifier}/${identifier}.txt`;
                        try {
                const response = await fetch(altUrl);
                        if (response.ok) {
                    const text = await response.text();
                        return text.substring(0, 10000);
                }
            } catch(e) { }

                        return null;
        }

                        async function getCoverUrl(identifier) {
            const coverPatterns = [
                        `https://archive.org/services/img/${identifier}`,
                        `https://archive.org/download/${identifier}/${identifier}_cover.jpg`,
                        `https://archive.org/download/${identifier}/${identifier}.jpg`
                        ];

                        for (const url of coverPatterns) {
                try {
                    const response = await fetch(url, {method: 'HEAD' });
                        if (response.ok) return url;
                } catch(e) { }
            }
                        return 'https://placehold.co/300x400/8B4513/white?text=Book';
        }

                        async function saveBookToLocal(bookData) {
                            // Save to localStorage first (backup)
                            let localBooks = JSON.parse(localStorage.getItem('readera_books') || '[]');
                        localBooks.push({
                            id: bookData.ia_id,
                        title: bookData.title,
                        author: bookData.author,
                        summary: bookData.summary,
                        cover_url: bookData.cover_url,
                        text: bookData.text,
                        savedAt: new Date().toISOString()
            });
                        localStorage.setItem('readera_books', JSON.stringify(localBooks));

                        // Also save to Supabase
                        try {
                const {error} = await supabase.from('books').insert({
                            title: bookData.title,
                        author: bookData.author,
                        summary: bookData.summary,
                        cover_url: bookData.cover_url,
                        pdf_url: bookData.pdf_url,
                        ia_id: bookData.ia_id,
                        genre: 'Creative Commons',
                        total_pages: 0,
                        views: 0
                });
                        if (error) throw error;
                        return true;
            } catch(e) {
                            console.error('Supabase error:', e);
                        return false; // Still saved in localStorage
            }
        }

                        async function fetchCollection() {
            const url = document.getElementById('collectionUrl').value.trim();
                        if (!url) {
                            log('❌ Please enter a collection URL', 'error');
                        return;
            }

                        // Extract identifier
                        let identifier = '';
                        const match = url.match(/\/details\/([^/?]+)/);
                        if (match) {
                            identifier = match[1];
            } else {
                            identifier = url.split('/').pop().split('?')[0];
            }

                        log(`🔍 Fetching collection: ${identifier}`, 'info');

                        // First, get list of books from collection
                        const searchUrl = `https://archive.org/advancedsearch.php?q=collection:${identifier} AND mediatype:texts&fl[]=identifier,title,creator,description,licenseurl&rows=50&output=json`;

                        try {
                const response = await fetch(searchUrl);
                        const data = await response.json();
                        const docs = data?.response?.docs || [];

                // Filter Creative Commons only
                const ccBooks = docs.filter(book => {
                    const license = (book.licenseurl || '').toLowerCase();
                        return license.includes('creativecommons') || license.includes('cc0') || license.includes('cc-by');
                });

                        log(`📚 Found ${ccBooks.length} Creative Commons books`, 'success');

                        let savedCount = 0;

                        for (let i = 0; i < ccBooks.length; i++) {
                    const book = ccBooks[i];
                        const iaId = book.identifier;

                        log(`📖 [${i + 1}/${ccBooks.length}] Processing: ${book.title?.substring(0, 50) || 'Untitled'}...`, 'info');

                        // Check if already saved
                        const existing = localStorage.getItem(`book_${iaId}`);
                        if (existing) {
                            log(`   ⏭️ Already saved, skipping`, 'info');
                        continue;
                    }

                        // Fetch full text
                        const fullText = await fetchBookText(iaId);
                        if (!fullText) {
                            log(`   ⚠️ No text available`, 'error');
                        continue;
                    }

                        // Get cover
                        const coverUrl = await getCoverUrl(iaId);

                        // Generate summary (first 500 chars of text)
                        const summary = fullText.substring(0, 1000) + '...';

                        // Save book
                        const bookData = {
                            ia_id: iaId,
                        title: book.title || 'Untitled',
                        author: book.creator || 'Unknown',
                        summary: summary,
                        cover_url: coverUrl,
                        text: fullText,
                        pdf_url: `https://archive.org/download/${iaId}/${iaId}.pdf`
                    };

                        const saved = await saveBookToLocal(bookData);

                        if (saved) {
                            localStorage.setItem(`book_${iaId}`, JSON.stringify(bookData));
                        savedCount++;
                        log(`   ✅ Saved: ${bookData.title}`, 'success');
                    } else {
                            log(`   ❌ Failed to save`, 'error');
                    }

                    // Small delay to avoid rate limiting
                    await new Promise(r => setTimeout(r, 1000));
                }

                        log(`🎉 Complete! Saved ${savedCount} books locally`, 'success');
                        displaySavedBooks();
                
            } catch (error) {
                            log(`❌ Error: ${error.message}`, 'error');
            }
        }

                        function displaySavedBooks() {
            const localBooks = JSON.parse(localStorage.getItem('readera_books') || '[]');
                        if (localBooks.length === 0) {
                            savedBooksDiv.innerHTML = '<p>No books saved yet.</p>';
                        return;
            }
            
            savedBooksDiv.innerHTML = localBooks.map(book => `
                        <div style="border-bottom: 1px solid #e2e8f0; padding: 0.5rem 0;">
                            <strong>${book.title}</strong><br>
                                <small>${book.author}</small><br>
                                    <small>Saved: ${new Date(book.savedAt).toLocaleString()}</small>
                                </div>
                                `).join('');
        }

                                document.getElementById('fetchBtn').addEventListener('click', fetchCollection);

                                // Display existing books on load
                                displaySavedBooks();
                                log('✅ Ready! Enter a collection URL and click Fetch', 'success');
                            </script>
                        </body>
                    </html>