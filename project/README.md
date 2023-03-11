# Individual Student Grades PDF Generator
Video Demo: [Youtube Link](https://youtu.be/cxnahe5X-yQ)

Download the Table Template: [Google Sheets URL](https://docs.google.com/spreadsheets/d/1ZNHzzuIZk_z7boio0fNZJrB0_DonN-RBu6migezPReQ/edit#gid=761350059)
### Description:
For my CS50P Final Project, I made a program that outputs the grades of each course participant in a single-paged pdf table.
As a teacher, I needed a way to give students their semester grades but didn't want to manually create a document for each individual student.

In order for this program to work, information must be inputted into the template found at the Google Docs URL.
The easiest would be to, while logged into your Google Account, make a copy of the Google Sheets to your own Google Sheets library. From there, after the relevant edits are made, one should download the Google Sheets as a .csv file and place it in the same folder that project.py is found.


The table can be generated using the following command line argument:
#
    python project.py [template.csv]

Currently, this project only supports English characters using Helvetica as the font. There were issues importing UTF-8 compatible fonts using the CS50 Codespace but if you are planning to this program locally, add the following line of code and replace instances of 'helvetica' with the relevant UTF-8 compatible font:
#
    pdf.add_font('[font name]', '', '[.ttf file]', uni=True)

**Note:** This program may break if trying to convert a very large number of assignments into a table. To my knowledge it will support around 30 assignments/assessments.