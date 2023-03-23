"""Script used to update the version number in the __init__.py file."""
import re


init_file = "wordcab/__init__.py"
version_regex = r"^__version__ = ['\"]([^'\"]*)['\"]"

with open(init_file) as f:
    content = f.read()

version = re.search(version_regex, content, re.M)

if version:
    current_version = version.group(1)
    print(f"Current version: {current_version}")
    new_version = input("Enter new version: ")
    content = re.sub(version_regex, f"__version__ = {new_version!r}", content, re.M)

    with open(init_file, "w") as f:
        f.write(content)
        print(f"Updated {init_file} with version: {new_version}")

else:
    raise RuntimeError("Unable to find __version__ string in __init__.py")
