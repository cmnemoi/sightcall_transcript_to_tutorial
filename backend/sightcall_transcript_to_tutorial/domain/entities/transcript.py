from sightcall_transcript_to_tutorial.domain.value_objects import TranscriptId
from sightcall_transcript_to_tutorial.domain.value_objects.transcript_content import TranscriptContent


class Transcript:
    def __init__(self, transcript_id: TranscriptId, content: TranscriptContent):
        self._transcript_id = transcript_id
        self._content = content

    @property
    def transcript_id(self) -> TranscriptId:
        return self._transcript_id

    @property
    def content(self) -> TranscriptContent:
        return self._content

    def __eq__(self, other):
        return (
            isinstance(other, Transcript)
            and self.transcript_id == other.transcript_id
            and self.content == other.content
        )

    def __repr__(self):
        return f"Transcript(transcript_id={self.transcript_id!r}, content={self.content!r})"
