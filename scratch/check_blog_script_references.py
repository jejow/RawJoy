import os
from bs4 import BeautifulSoup

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
blogs_path = os.path.join(workspace_root, "blogs")

# Let's inspect one of the blog post index.html files
sample_blog_post = os.path.join(blogs_path, "news", "blue-cat-portrait", "index.html")

if os.path.exists(sample_blog_post):
    with open(sample_blog_post, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    
    scripts = [s.get("src") for s in soup.find_all("script") if s.get("src")]
    print("Script references in blue-cat-portrait/index.html:")
    for src in scripts:
        print(f"  - {src}")
else:
    print("Sample blog post not found.")
