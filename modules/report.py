from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


class ReportGenerator:

    def generate_report(
        self,
        filename,
        info,
        ats_result,
        ai_analysis
    ):

        doc = SimpleDocTemplate(filename)

        styles = getSampleStyleSheet()

        story = []

        story.append(
            Paragraph(
                "<b>AI Recruitment Platform Report</b>",
                styles["Title"]
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                f"<b>Name:</b> {info['name']}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Email:</b> {info['email']}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Phone:</b> {info['phone']}",
                styles["BodyText"]
            )
        )

        story.append(Spacer(1, 12))

        story.append(
            Paragraph(
                f"<b>ATS Score:</b> {ats_result['score']}%",
                styles["Heading2"]
            )
        )

        story.append(Spacer(1, 12))

        story.append(
            Paragraph(
                f"<b>Matching Skills:</b><br/>{', '.join(ats_result['matching_skills'])}",
                styles["BodyText"]
            )
        )

        story.append(Spacer(1, 12))

        story.append(
            Paragraph(
                f"<b>Missing Skills:</b><br/>{', '.join(ats_result['missing_skills'])}",
                styles["BodyText"]
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "<b>Gemini AI Analysis</b>",
                styles["Heading1"]
            )
        )

        story.append(Spacer(1, 10))

        for line in ai_analysis.split("\n"):

            story.append(
                Paragraph(
                    line,
                    styles["BodyText"]
                )
            )

        doc.build(story)