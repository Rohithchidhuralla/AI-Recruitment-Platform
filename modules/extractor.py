import re


class ResumeExtractor:

    def extract(self, text):

        info = {}

        # -----------------------------
        # Name (Assume first non-empty line)
        # -----------------------------
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        if lines:
            info["name"] = lines[0]
        else:
            info["name"] = "Unknown"

        # -----------------------------
        # Email
        # -----------------------------
        email = re.findall(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text,
        )

        info["email"] = email[0] if email else ""

        # -----------------------------
        # Phone
        # -----------------------------
        phone = re.findall(
            r"(\+?\d[\d\s\-]{8,15}\d)",
            text,
        )

        info["phone"] = phone[0] if phone else ""

        # -----------------------------
        # LinkedIn
        # -----------------------------
        linkedin = re.findall(
            r"(https?://(?:www\.)?linkedin\.com/in/[^\s]+|linkedin\.com/in/[^\s]+)",
            text,
            re.IGNORECASE,
        )

        info["linkedin"] = linkedin[0] if linkedin else ""

        # -----------------------------
        # GitHub
        # -----------------------------
        github = re.findall(
            r"(https?://(?:www\.)?github\.com/[^\s]+|github\.com/[^\s]+)",
            text,
            re.IGNORECASE,
        )

        info["github"] = github[0] if github else ""

        # -----------------------------
        # Skills Database
        # -----------------------------
        skills_db = [
            "python",
            "java",
            "c",
            "c++",
            "sql",
            "mysql",
            "mongodb",
            "html",
            "css",
            "javascript",
            "react",
            "node",
            "django",
            "flask",
            "streamlit",
            "machine learning",
            "deep learning",
            "tensorflow",
            "pytorch",
            "opencv",
            "git",
            "github",
            "aws",
            "azure",
            "docker",
            "kubernetes",
            "linux",
            "excel",
            "power bi",
            "tableau"
        ]

        text_lower = text.lower()

        found = []

        for skill in skills_db:
            if skill in text_lower:
                found.append(skill.title())

        info["skills"] = sorted(set(found))

        return info