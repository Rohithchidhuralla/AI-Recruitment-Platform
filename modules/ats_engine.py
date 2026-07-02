from typing import Dict, List


class ATSEngine:
    """
    Compares resume skills with job description skills.
    """

    def calculate_score(
        self,
        resume_skills: List[str],
        job_skills: List[str]
    ) -> Dict:

        # Remove duplicates
        resume_set = {skill.lower() for skill in resume_skills}
        job_set = {skill.lower() for skill in job_skills}

        matching = sorted(resume_set & job_set)
        missing = sorted(job_set - resume_set)

        if len(job_set) == 0:
            score = 0
        else:
            score = round((len(matching) / len(job_set)) * 100)

        return {
            "score": score,
            "matching_skills": matching,
            "missing_skills": missing
        }