import streamlit as st

st.set_page_config(page_title="Generate your Email!!",page_icon=":📬:")


import streamlit as st

def main():
    st.title("Email Generator")
    
    # User input for sender's name
    sender_name = st.text_input("Sender's Name")
    
    # User input for recipient's name
    recipient_name = st.text_input("Recipient's Name")
    
    # User input for email subject/topic
    subject = st.text_input("Subject/Topic")
    
    # User input for email tone with dropdown
    tone_options = ['Formal', 'Casual', 'Friendly']
    tone = st.selectbox("Tone", tone_options)
    
    # User input for attachments
    attachments = st.file_uploader("Attachments", type=["pdf", "txt", "docx"], accept_multiple_files=True)
    
    # Create Email button
    if st.button("Create Email"):
        email_content = generate_email(sender_name, recipient_name, subject, tone, attachments)
        st.write("## Email Preview")
        st.write(email_content)

def generate_email(sender_name, recipient_name, subject, tone, attachments):
    # Generate the email content based on user inputs
    email_template = f"Dear {recipient_name},\n\n"
    
    if tone == 'Formal':
        email_template += "I hope this email finds you well. "
    elif tone == 'Casual':
        email_template += "Hey there, hope you're doing great! "
    else:
        email_template += "Hi, just wanted to drop you a quick note. "
    
    email_template += f"I wanted to discuss the topic of '{subject}'. "
    email_template += "Please find the attached files for your reference.\n\n"
    
    email_template += f"Best regards,\n{sender_name}"
    
    return email_template

if __name__ == "__main__":
    main()
