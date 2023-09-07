# Simple functions

Simple functions are available for all API endpoints. You can use them by importing them from `wordcab`.

```python
>>> from wordcab import get_stats

>>> stats = get_stats()
>>> stats
Stats(...)
```

They are simple wrappers around the client object. You can use the client object directly if you need more control.

## get_stats

::: src.wordcab.get_stats

## start_summary

::: src.wordcab.start_summary

## start_extract

::: src.wordcab.start_extract

## list_jobs

::: src.wordcab.list_jobs

## list_summaries

::: src.wordcab.list_summaries

## list_transcripts

::: src.wordcab.list_transcripts

## retrieve_job

::: src.wordcab.retrieve_job

## retrieve_summary

::: src.wordcab.retrieve_summary

## retrieve_transcript

::: src.wordcab.retrieve_transcript

## delete_job

::: src.wordcab.delete_job

## change_speaker_labels

::: src.wordcab.change_speaker_labels
