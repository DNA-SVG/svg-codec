
test:
	python3 simple.py encode ../test-images/river.svg __test.dna
	python3 simple.py decode __test.dna __test.svg
	diff __test.svg ../test-images/river.svg && echo "pass"
	@rm -f __test.svg __test.dna


