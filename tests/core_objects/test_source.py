# Copyright 2022-2023 The Wordcab Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test suite for the source dataclasses."""

import json
from pathlib import Path

import pytest

from wordcab.config import AVAILABLE_AUDIO_FORMATS
from wordcab.core_objects import (
    AssemblyAISource,
    AudioSource,
    BaseSource,
    DeepgramSource,
    GenericSource,
    InMemorySource,
    RevSource,
    SignedURLSource,
    VTTSource,
    WordcabTranscriptSource,
)
from wordcab.core_objects.utils import _get_deepgram_utterances


def test_available_audio_formats() -> None:
    """Test the AVAILABLE_AUDIO_FORMATS object."""
    assert AVAILABLE_AUDIO_FORMATS == [".flac", ".m4a", ".mp3", ".mpga", ".ogg", ".wav"]


def test_base_source(tmp_path: Path) -> None:
    """Test the BaseSource object."""
    path = f"{tmp_path}/test.txt"
    with open(path, "w") as f:
        f.write("test")

    with pytest.raises(ValueError):
        BaseSource()
    with pytest.raises(ValueError):
        BaseSource(filepath=Path(path), url="https://example.com")
    with pytest.raises(TypeError):
        BaseSource(filepath=123456)  # type: ignore
    with pytest.raises(FileNotFoundError):
        BaseSource(filepath=Path(f"{tmp_path}/does_not_exist.txt"))
    with pytest.raises(ValueError):
        BaseSource(url="123456")

    base = BaseSource(filepath=Path(path))
    assert base.filepath == Path(path)
    assert base.url is None
    assert base.url_headers is None
    assert base.source_type == "local"
    assert base._stem == Path(path).stem
    assert base._suffix == Path(path).suffix

    base = BaseSource(
        url="https://raw.githubusercontent.com/Wordcab/wordcab-python/main/tests/sample_1.json",
        url_headers={"Accept": "application/json", "Content-Type": "application/json"},
    )
    assert base.filepath is None
    assert (
        base.url
        == "https://raw.githubusercontent.com/Wordcab/wordcab-python/main/tests/sample_1.json"
    )
    assert base.url_headers == {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    assert base.source_type == "remote"
    assert base._stem == "sample_1"
    assert base._suffix == ".json"

    assert hasattr(base, "_load_file_from_path") and callable(base._load_file_from_path)
    assert hasattr(base, "_load_file_from_url") and callable(base._load_file_from_url)
    assert hasattr(base, "_check_if_url_is_valid") and callable(
        base._check_if_url_is_valid
    )
    assert hasattr(base, "prepare_payload")
    with pytest.raises(NotImplementedError):
        base.prepare_payload()
    assert hasattr(base, "prepare_headers")
    with pytest.raises(NotImplementedError):
        base.prepare_headers()

    base = BaseSource(filepath=path)
    assert base.filepath == Path(path)
    assert isinstance(base.filepath, Path)


def test_generic_source_with_filepath(tmp_path: Path) -> None:
    """Test the GenericSource object."""
    path = "tests/sample_1.txt"
    generic_source = GenericSource(filepath=Path(path))
    assert generic_source.filepath == Path(path)
    assert generic_source.url is None
    assert generic_source.source_type == "local"
    assert generic_source._stem == Path(path).stem
    assert generic_source._suffix == Path(path).suffix
    assert generic_source.file_object is not None
    assert hasattr(generic_source, "prepare_payload") and callable(
        generic_source.prepare_payload
    )
    assert generic_source.prepare_payload() == json.dumps(
        {"transcript": generic_source.file_object.decode("utf-8").splitlines()}
    )
    assert hasattr(generic_source, "prepare_headers") and callable(
        generic_source.prepare_headers
    )
    assert generic_source.prepare_headers() == {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    path = "tests/sample_1.json"
    generic_source = GenericSource(filepath=Path(path))
    assert generic_source.filepath == Path(path)
    assert generic_source.url is None
    assert generic_source.source_type == "local"
    assert generic_source._stem == Path(path).stem
    assert generic_source._suffix == Path(path).suffix
    assert generic_source.file_object is not None
    assert hasattr(generic_source, "prepare_payload") and callable(
        generic_source.prepare_payload
    )
    assert generic_source.prepare_payload() == json.dumps(
        {"transcript": json.loads(generic_source.file_object)}
    )
    assert hasattr(generic_source, "prepare_headers") and callable(
        generic_source.prepare_headers
    )
    assert generic_source.prepare_headers() == {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    md_path = f"{tmp_path}/test.md"
    with open(md_path, "w") as f:
        f.write("test")

    with pytest.raises(ValueError):
        GenericSource(filepath=Path(md_path))


def test_generic_source_with_url() -> None:
    """Test the GenericSource object."""
    generic_source = GenericSource(
        url="https://raw.githubusercontent.com/Wordcab/wordcab-python/main/tests/sample_1.txt",
        url_headers={"Accept": "application/json", "Content-Type": "application/json"},
    )
    assert generic_source.filepath is None
    assert (
        generic_source.url
        == "https://raw.githubusercontent.com/Wordcab/wordcab-python/main/tests/sample_1.txt"
    )
    assert generic_source.url_headers == {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    assert generic_source.source_type == "remote"
    assert generic_source._stem == "sample_1"
    assert generic_source._suffix == ".txt"
    assert generic_source.file_object is not None
    assert hasattr(generic_source, "prepare_payload") and callable(
        generic_source.prepare_payload
    )
    assert generic_source.prepare_payload() == json.dumps(
        {"transcript": generic_source.file_object.decode("utf-8").splitlines()}
    )
    assert hasattr(generic_source, "prepare_headers") and callable(
        generic_source.prepare_headers
    )
    assert generic_source.prepare_headers() == {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    generic_source = GenericSource(
        url="https://raw.githubusercontent.com/Wordcab/wordcab-python/main/tests/sample_1.json"
    )
    assert generic_source.filepath is None
    assert (
        generic_source.url
        == "https://raw.githubusercontent.com/Wordcab/wordcab-python/main/tests/sample_1.json"
    )
    assert generic_source.source_type == "remote"
    assert generic_source._stem == "sample_1"
    assert generic_source._suffix == ".json"
    assert generic_source.file_object is not None
    assert hasattr(generic_source, "prepare_payload") and callable(
        generic_source.prepare_payload
    )
    assert generic_source.prepare_payload() == json.dumps(
        {"transcript": json.loads(generic_source.file_object)}
    )
    assert hasattr(generic_source, "prepare_headers") and callable(
        generic_source.prepare_headers
    )
    assert generic_source.prepare_headers() == {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def test_audio_source(tmp_path: Path) -> None:
    """Test the AudioSource object."""
    path = "tests/sample_1.mp3"

    audio_source = AudioSource(filepath=Path(path))
    assert audio_source.filepath == Path(path)
    assert audio_source.url is None
    assert audio_source.source_type == "local"
    assert audio_source._stem == Path(path).stem
    assert audio_source._suffix == Path(path).suffix
    assert audio_source.file_object is not None
    assert hasattr(audio_source, "prepare_payload") and callable(
        audio_source.prepare_payload
    )
    assert audio_source.prepare_payload() == {"audio_file": audio_source.file_object}
    assert hasattr(audio_source, "prepare_headers") and callable(
        audio_source.prepare_headers
    )
    assert audio_source.prepare_headers() == {}

    aac_path = f"{tmp_path}/test.aac"
    with open(aac_path, "w") as f:
        f.write("test")

    with pytest.raises(ValueError):
        AudioSource(filepath=Path(aac_path))

    url = "https://github.com/Wordcab/wordcab-python/blob/main/tests/sample_1.mp3?raw=true"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    audio_source = AudioSource(url=url, url_headers=headers)
    assert audio_source.filepath is None
    assert audio_source.url == url
    assert audio_source.url_headers == headers
    assert audio_source.source_type == "remote"
    assert audio_source._stem == "sample_1"
    assert audio_source._suffix == ".mp3"
    assert audio_source.file_object is not None
    assert hasattr(audio_source, "prepare_payload") and callable(
        audio_source.prepare_payload
    )
    assert audio_source.prepare_payload() == {"audio_file": audio_source.file_object}
    assert hasattr(audio_source, "prepare_headers") and callable(
        audio_source.prepare_headers
    )
    assert audio_source.prepare_headers() == {}

    # Test filename with spaces and dots
    url = "https://example.com/test%20file%20with%20dots.mp3"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    audio_source = AudioSource(url=url, url_headers=headers)
    assert audio_source.filepath is None
    assert audio_source.url == url
    assert audio_source.url_headers == headers
    assert audio_source.source_type == "remote"
    assert audio_source._stem == "test file with dots"
    assert audio_source._suffix == ".mp3"
    assert audio_source.file_object is not None
    assert hasattr(audio_source, "prepare_payload") and callable(
        audio_source.prepare_payload
    )
    assert audio_source.prepare_payload() == {"audio_file": audio_source.file_object}
    assert hasattr(audio_source, "prepare_headers") and callable(
        audio_source.prepare_headers
    )
    assert audio_source.prepare_headers() == {}


def test_in_memory_source() -> None:
    """Test the InMemorySource object."""
    with pytest.raises(TypeError):
        InMemorySource(obj="test")  # type: ignore
    with pytest.raises(ValueError):
        InMemorySource(obj={"test": "test"})  # type: ignore
    with pytest.raises(TypeError):
        InMemorySource(obj={"transcript": "test"})  # type: ignore

    in_memory_source = InMemorySource(obj={"transcript": ["test"]})
    assert in_memory_source.obj == {"transcript": ["test"]}
    assert in_memory_source.source == "generic"
    assert in_memory_source.source_type == "in_memory"
    assert hasattr(in_memory_source, "prepare_payload") and callable(
        in_memory_source.prepare_payload
    )
    assert in_memory_source.prepare_payload() == json.dumps({"transcript": ["test"]})
    assert hasattr(in_memory_source, "prepare_headers") and callable(
        in_memory_source.prepare_headers
    )
    assert in_memory_source.prepare_headers() == {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def test_wordcab_transcript_source() -> None:
    """Test the WordcabTranscriptSource object."""
    source_obj = WordcabTranscriptSource(transcript_id="test")

    assert source_obj.transcript_id == "test"
    assert source_obj.source == "wordcab_transcript"
    assert source_obj.__repr__() == "WordcabTranscriptSource(transcript_id=test)"


def test_signed_url_source() -> None:
    """Test the SignedURLSource object."""
    with pytest.raises(NotImplementedError):
        SignedURLSource(url="https://example.com")


def test_rev_source() -> None:
    """Test the RevSource object."""
    with pytest.raises(NotImplementedError):
        RevSource(url="https://example.com")


def test_vtt_source() -> None:
    """Test the VTTSource object."""
    with pytest.raises(NotImplementedError):
        VTTSource(url="https://example.com")


def test_assembly_ai_source() -> None:
    """Test the AssemblyAISource object."""
    with pytest.raises(NotImplementedError):
        AssemblyAISource(url="https://example.com")


def test_deepgram_source() -> None:
    """Test the DeepgramSource object."""
    path = "tests/deepgram_sample.json"
    dg_source = DeepgramSource(filepath=Path(path))

    assert dg_source.filepath == Path(path)
    assert dg_source.url is None
    assert dg_source.source_type == "local"
    assert dg_source._stem == Path(path).stem
    assert dg_source._suffix == Path(path).suffix
    assert dg_source.file_object is not None
    assert hasattr(dg_source, "prepare_payload") and callable(dg_source.prepare_payload)
    assert dg_source.prepare_payload() == json.dumps(
        {"transcript": _get_deepgram_utterances(json.loads(dg_source.file_object))}
    )
    assert hasattr(dg_source, "prepare_headers") and callable(dg_source.prepare_headers)
    assert dg_source.prepare_headers() == {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
