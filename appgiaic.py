import streamlit as st
import black
import tempfile
import subprocess
import base64

# App Config
st.set_page_config(page_title="RefactorPro", page_icon="🧠", layout="wide")

# --- Custom CSS Styling ---
st.markdown("""
    <style>
    /* Body Theme */
    body {
        background-color: #0e1117;
        font-family: 'Segoe UI', sans-serif;
        color: #fff;
    }

    /* Sidebar Styling */
    .css-1d391kg, .css-1lcbmhc {
        background-color: #1a1d2e !important;
        color: #ffffff;
    }

    /* Header Styling */
    .main-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: #1f2937;
        padding: 1rem 2rem;
        border-radius: 12px;
        margin-bottom: 20px;
    }

    .main-header h1 {
        margin: 0;
        font-size: 2rem;
        color: #60a5fa;
    }

    .logo {
        width: 50px;
    }

    .code-box {
        background: #1e1e1e;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        font-size: 15px;
    }

    .download-button a {
        background-color: #2563eb;
        color: white;
        padding: 10px 20px;
        text-decoration: none;
        border-radius: 8px;
    }

    .footer {
        text-align: center;
        padding: 1rem;
        color: #888;
        font-size: 0.9rem;
        border-top: 1px solid #333;
        margin-top: 4rem;
    }

    .stButton>button {
        border-radius: 10px;
        background-color: #3b82f6;
        color: white;
        font-weight: bold;
        height: 3rem;
        width: 100%;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4711/4711987.png", width=100)
    st.title("🔧 RefactorPro")
    st.markdown("### The AI Code Cleaner")
    st.markdown("Built with ❤️ using:")
    st.markdown("- Streamlit\n- Black\n- Pylint")
    st.markdown("---")
    st.markdown("Paste your messy Python code below and get:")
    st.markdown("- ✅ Cleaned Code")
    st.markdown("- 📘 Issue Analysis")
    st.markdown("- 💡 AI-Powered Suggestions")

# --- Top Header ---
st.markdown("""
    <div class="main-header">
        <h1>🧠 Python Code Refactoring Assistant</h1>
        <img class="logo" src="https://cdn-icons-png.flaticon.com/512/1828/1828884.png"/>
    </div>
""", unsafe_allow_html=True)

st.markdown("Paste any messy Python code. This app will auto-refactor it, analyze errors, and explain what's wrong and how to fix it.")

# --- Input Code Area ---
code_input = st.text_area("📝 Your Messy Code", height=300)

# --- Utility Functions ---
def explain_pylint(output: str):
    explanations = {
        "unused-import": "🔸 **Unused Import**: Imported but not used.",
        "unused-variable": "🔸 **Unused Variable**: Declared but not used.",
        "undefined-variable": "🔸 **Undefined Variable**: Used before defining.",
    }
    result = []
    for key, msg in explanations.items():
        if key in output:
            result.append(msg)
    return "\n".join(result) if result else "✅ No major issues detected!"

def download_link(code: str, filename="refactored_code.py"):
    b64 = base64.b64encode(code.encode()).decode()
    return f'<div class="download-button"><a href="data:file/txt;base64,{b64}" download="{filename}">📥 Download Code</a></div>'

# --- Main Action ---
if st.button("🚀 Refactor & Analyze"):
    if not code_input.strip():
        st.warning("Please enter some code.")
    else:
        with st.spinner("⏳ Processing code..."):
            try:
                formatted_code = black.format_str(code_input, mode=black.FileMode())
            except Exception as e:
                st.error(f"Formatting error: {e}")
                formatted_code = code_input

            with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as tmp_file:
                tmp_file.write(formatted_code)
                tmp_path = tmp_file.name

            result = subprocess.run(
                ["pylint", tmp_path, "--disable=all", "--enable=unused-import,unused-variable,undefined-variable"],
                capture_output=True, text=True
            )

        st.markdown("### ✅ Refactored Code")
        st.code(formatted_code, language="python")
        st.markdown(download_link(formatted_code), unsafe_allow_html=True)

        st.markdown("### 🧪 Detected Issues")
        st.text(result.stdout)

        st.markdown("### 💡 Suggestions & Explanations")
        st.markdown(explain_pylint(result.stdout))

# --- Footer ---
st.markdown("""
    <div class="footer">
        Made with ❤️ by Mehak Alamgir | RefactorPro © 2025
    </div>
""", unsafe_allow_html=True)
