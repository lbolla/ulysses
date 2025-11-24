import os
import json
import urllib.request

from bs4 import BeautifulSoup


apiurl = "https://joyceproject.com/api/"
chaptersapiurl = os.path.join(apiurl, "chapters/")
notesapiurl = os.path.join(apiurl, "notes/")
outdir = "ulysses/"

def write(fname, title, content):
    os.makedirs(outdir, exist_ok=True)
    outfile = os.path.join(outdir, fname)
    if "<html>" not in content:
        content = f"""
        <html>
        <head><title>{title}</title></head>
        <body>{content}</body>
        </html>
        """
    with open(outfile, "w") as f:
        f.write(content)

def exists(fname):
    outfile = os.path.join(outdir, fname)
    return os.path.exists(outfile)

def download_chapter(id, number, title):
    if exists(id):
        return
    print("Downloading chapter", id, number, title)
    with urllib.request.urlopen(os.path.join(chaptersapiurl, id)) as f:
        chapter = json.loads(f.read().decode())
        html = chapter["html_source"]
        # write(id, title, html)
        return html

def download_chapters():
    if exists("index.html"):
        return
    print("Downloading chapters")
    with urllib.request.urlopen(chaptersapiurl) as f:
        data = f.read().decode()
        chapters = json.loads(data)
        for chapter in chapters:
            html = download_chapter(**chapter)
            chapter["html"] = html
        create_index(chapters)

def create_index(chapters):
    content = []
    for chapter in chapters:
        title = chapter["title"]
        html = f"""
        <h1 class="chapter">{chapter["number"]}. {title}</h1>
        {chapter["html"]}
        """
        content.append(html)
    content = f"""
    <html>
    <body>
      { ''.join(content) }
      <div class="chapter">
        <h1>Notes</h1>
    </div>
    </body>
    </html>
"""

    soup = BeautifulSoup(content, features='lxml')
    for span in soup.find_all("span"):
        if span.get("data-edition"):
            span.extract()

    content = str(soup)
    write("index.html", "Ulysses", content)

def download_note(id, title, **kwargs):
    if exists(id):
        return
    print("Downloading note", id, title)
    with urllib.request.urlopen(os.path.join(notesapiurl, id)) as f:
        chapter = json.loads(f.read().decode())
        html = chapter["html_source"]
        write(id, title, html)

def download_notes():
    print("Downloading notes")
    with urllib.request.urlopen(notesapiurl) as f:
        data = f.read().decode()
        notes = json.loads(data)
        for note in notes:
            download_note(**note)

def main():
    download_chapters()
    download_notes()

if __name__ == "__main__":
    main()