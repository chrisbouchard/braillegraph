.PHONY : doc

doc : README.rst

README.rst : README.md
	pandoc --from=markdown --to=rst README.md -o README.rst

