import argparse, csv, math, sys
from fpdf import FPDF


class PDF_Data:
    def __init__(self, csv_filepath):
        rows = []
        with open(csv_filepath, encoding="utf8") as csv_data:
            for row in csv.reader(csv_data):
                rows.append(row)
        self.data = rows
        self.headings = self.data[0][0:9]  # pdf document headings

class Table_Data(PDF_Data):
    def __init__(self, csv_filepath):
        super().__init__(csv_filepath)
        self.dates = self.data[2][1:]  # row 3 of csv file
        self.assignments = self.data[3][1:]  # row 4 of .csv file
        self.max_points = self.data[4][1:]  #
        self.students = self.data[5:]
        self.max_cols = math.floor(len(self.dates)/2)

class Cell_Data:
    def _init__(self):
        self.w = 0
        self.h = 0


def main():
    if len(sys.argv) != 2:
        csv = accept_csv(input('Enter template.csv filepath: '))
    else:
        csv = accept_csv()
    pdf = FPDF(orientation="L", format="A4")
    pdf_data, table, cell = PDF_Data(csv), Table_Data(csv), Cell_Data()
    cell.w, cell.h = (pdf.epw/table.max_cols), (pdf.font_size * 2.5)  # defining dimensions of one cell in PDF
    for student in table.students:
        origin = set_page_headers(student, pdf_data.headings, cell, pdf)
        set_table_row(table.dates, table, cell, pdf, origin, 1)
        set_table_row(table.assignments, table, cell, pdf, origin, 2)
        set_table_row(table.max_points, table, cell, pdf, origin, 3)
        set_table_row(student, table, cell, pdf, origin, 4)
    pdf.output("grades.pdf")


def accept_csv(file=None):
    parser = argparse.ArgumentParser(description="Convert csv grades to pdf")
    parser.add_argument("filepath", help="filepath of csv")
    args = parser.parse_args()
    if file != None:
        args.filepath = file
    if args.filepath[-4:] != '.csv':
        raise AttributeError('File provided was not .csv')
    return args.filepath


def set_page_headers(student, pdf_headings, cell, pdf):
        header_w = pdf.epw/6
        pdf.add_page()
        pdf.set_font("helvetica", size=14)
        header_ratio = [1, 2, 0.25, 0.5, 0.75, 1.75]
        i = 0
        for header in pdf_headings[:6]:
            if i == 3:
                pdf.multi_cell(header_w * header_ratio[i], cell.h, str(student[0]), border="B", align="L",
                        new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size)
            elif i == 5:
                pdf.multi_cell(header_w * header_ratio[i], cell.h, str(student[1]), border="B", align="L",
                        new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size)
            else:
                pdf.multi_cell(header_w * header_ratio[i], cell.h, str(header), border="B", align="L",
                        new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size)
            i += 1
        pdf.ln(cell.h)
        pdf.cell(pdf.epw, cell.h, f'{pdf_headings[6]} {pdf_headings[7]}')
        pdf.cell(0, 15, new_x="LMARGIN", new_y="NEXT")
        return pdf.y


def set_table_row(data, table, cell, pdf, y_position, row_num):
    counter = 0
    pdf.y = y_position + cell.h * (row_num - 1)
    pdf.set_font("helvetica", "B", size=8)
    if row_num == 4:  # special case for score row
        data = data[2:]
        pdf.multi_cell(cell.w, cell.h, 'Score:', 1, align="C", new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size*2)
        for item in data:
            if counter == table.max_cols - 1:
                pdf.cell(0,cell.h*5, new_x="LMARGIN", new_y="NEXT")
                pdf.cell(cell.w, cell.h, 'Score:', 1, align="C")
                pdf.multi_cell(cell.w, cell.h, item, 1, align="C", new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size*2)
                counter += 2
            elif counter == (table.max_cols * 2) - 1:
                pdf.cell(0,cell.h*5, new_x="LMARGIN", new_y="NEXT")
                pdf.cell(cell.w, cell.h, 'Score:', 1, align="C")
                pdf.multi_cell(cell.w, cell.h, item, 1, align="C", new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size*2)
                counter = 2
            else:
                pdf.multi_cell(cell.w, cell.h, item, 1, align="C", new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size*2)
                counter += 1
        pdf.ln()

    else:  # all other rows
        for item in data:
            if counter == table.max_cols:
                pdf.cell(0,cell.h*5, new_x="LMARGIN", new_y="NEXT")
                pdf.multi_cell(cell.w, cell.h, data[0], 1, align="C", new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size*2)
                pdf.multi_cell(cell.w, cell.h, item, 1, align="C", new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size*2)
                counter += 2
            elif (table.max_cols * 2) == counter:
                pdf.cell(0,cell.h*5, new_x="LMARGIN", new_y="NEXT")
                pdf.multi_cell(cell.w, cell.h, data[0], 1, align="C", new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size*2)
                pdf.multi_cell(cell.w, cell.h, item, 1, align="C", new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size*2)
                counter = 2
            else:
                pdf.multi_cell(cell.w, cell.h, item, 1, align="C", new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size*2)
                counter += 1
        pdf.ln()


if __name__ == "__main__":
    main()