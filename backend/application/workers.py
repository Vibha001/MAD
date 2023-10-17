from celery import Celery
from datetime import datetime
from celery.schedules import crontab
from application.sessions import ThDetails
# from flask_mail import Message,Mail
from flask import current_app  # Import current_app from Flask
from datetime import datetime, timedelta,date
from application.models import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



celery = Celery(
    "Application Jobs",
    broker="redis://127.0.0.1:6379/1",
    backend="redis://127.0.0.1:6379/2",
    enable_utc=False,
    timezone="Asia/Calcutta",
)
celery.conf.broker_connection_retry_on_startup = True



class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with current_app.app_context():
            return self.run(*args, **kwargs)


@celery.task()
def add_together(a, b):
    return a + b


@celery.task()
def say_hello(name):
    print("INSIDE TASK")
    print("HELLO", name)
    return "HELLO VIBHA"


@celery.task()
def Curr_time():
    print("START")
    now = datetime.now()
    print("now = ", now)
    dtstr = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time = ", dtstr)
    print("COMPLETE ")
    return dtstr


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, rem_email.s(), name="Every day")#
    sender.add_periodic_task(crontab(day_of_month=1, hour=0, minute=0), send_monthly_progress_reports.s(), name="Monthly Progress Report")


@celery.task()
def generate_th_csv(vid):
    show_data = ThDetails(vid)
    fields = [
        "show_id",
        "show_name",
        "ratings",
        "show_tags",
        "ticket_price",
        "timings",
        "seats",
        "booked",
    ]
    f = ["sid", "sname", "srate", "stags", "sprice", "time", "seats", "booked"]
    csv_file_path = f"static/th_data_{vid}.csv"
    with open(csv_file_path, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        for row in show_data:
            csvwriter.writerow([row[field] for field in f])
    return "csv created... "


@celery.task()
def rem_email():
    res = send_remainder_emails()
    if res:
        return "Reminder Sent successfully"
    else:
        return "Failed to send reminder"

def send_remainder_emails():
    try:
        # Get the users not logged in
        time_threshold = datetime.utcnow() - timedelta(hours=24)
        inactive_users = (
            User.query.join(RolesUsers)
            .filter(RolesUsers.role_id == 2)
            .filter(User.last_active <= time_threshold)
            .all()
        )

        # Set the message to send
        message = ""
        if len(inactive_users) == 0:
            message = "There are inactive mails to be sent"
        else:
            message = "You have not logged in the past 24hrs.. login to find out the latest shows available in your location."

        # Send the email to users
        for user in inactive_users:
            # send_email(recipients=[user.email],subject="Login Notification",body=message,)
            result = send_email.apply_async(args=["Login Notification - TicketShow", [user.email], message])


        return True
    except Exception as e:
        print(e)
        return False

@celery.task()
def send_email(subject, recipients, body, is_html=False):
    try:
        # Set up the SMTP server and login
        smtp_server = current_app.config["MAIL_SERVER"]
        smtp_port = current_app.config["MAIL_PORT"]
        smtp_username = current_app.config["MAIL_USERNAME"]
        smtp_password = current_app.config["MAIL_PASSWORD"]

        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(smtp_username, smtp_password)

        # Create the email message
        msg = MIMEMultipart()
        msg["From"] = smtp_username
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = subject
        if is_html:
            # If it's an HTML email, set the MIME type to HTML
            msg.attach(MIMEText(body, "html"))
        else:
            # If it's not HTML, set the MIME type to plain text
            msg.attach(MIMEText(body, "plain"))


        # Send the email
        server.sendmail(smtp_username, recipients, msg.as_string())
        server.quit()

        return "Email sent successfully!"
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return f"Failed to send email: {str(e)}"

@celery.task()
def send_monthly_progress_reports():
    try:
        # Get all users with role_id 2 (adjust this query based on your database structure)
        users = User.query.join(RolesUsers).filter(RolesUsers.role_id == 2).all()

        if not users:
            return "No users with role_id 2 found."

        for user in users:
            # Get the user's bookings for the previous month
            # print(user.email)
            user_bookings = get_user_bookings_for_previous_month(user.id)

            # if not user_bookings:
            #     continue

            # Generate the progress report HTML content (customize this part as needed)
            # print(user.email)
            report_content = f"<h1>Monthly Progress Report for User {user.username}</h1>"
            report_content += "<h2>Bookings for the Previous Month:</h2>"
            report_content += "<ul>"
            for booking in user_bookings:
                booking_date_str = booking['Date']
                booking_date = datetime.strptime(booking_date_str, '%Y-%m-%d %H:%M:%S')
                report_content += f"<li>Booking ID: {booking['BookingID']}, Tickets: {booking['Tickets']}, Date: {booking_date.strftime('%Y-%m-%d %H:%M:%S')},Show Name: {booking['ShowName']}, Show Ratings: {booking['ShowRatings']}, Venue: {booking['VenueName']}</li>"
            report_content += "</ul>"

            # Send the progress report via email
            subject = "Monthly Progress Report"
            recipients = [user.email]
            send_email(subject, recipients, report_content,is_html=True)

        return "Monthly progress reports sent successfully."
    except Exception as e:
        print(e)
        return f"Failed to send the monthly progress reports: {str(e)}"

def get_user_bookings_for_previous_month(user_id):
    try:
        # Calculate the first day of the current month
        today = date.today()
        first_day_of_current_month = today.replace(day=1)

        # Calculate the first day of the previous month
        first_day_of_previous_month = first_day_of_current_month.replace(month=first_day_of_current_month.month - 1)

        # Calculate the last day of the previous month
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)

        # Query the bookings for the previous month
        user_bookings = Booking.query.filter(
            Booking.uid == user_id,
            Booking.date >= first_day_of_previous_month,
            Booking.date <= last_day_of_previous_month
        ).all()

        # Prepare a list to store the formatted booking details
        formatted_bookings = []

        for booking in user_bookings:
            show = Show.query.get(booking.sid)
            venue = Venue.query.get(booking.vid)

            booking_details = {
                "BookingID": booking.id,
                "Tickets": booking.tickets,
                "Date": booking.date.strftime('%Y-%m-%d %H:%M:%S'),
                "ShowName": show.sname if show else "N/A",
                "ShowRatings": show.srate if show else "N/A",
                "VenueName": venue.vname if venue else "N/A"
            }

            formatted_bookings.append(booking_details)


        return formatted_bookings

    except Exception as e:
        print(e)
        return []

