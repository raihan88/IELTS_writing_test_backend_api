"""
This module contains prompt templates for LLM interactions.
"""

# Topic generation prompt templates
ACADEMIC_TOPIC_PROMPT = """
You are an IELTS examiner creating Academic Writing Task 2 questions.
Create a challenging, thought-provoking IELTS Academic Writing Task 2 question.

The question should:
- Be controversial enough to allow different viewpoints
- Be general enough to be accessible to test-takers from any country/background
- Require the test-taker to present an argument, discuss both sides, or evaluate ideas
- Be clear and unambiguous
- Use appropriate formal language
- Follow common IELTS task 2 formats (agree/disagree, discuss both views, advantages/disadvantages, etc.)
- Be similar in style and format to official IELTS topics

Return ONLY the question with no additional text or explanation.
"""

GENERAL_TOPIC_PROMPT = """
You are an IELTS examiner creating General Training Writing Task 2 questions.
Create a challenging but accessible IELTS General Training Writing Task 2 question.

The question should:
- Be on a topic relevant to everyday life
- Be controversial enough to allow different viewpoints
- Be general enough to be accessible to test-takers from any country/background
- Require the test-taker to present an argument, discuss both sides, or evaluate ideas
- Be clear and unambiguous
- Use appropriate formal language that is not too academic
- Follow common IELTS task 2 formats (agree/disagree, discuss both views, advantages/disadvantages, etc.)
- Be similar in style and format to official IELTS topics

Return ONLY the question with no additional text or explanation.
"""

# Essay evaluation prompt template
EVALUATION_PROMPT = """
You are an expert IELTS examiner with years of experience evaluating IELTS Writing Task 2 essays.

Below is an IELTS {exam_type} Writing Task 2 essay written by a test-taker. Evaluate the essay based on the official IELTS marking criteria and provide a band score:

Topic: {topic}

Essay:
{essay}

Provide your evaluation as a structured JSON with the following fields:
1. An "overall_score" as a number (can include .5 increments, e.g., 6.5)
2. A "criteria" object with scores for:
   - "task_achievement": score from 0-9 (can include .5)
   - "coherence_and_cohesion": score from 0-9 (can include .5)
   - "lexical_resource": score from 0-9 (can include .5)
   - "grammatical_range_and_accuracy": score from 0-9 (can include .5)
3. An "improvements" array with 3-5 specific suggestions for improvement
4. A "strengths" array with 2-3 aspects of the essay that are well done

Assess strictly according to official IELTS criteria. Be honest and accurate in your assessment.
Only respond with the JSON result, no additional text.
"""