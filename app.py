import streamlit as st
from langchain import PromptTemplate
from langchain.llms import Clarifai

st.set_page_config(page_title="Generate your Email!!",page_icon=":📬:")

def main():
    st.title("Email Generator")
    
    
    # User input for sender's name
    sender_name = st.text_input("Sender's Name", key="sender_name")
    
    # User input for recipient's name
    recipient_name = st.text_input("Recipient's Name", key="recipient_name")
    
    # User input for email subject/topic
    subject = st.text_input("Subject/Topic", key="subject")
    
    # User input for extra detail
    extra_detail = st.text_input("Extra Detail", key="extra_detail")
    
    # User input for email tone with dropdown
    tone_options = ['Formal', 'Casual', 'Friendly']
    tone = st.selectbox("Tone", tone_options, key="tone")
    
    # User input for preferred email length
    length_options = ['Short', 'Medium', 'Long']
    preferred_length = st.selectbox("Preferred Length", length_options, key="preferred_length")
    
    # User input for attachments
    attachments = st.file_uploader("Attachments", type=["pdf", "txt", "docx"], accept_multiple_files=True, key="attachments")
    
    # Create Email button
    if st.button("Create Email"):
        email_content = generate_email(sender_name, recipient_name, subject, extra_detail, tone, preferred_length, attachments)
        st.write("## Email Preview")
        st.write(email_content)


# function to generate email
def generate_email(sender_name, recipient_name, subject, extra_detail, tone, preferred_length, attachments):
    # Generate the email content based on user inputs
    # email_template = f"Dear {recipient_name},\n\n"
    
    # if tone == 'Formal':
    #     email_template += "I hope this email finds you well. "
    # elif tone == 'Casual':
    #     email_template += "Hey there, hope you're doing great! "
    # else:
    #     email_template += "Hi, just wanted to drop you a quick note. "
    
    # email_template += f"I wanted to discuss the topic of '{subject}'. "
    # email_template += "Please find the attached files for your reference.\n\n"
    
    # email_template += f"Best regards,\n{sender_name}"

    
    ######################################################################################################
    # In this section, we set the user authentication, user and app ID, model details, and the URL of 
    # the text we want as an input. Change these strings to run your own example.
    ######################################################################################################

    # Your PAT (Personal Access Token) can be found in the portal under Authentification
    PAT = '30cbbd7e47ba49c7a013f03c44f2b289'
    # Specify the correct user_id/app_id pairings
    # Since you're making inferences outside your app's scope
    USER_ID = 'meta'
    APP_ID = 'Llama-2'
    # Change these to whatever model and text URL you want to use
    MODEL_ID = 'llama2-13b-chat'
    MODEL_VERSION_ID = '79a1af31aa8249a99602fc05687e8f40'
    TEXT_FILE_URL = 'https://samples.clarifai.com/negative_sentence_12.txt'

    ############################################################################
    # YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE TO RUN THIS EXAMPLE
    ############################################################################

    from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
    from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
    from clarifai_grpc.grpc.api.status import status_code_pb2

    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (('authorization', 'Key ' + PAT),)

    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
            model_id=MODEL_ID,
            version_id=MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            url=TEXT_FILE_URL
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        raise Exception(f"Post model outputs failed, status: {post_model_outputs_response.status.description}")

    # Since we have one input, one output will exist here
    output = post_model_outputs_response.outputs[0]

    print("Completion:\n")
    print(output.data.text.raw)


    # template for building the prompt
    template = """Generate an email from {sender_name} to {recipient_name} with the following details:\nSubject: {subject}\nTone: {tone}. Consider the preferred length: {preferred_length} and details: {extra_detail}. 
    Write it as if you are the sender. Write it in proper format."""
    
    # if attachments:
    #     attachment_names = ", ".join([attachment.name for attachment in attachments])
    #     prompt += f"\nAttachments: {attachment_names}"

    # creating the final prompt
    prompt=PromptTemplate(
        input_variables=["sender_name","recipient_name","subject","tone","preferred_length","extra_detail"],
        template=template,)
    
    llm=Clarifai(pat='e620301e1ebe4aa5ba634bcc668f8274',user_id='meta',app_id='Llama-2',model_id='llama2-13b-chat')

    # generating response using LLM
    response=llm(prompt.format(subject=subject,sender_name=sender_name,recipient_name=recipient_name,tone=tone,preferred_length=preferred_length,extra_detail=extra_detail))
    print(response)

    return response
    
    # return email_template

if __name__ == "__main__":
    main()
