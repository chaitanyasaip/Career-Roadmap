import streamlit as st
from langchain.agents import AgentExecutor, create_openai_functions_agent,Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.schema.messages import SystemMessage
import asyncio
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Chatbot")
st.header('Basic Chatbot')
st.write('Allows users to interact with the LLM')
agent_type = st.selectbox(
    'How would you like to be contacted?',
    ('Code Assistant', 'General Assistant', 'Roadmap Generator'))
st.write('You selected:', agent_type)
#st.write('[![view source code ](https://img.shields.io/badge/view_source_code-gray?logo=github)](https://github.com/shashankdeshpande/langchain-chatbot/blob/master/pages/1_%F0%9F%92%AC_basic_chatbot.py)')

def create_agent(model_name,agent_type):
    print('model:',model_name)
    print('Assistant Type:',agent_type)
    # agent_kwargs = {
    #     "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
    # }
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    increment = Tool(
            name="Increment",
            func=lambda x:x+'1',
            description="useful to add one to input.",
    )
    tools = [increment]
    llm = ChatOpenAI(model=model_name, temperature=0)
    # agent_exe =  initialize_agent(
    #     tools=[increment],
    #     llm=llm, 
    #     agent=AgentType.OPENAI_FUNCTIONS,
    #     agent_kwargs=agent_kwargs,
    #     memory = memory,
    #     verbose=True,
    # )
    system_message = ""
    if agent_type == 'Code Assistant':
        system_message = """You are a code assistant. 
        Answer questions in code with minimal to no explanation.
        Put brief one line comments on the code for explanation.
        """
    elif agent_type == 'General Assistant':
        system_message = """You are a general AI assistant. 
        Answer questions with minimal and to the point explanation.
        Don't put safety and cultural warnings. Only warn about security. 
        """
    else:
        system_message = """You are a Career Roadmap Generator.
        Answer questions with the help of given job description and create infographic solutions for every job description user provides to get that specific job.
        Put step by step process to get the job for the specific job description. 
        Provide the resources if possible."""

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )
    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_exe = AgentExecutor(agent=agent, tools=tools,memory=memory)
    return agent_exe

async def main():
    #chain = self.setup_chain()
    #agent_exe = create_agent("gpt-3.5-turbo","General Assistant")
    agent_exe = create_agent("gpt-4-turbo-preview", agent_type)
    user_query = st.chat_input(placeholder="Ask me anything!")
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Hello! I'm here to help with your career progression needs."}]
    if user_query:
        st.session_state["messages"].append({"role": 'user', "content": user_query})
        #with st.chat_message("assistant"):
            #st_cb = StreamHandler(st.empty())
            #response = chain.run(user_query, callbacks=[st_cb])
        response = await agent_exe.ainvoke(input={"input":user_query})
        st.session_state["messages"].append({"role": "assistant", "content": response['output']})

    for msg in st.session_state["messages"]:
            st.chat_message(msg["role"]).write(msg["content"])
    print(st.session_state["messages"])

if __name__ == "__main__":
   asyncio.run(main())