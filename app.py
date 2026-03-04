import streamlit as st
from src.agent import agent_app

st.set_page_config(page_title="Country Q&A Agent", page_icon="🌍")

st.title("🌍 Country Q&A Agent")
st.markdown("Ask me anything about countries (e.g., population, capital, currencies)!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is the capital and population of Brazil?"):
    # Add user message to state and UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Invoke LangGraph Agent
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            initial_state = {
                "query": prompt,
                "country": None,
                "requested_fields": [],
                "api_response": None,
                "final_answer": "",
                "error": None
            }
            try:
                result = agent_app.invoke(initial_state)
                answer = result["final_answer"]
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                error_msg = f"An error occurred: {str(e)}"
                st.error(error_msg)