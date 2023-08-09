import os

import streamlit as st
from dotenv import load_dotenv

from chains import get_pass_email_langchain_normal_prompts
# , get_pass_email_langchain_chat_prompts, \
    # get_pass_email_langchain_no_chain, get_pass_email_no_langchain
from utils import read_docx, write_string_to_word

load_dotenv()

chat_model_dict = {
    'LangChain Prompt Template': get_pass_email_langchain_normal_prompts,
    # 'Langchain ChatPrompt Template': get_cover_letter_langchain_chat_prompts,
    # "Langchain no chain": get_cover_letter_langchain_no_chain,
    # 'Custom code': get_cover_letter_no_langchain
}

def build_streamlit_app():
    # Set the title of the Streamlit app to 'Pass Email Generator'
    st.title('Pass Email Generator')

    # Create an input box in the sidebar of the app for the OpenAI API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key is None:
        openai_api_key = st.sidebar.text_input('OpenAI API Key')

    pass_email_type = st.sidebar.selectbox(
        'Select the pass email generation method',
        tuple(chat_model_dict.keys())
    )

    model = 'gpt-3.5-turbo'
        
    # Create a text input area for founder names
    founder_names = st.text_area('Write founder names here')
    
    # Create a file uploader widget for uploading a pdf file (the user's resume)
    deck = st.file_uploader("Upload your Pitch Deck", type='pdf')
    deck_text = None

    # If a resume has been uploaded, read the text from the pdf file
    if deck is not None:
        deck_text = read_pdf(deck)

    # Create a text input area for pasting the company description
    company_description = st.text_area('Paste the company description here')

    # Create a text input area for pasting any additional company information
    concerns = st.text_area('Write your concerns here')

    # Create a button for generating the cover letter
    if st.button('Generate Pass Email'):
        # Check if the OpenAI key, resume, and company description are provided
        if not openai_api_key or not openai_api_key.startswith('sk-'):
            # Display a warning if the OpenAI API key is not provided or is invalid
            st.warning('Please enter your OpenAI API key!', icon='⚠️')
        elif deck is None:
            # Display a warning if the resume has not been uploaded
            st.warning('Please upload a deck!', icon='⚠️')
        elif not company_description:
            # Display a warning if the company description is not provided
            st.warning('Please enter the company description!', icon='⚠️')
        else:
            # If all conditions are met, call the pass email generation function
            # Show a spinner while the function is running
            with st.spinner('Generating your pass email...'):
                result = chat_model_dict[pass_email_type](
                    founder_names = founder_names,
                    deck=deck_text,
                    company_description=company_description,
                    concerns=concerns,
                    openai_api_key=openai_api_key,
                    model=model
                )
            # Display a success message when the pass email generation is completed
            st.success('Pass Email generation completed!')

            # Write the generated pass email to the app
            st.write('**Your Generated Pass Email:**')
            st.write(result)
            # Create a Word document
            write_string_to_word(result, filename="pass_email.docx")

            # Create a download button for the cover letter document
            with open("pass_email.docx", "rb") as file:
                btn = st.download_button(
                    "Download Pass Email",
                    file,
                    file_name="Pass_Email.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )

if __name__ == '__main__':
    build_streamlit_app()
