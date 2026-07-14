from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message

app = Flask(__name__)

# CORS — restrict to known origins
CORS(app, origins=[
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "https://libertybell-loans.com",
    "https://libertybellmortgage.netlify.app"
])

# EMAIL CONFIG — Gmail SMTP
# Step 1: Go to myaccount.google.com/apppasswords
# Step 2: Create an App Password for "Mail"
# Step 3: Replace the values below
app.config['MAIL_SERVER']        = 'smtp.gmail.com'
app.config['MAIL_PORT']          = 587
app.config['MAIL_USE_TLS']       = True
app.config['MAIL_USERNAME']      = 'your_gmail@gmail.com'    # replace
app.config['MAIL_PASSWORD']      = 'your_app_password_here'  # replace
app.config['MAIL_DEFAULT_SENDER'] = 'your_gmail@gmail.com'   # replace

mail = Mail(app)

# Loan officer email routing
LOAN_OFFICER_EMAILS = {
    'carol-nguyen':  'carol.nguyen@libertybell-loans.com',
    'lauren-ho':     'lauren.ho@libertybell-loans.com',
    'alexia-nguyen': 'alexia.nguyen@libertybell-loans.com',
    'assign':        'carol.nguyen@libertybell-loans.com'
}

@app.route('/api/apply', methods=['POST'])
def apply():
    data = request.get_json()

    print("New application received:")
    print(data)

    borrower = (data.get('first_name', '') + ' ' + data.get('last_name', '')).strip() or 'Unknown Borrower'
    lo_key   = data.get('loan_officer_key', 'assign')
    lo_email = LOAN_OFFICER_EMAILS.get(lo_key, LOAN_OFFICER_EMAILS['assign'])
    lo_name  = data.get('loan_officer', 'Your Loan Officer')

    try:
        # Email to loan officer
        officer_body = f"""
New loan application received from {borrower}.

LOAN DETAILS
------------
Loan Officer:   {lo_name}
Purpose:        {data.get('purpose', '-')}
Loan Program:   {data.get('loan_type', '-')}
Loan Term:      {data.get('loan_term', '-')}
Property Value: {data.get('property_value', '-')}
Down Payment:   {data.get('down_payment', '-')}
Loan Amount:    {data.get('loan_amount', '-')}
Property ZIP:   {data.get('property_zip', '-')}
Property Type:  {data.get('property_type', '-')}
Property Use:   {data.get('property_use', '-')}

BORROWER
--------
Name:           {borrower}
Email:          {data.get('email', '-')}
Phone:          {data.get('phone', '-')}
DOB:            {data.get('dob', '-')}
Address:        {data.get('address', '-')}
Co-Borrower:    {data.get('co_borrower', 'No')}
Co-Name:        {data.get('co_name', '-')}

EMPLOYMENT & FINANCES
---------------------
Employment:     {data.get('emp_status', '-')}
Employer:       {data.get('employer', '-')}
Job Title:      {data.get('job_title', '-')}
Monthly Income: {data.get('monthly_income', '-')}
Other Income:   {data.get('other_income', '-')}
Credit Score:   {data.get('credit_score', '-')}
Monthly Debts:  {data.get('monthly_debts', '-')}
Bank Assets:    {data.get('bank_assets', '-')}
Invest Assets:  {data.get('invest_assets', '-')}

NOTES
-----
{data.get('notes', 'None')}
        """.strip()

        mail.send(Message(
            subject=f"New Loan Application - {borrower}",
            recipients=[lo_email],
            body=officer_body
        ))
        print(f"Officer email sent to {lo_email}")

        # Confirmation email to borrower
        borrower_email = data.get('email', '')
        if borrower_email:
            confirm_body = f"""
Dear {borrower},

Thank you for submitting your loan application to Liberty Bell Mortgage.

Your loan officer will be in touch within one business day to discuss your options and next steps.

YOUR APPLICATION SUMMARY
------------------------
Purpose:        {data.get('purpose', '-')}
Loan Program:   {data.get('loan_type', '-')}
Loan Term:      {data.get('loan_term', '-')}
Property Value: {data.get('property_value', '-')}
Loan Amount:    {data.get('loan_amount', '-')}
Loan Officer:   {lo_name}

Questions? Contact us:
Phone:   (408) 373-6534
Email:   carol.nguyen@libertybell-loans.com
Address: 2670 S. White Road, Ste. 135, San Jose, CA 95148

Thank you for choosing Liberty Bell Mortgage.

The Liberty Bell Mortgage Team
NMLS #337503 | DRE #01848265 | Equal Housing Opportunity
            """.strip()

            mail.send(Message(
                subject="Your Liberty Bell Mortgage Application - Received",
                recipients=[borrower_email],
                body=confirm_body
            ))
            print(f"Confirmation sent to {borrower_email}")

    except Exception as e:
        print(f"Email error (will still save to DB): {e}")

    return jsonify({'status': 'received'})

if __name__ == '__main__':
    app.run(debug=True)