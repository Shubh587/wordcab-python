# Bump the version number for release
bump-patch:
	poetry version patch
	python update_version.py

bump-minor:
	poetry version minor
	python update_version.py

bump-major:
	poetry version major
	python update_version.py
