import streamlit as st
import sys
import os
import time
import html as html_lib

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../src"))
from inference import get_completion, load_model

st.set_page_config(page_title="CodePilot", page_icon="lightning", layout="wide")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Syne:wght@400;700;800&display=swap');
html, body, [data-testid="stApp"] {
    background: #0d0f12 !important;
    color: #e2e8f0;
    font-family: 'Syne', sans-serif;
}
.stTextArea textarea {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 14px !important;
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    color: #79c0ff !important;
    border-radius: 10px;
    padding: 16px;
    line-height: 1.7;
}
.sug-box {
    background: #161b22;
    border: 1px solid #238636;
    border-left: 4px solid #3fb950;
    border-radius: 10px;
    padding: 16px 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13.5px;
    color: #3fb950;
    white-space: pre-wrap;
    line-height: 1.7;
    margin-top: 8px;
}
.combined-box {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 16px 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13.5px;
    white-space: pre-wrap;
    line-height: 1.7;
}
.old-code { color: #79c0ff; }
.new-code { color: #3fb950; }
div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #238636, #2ea043);
    color: white;
    border: none;
    border-radius: 8px;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

st.markdown("""
<div style='padding: 2rem 0 1rem'>
  <h1 style='font-family: Syne; font-size: 2.8rem; font-weight: 800; color: #e2e8f0;
             margin: 0; letter-spacing: -1px;'>CodePilot</h1>
  <p style='color: #8b949e; font-size: .95rem; margin-top: .4rem;'>
    Fine-tuned CodeGPT &middot; Python autocompletion &middot; Runs 100% locally
  </p>
</div>
""", unsafe_allow_html=True)
st.divider()

if "model_loaded" not in st.session_state:
    with st.spinner("Loading model... (~10 sec on first launch)"):
        load_model()
    st.session_state["model_loaded"] = True

if "history" not in st.session_state:
    st.session_state["history"] = []

col_main, col_side = st.columns([3, 1], gap="large")

with col_side:
    st.markdown("#### Settings")
    max_tokens  = st.slider("Suggestion length (tokens)", 20, 120, 50, step=10)
    num_lines   = st.slider("Max lines to suggest", 1, 6, 3)
    temperature = st.slider("Creativity", 0.1, 1.2, 0.7, step=0.05,
                            help="Lower = focused, Higher = creative")
    top_p       = st.slider("Top-p sampling", 0.5, 1.0, 0.95, step=0.05)
    st.markdown("---")
    st.markdown("#### Recent prompts")
    for h in reversed(st.session_state["history"][-4:]):
        st.caption(h["prompt"][:45] + "...")

with col_main:
    EXAMPLES = [
        "def calculate_average(numbers):\n    ",
        "def binary_search(arr, target):\n    left, right = 0, len(arr) - 1\n    ",
        "class Stack:\n    def __init__(self):\n        ",
        "def merge_sort(arr):\n    ",
        "import pandas as pd\n\ndef clean_dataframe(df):\n    ",
    ]
    selected = st.selectbox("Load an example:", ["Custom..."] + EXAMPLES)
    default  = selected if selected != "Custom..." else "def "

    user_code = st.text_area(
        "", value=default, height=220,
        placeholder="Start typing your Python function here...",
        label_visibility="collapsed"
    )

    b1, b2, b3 = st.columns([2, 1, 1])
    with b1:
        suggest = st.button("Get Suggestion", use_container_width=True)
    with b2:
        accept  = st.button("Accept + Continue", use_container_width=True)
    with b3:
        clear   = st.button("Clear", use_container_width=True)

    if clear:
        st.session_state["last_suggestion"] = ""
        st.rerun()

    if suggest and user_code.strip():
        with st.spinner("Thinking..."):
            sug = get_completion(
                user_code,
                max_new_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                num_lines=num_lines,
            )
        st.session_state["last_suggestion"] = sug
        st.session_state["last_prompt"]     = user_code
        st.session_state["history"].append({"prompt": user_code, "suggestion": sug})

    if accept and st.session_state.get("last_suggestion"):
        merged = st.session_state["last_prompt"] + st.session_state["last_suggestion"]
        st.session_state["last_suggestion"] = ""
        st.success("Accepted! Copy the merged code below, paste it back, and keep writing.")
        st.code(merged, language="python")

    sug = st.session_state.get("last_suggestion", "")
    if sug:
        st.markdown("---")
        st.markdown("#### AI Suggestion")
        st.markdown(f'<div class="sug-box">{html_lib.escape(sug)}</div>',
                    unsafe_allow_html=True)
        st.markdown("<br><b>Combined preview</b> (your code + suggestion):",
                    unsafe_allow_html=True)
        prompt = st.session_state.get("last_prompt", user_code)
        st.markdown(
            f'<div class="combined-box">'
            f'<span class="old-code">{html_lib.escape(prompt)}</span>'
            f'<span class="new-code">{html_lib.escape(sug)}</span>'
            f'</div>',
            unsafe_allow_html=True
        )