from openpyxl import Workbook


class ExcelExporter:

    def export(self, candidates, filename):

        wb = Workbook()
        ws = wb.active
        ws.title = "Candidates"

        ws.append([
            "ID",
            "Name",
            "Email",
            "Phone",
            "ATS Score",
            "Skills",
            "Resume"
        ])

        for row in candidates:
            ws.append(row)

        wb.save(filename)