import uuid
from typing import List

from pydantic import BaseModel, Field


class MinimalSource(BaseModel):
    """
    represents a single source of information.
    """

    file_path: str
    first_character_index: int
    last_character_index: int


class UnansweredQuestion(BaseModel):
    """
    represent an unanswered question
    """

    question_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str


class AnsweredQuestion(UnansweredQuestion):
    """
    represent an answered question
    """

    sources: List[MinimalSource]
    answer: str


class RagDataset(BaseModel):
    """
    represents a dataset of RAG questions
    """

    rag_questions: List[AnsweredQuestion | UnansweredQuestion]


class MinimalSearchResults(BaseModel):
    """
    represent the search results
    """

    question_id: str
    question: str
    retrieved_sources: List[MinimalSource]


class MinimalAnswer(MinimalSearchResults):
    """
    represent the search answer
    """

    answer: str


class StudentSearchResults(BaseModel):
    """
    represent search results
    """

    search_results: List[MinimalSearchResults]
    k: int


class StudentSearchResultsAndAnswer(BaseModel):
    """
    represent search results with answers
    """

    search_results: List[MinimalAnswer]
    k: int
