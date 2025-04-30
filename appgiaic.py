import streamlit as st
import black
import tempfile
import subprocess
import base64

st.set_page_config(page_title="Python Code Refactoring Assistant", layout="wide")

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4711/4711987.png", width=100)
    st.markdown("## 🧠 Code Refactoring Tool")
    st.markdown("Improve messy Python code in one click.")
    st.markdown("---")
    st.info("Built with ❤️ using Streamlit, Black & Pylint.")

# Custom CSS
st.markdown("""
    <style>
        .main { background-color: #0e1117; color: white; }
        .stTextArea textarea { background-color: #1e212d; color: white; border-radius: 8px; }
        .stButton>button { background-color: #4a90e2; color: white; border-radius: 10px; }
        .css-18e3th9 { padding: 1rem 2rem 2rem 2rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🛠️ Python Code Refactoring Assistant")
st.markdown("Paste your **messy Python code**, and this tool will refactor it, analyze issues, and explain everything!")

code_input = st.text_area("🔧 Paste your Python code here", height=300)

def explain_pylint(output: str):
    """Basic explanation for common pylint errors."""
    explanations = {
        "unused-import": "🔸 **Unused Import**: You imported a module or function that wasn't used.",
        "unused-variable": "🔸 **Unused Variable**: You created a variable that was never used.",
        "undefined-variable": "🔸 **Undefined Variable**: You used a variable that was never defined.",
    }
    result = []
    for key, msg in explanations.items():
        if key in output:
            result.append(msg)
    return "\n".join(result) if result else "✅ No critical issues found!"

def download_link(code: str, filename="refactored_code.py"):
    """Generate a download link."""
    b64 = base64.b64encode(code.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">📥 Download Refactored Code</a>'

if st.button("✨ Refactor & Analyze"):
    if not code_input.strip():
        st.warning("Please paste some code first.")
    else:
        # Format code with Black
        try:
            formatted_code = black.format_str(code_input, mode=black.FileMode())
        except Exception as e:
            st.error(f"Black Formatting Error: {e}")
            formatted_code = code_input

        st.success("✅ Code Refactored Successfully!")

        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as tmp_file:
            tmp_file.write(formatted_code)
            tmp_path = tmp_file.name

        # Run pylint
        result = subprocess.run(
            ["pylint", tmp_path, "--disable=all", "--enable=unused-import,unused-variable,undefined-variable"],
            capture_output=True, text=True
        )

        # Output
        st.subheader("📌 Refactored Code")
        st.code(formatted_code, language="python")
        st.markdown(download_link(formatted_code), unsafe_allow_html=True)

        st.subheader("🧪 Pylint Issues Found")
        st.markdown(f"```\n{result.stdout}\n```")

        st.subheader("💡 Explanation of Issues")
        st.markdown(explain_pylint(result.stdout))
