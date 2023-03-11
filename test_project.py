import pytest
from fpdf import FPDF

from project import PDF_Data, Table_Data, Cell_Data, accept_csv, set_page_headers, set_table_row


def test_csv_input():
    assert accept_csv('template.csv') == 'template.csv'
    with pytest.raises(AttributeError):
        accept_csv()
        accept_csv('template.pdf')
        accept_csv('template.csvv')


def test_pdf_header_creation():
    csv = accept_csv('template.csv')
    pdf = FPDF(orientation="L", format="A4")
    pdf_data, table, cell = PDF_Data(csv), Table_Data(csv), Cell_Data()
    cell.w, cell.h = (pdf.epw/table.max_cols), (pdf.font_size * 2.5)
    set_page_headers(table.students[0], pdf_data.headings, cell, pdf)


def test_table_creation():
    csv = accept_csv('template.csv')
    pdf = FPDF(orientation="L", format="A4")
    pdf_data, table, cell = PDF_Data(csv), Table_Data(csv), Cell_Data()
    cell.w, cell.h = (pdf.epw/table.max_cols), (pdf.font_size * 2.5)

    for student in table.students:
        origin = set_page_headers(student, pdf_data.headings, cell, pdf)
        set_table_row(table.dates, table, cell, pdf, origin, 1)
        set_table_row(table.assignments, table, cell, pdf, origin, 2)
        set_table_row(table.max_points, table, cell, pdf, origin, 3)
        set_table_row(student, table, cell, pdf, origin, 4)

    pdf.output('grades.pdf')