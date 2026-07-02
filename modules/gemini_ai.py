import os

from google import genai
from google.genai import types

from config import GEMINI_API_KEY


class GeminiAI:
    """
    Gemini AI Service
    """

    def __init__(self):

        if not GEMINI_API_KEY:
            raise ValueError("Gemini API Key not found.")

        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def analyze_resume(
        self,
        resume_text,
        ats_score,
        matching_skills,
        missing_skills
    ):

        prompt = f"""
You are an expert Technical Recruiter.

Analyze the following resume.

Resume:

{resume_text}

ATS Score:
{ats_score}

Matching Skills:
{matching_skills}

Missing Skills:
{missing_skills}

Generate the following:

1. Resume Summary

2. Strengths

3. Weaknesses

4. Missing Skills Analysis

5. Resume Improvement Suggestions

6. Five Technical Interview Questions

Format the response in Markdown.
"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,
            ),
        )

        return response.text