# poetry  add deepdiff

clean:
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
	/bin/rm -fR docs
	/bin/rm -fR docs-source/-autosummary

doc:
	poetry run sphinx-build -b html docs-source docs/

test:
	poetry run  coverage run  --source=fossmerge -m pytest -vvv --tb=auto  tests

run:
	poetry run fossmerge_cli


black:
	poetry run  black tests
	poetry run  black fossmerge
	
