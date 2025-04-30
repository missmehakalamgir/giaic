import streamlit as st
import black
import tempfile
import subprocess
import base64

st.set_page_config(
    page_title="Python Refactoring Assistant",
    layout="wide",
    page_icon="🛠️"
)

# --- Custom CSS for complex layout ---
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
    }
    .reportview-container {
        background: #0e1117;
    }
    .sidebar .sidebar-content {
        padding-top: 2rem;
        background: #1a1d2e;
    }
    .css-1d391kg {padding-top: 3rem;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .logo-container {
        text-align: center;
        margin-bottom: 20px;
    }
    .footer {
        text-align: center;
        padding: 20px;
        font-size: 0.9rem;
        color: gray;
        border-top: 1px solid #333;
        margin-top: 3rem;
    }
    .download-button a {
        background-color: #1f77b4;
        color: white;
        padding: 10px 20px;
        text-decoration: none;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar/Navbar (Top) ---
with st.sidebar:
    st.image("https://yt3.googleusercontent.com/aeRr2sBTduWzH5Xq40kUw4xL8O3iu2yg8_czNTbWwlTnTqBpWJqivSq91MSWZoWZJvMMW4sGQg=s900-c-k-c0x00ffffff-no-rj.png", width=120)
    st.title("🔧 Code Refactor Pro")
    st.markdown("Built with `Streamlit`, `Black`, and `Pylint`")
    st.markdown("---")
    st.info("Paste messy Python code → Clean & Explain it!")

# --- Main Header ---
st.markdown("<div class='logo-container'><h1>🛠️ Python Code Refactoring Assistant</h1></div>", unsafe_allow_html=True)
st.markdown("Paste your messy Python code below. This tool will refactor it, detect common issues, and explain the improvements.")

# --- Code Input Area ---
code_input = st.text_area("🔧 Paste your Python code", height=300, key="input_code")

# --- Functions ---
def explain_pylint(output: str):
    explanations = {
        "unused-import": "🔸 **Unused Import**: Module imported but not used.",
        "unused-variable": "🔸 **Unused Variable**: Variable declared but never used.",
        "undefined-variable": "🔸 **Undefined Variable**: Variable used before being defined.",
    }
    result = []
    for key, msg in explanations.items():
        if key in output:
            result.append(msg)
    return "\n".join(result) if result else "✅ No major issues found!"

def download_link(code: str, filename="refactored_code.py"):
    b64 = base64.b64encode(code.encode()).decode()
    return f'<div class="download-button"><a href="data:file/txt;base64,{b64}" download="{filename}">📥 Download Refactored Code</a></div>'

# --- Action Button ---
if st.button("✨ Refactor & Analyze"):
    if not code_input.strip():
        st.warning("Please paste some code.")
    else:
        with st.spinner("🔄 Refactoring..."):
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

        # --- Output Section ---
        st.markdown("## ✅ Refactored Code")
        st.code(formatted_code, language="python")
        st.markdown(download_link(formatted_code), unsafe_allow_html=True)

        st.markdown("## 🧪 Pylint Report")
        st.text(result.stdout)

        st.markdown("## 💡 Explanation of Issues")
        st.markdown(explain_pylint(result.stdout))

# --- Footer ---
st.markdown("<div class='footer'>🚀 Created by Mehak Alamgir | Streamlit UI/UX Pro Edition</div>", unsafe_allow_html=True)
