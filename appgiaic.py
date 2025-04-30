import streamlit as st
import black
import subprocess
import tempfile
import base64

# Page config
st.set_page_config(page_title="RefactorPro", page_icon="🧠", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    body {
        background: linear-gradient(145deg, #0f2027, #203a43, #2c5364);
        color: #f0f0f0;
        font-family: 'Segoe UI', sans-serif;
    }
    .title-bar {
        text-align: center;
        padding: 2rem 1rem 1rem;
    }
    .title-bar h1 {
        font-size: 3rem;
        margin: 0;
        color: #60a5fa;
    }
    .title-bar p {
        font-size: 1.2rem;
        color: #cbd5e1;
    }
    .code-card {
        background-color: #1e293b;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .stButton>button {
        background-color: #3b82f6;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 3rem;
        font-size: 16px;
    }
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.9rem;
        padding: 2rem 1rem 1rem;
        margin-top: 3rem;
        border-top: 1px solid #475569;
    }
    .download-button a {
        background: #22c55e;
        color: white;
        padding: 10px 20px;
        text-decoration: none;
        border-radius: 8px;
        display: inline-block;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("""
    <div class="title-bar">
        <img src="https://cdn-icons-png.flaticon.com/512/4711/4711987.png" width="80"/>
        <h1>RefactorPro</h1>
        <p>Turn messy Python code into clean, professional code using AI & best practices.</p>
    </div>
""", unsafe_allow_html=True)

# --- Layout ---
col1, col2 = st.columns(2)

# --- Code Input ---
with col1:
    st.markdown("### 📝 Input Your Messy Python Code")
    with st.container():
        code_input = st.text_area("Paste here:", height=300, key="input")

# --- Output & Actions ---
def run_refactor(code):
    try:
        formatted_code = black.format_str(code, mode=black.FileMode())
    except Exception as e:
        formatted_code = code

    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as tmp_file:
        tmp_file.write(formatted_code)
        tmp_path = tmp_file.name

    result = subprocess.run(
        ["pylint", tmp_path, "--disable=all", "--enable=unused-import,unused-variable,undefined-variable"],
        capture_output=True, text=True
    )
    return formatted_code, result.stdout

def download_link(code, filename="refactored_code.py"):
    b64 = base64.b64encode(code.encode()).decode()
    return f'<div class="download-button"><a href="data:file/txt;base64,{b64}" download="{filename}">📥 Download Code</a></div>'

with col2:
    st.markdown("### ⚙️ Refactored Code + Analysis")
    if st.button("🚀 Refactor Now"):
        if not code_input.strip():
            st.warning("⚠️ Please input some code first.")
        else:
            formatted_code, analysis = run_refactor(code_input)
            st.markdown("#### ✅ Cleaned Code")
            st.code(formatted_code, language="python")
            st.markdown(download_link(formatted_code), unsafe_allow_html=True)

            st.markdown("#### 🧪 Detected Issues")
            st.code(analysis)

            st.markdown("#### 💡 AI Suggestions")
            if "unused-import" in analysis:
                st.markdown("- 🔸 **Unused Import:** Remove unused import lines.")
            if "unused-variable" in analysis:
                st.markdown("- 🔸 **Unused Variable:** Remove or use defined variables.")
            if "undefined-variable" in analysis:
                st.markdown("- 🔸 **Undefined Variable:** Make sure all variables are defined before use.")
            if all(x not in analysis for x in ["unused", "undefined"]):
                st.success("✅ No major issues found!")

# --- Footer ---
st.markdown("""
    <div class="footer">
        RefactorPro © 2025 — Built with ❤️ by Mehak Alamgir<br>
        Making your messy code clean, one click at a time.
    </div>
""", unsafe_allow_html=True)
""")

---

## 📦 `requirements.txt`
```txt
streamlit
black
pylint
