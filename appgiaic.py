# RefactorPro - Full UI/UX Upgraded Version
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
import streamlit_lottie as st_lottie
import json

st.set_page_config(page_title="RefactorPro", page_icon="🧠", layout="wide")

# Load Lottie animation
@st.cache_data
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Load animation
animation = load_lottiefile("/mnt/data/ai-coding.json")  # Replace with your local JSON Lottie file

# Custom CSS
st.markdown("""
    <style>
        .big-title {text-align: center; font-size: 3em; color: #2575fc; font-weight: bold;}
        .subtitle {text-align: center; font-size: 20px; color: #444; font-style: italic;}
        .feature-box {background: linear-gradient(to right, #6a11cb, #2575fc); padding: 15px; border-radius: 8px; color: white; text-align: center; margin-bottom: 20px;}
        .doc-box {background: linear-gradient(to right, #34d399, #10b981); padding: 15px; border-radius: 8px; color: white; text-align: center;}
        .download-btn a:hover {transform: scale(1.05); box-shadow: 0px 4px 12px rgba(0,0,0,0.2);}
        .score-box {background: linear-gradient(to right, #34d399, #10b981); padding: 10px; border-radius: 8px; text-align: center; color: white; font-size: 24px; font-weight: bold;}
        .footer {text-align: center; font-size: 14px; color: #aaa; margin-top: 40px;}
        .social-icons img {width: 25px; margin: 0 5px; vertical-align: middle;}
    </style>
""", unsafe_allow_html=True)

# Title & Animation
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("<div class='big-title'>RefactorPro 🚀</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Empower your Python code with AI-driven formatting, optimization, and analysis</div>", unsafe_allow_html=True)
with col2:
    st_lottie.st_lottie(animation, height=200, speed=1, loop=True)

# Sidebar Features & Docs
with st.sidebar:
    st.markdown("<div class='feature-box'><h2>🔧 Features</h2><p>Refactor, analyze, optimize your code.</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='doc-box'><h3>📘 Documentation</h3><p>Get started with AI-driven optimization.</p></div>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Code", help="Reset your code input"):
        st.session_state.code_input = ""

# Initialize session state
if "code_input" not in st.session_state:
    st.session_state.code_input = ""

# Tabs for workflow
tabs = st.tabs(["📝 Code Input", "⚙️ Refactored Output", "🎯 Scorecard", "📊 Module Graph"])

# --- Code Input Tab --- #
with tabs[0]:
    code_input = st.text_area("Paste your Python code here:", value=st.session_state.code_input, height=300, key="input_code")

# Refactoring Functions
def refactor_code(code):
    sorted_code = isort.code(code)
    formatted_code = black.format_file_contents(sorted_code, fast=False, mode=black.Mode())
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as tmp_file:
        tmp_file.write(formatted_code)
        tmp_path = tmp_file.name
    result = subprocess.run(["flake8", tmp_path], capture_output=True, text=True)
    return formatted_code, result.stdout

def count_issues(output):
    return {
        "Unused Imports": len(re.findall(r"unused-import", output)),
        "Unused Variables": len(re.findall(r"unused-variable", output)),
        "Undefined Variables": len(re.findall(r"undefined-variable", output))
    }

def quality_score(issue_count):
    total = sum(issue_count.values())
    return max(0, 100 - total * 10)

def extract_imports(code):
    tree = ast.parse(code)
    imports = [node.names[0].name for node in tree.body if isinstance(node, ast.Import)]
    return imports

def plot_import_usage(imports):
    import_counts = {imp: imports.count(imp) for imp in set(imports)}
    colors = [f"rgb({random.randint(50,255)}, {random.randint(50,255)}, {random.randint(50,255)})" for _ in import_counts]
    fig = px.bar(x=list(import_counts.keys()), y=list(import_counts.values()),
                 labels={'x':'Modules', 'y':'Usage Count'},
                 title="📊 Module Usage", color=list(import_counts.keys()),
                 color_discrete_sequence=colors)
    fig.update_layout(bargap=0.3)
    st.plotly_chart(fig, use_container_width=True)

def download_button(code):
    b64 = base64.b64encode(code.encode()).decode()
    return f'''
    <div class="download-btn" style="text-align: center; padding: 10px;">
        <a href="data:file/txt;base64,{b64}" download="refactored.py" style="
            background: linear-gradient(to right, #6a11cb, #2575fc);
            padding: 12px 20px;
            border-radius: 8px;
            color: white;
            text-align: center;
            font-weight: bold;
            font-size: 18px;
            text-decoration: none;"> 📅 Download Refactored Code </a>
    </div>
    '''

# Refactor Button
if st.button("⚙️ Refactor Now"):
    if not code_input.strip():
        st.warning("Please paste some code to analyze.")
    else:
        cleaned_code, analysis = refactor_code(code_input)
        issues = count_issues(analysis)
        score = quality_score(issues)
        used_imports = extract_imports(code_input)

        with tabs[1]:
            st.markdown("#### ✅ Cleaned & Refactored Code")
            st.code(cleaned_code, language="python")
            st.markdown(download_button(cleaned_code), unsafe_allow_html=True)

        with tabs[2]:
            st.markdown(f"<div class='score-box'>📊 Code Quality Score: {score}</div>", unsafe_allow_html=True)
            st.progress(score)
            st.json(issues)

        with tabs[3]:
            if used_imports:
                plot_import_usage(used_imports)
            else:
                st.info("No modules found in the code.")

# Footer with Social Icons
st.markdown("""
    <div class='footer'>
        RefactorPro &copy; 2025 &mdash; Built with ❤️ by Mehak Alamgir<br>
        <div class='social-icons'>
            <a href="https://github.com/mehakalamgir"><img src="https://cdn-icons-png.flaticon.com/512/25/25231.png"></a>
            <a href="https://linkedin.com/in/mehakalamgir"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png"></a>
            <a href="https://youtube.com/@mehakalamgir"><img src="https://cdn-icons-png.flaticon.com/512/1384/1384060.png"></a>
        </div>
    </div>
""", unsafe_allow_html=True)
