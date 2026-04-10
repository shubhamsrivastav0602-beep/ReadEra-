<div style="font-family: 'Fira Code', 'Courier New', monospace; color: #e1e1e1; background-color: #2d1b4e; line-height: 1.6; max-width: 900px; margin: auto; padding: 60px; border-radius: 4px; box-shadow: 0 10px 60px rgba(155, 89, 182, 0.2); border: 1px solid #9b59b644; border-top: 20px solid #9b59b6; position: relative; overflow: hidden;">

<!-- Wizard Overlay -->
<div style="position: absolute; top: -50px; left: -50px; font-size: 15rem; color: #9b59b608; z-index: 0; opacity: 0.5; pointer-events: none;">🪄</div>

<!-- Mystical Logic Header -->
<div style="text-align: left; border-bottom: 1px solid #9b59b644; padding-bottom: 30px; margin-bottom: 50px; position: relative; z-index: 1;">
    <h3 style="letter-spacing: 5px; color: #9b59b6; font-size: 0.8rem; margin: 0; text-transform: uppercase; font-weight: bold;">[ THE WIZARD BOOK ]</h3>
    <h1 style="font-size: 2.8rem; margin: 15px 0; color: #ffffff; font-weight: 300; line-height: 1.1; letter-spacing: -1px;">Structure and Interpretation of Computer Programs</h1>
    <p style="font-size: 1.25rem; color: #9b59b6; font-style: italic;">"Programs must be written for people to read, and only incidentally for machines to execute."</p>
</div>

<!-- Intro Section -->
<div style="display: flex; gap: 40px; margin-bottom: 60px; flex-wrap: wrap; align-items: start; position: relative; z-index: 1;">
    <div style="flex: 1; min-width: 250px; background: #1a102e; padding: 10px; border: 1px solid #9b59b633;">
        <img src="https://covers.openlibrary.org/b/isbn/9780262510875-L.jpg" alt="SICP Cover" style="width: 100%; border-radius: 2px; filter: contrast(1.2) hue-rotate(280deg);">
    </div>
    <div style="flex: 1.5; min-width: 300px;">
        <h2 style="color: #ffffff; font-size: 2.2rem; margin-top: 0; font-weight: 300;">Abelson & Sussman’s Lisp Alchemy</h2>
        <p style="text-align: justify; font-size: 1.15rem; color: #e1e1e1;">
            SICP is the most profound meditation on the nature of computation ever written. Using Scheme (a dialect of Lisp), Abelson and Sussman teach the fundamental principles of abstraction, modularity, and the creation of metalinguistic languages. It is the book that teaches you how to build a language to solve a problem, rather than just solving the problem in a language.
        </p>
        <div style="margin-top: 35px; background: rgba(155, 89, 182, 0.1); padding: 30px; border-radius: 4px; border: 1px solid #9b59b6; font-family: monospace; font-style: italic; color: #fff; font-size: 1.15rem;">
            "(define (eval exp env) ... )"
        </div>
    </div>
</div>

<!-- Visual: The Substitution Model -->
<div style="background: #1a102e; border: 1px solid #9b59b6; padding: 40px; border-radius: 10px; margin-bottom: 60px; text-align: left; position: relative; z-index: 1;">
    <h3 style="color: #9b59b6; text-transform: uppercase; letter-spacing: 2px; text-align: center; margin-bottom: 30px;">[ THE RECURSIVE ASCENT ]</h3>
    <pre style="font-family: 'Fira Code', monospace; font-size: 12px; line-height: 1.4; color: #9b59b6;">
(sqrt 2)
➔ (sqrt-iter 1.0 2)
   ➔ (if (good-enough? 1.0 2) 1.0 (sqrt-iter (improve 1.0 2) 2))
      ➔ (sqrt-iter 1.5 2)
         ➔ ...
    </pre>
    <p style="font-size: 0.85rem; color: #888; margin-top: 25px; text-align: center;">Abstracting the process of evolution.</p>
</div>

<!-- High-Level Philosophical Analysis -->
<div style="margin-bottom: 60px; position: relative; z-index: 1;">
    <h3 style="color: #ffffff; font-size: 1.8rem; margin-bottom: 25px; border-bottom: 1px solid #9b59b644;">The Architecture of the Mind</h3>
    <div style="column-count: 2; column-gap: 50px; text-align: justify; font-size: 1.05rem; color: #e1e1e1; opacity: 0.9;">
        SICP treats programming as a primary means of managing complexity. It introduces the "Substitution Model" of evaluation and moves through the creation of data abstractions, the control of state, and the development of interpreters. The final chapters, which detail the creation of a register machine, bridge the gap between high-level functional concepts and the physical reality of hardware. 
        <br><br>
        The book’s most radical claim is that the boundaries between "data" and "code" are fluid. Through the use of higher-order functions (functions that take other functions as arguments), SICP shows how to build "Language-Oriented" systems. <em>SICP</em> is a mandatory rigorous training for any aspiring wizard of the digital age. It provides a visceral and high-fidelity roadmap for the evolution of the programmer's soul. It is a work of absolute intellectual beauty.
    </div>
</div>

<!-- Verdict -->
<div style="border-top: 1px solid #9b59b633; padding-top: 50px; text-align: center; position: relative; z-index: 1;">
    <h3 style="color: #9b59b6; font-size: 1.5rem; margin-bottom: 25px;">[ LOGOUT: WIZARD_SESSION ]</h3>
    <p style="color: #888; font-style: italic; max-width: 700px; margin: auto; font-size: 1.15rem;">
        "SICP is the book that separates the 'coder' from the 'computer scientist.' It is the most challenging and rewarding work in the field."
    </p>
    <div style="margin-top: 50px; font-size: 1.5rem; color: #9b59b6; letter-spacing: 20px;">🪄 🛡️ ⚙️</div>
</div>

</div>
