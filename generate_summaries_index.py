#!/usr/bin/env python3
"""
Generate a comprehensive summaries index with all summaries content
"""

import os
import json
import glob
from pathlib import Path

def generate_summaries_index():
    """Generate summaries index with all content"""
    summaries = {}
    summaries_dir = "summaries"
    
    # Scan all summary files
    for md_file in glob.glob(os.path.join(summaries_dir, "**/*.md"), recursive=True):
        try:
            # Get category from directory name
            relative_path = os.path.relpath(md_file, summaries_dir)
            parts = relative_path.split(os.sep)
            category = parts[0] if len(parts) > 1 else "Unknown"
            filename = os.path.basename(md_file)
            
            # Remove numbering prefix if exists (e.g., "01_" -> "")
            book_name = filename.replace(".md", "")
            if book_name[0].isdigit() and book_name[1] == "_":
                book_name = book_name[3:]  # Remove "01_"
            
            # Replace underscores with spaces
            book_name = book_name.replace("_", " ")
            
            # Read content
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            summaries[book_name] = {
                "id": book_name.lower().replace(" ", "_"),
                "title": book_name,
                "category": category,
                "path": relative_path.replace("\\", "/"),
                "content": content,
                "word_count": len(content.split()),
                "file_size": len(content)
            }
            
            print(f"✓ {category}: {book_name}")
        except Exception as e:
            print(f"✗ Error reading {md_file}: {e}")
    
    # Save to JSON
    output_dir = "public/summaries"
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, "all_summaries.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summaries, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Generated index with {len(summaries)} summaries")
    print(f"📁 Saved to: {output_file}")
    print(f"📊 Total size: {sum(s['file_size'] for s in summaries.values()) / 1024 / 1024:.2f} MB")
    
    # Also create a lightweight index with just metadata (without content)
    metadata_index = {
        title: {
            "id": data["id"],
            "category": data["category"],
            "word_count": data["word_count"],
            "path": data["path"]
        }
        for title, data in summaries.items()
    }
    
    metadata_file = os.path.join(output_dir, "summaries_metadata.json")
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata_index, f, ensure_ascii=False, indent=2)
    
    print(f"📄 Lightweight metadata index saved to: {metadata_file}")

if __name__ == "__main__":
    generate_summaries_index()
