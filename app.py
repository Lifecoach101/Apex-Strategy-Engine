import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(page_title="Apex Strategy Engine", page_icon="📈")
st.title("Apex Strategy Engine")

api_key = st.text_input("Enter Groq API Key", type="password")

if api_key:
    client = Groq(api_key=api_key)

    refined_system_prompt = """
    You are an Elite Global Strategy Consultant. Your output must be indistinguishable from a top-tier consulting firm.
    
    RULES:
    1. PYRAMID PRINCIPLE: Start with the Executive Recommendation. Back it with 3 core pillars.
    2. REALISM: Never suggest unrealistic growth without a granular, multi-year plan. Pivot to a 'Viable Path to Market'.
    3. DATA-FIRST: If critical business metrics are missing (e.g., CAC, LTV), ask the user for them.
    4. NO FLUFF: Be specific, analytical, and actionable.
    5. MECE FRAMEWORK: Ensure analysis is Mutually Exclusive and Collectively Exhaustive.
    """

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": refined_system_prompt}]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Define your business challenge:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Synthesizing strategic roadmap..."):
                try:
                    # Try the high-intelligence model first
                    response = client.chat.completions.create(
                        messages=st.session_state.messages,
                        model="llama-3.1-70b-versatile",
                        temperature=0.3
                    )
                except Exception:
                    # Fallback to the faster, lighter model if 70B fails
                    response = client.chat.completions.create(
                        messages=st.session_state.messages,
                        model="llama-3.1-8b-instant",
                        temperature=0.3
                    )
                
                content = response.choices[0].message.content
                st.markdown(content)
                st.session_state.messages.append({"role": "assistant", "content": content})
