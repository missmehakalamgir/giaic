import streamlit as st
import black
import tempfile
import subprocess

st.set_page_config(page_title="Python Code Refactoring Assistant", layout="wide")

# Custom CSS
st.markdown("""
    <style>
        .main { background-color: #0e1117; color: white; }
        .stTextArea textarea { background-color: #1e212d; color: white; border-radius: 8px; }
        .stButton>button { background-color: #4a90e2; color: white; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🛠️ Python Code Refactoring Assistant")
st.markdown("Paste your **messy Python code**, and let this tool auto-format and analyze it!")

code_input = st.text_area("🔧 Paste your Python code here", height=300)

if st.button("✨ Refactor & Analyze"):
    if not code_input.strip():
        st.warning("Please paste some code first.")
    else:
        # Format code using Black
        try:
            formatted_code = black.format_str(code_input, mode=black.FileMode())
        except Exception as e:
            st.error(f"Black Formatting Error: {e}")
            formatted_code = code_input

        st.subheader("✅ Refactored Code")
        st.code(formatted_code, language="python")

        # Save to temp file for pylint analysis
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as temp_file:
            temp_file.write(formatted_code)
            temp_file_path = temp_file.name

        # Run pylint
        result = subprocess.run(
            ["pylint", temp_file_path, "--disable=all", "--enable=unused-import,unused-variable,undefined-variable"],
            capture_output=True, text=True
        )
        st.subheader("📘 Suggested Improvements (from Pylint)")
        st.markdown(f"```\n{result.stdout}\n```")
