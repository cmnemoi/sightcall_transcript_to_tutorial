from openai import OpenAI

from sightcall_transcript_to_tutorial.domain.config.settings import settings
from sightcall_transcript_to_tutorial.domain.entities.transcript import Transcript
from sightcall_transcript_to_tutorial.domain.entities.tutorial import Tutorial
from sightcall_transcript_to_tutorial.domain.exceptions.tutorial_generation_error import TutorialGenerationError
from sightcall_transcript_to_tutorial.domain.gateways.tutorial_generator_gateway_interface import (
    TutorialGeneratorGatewayInterface,
)
from sightcall_transcript_to_tutorial.domain.value_objects.tutorial_id import TutorialId
from sightcall_transcript_to_tutorial.domain.value_objects.user_id import UserId


class OpenAITutorialGeneratorGateway(TutorialGeneratorGatewayInterface):
    def __init__(self):
        api_key = settings.openai_api_key
        if not api_key:
            raise TutorialGenerationError("OPENAI_API_KEY not set in environment/config")
        self.openai_client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
        self.max_tokens = 10_000
        self.temperature = 0.1

    def generate_tutorial(self, transcript: Transcript, user_id: UserId) -> Tutorial:
        try:
            system_prompt = (
                "You are a helpful assistant that generates clear, concise, and actionable tutorials. "
                "Given a transcript of a support or troubleshooting session, your job is to extract only the meaningful steps "
                "that contributed to resolving or handling the issue. Ignore trivial dialogue, greetings, or unrelated conversation. "
                "Summarize the process as a step-by-step tutorial that someone else could follow to resolve a similar issue. "
                "Each step should be clear, actionable, and only included if it adds value."
            )
            user_prompt = (
                "Extract relevant steps from the transcript below. "
                "Generate a clear, step-by-step tutorial summarizing how the issue was resolved or handled. "
                "Include steps only when meaningful (avoid trivial dialogue).\n\n"
                f"Transcript:\n{transcript.content}"
            )
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            content = response.choices[0].message.content.strip()
            return Tutorial(
                tutorial_id=TutorialId.generate(),
                title=self._generate_tutorial_name_from_content(content),
                content=content,
                user_id=user_id,
            )
        except Exception as e:
            raise TutorialGenerationError(str(e))

    def _generate_tutorial_name_from_content(self, content: str) -> str:
        prompt = f"Generate a name for a tutorial from this content:\n{content}"
        response = self.openai_client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates clear, concise, and actionable tutorials.",
                },
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content.strip()
