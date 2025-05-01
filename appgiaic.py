import streamlit as st
import black
import isort
import subprocess
import tempfile
import base64
import re
import plotly.express as px
import random
import ast
from radon.complexity import cc_visit

# Set up page configuration
st.set_page_config(page_title="RefactorPro", page_icon="🧠", layout="wide")

# ===== Custom CSS for professional layout =====
st.markdown("""
    <style>
        body {
            background-color: black;
            font-family: 'Segoe UI', sans-serif;
        }
        .main h1, .main p, .main h2, .main h3 {
            text-align: center;
        }
        .feature-box, .doc-box, .score-box, .download-box {
            padding: 20px;
            border-radius: 12px;
            color: white;
            margin-bottom: 20px;
        }
        .feature-box {
            background: linear-gradient(to right, #6a11cb, #2575fc);
        }
        .doc-box {
            background: linear-gradient(to right, #34d399, #10b981);
        }
        .score-box {
            font-size: 24px;
            font-weight: bold;
            background: linear-gradient(to right, #34d399, #10b981);
        }
        .download-box a {
            background: linear-gradient(to right, #6a11cb, #2575fc);
            padding: 12px 20px;
            border-radius: 8px;
            color: white;
            text-align: center;
            font-weight: bold;
            font-size: 18px;
            text-decoration: none;
        }
    </style>
""", unsafe_allow_html=True)

# ===== Title & Description =====
st.markdown("""
    <h1 style='color: #2575fc;'>RefactorPro 🚀</h1>
    <p style='font-size: 18px;'>AI-powered Python code optimizer. Format, analyze, and improve with ease!</p>
""", unsafe_allow_html=True)

# ===== Sidebar Layout =====
with st.sidebar:
    st.markdown("<div class='feature-box'><h2>🔧 Features</h2><p>Refactor, analyze, optimize your code.</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='doc-box'><h3>📘 Documentation</h3><p>Get started with AI-driven optimization.</p></div>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Code", help="Reset your code input"):
        st.session_state.code_input = ""

# ===== Code Input Section =====
st.subheader("📝 Paste Your Code")
if "code_input" not in st.session_state:
    st.session_state.code_input = ""

with st.expander("📝 Enter your Python code", expanded=True):
    code_input = st.text_area("Code Input", value=st.session_state.code_input, height=300, key="input_code")

# ===== Function: Refactor Code =====
def refactor_code(code):
    sorted_code = isort.code(code)
    formatted_code = black.format_file_contents(sorted_code, fast=False, mode=black.Mode())

    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as tmp_file:
        tmp_file.write(formatted_code)
        tmp_path = tmp_file.name

    result = subprocess.run(["flake8", tmp_path], capture_output=True, text=True)
    return formatted_code, result.stdout

# ===== Function: Count Issues =====
def count_issues(output):
    return {
        "Unused Imports": len(re.findall(r"unused-import", output)),
        "Unused Variables": len(re.findall(r"unused-variable", output)),
        "Undefined Variables": len(re.findall(r"undefined-variable", output))
    }

# ===== Function: Quality Score =====
def quality_score(issue_count):
    total_issues = sum(issue_count.values())
    return max(0, 100 - total_issues * 10)

# ===== Function: Extract Imports =====
def extract_imports(code):
    tree = ast.parse(code)
    imports = [node.names[0].name for node in tree.body if isinstance(node, ast.Import)]
    return imports

# ===== Function: Plot Import Usage =====
def plot_import_usage(imports):
    import_counts = {imp: imports.count(imp) for imp in set(imports)}
    colors = [f"rgb({random.randint(50,255)}, {random.randint(50,255)}, {random.randint(50,255)})" for _ in import_counts]

    fig = px.bar(
        x=list(import_counts.keys()), 
        y=list(import_counts.values()), 
        labels={'x':'Modules', 'y':'Usage Count'}, 
        title="📊 Module Usage",
        color=list(import_counts.keys()),
        color_discrete_sequence=colors
    )
    fig.update_layout(bargap=0.3)
    st.plotly_chart(fig, use_container_width=True)

# ===== Function: Download Button =====
def download_button(code):
    b64 = base64.b64encode(code.encode()).decode()
    return f'''<div class="download-box"><a href="data:file/txt;base64,{b64}" download="refactored.py">📥 Download Refactored Code</a></div>'''

# ===== Refactor Output Section =====
st.subheader("⚙️ Refactored Output")

if st.button("🔧 Refactor Now", help="Click to format & analyze your code"):
    if not code_input.strip():
        st.toast("⚠️ Please paste some Python code", icon="⚠️")
    else:
        with st.spinner("🔧 Processing..."):
            cleaned_code, analysis = refactor_code(code_input)
            issues = count_issues(analysis)
            score = quality_score(issues)

        st.markdown("#### ✅ Cleaned Code")
        st.code(cleaned_code, language="python")
        st.markdown(download_button(cleaned_code), unsafe_allow_html=True)

        st.markdown(f"<div class='score-box'>💯 Code Quality Score: {score}</div>", unsafe_allow_html=True)
        st.progress(score)

        st.subheader("📊 Module Usage Statistics")
        used_imports = extract_imports(code_input)
        if used_imports:
            plot_import_usage(used_imports)
        else:
            st.markdown("⚠️ No imports found in the code.")

# ===== Footer =====
st.markdown("<p style='text-align: center;'>RefactorPro © 2025 — Built with ❤️ by Mehak Alamgir</p>", unsafe_allow_html=True)
