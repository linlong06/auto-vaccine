# Vaccine Hunter

The purpose of this application is to help people search for COVID vaccine availability automatically. The sample script works for appointments tracking from CVS.

To run the script properly, please follow the following steps:
1) Clone the script to your local repository, and you need to have python installed.
2) Install packages including Selenium, Twilio API, and schedule.
3) Set up an account in Twilio and buy a phone number, and set the environment variables according to instructions below. 
4) Run the main application (app.py) with your preferred schedule intervals if everything is all set.

Environmente Variables:
TWILIO_ACCOUNT_SID: SID of your Twilio account.
TWILIO_AUTH_TOKEN: Token of your Twilio account.
CHROME_DRIVER_PATH: The path to the installed Chrome driver in your machine (need to make sure it is the same version as your Chrome browser).
DOB: Date of Birth to be input to CVS appointment website.
TWILIO_PHONE_NUMBER: The phone number bought from Twilio, from which the alert messages are sending from.
PERSONAL_PHONE_NUMBER: The personal phone number that alert messages are sending to.
