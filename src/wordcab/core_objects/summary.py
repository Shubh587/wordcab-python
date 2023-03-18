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

"""Wordcab API Summary object."""

import logging
import textwrap
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

from ..config import SUMMARY_TYPES


logger = logging.getLogger(__name__)


@dataclass
class StructuredSummary:
    """Structured summary object."""

    summary: Union[str, Dict[str, str]]
    context: Optional[
        Dict[str, Union[str, List[str], Dict[str, Union[str, List[str]]]]]
    ] = field(default=None)
    summary_html: Optional[Union[str, Dict[str, str]]] = field(default=None)
    end: Optional[str] = field(default=None)
    end_index: Optional[int] = field(default=None)
    start: Optional[str] = field(default=None)
    start_index: Optional[int] = field(default=None)
    timestamp_end: Optional[int] = field(default=None)
    timestamp_start: Optional[int] = field(default=None)
    transcript_segment: Optional[List[Dict[str, Union[str, int]]]] = field(default=None)

    def __repr__(self) -> str:
        """Return a string representation of the object without the None values."""
        return f"{self.__class__.__name__}({', '.join(f'{k}={v!r}' for k, v in self.__dict__.items() if v is not None)})"


@dataclass
class BaseSummary:
    """Summary object."""

    job_status: str
    summary_id: str
    display_name: Optional[str] = field(default=None)
    job_name: Optional[str] = field(default=None)
    process_time: Optional[str] = field(default=None)
    speaker_map: Optional[Dict[str, str]] = field(default=None)
    source: Optional[str] = field(default=None)
    source_lang: Optional[str] = field(default=None)
    summary_type: Optional[str] = field(default=None)
    summary: Optional[Dict[str, Any]] = field(default=None)
    target_lang: Optional[str] = field(default=None)
    transcript_id: Optional[str] = field(default=None)
    time_started: Optional[str] = field(default=None)
    time_completed: Optional[str] = field(default=None)

    def __post_init__(self) -> None:
        """Post init."""
        if self.summary_type:
            if self.summary_type not in SUMMARY_TYPES:
                raise ValueError(
                    f"Summary type must be one of {SUMMARY_TYPES}, not {self.summary_type}"
                )

        if self.time_started and self.time_completed:
            if self.time_started == self.time_completed:
                raise ValueError("time_started and time_completed must be different")

    def get_summaries(self) -> Dict[str, List[Union[str, List[str]]]]:
        """
        Get the summaries as a dictionary with the summary length as key and the summaries as values.

        Returns
        -------
        Dict[str, List[Union[str, List[str]]]]
            The summaries as a dictionnary with the summary length as key and the summaries as values.
            If the summary type is brief, the summaries are returned as a list of list of str,
            otherwise they are returned as a list of str.
        """
        if self.summary is None:
            return {}

        summaries: Dict[str, Any] = {}

        for summary_len in self.summary:
            summaries_list = [
                s.summary for s in self.summary[summary_len]["structured_summary"]
            ]

            if self.summary_type == "brief":
                summaries_list = [
                    [s["title"], s["brief_summary"]] for s in summaries_list
                ]

            summaries[summary_len] = summaries_list

        return summaries

    def get_formatted_summaries(
        self, add_context: Optional[bool] = False
    ) -> Dict[str, str]:
        """Format the summaries in an human readable format.

        Return the summaries as a dictionary in an human readable format with the summary length as key
        and the summaries as values.

        Parameters
        ----------
        add_context : bool, optional
            If True, add the context items to the summary, by default False.

        Returns
        -------
        Dict[str, str]
            The summaries as a dictionary with the summary length as key and the summaries as values formatted
            in an human readable format.
        """
        if self.summary is None:
            return {}

        summaries: Dict[str, Any] = {}

        for summary_len in self.summary:
            summaries[summary_len] = self._format_summary(
                self.summary[summary_len]["structured_summary"],
                summary_len,
                add_context,
            )

        return summaries

    def _format_summary(
        self,
        structured_summaries: List[StructuredSummary],
        summary_len: str,
        add_context: Optional[bool] = False,
    ) -> str:
        """
        Format the summary in an human readable format.

        Parameters
        ----------
        structured_summaries : List[StructuredSummary]
            The structured summary object.
        summary_len : str
            The summary length.
        add_context : bool, optional
            If True, add the context items to the summary. By default False.

        Returns
        -------
        str
            The summary formatted in an human readable format.
        """
        total_summary = len(structured_summaries)

        txt = f"{self.summary_type} - length: {summary_len}\n\n"
        for i in range(total_summary):
            txt += f"[{i + 1}/{total_summary}]"

            if self.summary_type == "brief":
                txt += f"Title: {self._textwrap(structured_summaries[i].summary['title'])}\n"
                txt += f"Summary: {self._textwrap(structured_summaries[i].summary['brief_summary'])}\n\n"
            else:
                txt += f"{self._textwrap(structured_summaries[i].summary)}\n\n"

            if add_context and structured_summaries[i].context:
                txt += f"{self._get_context_items(structured_summaries[i].context)}\n\n"

        return txt

    def _get_context_items(self, context: Dict[str, Any]) -> str:
        """Get the context items."""
        context_items = ""

        if "issue" in context:
            context_items += f"Issue: {context['issue']}\n"

        if "purpose" in context:
            context_items += f"Purpose: {context['purpose']}\n"

        if "next_steps" in context:
            context_items += f"Next steps: {context['next_steps']}\n"

        if "discussion_points" in context:
            context_items += f"Discussion points: {context['discussion_points']}\n"

        if "keywords" in context:
            context_items += f"Keywords: {context['keywords']}\n"

        return context_items

    def _textwrap(self, text_to_wrap: str, width: int = 80) -> str:
        """
        Return a formatted string with the text wrapped to the specified width using textwrap.

        Parameters
        ----------
        text_to_wrap : str
            The text to wrap.
        width : int
            The width to wrap the text to, by default 80.

        Returns
        -------
        str
            The formatted string with the text wrapped to the specified width.
        """
        return "\n".join(textwrap.wrap(text_to_wrap, width=width))


@dataclass
class ListSummaries:
    """List summaries object."""

    page_count: int
    next_page: str
    results: List[BaseSummary]
