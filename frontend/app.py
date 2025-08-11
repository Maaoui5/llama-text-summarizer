import streamlit as st
import requests

st.set_page_config(page_title="LLaMA Text Summarizer")
st.title("LLaMA Text Summarizer")

text = st.text_area("Enter text to summarize:", height=300)

if st.button("Summarize"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Generating summary..."):
            try:
                res = requests.post("http://localhost:8000/summarize/", data={"text": text}, timeout=60)
                res.raise_for_status()
                summary = res.json().get("summary", "No summary returned.")
                st.subheader("Summary")
                st.write(summary)
            except Exception as e:
                st.error(f"Error: {e}")
