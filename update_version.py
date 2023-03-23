"""Script used to update the version number in the __init__.py file."""
import re


init_file = "src/wordcab/__init__.py"
version_regex = r"^__version__ = ['\"]([^'\"]*)['\"]"

with open(init_file) as f:
    content = f.read()
    previous_version = re.search(version_regex, content, re.M)

project_toml = "pyproject.toml"
toml_version_regex = r"^version = ['\"]([^'\"]*)['\"]"

with open(project_toml) as f:
    toml_content = f.read()
    toml_version = re.search(toml_version_regex, content, re.M)

if previous_version and toml_version:
    if previous_version.group(1) == toml_version.group(1):
        print(f"Version {previous_version.group(1)} already up to date")
        exit(0)
    else:
        new_version = toml_version.group(1)
        content = re.sub(version_regex, f"__version__ = {new_version!r}", content, re.M)

        with open(init_file, "w") as f:
            f.write(content)
            print(f"Updated {init_file} with version: {new_version}")

else:
    raise RuntimeError("Unable to find __version__ string in __init__.py")
