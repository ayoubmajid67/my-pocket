import os 
from dotenv import load_dotenv
import ssl 
import smtplib
from email.message import EmailMessage
import string
import random

# Load environment variables
load_dotenv()

def create_email_body(code, username='user'):

    body = f"""\
    <html>
    <head></head>
    <body>
        <p>Dear {username},</p>
        <p>Your authentication code is:</p>
        <h2 style="color: #d65f32; font-size: 20px;">{code}</h2>
        <p>Please use this code to complete your authentication process.</p>
        <p>If you didn't request this code, please ignore this email.</p>
        <br>
        <img  alt ='My pocket logo' src='https://instagram.frba2-1.fna.fbcdn.net/v/t51.2885-19/480122084_1620771322140371_7577125648193206911_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_ht=instagram.frba2-1.fna.fbcdn.net&_nc_cat=111&_nc_oc=Q6cZ2AETYOrUoC8l11J8K8wFF6wipueaCRqn2lO4MiganMpBe9MY09uiUlbQSZ_DRvG2rTI&_nc_ohc=fqYEFPBw4NAQ7kNvgGTw-y-&_nc_gid=ec51cb930e734116820311e45a9d2beb&edm=ALGbJPMBAAAA&ccb=7-5&oh=00_AYAyWSRDfY75oGt_-5wjgStbhGO8UCW1E8-PKnFg_6FlOQ&oe=67C572AD&_nc_sid=7d3ac5'   />
        <p> <strong>Best regards,</strong> <br> MyPocket Team</p>
    </body>
    </html>
    """
    return body

def create_review_notification_body(username='user'):
    body = f"""\
    <html>
    <head></head>
    <body>
        <p>Dear {username},</p>
        <p>Thank you for registering with MyPocket. Your account is currently under review by our team.</p>
        <p>We will complete the review process within the next 24 hours. Once the review is complete, you will receive an activation email to finalize your registration.</p>
        <p>Please be patient while we verify your information. If you have any questions, feel free to reach out to our support team.</p>
        <br>
        <img alt='MyPocket logo' src='https://instagram.frba2-1.fna.fbcdn.net/v/t51.2885-19/480122084_1620771322140371_7577125648193206911_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_ht=instagram.frba2-1.fna.fbcdn.net&_nc_cat=111&_nc_oc=Q6cZ2AETYOrUoC8l11J8K8wFF6wipueaCRqn2lO4MiganMpBe9MY09uiUlbQSZ_DRvG2rTI&_nc_ohc=fqYEFPBw4NAQ7kNvgGTw-y-&_nc_gid=ec51cb930e734116820311e45a9d2beb&edm=ALGbJPMBAAAA&ccb=7-5&oh=00_AYAyWSRDfY75oGt_-5wjgStbhGO8UCW1E8-PKnFg_6FlOQ&oe=67C572AD&_nc_sid=7d3ac5' />
        <p><strong>Best regards,</strong><br>MyPocket Team</p>
    </body>
    </html>
    """
    return body


def create_activation_notification_body(email, username='user', is_activated=True, login_url="https://example.com/login"):
    if is_activated:
        # Successful activation email body
        body = f"""\
        <html>
        <head></head>
        <body>
            <p>Dear {username},</p>
            <p>Congratulations! Your account has been successfully activated.</p>
            <p>You can now log in to your account using the button below:</p>
            <p><a href="{login_url}" style="background-color: #d65f32; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Join Us</a></p>
            <p>If you encounter any issues, please reply to this email or contact our support team.</p>
            <br>
            <img alt='MyPocket logo' src='https://instagram.frba2-1.fna.fbcdn.net/v/t51.2885-19/480122084_1620771322140371_7577125648193206911_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_ht=instagram.frba2-1.fna.fbcdn.net&_nc_cat=111&_nc_oc=Q6cZ2AETYOrUoC8l11J8K8wFF6wipueaCRqn2lO4MiganMpBe9MY09uiUlbQSZ_DRvG2rTI&_nc_ohc=fqYEFPBw4NAQ7kNvgGTw-y-&_nc_gid=ec51cb930e734116820311e45a9d2beb&edm=ALGbJPMBAAAA&ccb=7-5&oh=00_AYAyWSRDfY75oGt_-5wjgStbhGO8UCW1E8-PKnFg_6FlOQ&oe=67C572AD&_nc_sid=7d3ac5' />
            <p><strong>Best regards,</strong><br>MyPocket Team</p>
        </body>
        </html>
        """
    else:
        # Failed activation email body
        body = f"""\
        <html>
        <head></head>
        <body>
            <p>Dear {username},</p>
            <p>We regret to inform you that your account could not be activated at this time.</p>
            <p>This may have occurred due to an issue during the verification process. To reclaim your account, please follow the steps below:</p>
            <ol>
                <li>Ensure all required documents are correctly submitted.</li>
                <li>Contact our support team for assistance.</li>
            </ol>
            <p>If you believe this is a mistake, please reply to this email or contact us directly.</p>
            <br>
            <img alt='MyPocket logo' src='https://instagram.frba2-1.fna.fbcdn.net/v/t51.2885-19/480122084_1620771322140371_7577125648193206911_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_ht=instagram.frba2-1.fna.fbcdn.net&_nc_cat=111&_nc_oc=Q6cZ2AETYOrUoC8l11J8K8wFF6wipueaCRqn2lO4MiganMpBe9MY09uiUlbQSZ_DRvG2rTI&_nc_ohc=fqYEFPBw4NAQ7kNvgGTw-y-&_nc_gid=ec51cb930e734116820311e45a9d2beb&edm=ALGbJPMBAAAA&ccb=7-5&oh=00_AYAyWSRDfY75oGt_-5wjgStbhGO8UCW1E8-PKnFg_6FlOQ&oe=67C572AD&_nc_sid=7d3ac5' />
            <p><strong>Best regards,</strong><br>MyPocket Team</p>
        </body>
        </html>
        """

    return body


def send_email(email_receiver,body, subject="Authentication Code"):
    try:
        # Retrieve the app password from environment variables
        app_password = os.environ.get("email_password")
        email_sender="ayoubmajid71@gmail.com"

        # Create email message
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.add_alternative(body, subtype='html')

        # Establish SMTP connection and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, app_password)
            smtp.send_message(em)

        # print('Email sent successfully. Please check your inbox for the authentication code.')
        return True  # Email sent successfully
    except smtplib.SMTPRecipientsRefused:
        # Handle case where email address is not found
        return False  # Email address not found
    except Exception as e:
        # Handle other exceptions (e.g., SMTP server error)
        print(f"Error sending email: {e}")
        return False  # Error sending email


# Function to generate a random verification code consisting of numbers only
def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

if __name__ == "__main__":
    # Example usage
    email_sender = "ayoubmajid71@gmail.com"
    email_receiver = "mypocket.ma@gmail.com"
    code = generate_verification_code()
    print(send_email(email_sender, email_receiver, code))
    print(generate_verification_code())