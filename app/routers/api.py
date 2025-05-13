from fastapi import APIRouter, HTTPException, Depends
from ..models.schemas import (
    TopicRequest,
    TopicResponse,
    EvaluationRequest,
    EvaluationResponse
)
from ..services.llm_services import get_llm_service

router = APIRouter(prefix="/api", tags=["IELTS API"])

@router.post("/generate-topic", response_model=TopicResponse)
async def generate_topic(request: TopicRequest):
    """
    Generate an IELTS writing topic based on the exam type.
    """
    try:
        llm_service = get_llm_service()
        topic = await llm_service.generate_topic(request.exam_type)
        return TopicResponse(topic=topic)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating topic: {str(e)}")


@router.post("/evaluate-essay", response_model=EvaluationResponse)
async def evaluate_essay(request: EvaluationRequest):
    """
    Evaluate an IELTS essay using LLM and provide scores and feedback.
    """
    # Validate word count
    if request.word_count < 150:
        raise HTTPException(
            status_code=400, 
            detail="Essay must be at least 150 words for Task 2."
        )
    
    try:
        llm_service = get_llm_service()
        evaluation = await llm_service.evaluate_essay(
            exam_type=request.exam_type,
            topic=request.topic,
            essay=request.essay
        )
        return evaluation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating essay: {str(e)}")