from uuid import uuid4

from app.domain import (
    Prompt,
    PromptBuilder,
    PromptTemplateSource,
    RetrievedContext,
    TextChunk,
)

TEMPLATE = """System line.

Context:
{context}

Question:
{question}
"""


class StaticPromptTemplateSource:
    """In-memory prompt template source for unit tests."""

    def __init__(self, template: str) -> None:
        self._template = template

    def get_template(self) -> str:
        return self._template

    def set_template(self, template: str) -> None:
        self._template = template


def _make_builder() -> PromptBuilder:
    source: PromptTemplateSource = StaticPromptTemplateSource(TEMPLATE)
    return PromptBuilder(template_source=source)


def _make_chunk(content: str, index: int = 0) -> TextChunk:
    return TextChunk(
        chunk_id=uuid4(),
        content=content,
        source_filename="source.txt",
        index=index,
    )


def test_builds_prompt_with_context_and_question() -> None:
    builder = _make_builder()
    context = RetrievedContext(
        chunks=(
            _make_chunk("First fact about Python.", 0),
            _make_chunk("Second fact about FastAPI.", 1),
        )
    )

    result = builder.build("What is Python?", context)

    assert isinstance(result, Prompt)
    assert "System line." in result.text
    assert "- First fact about Python." in result.text
    assert "- Second fact about FastAPI." in result.text
    assert "What is Python?" in result.text


def test_builds_prompt_with_empty_context() -> None:
    builder = _make_builder()
    context = RetrievedContext(chunks=())

    result = builder.build("Any question?", context)

    assert isinstance(result, Prompt)
    assert "Context:" in result.text
    assert "Question:" in result.text
    assert "Any question?" in result.text


def test_context_chunks_appear_in_order() -> None:
    builder = _make_builder()
    context = RetrievedContext(
        chunks=(
            _make_chunk("Alpha", 0),
            _make_chunk("Beta", 1),
            _make_chunk("Gamma", 2),
        )
    )

    result = builder.build("Order?", context)

    alpha_pos = result.text.index("- Alpha")
    beta_pos = result.text.index("- Beta")
    gamma_pos = result.text.index("- Gamma")
    assert alpha_pos < beta_pos < gamma_pos
