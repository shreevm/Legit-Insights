import streamlit as st

page_bg_img = '''
<style>

[data-testid="stSidebarContent"]{
    background: linear-gradient(0deg, #588EAD 0%, #151414 100%);   
    }
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

import streamlit as st
import smtplib
from email.message import EmailMessage

# Function to send email notification
def send_email_notification(email_address):
    EMAIL_HOST = ''  # e.g., 'smtp.gmail.com'
    EMAIL_PORT = 587  # For Gmail, use 587
    EMAIL_ADDRESS = ''  # Your email address
    EMAIL_PASSWORD = ''  # Your email password

    msg = EmailMessage()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email_address
    msg['Subject'] = 'Notification from Your Website'

    body = "Hello! This is a notification from your website."
    msg.set_content(body)

    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

def main():
    st.title("LEGIT Settings")

    # Notification Settings
    st.header("Notification Settings")
    notification_enabled = st.checkbox("Enable Notifications")

    if notification_enabled:
        email = st.text_input("Enter Email Address")

    # Email Notification Settings
    st.header("Email Notification Settings")
    email_notification_enabled = st.checkbox("Enable Email Notifications")

    if email_notification_enabled:
        email = st.text_input("Enter Email Address")

    # Subscription Payment Settings
    st.header("Subscription Payment")

    subscription_options = ["Basic", "Pro", "Premium"]
    subscription_type = st.selectbox("Select Subscription Plan", subscription_options)

    # Display subscription details based on selection
    if subscription_type == "Basic":
        price_per_month = "49₹"
        features = ["Basic features"]
    elif subscription_type == "Pro":
        price_per_month = "149₹"
        features = ["Pro features", "Advanced analytics"]
    elif subscription_type == "Premium":
        price_per_month = "999₹"
        features = ["Premium features", "Custom support"]

    st.write(f"Price per Month: {price_per_month}")
    st.write("Features:")
    for feature in features:
        st.write(f"- {feature}")

    # Save settings
    if st.button("Save Settings"):
        saved_notification_settings = {
            "notification_enabled": notification_enabled,
            "email_notification_enabled": email_notification_enabled,
            "subscription_type": subscription_type,
            "email_address": email if notification_enabled or email_notification_enabled else None
        }

        st.write("Settings saved successfully!")
        st.write(saved_notification_settings)

        # Send email notification if enabled
        if email_notification_enabled and email:
            if send_email_notification(email):
                st.success(f"Notification sent to {email}")
            else:
                st.error("Failed to send notification. Please check your email settings.")

if __name__ == "__main__":
    main()
