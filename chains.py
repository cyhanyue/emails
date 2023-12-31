from typing import Optional

import openai
from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage

from prompts import system_prompt, user_information

def get_email_langchain_normal_prompts(
        founder_names: str,
        company_name: str,
        openai_api_key: str,
        model: str,
        areas: str,
        deck: Optional[str] = None,
        company_description: Optional[str] = None
) -> str:
    llm = ChatOpenAI(
        model=model,
        temperature=0.2,
        openai_api_key=openai_api_key
    )
        
    prompt = system_prompt + "\n---\n" + user_information + "\n---\nPass Email:"
    prompt_template = PromptTemplate.from_template(prompt)
        
    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt_template
    )

    deck = deck if deck is not None else "None"
    company_description = company_description if company_description is not None else "None"
        
    args = {
        "founder_names": founder_names,
        "deck": deck,
        "company_name": company_name,
        "areas": areas,
        "company_description": company_description
    }

    return llm_chain.run(args)
