import streamlit as st
import sympy as sp
import wikipedia
from duckduckgo_search import DDGS

# Page setup
st.set_page_config(page_title="SmartBot AI")

st.title("💬 SmartBot")
st.write("A simple AI-style chatbot that answers questions using search and knowledge tools.")

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Helper functions
def solve_math(question):
    try:
        result = sp.sympify(question)
        return f"🧮 **Math Result:** {result}"
    except:
        return None

def wiki_search(question):
    try:
        return wikipedia.summary(question, sentences=3)
    except:
        return None

def web_search(question):
    try:
        with DDGS() as ddgs:
            results = [r["body"] for r in ddgs.text(question, max_results=2)]
        return "\n".join(results)
    except:
        return None

def generate_answer(question):

    # Try math first
    math = solve_math(question)
    if math:
        return math

    # Try Wikipedia
    wiki = wiki_search(question)
    if wiki:
        return wiki

    # Try web search
    web = web_search(question)
    if web:
        return web

    return "Sorry, I couldn't find an answer for that."

# Chat input
if prompt := st.chat_input("Ask something..."):

    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate answer
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_answer(prompt)
            st.markdown(response)

    # Save response
    st.session_state.messages.append({"role": "assistant", "content": response})
