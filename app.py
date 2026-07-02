import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(page_title="Apex Strategy Engine", page_icon="📈")
st.title("Apex Strategy Engine")

# API Key input
api_key = st.text_input("Enter Groq API Key", type="password")

if api_key:
    client = Groq(api_key=api_key)

    # Initialize chat history in session_state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": """
            You are an Elite Global Strategy Consultant. Follow these rules:
            1. THE PYRAMID PRINCIPLE: Start with the Executive Summary.
            2. MECE FRAMEWORK: Ensure analysis is Mutually Exclusive and Collectively Exhaustive.
            3. ECONOMIC LOGIC: Use Marginal Analysis and ROI.
            4. AGGRESSIVE SCALING: Focus on 10x growth.
            5. EXECUTION: Provide a 30-day "Critical Path" with KPIs.
            """}
        ]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Define your strategic objective or business challenge:"):
        # Add user message to state and display it
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("Synthesizing strategic roadmap..."):
                try:
                    stream = client.chat.completions.create(
                        messages=st.session_state.messages,
                        model="llama-3.1-8b-instant",
                    )
                    response = stream.choices[0].message.content
                    st.markdown(response)
                    # Add assistant response to state
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"An error occurred: {e}")
