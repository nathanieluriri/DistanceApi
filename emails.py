# SMTP server details
from fastapi import HTTPException
import yagmail

smtp_user = 'admin@247doordelivery.co.uk'
smtp_password = 'Password10!'
smtp_host = 'smtp.hostinger.com'
smtp_port = 465

# Function to send a simple payment complete emailSure! Here are all the email templates for "247 Door Delivery" in one place for easy copying:


def send_payment_complete_email(customer_email):
    email_subject = 'Payment Completed Successfully! 💰'
    email_body = """
    <html>
    <body>
        <h2>Payment Completed Successfully</h2>
        <p>Dear Customer,</p>
        <p>We are pleased to inform you that your payment has been completed successfully.</p>
        <p>Thank you for your business!</p>
        <p>Best regards,<br>247 Door Delivery</p>
    </body>
    </html>
    """
    
    try:
        with yagmail.SMTP(smtp_user, smtp_password, host=smtp_host, port=smtp_port) as yag:
            yag.send(to=customer_email, subject=email_subject, contents=email_body)
            print(f"Email sent to {customer_email} successfully!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

def send_payment_canceled_email(customer_email):
    email_subject = 'Payment Canceled Successfully! 💰'
    email_body = """
    <html>
    <body>
        <h2>Payment Canceled</h2>
        <p>Dear Customer,</p>
        <p>This is to inform you that your payment to 247 Door Delivery has been canceled successfully.</p>
        <p>A refund will be processed shortly.</p>
        <p>Thank you for your understanding.</p>
        <p>Best regards,<br>247 Door Delivery</p>
    </body>
    </html>
    """
    
    try:
        with yagmail.SMTP(smtp_user, smtp_password, host=smtp_host, port=smtp_port) as yag:
            yag.send(to=customer_email, subject=email_subject, contents=email_body)
            print(f"Email sent to {customer_email} successfully!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

def send_payment_delay_email_deliver(customer_email):
    email_subject = 'Delivery Update: Slight Delay'
    email_body = """
    <html>
    <body>
        <h2>Update on Your Delivery</h2>
        <p>Dear Customer,</p>
        <p>We wanted to inform you that there is a slight delay in the delivery of your package.</p>
        <p>Rest assured, your package is safe with us and will be delivered to you soon.</p>
        <p>Thank you for your patience!</p>
        <p>Best regards,<br>247 Door Delivery</p>
    </body>
    </html>
    """
    
    try:
        with yagmail.SMTP(smtp_user, smtp_password, host=smtp_host, port=smtp_port) as yag:
            yag.send(to=customer_email, subject=email_subject, contents=email_body)
            print(f"Email sent to {customer_email} successfully!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")


def send_payment_delay_email_pickUp(customer_email):
    email_subject = 'Notice: Delay in Order Pickup'
    email_body = """
    <html>
    <body>
        <h2>Delay in Order Pickup</h2>
        <p>Dear Customer,</p>
        <p>We wanted to inform you that there is a slight delay in the pickup of your order.</p>
        <p>Rest assured, we will be picking up your order soon.</p>
        <p>Thank you for your understanding!</p>
        <p>Best regards,<br>247 Door Delivery</p>
    </body>
    </html>
    """
    
    try:
        with yagmail.SMTP(smtp_user, smtp_password, host=smtp_host, port=smtp_port) as yag:
            yag.send(to=customer_email, subject=email_subject, contents=email_body)
            print(f"Email sent to {customer_email} successfully!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

def send_email_to_notify_customer_that_the_item_has_been_picked_up(customer_email):
    email_subject = 'Your Item has been Picked Up! 📦'
    email_body = """
    <html>
    <body>
        <h2>Your Item has been Picked Up</h2>
        <p>Dear Customer,</p>
        <p>We are pleased to inform you that your item has been successfully picked up.</p>
        <p>Thank you for choosing 247 Door Delivery!</p>
        <p>Best regards,<br>247 Door Delivery</p>
    </body>
    </html>
    """
    
    try:
        with yagmail.SMTP(smtp_user, smtp_password, host=smtp_host, port=smtp_port) as yag:
            yag.send(to=customer_email, subject=email_subject, contents=email_body)
            print(f"Email sent to {customer_email} successfully!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

def send_email_to_notify_customer_that_the_item_has_been_delivered(customer_email):
    email_subject = 'Your Item has been Delivered! 🎉'
    email_body = """
    <html>
    <body>
        <h2>Your Item has been Delivered</h2>
        <p>Dear Customer,</p>
        <p>We are excited to let you know that your item has been successfully delivered!</p>
        <p>Thank you for choosing 247 Door Delivery!</p>
        <p>Best regards,<br>247 Door Delivery</p>
    </body>
    </html>
    """
    
    try:
        with yagmail.SMTP(smtp_user, smtp_password, host=smtp_host, port=smtp_port) as yag:
            yag.send(to=customer_email, subject=email_subject, contents=email_body)
            print(f"Email sent to {customer_email} successfully!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
