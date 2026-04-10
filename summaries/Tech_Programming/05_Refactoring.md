<div style="font-family: 'Consolas', 'Monaco', 'Courier New', monospace; color: #1a1a1a; background-color: #f0fdf4; line-height: 1.6; max-width: 900px; margin: auto; padding: 60px; border-radius: 4px; box-shadow: 0 4px 50px rgba(0,0,0,0.05); border: 2px solid #2ecc71; border-top: 15px solid #2ecc71;">

<!-- Precision Header -->
<div style="text-align: left; border-bottom: 2px solid #2ecc71; padding-bottom: 30px; margin-bottom: 40px;">
    <h3 style="color: #27ae60; text-transform: uppercase; letter-spacing: 5px; font-size: 0.8rem; margin: 0; font-weight: bold;">System Evolution Laboratory</h3>
    <h1 style="font-size: 3.5rem; margin: 10px 0; color: #1a1a1a; font-weight: 300; line-height: 1;">Refactoring</h1>
    <p style="font-size: 1.25rem; color: #2ecc71; font-style: italic;">Improving the Design of Existing Code.</p>
</div>

<!-- Intro Section -->
<div style="display: flex; gap: 40px; margin-bottom: 50px; flex-wrap: wrap; align-items: start;">
    <div style="flex: 1; min-width: 250px; background: #fff; padding: 10px; border: 1px solid #2ecc7133;">
        <img src="https://covers.openlibrary.org/b/isbn/9780134757599-L.jpg" alt="Refactoring Cover" style="width: 100%; filter: saturate(0.8) contrast(1.1);">
    </div>
    <div style="flex: 1.5; min-width: 300px;">
        <h2 style="color: #27ae60; font-size: 2rem; margin-top: 0;">Martin Fowler’s Surgical Optimization</h2>
        <p style="text-align: justify; font-size: 1.1rem; color: #1a1a1a;">
            Martin Fowler defines refactoring as a "controlled technique for improving the design of an existing body of code, without changing its external behavior." In the fast-paced world of Agile development, <em>Refactoring</em> is the essential guardrail that prevents software from rotting under the weight of its own complexity.
        </p>
        <div style="margin-top: 30px; background: #fff; padding: 25px; border-left: 5px solid #2ecc71; color: #1a1a1a; font-size: 1rem;">
            <p style="margin: 0; font-weight: bold; color: #27ae60;">CORE PRINCIPLE:</p>
            <p style="margin: 5px 0 0 0; font-style: italic;">"Any fool can write code that a computer can understand. Good programmers write code that humans can understand."</p>
        </div>
    </div>
</div>

<!-- Diagnostic: Code Smells Checklist -->
<div style="background: white; border: 1px solid #2ecc7122; padding: 40px; border-radius: 10px; margin-bottom: 50px;">
    <h3 style="color: #27ae60; text-transform: uppercase; letter-spacing: 2px; text-align: center; margin-bottom: 30px;">DIAGNOSING CODE SMELLS</h3>
    <ul style="list-style: none; padding-left: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; font-size: 1rem;">
        <li>🚨 <strong>Long Method:</strong> Do one thing only.</li>
        <li>🚨 <strong>Large Class:</strong> Adhere to SRP.</li>
        <li>🚨 <strong>Shotgun Surgery:</strong> One change, many files.</li>
        <li>🚨 <strong>Feature Envy:</strong> Class too busy with another.</li>
        <li>🚨 <strong>Primitive Obsession:</strong> Use objects, not long.</li>
        <li>🚨 <strong>Data Clumps:</strong> Groups that always stay together.</li>
    </ul>
</div>

<!-- High-Level Engineering Analysis -->
<div style="margin-bottom: 60px;">
    <h3 style="color: #1a1a1a; font-size: 1.8rem; margin-bottom: 25px;">The Two Hats Concept</h3>
    <div style="column-count: 2; column-gap: 40px; text-align: justify; font-size: 1rem; color: #333;">
        Fowler introduces the "Two Hats" rule of programming: when you're adding functional code, you don't refactor; when you're refactoring, you don't add function. This separation of concerns is vital for managing technical debt. He outlines hundreds of specific refactorings—like "Extract Method" or "Replace Temp with Query"—each backed by a rigorous step-by-step process. 
        <br><br>
        Crucially, refactoring is impossible without a solid suite of automated tests. Tests provide the "safety net" that allows an engineer to fearlessly reorganize code. <em>Refactoring</em> is a mandatory rigorous training for any developer who wants to ensure that their systems remain agile, readable, and structurally sound throughout their long lifecycle.
    </div>
</div>

<!-- Verdict -->
<div style="border-top: 2px solid #2ecc71; padding-top: 40px; text-align: center;">
    <h3 style="color: #27ae60; font-size: 1.5rem; margin-bottom: 20px;">The Verdict</h3>
    <p style="color: #7f8c8d; font-style: italic; max-width: 700px; margin: auto;">
        "Refactoring is the difference between a legacy codebase that developers hate and a thriving system that developers love. It is the core of sustainable software."
    </p>
    <div style="margin-top: 40px; font-size: 1.8rem; color: #2ecc71;">🧼 ⚙️ 📉</div>
</div>

</div>
