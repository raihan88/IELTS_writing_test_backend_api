from pydantic import BaseModel, Field
from typing import List, Optional, Literal


class TopicRequest(BaseModel):
    exam_type: Literal["academic", "general"] = Field(
        ..., description="Type of IELTS exam (academic or general)"
    )


class TopicResponse(BaseModel):
    topic: str = Field(..., description="Generated IELTS topic")


class EvaluationRequest(BaseModel):
    exam_type: Literal["academic", "general"] = Field(
        ..., description="Type of IELTS exam (academic or general)"
    )
    topic: str = Field(..., description="The IELTS topic/question")
    essay: str = Field(..., description="The essay written by the user")
    word_count: int = Field(..., description="Word count of the essay")


class CriteriaScores(BaseModel):
    task_achievement: float = Field(..., description="Score for Task Achievement")
    coherence_and_cohesion: float = Field(..., description="Score for Coherence and Cohesion")
    lexical_resource: float = Field(..., description="Score for Lexical Resource")
    grammatical_range_and_accuracy: float = Field(
        ..., description="Score for Grammatical Range and Accuracy"
    )


class EvaluationResponse(BaseModel):
    overall_score: float = Field(..., description="Overall band score")
    criteria: CriteriaScores = Field(..., description="Scores for individual criteria")
    improvements: List[str] = Field(..., description="Suggestions for improvement")
    strengths: Optional[List[str]] = Field(None, description="Areas of strength")