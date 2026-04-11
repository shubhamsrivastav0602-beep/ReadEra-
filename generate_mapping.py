import os
import json
import re
from pathlib import Path

# Map summaries to their IDs
mapping = {}

# Scan all summary directories
summaries_base = os.path.join(os.path.dirname(__file__), 'summaries')

for category_dir in os.listdir(summaries_base):
    category_path = os.path.join(summaries_base, category_dir)
    if not os.path.isdir(category_path):
        continue
    
    # Get all markdown files in the category
    for filename in os.listdir(category_path):
        if filename.endswith('.md'):
            filepath = os.path.join(category_path, filename)
            relative_path = os.path.relpath(filepath, os.path.dirname(__file__))
            
            # Generate ID from filename
            # Remove numbering and extension, convert to lowercase with underscores
            base_name = filename.replace('.md', '')
            # Remove leading numbers and underscore (e.g., "02_" from "02_The_Intelligent_Investor")
            id_name = re.sub(r'^\d+_', '', base_name).lower().replace(' ', '_')
            
            # Use relative path with forward slashes
            relative_path = relative_path.replace('\\', '/')
            
            mapping[id_name] = relative_path
            
            # Also add alternative ID format (with numbers)
            alt_id = base_name.lower().replace(' ', '_')
            if alt_id not in mapping:
                mapping[alt_id] = relative_path

# Write to mapping.json in public/summaries
output_path = os.path.join(os.path.dirname(__file__), 'public', 'summaries', 'mapping.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(mapping, f, indent=2, ensure_ascii=False)

print(f"Generated mapping with {len(mapping)} entries")
print(f"Saved to {output_path}")

# Show sample entries
print("\nSample entries:")
for i, (k, v) in enumerate(sorted(mapping.items())[:10]):
    print(f"  {k}: {v}")
