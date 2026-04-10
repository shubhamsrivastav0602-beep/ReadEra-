< !DOCTYPE html >
    <html lang="en">
        <head>
            <meta charset="UTF-8">
                <title>Fetch & Save Books</title>
                <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
                <style>
                    body {font - family: system-ui; max-width: 800px; margin: 2rem auto; padding: 1rem; }
                    button {background: #8B4513; color: white; padding: 0.8rem 1.5rem; border: none; border-radius: 12px; cursor: pointer; }
                    pre {background: #f1f5f9; padding: 1rem; border-radius: 12px; overflow-x: auto; }
                </style>
        </head>
        <body>
            <h1>📚 ReadEra - Bulk Book Fetcher</h1>
            <p>Internet Archive se <strong>Public Domain + CC</strong> books fetch karo aur Supabase mein save karo.</p>

            <div>
                <label>Collection URL (default: Hindi books)</label>
                <input type="text" id="collectionUrl" value="https://archive.org/details/booksbylanguage_hindi" style="width: 100%; padding: 0.5rem; margin: 0.5rem 0;">
            </div>

            <button id="fetchBtn">📖 Fetch & Save Books</button>

            <h3>📋 Logs:</h3>
            <pre id="logs">Ready. Click Fetch to start...</pre>

            <script>
                const SUPABASE_URL = "https://ryzbikpzxphrsdctvqp.supabase.co";
                const SUPABASE_KEY = "sb_publishable_MPqGLh4Z15HdLuTRQ81SzA_Ssm9n";
                const supabase = supabaseClient.createClient(SUPABASE_URL, SUPABASE_KEY);

                const logs = document.getElementById('logs');
                const fetchBtn = document.getElementById('fetchBtn');

                function log(msg) {
                    logs.innerText += `\n${new Date().toLocaleTimeString()} - ${msg}`;
                logs.scrollTop = logs.scrollHeight;
        }
        
        fetchBtn.addEventListener('click', async () => {
            const url = document.getElementById('collectionUrl').value.trim();
                if (!url) {log('❌ Enter URL'); return; }

                fetchBtn.disabled = true;
                log('🚀 Starting fetch...');

                try {
                    let identifier = url.match(/\/details\/([^/?]+)/)?.[1] || url.split('/').pop();
                const apiUrl = `https://archive.org/advancedsearch.php?q=collection:${identifier} AND mediatype:texts&fl[]=identifier,title,creator,description,licenseurl,date&rows=100&output=json`;

                const response = await fetch(apiUrl);
                const data = await response.json();
                const docs = data?.response?.docs || [];

                log(`📚 Total books found: ${docs.length}`);

                let saved = 0;
                for (const book of docs) {
                    const license = (book.licenseurl || '').toLowerCase();
                const isPublic = !license || license.includes('publicdomain') || !license.includes('copyright');
                const isCC = license.includes('creativecommons') || license.includes('cc0');

                if (isPublic || isCC) {
                        const bookData = {
                    title: (book.title || 'Untitled').slice(0, 200),
                author: (book.creator || 'Unknown').slice(0, 100),
                summary: (book.description || 'No summary available').slice(0, 5000),
                genre: 'Internet Archive',
                pdf_url: `https://archive.org/download/${book.identifier}/${book.identifier}.pdf`,
                cover_url: 'https://placehold.co/300x400/8B4513/white?text=Book',
                total_pages: 0,
                views: 0
                        };

                const {error} = await supabase.from('books').insert(bookData);
                if (!error) saved++;
                if (saved % 10 === 0) log(`💾 Saved ${saved} books so far...`);
                    }
                }
                log(`✅ DONE! Saved ${saved} Public Domain/CC books to Supabase.`);
            } catch (err) {
                    log(`❌ Error: ${err.message}`);
            }
                fetchBtn.disabled = false;
        });
            </script>
        </body>
    </html>