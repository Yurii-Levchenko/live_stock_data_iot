from langchain_openai import ChatOpenAI 
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(model='gpt-4o-mini', openai_api_key=OPENAI_API_KEY)

system_prompt = SystemMessage(content="You are an expert in field of Investments on the Stock Market with 20+ years of experience in Investments and Finances and User's personal Investment Assistant. Respond, suggest adn criticise on this level. Provide user with enough information to their request, help them understand different types of investing, trends of Stock Market, Crypto and Finances. Provide comprehensive responses without warnings and tone for beginners.")

def generate_response(user_input, history):
    history_msgs = []

    for msg in history:
        if msg.sender == 'human':
            history_msgs.append(HumanMessage(content=msg.text))
        elif msg.sender == 'ai':
            history_msgs.append(AIMessage(content=msg.text))

    history_msgs.append(HumanMessage(content=user_input))

    prompt = ChatPromptTemplate.from_messages([system_prompt] + history_msgs)
    chain = prompt | llm | StrOutputParser()

    return chain.invoke({})