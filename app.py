import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(page_title="Apex Strategy Engine", page_icon="📈")
st.title("Apex Strategy Engine")

api_key = st.text_input("Enter Groq API Key", type="password")

if api_key:
    client = Groq(api_key=api_key)

    # UPDATED SYSTEM PROMPT: Constraint-First Approach
    refined_system_prompt = """
    You are an Elite Global Strategy Consultant. Your primary goal is to provide realistic, 
    actionable advice based on the user's specific constraints (Budget, Users, Time).
    
    CRITICAL RULES:
    1. CONSTRAINT-FIRST: Before suggesting any strategy, analyze the user's current resources. 
       If the user has 'zero budget', do NOT suggest paid marketing, events, or hiring. 
       Focus exclusively on organic, high-leverage, and grassroots growth tactics.
    2. PYRAMID PRINCIPLE: Start with the Executive Recommendation.
    3. REALISM: If a user asks for a billion-dollar goal with zero resources, explicitly state 
       why this is currently impossible and provide a 'Path to First 10 Customers' instead.
    4. MECE FRAMEWORK: Ensure analysis is Mutually Exclusive and Collectively Exhaustive.
    5. DATA-FIRST: If the user provides vague info, ask specific diagnostic questions about 
       their product-market fit before giving a strategy.
    6. NO FLUFF: Be direct, analytical, and professional.
    """

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": refined_system_prompt}]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Define your objective (e.g., 'I have no budget, how to get first users?'):"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing constraints and formulating strategy..."):
                try:
                    # Model remains 70b for high reasoning, fallback to 8b
                    response = client.chat.completions.create(
                        messages=st.session_state.messages,
                        model="llama-3.1-70b-versatile",
                        temperature=0.2 # Lowered further to stick strictly to constraints
                    )
                    content = response.choices[0].message.content
                    st.markdown(content)
                    st.session_state.messages.append({"role": "assistant", "content": content})
                except Exception:
                    response = client.chat.completions.create(
                        messages=st.session_state.messages,
                        model="llama-3.1-8b-instant",
                        temperature=0.2
                    )
                    content = response.choices[0].message.content
                    st.markdown(content)
                    st.session_state.messages.append({"role": "assistant", "content": content})
