"""Prompt construction for retrieval-augmented generation."""

from __future__ import annotations

from app.domain.prompt import Prompt
from app.domain.prompt_template_source import PromptTemplateSource
from app.domain.retrieved_context import RetrievedContext


class PromptBuilder:
    """Build LLM prompts from a template, context, and user question."""

    def __init__(self, template_source: PromptTemplateSource) -> None:
        self._template_source = template_source

    def build(self, question: str, context: RetrievedContext) -> Prompt:
        """Render the configured template with context and question."""
        if context.chunks:
            context_text = "\n".join(f"- {chunk.content}" for chunk in context.chunks)
        else:
            context_text = ""

        template = self._template_source.get_template()
        prompt_text = template.format(context=context_text, question=question)
        return Prompt(text=prompt_text)
