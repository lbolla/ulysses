import glob
import os
from bs4 import BeautifulSoup

def clean_chapter(fname: str, number: int, title: str):
    with open(fname) as input:
        soup = BeautifulSoup(input.read(), features='lxml')

    if soup.head:
        for x in soup.head.find_all('link'):
            x.extract()
        for x in soup.head.find_all('script'):
            x.extract()
        for x in soup.head.find_all('meta'):
            x.extract()

    toolbar = soup.find(id='toolbar')
    if toolbar:
        toolbar.extract()

    for header in soup.find_all("div", "reader-header"):
        header.extract()

    chapter = soup.find_all("div", "container")[0]
    del chapter["style"]
    h1 = soup.new_tag("h1")
    h1["class"] = "chapter"
    h1.string = f"{number}. {title}"
    chapter.insert(0, h1)
    return chapter

def clean_note(fname: str):
    with open(fname) as input:
        soup = BeautifulSoup(input.read(), features='lxml')

    if soup.head:
        for x in soup.head.find_all('link'):
            x.extract()
        for x in soup.head.find_all('script'):
            x.extract()
        for x in soup.head.find_all('meta'):
            x.extract()

    toolbar = soup.find(id='toolbar')
    if toolbar:
        toolbar.extract()

    enote = soup.find(id="expandednote")
    if enote:
        del enote["style"]

    for b in soup.find_all("button"):
        b.extract()

    output_fname = 'cleaned/notes/' + fname.split('/', 1)[1]
    with open(output_fname, 'w') as output:
        output.write(soup.prettify())

os.makedirs('cleaned/notes', exist_ok=True)

chapters = [
    ('Telemachus', "telem.html"),
    ('Nestor', "nestor.html"),
    ('Proteus', "proteus.html"),
    ('Calypso', "calypso.html"),
    ('Lotus Eaters', "lotus.html"),
    ('Hades', "hades.html"),
    ('Aeolus', "aeolus.html"),
    ('Lestrygonians', "lestry.html"),
    ('Scylla and Charybdis', "scylla.html"),
    ('Wandering Rocks', "wrocks.html"),
    ('Sirens', "sirens.html"),
    ('Cyclops', "cyclops.html"),
    ('Nausicaa', "nausicaa.html"),
    ('Oxen of the Sun', "oxen.html"),
    ('Circe', "circe.html"),
    ('Eumaeus', "eumaeus.html"),
    ('Ithaca', "ithaca.html"),
    ('Penelope', "penelope.html"),
]

cleaned = []
for i, (chapter_title, chapter_file) in enumerate(chapters):
    f = 'chapters/' + chapter_file
    print(f)
    cc = clean_chapter(f, i + 1, chapter_title)
    cleaned.append(cc)

all_chapters = ''.join(c.prettify() for c in cleaned)
with open('cleaned/index.html', 'w') as f:
    f.write(f'''
    <html>
        <head>
            <title>Ulysses</title>
        </head>
        <body>
        {all_chapters}
        <div class="chapter"><h1>Notes</h1></div>
        </body>
    </html
    ''')

notes = glob.glob('notes/*.htm')
for f in notes:
    print(f)
    clean_note(f)