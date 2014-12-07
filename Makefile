.PHONY : doc

doc : README.rst

README.rst : README.md
	pandoc --from=markdown_github --to=rst --no-highlight \
	    README.md \
	    -o README.rst

