# Wordcab Python

[![PyPI](https://img.shields.io/pypi/v/wordcab.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/wordcab.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/wordcab)][python version]
[![License](https://img.shields.io/pypi/l/wordcab)][license]

[![Read the documentation at https://wordcab-python.readthedocs.io/](https://img.shields.io/readthedocs/wordcab-python/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/Wordcab/wordcab-python/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/Wordcab/wordcab-python/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/wordcab-python/
[status]: https://pypi.org/project/wordcab-python/
[python version]: https://pypi.org/project/wordcab-python
[read the docs]: https://wordcab-python.readthedocs.io/
[tests]: https://github.com/Wordcab/wordcab-python/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/Wordcab/wordcab-python
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Wordcab

### What is Wordcab?

**Summarize any business communications at scale with Wordcab's API.**

**Wordcab** is a summarization service that provides a simple API to summarize any `audio`, `text`, or `JSON` file.

It also includes compatibility with famous transcripts platforms like [AssemblyAI](https://www.assemblyai.com/),
[Deepgram](https://deepgram.com/), [Rev.ai](https://www.rev.ai/), [Otter.ai](https://otter.ai/), or
[Sonix.ai](https://sonix.ai/).

### Getting started

You can learn more about Wordcab services and pricing on [our website](https://wordcab.com/).

If you want to try out the API, you can [signup](https://wordcab.com/signup/) for a free account and start using the API
right away.

## Requirements

- Os: Linux, Mac, Windows
- Python 3.8+

## Installation

You can install _Wordcab Python_ via [pip] from [PyPI]:

```console
$ pip install wordcab
```

Start using the API with any python script right away!

## Usage

Check this quick demo video:

[<img src="https://cdn.loom.com/sessions/thumbnails/25150a30c593467fa1632145ff2dea6f-with-play.gif" width="50%">](https://www.loom.com/embed/25150a30c593467fa1632145ff2dea6f "Quick Python Package Demo")

### Start Summary full pipeline

```python
import time
from wordcab import retrieve_job, retrieve_summary, start_summary
from wordcab.core_objects import AudioSource, GenericSource, InMemorySource


# Prepare your input source
## For a transcript stored as a .txt or .json file
source = GenericSource(filepath="path/to/file.txt")  # Or file.json
## For a transcript stored as an audio file
source = AudioSource(filepath="path/to/file.mp3")
## For a transcript already in memory
transcript = {"transcript": ["SPEAKER A: Hello.", "SPEAKER B: Hi."]}
source = InMemorySource(obj=transcript)

# Launch the Summarization job
job = start_summary(
	source_object=source,
	display_name="sample_txt",
	summary_type="no_speaker",
	summary_length=3,
	tags=["sample", "text"],
)

# Wait for the job completion
while True:
	job = retrieve_job(job_name=job.job_name)
	if job.job_status == "SummaryComplete":
		break
	else:
		time.sleep(3)
	
# Get the summary id
summary_id = job.summary_details["summary_id"]
# Retrieve the summary
summary = retrieve_summary(summary_id=summary_id)

# Get all information from the retrieved summary
for k, v in summary.__dict__.items():
    print(f"{k}: {v}")

# Get the summary as one block of text
for k, v in summary.summary:
	print(f"Summary Length: {k}")
	print(f"Summary: {v['structured_summary'].summary}")
```

Please see the [Documentation](https://wordcab-python.readthedocs.io/) for details.

## Contributing

Contributions are very welcome. 🚀
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [Apache 2.0 license][license],
_Wordcab Python SDK_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/Wordcab/wordcab-python/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/Wordcab/wordcab-python/blob/main/LICENSE
[contributor guide]: https://github.com/Wordcab/wordcab-python/blob/main/CONTRIBUTING.md
[command-line reference]: https://wordcab-python.readthedocs.io/en/latest/usage.html
