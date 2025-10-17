#!/usr/bin/env python3
"""
Detailed Caregiver Agreement Document Processor
Creates a more detailed .docx file with all specific information from the images
"""

from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.shared import OxmlElement, qn
import os

def create_detailed_caregiver_agreement():
    """Create a detailed .docx file from the caregiver agreement text"""
    
    # Create a new Document
    doc = Document()
    
    # Set document margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
    
    # Title
    title = doc.add_heading('CAREGIVER AGREEMENT', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Add a line break
    doc.add_paragraph()
    
    # Page 1 Content
    doc.add_heading('I. The Parties', level=1)
    p1 = doc.add_paragraph()
    p1.add_run('This Caregiver Services Agreement, becomes effective immediately September 2, 2025 made by and between:')
    
    doc.add_paragraph()
    doc.add_paragraph('Family Representative(s):')
    doc.add_paragraph('address of _________________________')
    doc.add_paragraph('AND')
    doc.add_paragraph('with a mailing _________________________')
    doc.add_paragraph('City of Jacksonville, State of Florida,')
    
    doc.add_paragraph()
    doc.add_paragraph('Caregiver Provider: Cynthia Garcia, with a mailing address of 168 Asbury Hill Court, City of Jacksonville, State of Florida.')
    
    doc.add_paragraph()
    p2 = doc.add_paragraph()
    p2.add_run('Caregiver Provider and Family Representative(s) are each referred to herein as a "Party" and, collectively, as the "Parties."')
    
    doc.add_paragraph()
    p3 = doc.add_paragraph()
    p3.add_run('NOW, THEREFORE, FOR AND IN CONSIDERATION of the mutual promises and agreements contained herein, the hires the Child Care Provider to work under the terms and conditions hereby agreed upon by the Parties:')
    
    # Page 2 Content
    doc.add_heading('II. The Care Recipient(s)', level=1)
    p4 = doc.add_paragraph()
    p4.add_run('This Agreement shall only be for the following senior(s) named below:')
    
    # Table for care recipients
    table = doc.add_table(rows=4, cols=2)
    table.style = 'Table Grid'
    
    # Header row
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = "Senior's Name"
    hdr_cells[1].text = "Date of Birth"
    
    # Empty rows for filling
    for i in range(1, 4):
        row_cells = table.rows[i].cells
        row_cells[0].text = "_________________________"
        row_cells[1].text = "_________________________"
    
    doc.add_paragraph()
    p5 = doc.add_paragraph()
    p5.add_run('Hereinafter known as the "Care Recipient(s)".')
    
    # Page 3 Content
    doc.add_heading('III. Term/Termination', level=1)
    p6 = doc.add_paragraph()
    p6.add_run('The term of this Agreement shall commence on September 02, 2025 and terminate: (check one)')
    
    doc.add_paragraph()
    doc.add_paragraph('☑ At-Will with written notification of at least 14 days\' notice.')
    doc.add_paragraph('☐ On the date of ______, 20___')
    
    doc.add_paragraph()
    p7 = doc.add_paragraph()
    p7.add_run('The first 14 Days will be regarded as a trial period, in which case either party may terminate the contract without notice. After the first 14 Days of enrollment, a 14 Day written notice from parent or provider is required to terminate the contract, with the exception of gross misconduct on part of the provider, family representative, or care recipient. This is grounds for immediate discontinuation of service. In cases of non-payment, legal action may be taken, and the family representative(s) will pay all legal fees incurred.')
    
    # Page 4 Content
    doc.add_heading('IV. Caregiver Services', level=1)
    p8 = doc.add_paragraph()
    p8.add_run('The daily care services provided include:')
    
    services = [
        'Friendly conversation and emotional support',
        'Accompaniment on walks, errands, or appointments',
        'Light household tasks (tidying, light laundry, meal prep)',
        'Reading, games, hobbies, and social engagement',
        'Assistance with reminders (medication, appointments)',
        'Other: _________________________'
    ]
    
    for service in services:
        doc.add_paragraph(f'• {service}', style='List Bullet')
    
    doc.add_paragraph()
    p9 = doc.add_paragraph()
    p9.add_run('Note: This is a non-medical service and does not include medical care, personal hygiene assistance, or lifting. The services are "Hereinafter known as the \'Caregiver Services\'".')
    
    # Page 5 Content
    doc.add_heading('V. Schedule', level=1)
    p10 = doc.add_paragraph()
    p10.add_run('The weekly schedule for services:')
    
    # Schedule table
    schedule_table = doc.add_table(rows=6, cols=3)
    schedule_table.style = 'Table Grid'
    
    # Header row
    schedule_hdr = schedule_table.rows[0].cells
    schedule_hdr[0].text = "Days"
    schedule_hdr[1].text = "Start Time"
    schedule_hdr[2].text = "End Time"
    
    # Days of the week
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    for i, day in enumerate(days, 1):
        row_cells = schedule_table.rows[i].cells
        row_cells[0].text = f"☑ {day}"
        row_cells[1].text = "10:00 AM ☑"
        row_cells[2].text = "2:00 PM ☑"
    
    doc.add_paragraph()
    doc.add_heading('a.) Late Clock-in', level=2)
    doc.add_paragraph('Describes the procedure if the caregiver is late.')
    
    doc.add_heading('b.) Overtime Care (with approval)', level=2)
    doc.add_paragraph('Rate: $25 per hour')
    
    doc.add_heading('c.) Overtime Care (without approval)', level=2)
    doc.add_paragraph('Rate: $30 per hour')
    
    # Page 6 Content
    doc.add_heading('VI. Deposit', level=1)
    p11 = doc.add_paragraph()
    p11.add_run('Deposit requirements: (check one)')
    
    doc.add_paragraph()
    doc.add_paragraph('☐ Required to pay a deposit in the amount of $_________________________')
    doc.add_paragraph('☐ No deposit required')
    
    # Page 7 Content
    doc.add_heading('VII. Payment Amount', level=1)
    p12 = doc.add_paragraph()
    p12.add_run('Under this Agreement, the Caregiver Provider shall provide Services of $25.00 for each senior per hour. Hereinafter known as the "Payment Amount".')
    
    doc.add_heading('VIII. Payment Method', level=1)
    p13 = doc.add_paragraph()
    p13.add_run('The Payment Amount shall be paid: (check one)')
    
    payment_options = [
        'Daily',
        'Weekly',
        'Bi-Weekly', 
        'Monthly',
        'Other: _________________________'
    ]
    
    doc.add_paragraph()
    for i, option in enumerate(payment_options):
        if i == 1:  # Weekly is checked
            doc.add_paragraph(f'☑ {option}')
        else:
            doc.add_paragraph(f'☐ {option}')
    
    doc.add_paragraph()
    p14 = doc.add_paragraph()
    p14.add_run('Hereinafter known as the "Payment Method". The Payment Amount and Payment Method shall be referred to as "Compensation".')
    
    # Page 8 Content
    doc.add_heading('IX. Holidays/Vacation Times', level=1)
    p15 = doc.add_paragraph()
    p15.add_run('The Parties acknowledge and agree that the Caregiver Provider will not be available on the following national holidays: (check all that apply)')
    
    holidays = [
        "New Year's Eve/New Year's Day",
        "Martin Luther King Jr Day",
        "Memorial Day",
        "Good Friday",
        "Independence Day",
        "Labor Day",
        "Halloween Day (anytime after 3:30pm)",
        "Thanksgiving Day/Day after Thanksgiving",
        "Christmas Eve/Christmas Day"
    ]
    
    checked_holidays = [0, 7, 8]  # Indices of checked holidays
    
    doc.add_paragraph()
    for i, holiday in enumerate(holidays):
        if i in checked_holidays:
            doc.add_paragraph(f'☑ {holiday}')
        else:
            doc.add_paragraph(f'☐ {holiday}')
    
    doc.add_paragraph()
    doc.add_paragraph('The following vacation times shall be administered to each Party: (check all that apply):')
    
    doc.add_paragraph()
    doc.add_paragraph('☑ Client(s) Vacation. The Client(s) must provide at least 14 day(s) notice before their Senior(s) is on vacation. During the Client(s) vacation, the Family Representative(s) are not required to pay for Child Care Services during such vacation.')
    
    doc.add_paragraph()
    doc.add_paragraph('☑ Caregiver Provider Vacation. The Caregiver Provider must provide at least 14 day(s) notice before going on vacation.')
    
    # Page 9 Content
    doc.add_heading('X. Cancelling Scheduled Visit', level=1)
    p16 = doc.add_paragraph()
    p16.add_run('If any Family Representative(s) are to cancel, the Caregiver Provider requires that at least 7 day(s) notice be provided. If any Visit(s) are cancelled with proper notice, the Family Representative(s) shall be charged $0.00 for the cancelled day(s).')
    
    doc.add_paragraph()
    p17 = doc.add_paragraph()
    p17.add_run('If any Visit(s) are cancelled without proper notice, the Family Representative(s) shall be charged the full amount as if their Senior(s) were provided with the Caregiver Services for the cancelled period.')
    
    # Page 10 Content
    doc.add_heading('XI. Health Matters', level=1)
    p18 = doc.add_paragraph()
    p18.add_run('Inform caregivers of illness and detailed responsibilities for family representatives regarding backup care, refund policies, and conditions related to COVID-19 symptoms.')
    
    doc.add_heading('Note:', level=2)
    doc.add_paragraph('Responsibilities for family representatives regarding backup care, refund policies, and conditions related to COVID-19 symptoms.')
    
    doc.add_heading('XII. Governing Law', level=1)
    doc.add_paragraph('This agreement is governed by the laws of the State of Florida.')
    
    doc.add_heading('XIII. Severability', level=1)
    doc.add_paragraph('If any part of the agreement is found invalid, the rest remains in effect.')
    
    doc.add_heading('XIV. Additional Terms & Conditions', level=1)
    doc.add_paragraph('')  # Empty as shown in the document
    
    doc.add_heading('XVI. Entire Agreement', level=1)
    doc.add_paragraph('This document represents the complete agreement between the parties.')
    
    # Signature section
    doc.add_heading('SIGNATURES', level=1)
    
    doc.add_heading('Family Representative(s):', level=2)
    doc.add_paragraph('Signature: _________________________')
    doc.add_paragraph('Print Name: _________________________')
    doc.add_paragraph('Date: _________________________')
    
    doc.add_paragraph()
    doc.add_paragraph('Signature: _________________________')
    doc.add_paragraph('Print Name: _________________________')
    doc.add_paragraph('Date: _________________________')
    
    doc.add_paragraph()
    doc.add_heading('Child Care Provider\'s:', level=2)
    doc.add_paragraph('Signature: _________________________')
    doc.add_paragraph('Print Name: _________________________')
    doc.add_paragraph('Date: _________________________')
    
    return doc

def main():
    """Main function to create the detailed caregiver agreement document"""
    print("📄 Creating Detailed Caregiver Agreement Document...")
    
    try:
        # Create the document
        doc = create_detailed_caregiver_agreement()
        
        # Save the document
        output_file = "Caregiver_Agreement_Detailed.docx"
        doc.save(output_file)
        
        print(f"✅ Detailed document created successfully: {output_file}")
        print(f"📁 File saved in: {os.path.abspath(output_file)}")
        
        # Get file size
        file_size = os.path.getsize(output_file)
        print(f"📊 File size: {file_size:,} bytes")
        
    except Exception as e:
        print(f"❌ Error creating detailed document: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
