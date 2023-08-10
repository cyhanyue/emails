import os

import streamlit as st
from dotenv import load_dotenv

from chains import get_email_langchain_normal_prompts
from utils import write_string_to_word
from utils import read_pdf

load_dotenv()

chat_model_dict = {
    'LangChain Prompt Template': get_email_langchain_normal_prompts 
}

def build_streamlit_app():
    # Set the title of the Streamlit app to 'Pass Email Generator'
    st.title('Outreach Email Generator')

    # Create an input box in the sidebar of the app for the OpenAI API key
    openai_api_key = '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' 
    # openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key is None:
        openai_api_key = st.sidebar.text_input('OpenAI API Key', 'visit )

    pass_email_type = st.sidebar.selectbox(
        'Select the outreach email generation method',
        tuple(chat_model_dict.keys())
    )

    model = 'gpt-3.5-turbo'
        
    # Create a text input area for founder names
    founder_names = st.text_area('Paste the founder names here')

    # Create a text input area for pasting the company description
    company_name = st.text_area('Paste the company name here')

    # Create a text input area for selectiong an area of expertise
    areas = st.selectbox(
        'Select the industry the company fall into',
        (
            'eCommerce',
            'Fintech',
            'SaaS',
            'Digital Health',
            'Health and Wellness',
            'GSB'
        )
    )

    # Create a file uploader widget for uploading a pdf file (the user's resume)
    deck = st.file_uploader("Upload Pitch Deck", type='pdf')
    deck_text = None

    # If a deck has been uploaded, read the text from the pdf file
    if deck is not None:
        deck_text = read_pdf(deck)

   # create a text input area for pasting a company website
    company_description =st.text_area('Enter brief company description')

    # if a company description is provided, use it
    if company_description is not None:
        company_description = company_description

    # Create a button for generating the cover letter
    if st.button('Generate Email'):
        # Check if the OpenAI key, resume, and company description are provided
        if not openai_api_key or not openai_api_key.startswith('sk-'):
            # Display a warning if the OpenAI API key is not provided or is invalid
            st.warning('Please enter your OpenAI API key!', icon='⚠️')
        elif not company_name:
            # Display a warning if the company name is not provided
            st.warning('Please enter the company name!', icon='⚠️')
        else:
            # If all conditions are met, call the pass email generation function
            # Show a spinner while the function is running
            with st.spinner('Generating your email...'):
                result = chat_model_dict[pass_email_type](
                    founder_names = founder_names,
                    deck=deck_text,
                    company_name=company_name,
                    areas=areas,
                    company_description = company_description,
                    openai_api_key=openai_api_key,
                    model=model
                )
            # Display a success message when the pass email generation is completed
            st.success('Email generation completed!')

            # Write the generated pass email to the app
            st.write('**Your Generated Email:**')
            st.write(result)
            # Create a Word document
            write_string_to_word(result, filename="outreach_email.docx")

            # Create a download button for the cover letter document
            with open("outreach_email.docx", "rb") as file:
                btn = st.download_button(
                    "Download Email",
                    file,
                    file_name="Email.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )

if __name__ == '__main__':
    build_streamlit_app()
