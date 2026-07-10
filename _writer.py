import os

PAGES_DIR = r"D:\my-wiki\知识库"
os.makedirs(PAGES_DIR, exist_ok=True)
count = 0

def write_page(filename, content):
    global count
    path = os.path.join(PAGES_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    count += 1
    print(f"OK: {filename}")

def enrich_page(filename, insert_before, new_text):
    path = os.path.join(PAGES_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    pos = content.find(insert_before)
    if pos >= 0:
        content = content[:pos] + new_text + "\n" + content[pos:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"ENRICHED: {filename}")
