import json
import google.generativeai as genai
import httpx
from ..config import GEMINI_API_KEY, DEEPSEEK_API_KEY, ACTIVE_LLM
from ..models.schemas import EvaluationResponse, CriteriaScores
from .prompt_templates import (
    ACADEMIC_TOPIC_PROMPT,
    GENERAL_TOPIC_PROMPT,
    EVALUATION_PROMPT
)


class LLMService:
    """Base class for LLM services"""
    async def generate_topic(self, exam_type):
        raise NotImplementedError("Subclasses must implement generate_topic")
    
    async def evaluate_essay(self, exam_type, topic, essay):
        raise NotImplementedError("Subclasses must implement evaluate_essay")


class GeminiService(LLMService):
    """Service for interacting with Google's Gemini API"""
    
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        
        genai.configure(api_key=GEMINI_API_KEY)
        # self.model = genai.GenerativeModel('gemini-1.5-pro-latest')
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    async def generate_topic(self, exam_type):
        """Generate an IELTS topic based on exam type"""
        prompt = ACADEMIC_TOPIC_PROMPT if exam_type == "academic" else GENERAL_TOPIC_PROMPT
        
        response = self.model.generate_content(prompt)
        return response.text.strip()
    
    async def evaluate_essay(self, exam_type, topic, essay):
        """Evaluate an IELTS essay using Gemini"""
        prompt = EVALUATION_PROMPT.format(
            exam_type=exam_type,
            topic=topic,
            essay=essay
        )
        
        response = self.model.generate_content(prompt)
        result = json.loads(response.text)
        
        return EvaluationResponse(
            overall_score=result["overall_score"],
            criteria=CriteriaScores(
                task_achievement=result["criteria"]["task_achievement"],
                coherence_and_cohesion=result["criteria"]["coherence_and_cohesion"],
                lexical_resource=result["criteria"]["lexical_resource"],
                grammatical_range_and_accuracy=result["criteria"]["grammatical_range_and_accuracy"]
            ),
            improvements=result["improvements"],
            strengths=result.get("strengths", [])
        )


class DeepSeekService(LLMService):
    """Service for interacting with DeepSeek API"""
    
    def __init__(self):
        if not DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY environment variable is not set")
        
        self.api_key = DEEPSEEK_API_KEY
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    async def _call_api(self, prompt):
        """Make a call to the DeepSeek API"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.api_url,
                headers=self.headers,
                json={
                    "model": "deepseek-r1",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 2000
                },
                timeout=30.0
            )
            
            response.raise_for_status()
            return response.json()
    
    async def generate_topic(self, exam_type):
        """Generate an IELTS topic based on exam type"""
        prompt = ACADEMIC_TOPIC_PROMPT if exam_type == "academic" else GENERAL_TOPIC_PROMPT
        
        response = await self._call_api(prompt)
        return response["choices"][0]["message"]["content"].strip()
    
    async def evaluate_essay(self, exam_type, topic, essay):
        """Evaluate an IELTS essay using DeepSeek"""
        prompt = EVALUATION_PROMPT.format(
            exam_type=exam_type,
            topic=topic,
            essay=essay
        )
        
        response = await self._call_api(prompt)
        result_text = response["choices"][0]["message"]["content"]
        result = json.loads(result_text)
        
        return EvaluationResponse(
            overall_score=result["overall_score"],
            criteria=CriteriaScores(
                task_achievement=result["criteria"]["task_achievement"],
                coherence_and_cohesion=result["criteria"]["coherence_and_cohesion"],
                lexical_resource=result["criteria"]["lexical_resource"],
                grammatical_range_and_accuracy=result["criteria"]["grammatical_range_and_accuracy"]
            ),
            improvements=result["improvements"],
            strengths=result.get("strengths", [])
        )


def get_llm_service() -> LLMService:
    """Factory function to get the configured LLM service"""
    if ACTIVE_LLM.lower() == "gemini":
        return GeminiService()
    elif ACTIVE_LLM.lower() == "deepseek":
        return DeepSeekService()
    else:
        # Default to Gemini if no valid selection
        return GeminiService()