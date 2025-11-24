all: clean download epub

clean:
	rm -rf cleaned ulysses

download:
	python download.py

epub:
	ebook-convert ulysses/index.html ulysses.epub --cover cover-monochrome.jpg --authors Joyce --title Ulysses

view:
	ebook-viewer ulysses.epub

staging_clean:
	python clean.py

staging_notes:
	wget -r https://joyce-staging.net/pages/indexoftitles.htm
	mv joyce-staging.net/notes .

staging_img:
	cp -R --update=none notes/episode_* cleaned/notes

staging_epub:
	ebook-convert cleaned/index.html staging-ulysses.epub --cover cover-monochrome.jpg --authors Joyce --title Ulysses