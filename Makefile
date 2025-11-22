all: clean cleaned epub

clean:
	rm -rf cleaned

cleaned:
	python main.py

download_notes:
	wget -r https://joyce-staging.net/pages/indexoftitles.htm
	mv joyce-staging.net/notes .

epub:
	ebook-convert cleaned/index.html ulysses.epub --cover cover-monochrome.jpg --authors Joyce --title Ulysses

img:
	cp -R --update=none notes/episode_* cleaned/notes

view:
	ebook-viewer ulysses.epub