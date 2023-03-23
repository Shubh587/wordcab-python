"""Script used to update the version number in the __init__.py file."""
import re


# __init__.py file
init_file = "src/wordcab/__init__.py"
version_regex = r"^__version__ = ['\"]([^'\"]*)['\"]"

with open(init_file) as f:
    init_content = f.read()

previous_version = re.search(version_regex, init_content, re.M)

# pyproject.toml file
project_toml = "pyproject.toml"
toml_version_regex = r"^version = ['\"]([^'\"]*)['\"]"

with open(project_toml) as f:
    toml_content = f.read()

toml_version = re.search(toml_version_regex, toml_content, re.M)

if previous_version and toml_version:
    if previous_version.group(1) == toml_version.group(1):
        print(f"Version {previous_version.group(1)} already up to date")
        exit(0)

    else:
        content = init_content.replace(
            f"__version__ = {previous_version.group(1)!r}",
            f"__version__ = {toml_version.group(1)!r}",
        )

        with open(init_file, "w") as f:
            f.write(content)

        print(f"Updated {init_file} with version: {toml_version.group(1)}")

else:
    print(toml_version, previous_version)
    raise RuntimeError("Unable to find version string.")
