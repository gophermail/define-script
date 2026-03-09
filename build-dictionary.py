#!/usr/bin/env python3
"""
One-time import script: converts kaikki.org JSONL dump into a SQLite dictionary.
Usage: python3 build-dictionary.py /path/to/raw-wiktextract-data.jsonl.gz
The .gz file is read directly without fully decompressing first.
"""

import sys
import gzip
import json
import sqlite3
import os

DB_PATH = os.path.expanduser("~/.local/bin/define-script/dictionary.db")
JSONL_GZ = sys.argv[1] if len(sys.argv) > 1 else "raw-wiktextract-data.jsonl.gz"

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

print(f"Creating database at {DB_PATH}")
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS definitions")
c.execute("""
    CREATE TABLE definitions (
        word TEXT NOT NULL,
        pos  TEXT,
        def  TEXT NOT NULL
    )
""")

count = 0
skipped = 0

print(f"Reading {JSONL_GZ} ...")

with gzip.open(JSONL_GZ, "rt", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            skipped += 1
            continue

        # English words only
        if entry.get("lang_code") != "en":
            continue

        word = entry.get("word", "").strip()
        pos  = entry.get("pos", "").strip()
        if not word:
            continue

        for sense in entry.get("senses", []):
            glosses = sense.get("glosses", [])
            if not glosses:
                continue
            # Use the most specific gloss (last one)
            definition = glosses[-1].strip()
            if definition:
                c.execute("INSERT INTO definitions VALUES (?, ?, ?)", (word, pos, definition))
                count += 1

        if count % 100000 == 0 and count > 0:
            print(f"  {count:,} definitions imported...")
            conn.commit()

conn.commit()

print(f"\nBuilding index...")
c.execute("CREATE INDEX idx_word ON definitions(word COLLATE NOCASE)")
conn.commit()
conn.close()

print(f"\nDone! {count:,} definitions imported, {skipped} lines skipped.")
print(f"Database saved to: {DB_PATH}")
