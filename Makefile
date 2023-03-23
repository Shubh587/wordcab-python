# Bump the version number for release
bumpversion-patch:
	poetry version patch
	python update_version.py

bumpversion-minor:
	poetry version minor
	python update_version.py

bumpversion-major:
	poetry version major
	python update_version.py
