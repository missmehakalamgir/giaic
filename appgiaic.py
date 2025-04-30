
import streamlit as st
import black
import isort
import subprocess
import tempfile
import base64
import re
import plotly.graph_objects as go
from radon.complexity import cc_visit

# Set up page configuration
st.set_page_config(page_title="RefactorPro", page_icon="🧠", layout="wide")

# Dark Mode Toggle
mode = st.toggle("🌙 Dark Mode", value=True)
dark_mode_css = """
<style>
body {
    background-color: #1e293b;
    color: white;
    font-family: 'Segoe UI', sans-serif;
}
.sidebar .sidebar-content {
    background-color: #0f172a;
}
h1, h2, h3, h4 {
    color: #60a5fa;
}
.footer {
    text-align: center;
    margin-top: 2rem;
    padding: 1rem;
    color: #94a3b8;
    border-top: 1px solid #475569;
}
.stButton>button {
    background-color: #3b82f6;
    color: white;
    border-radius: 8px;
    height: 3rem;
    font-size: 16px;
    font-weight: bold;
}
.download {
    margin-top: 1rem;
}
.download a {
    background-color: #10b981;
    padding: 10px 20px;
    border-radius: 8px;
    text-decoration: none;
    color: white;
}
.stTextArea>div>div>textarea {
    background-color: #334155;
    color: white;
    border: 1px solid #475569;
}
.stProgress>div {
    background-color: #3b82f6;
}
</style>
"""
light_mode_css = """
<style>
body {
    background-color: white;
    color: black;
}
.sidebar .sidebar-content {
    background-color: #e2e8f0;
}
h1, h2, h3, h4 {
    color: #2563eb;
}
.footer {
    text-align: center;
    margin-top: 2rem;
    padding: 1rem;
    color: #64748b;
    border-top: 1px solid #94a3b8;
}
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    height: 3rem;
    font-size: 16px;
    font-weight: bold;
}
.download a {
    background-color: #059669;
}
</style>
"""

st.markdown(dark_mode_css if mode else light_mode_css, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4711/4711987.png", width=100)
    st.title("RefactorPro")
    st.markdown("🚀 Clean your Python code with AI\n🔍 Analyze & visualize issues\n📥 Export clean code")
    if st.button("Clear Code"):
        st.session_state.code_input = ""

# Title
st.markdown("<h1 style='text-align:center;'>RefactorPro - Python Code Refactoring Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Paste your code, refactor it, and analyze it like a pro developer.</p>", unsafe_allow_html=True)

# Input Code Section
st.subheader("📝 Input Code")
if "code_input" not in st.session_state:
    st.session_state.code_input = ""  # Initialize input code state

with st.expander("📝 Paste your Python code here", expanded=True):
    code_input = st.text_area("Code Input", value=st.session_state.code_input, height=300, key="input_code")

# Refactor Code Function
def refactor_code(code):
    sorted_code = isort.code(code)
    formatted_code = black.format_file_contents(sorted_code, fast=False, mode=black.Mode())

    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as tmp_file:
        tmp_file.write(formatted_code)
        tmp_path = tmp_file.name

    result = subprocess.run(
        ["flake8", tmp_path], capture_output=True, text=True
    )
    return formatted_code, result.stdout

# Count issues from lint result
def count_issues(output):
    return {
        "Unused Imports": len(re.findall(r"unused-import", output)),
        "Unused Variables": len(re.findall(r"unused-variable", output)),
        "Undefined Variables": len(re.findall(r"undefined-variable", output))
    }

# Quality score calculation
def quality_score(issue_count):
    total_issues = sum(issue_count.values())
    return max(0, 100 - total_issues * 10)

# Analyze complexity
def analyze_complexity(code):
    results = cc_visit(code)
    complexity_scores = {func.name: func.complexity for func in results}
    return complexity_scores

# Function to create download button
def download_button(code):
    b64 = base64.b64encode(code.encode()).decode()
    href = f'<div class="download"><a href="data:file/txt;base64,{b64}" download="refactored.py">📥 Download Refactored Code</a></div>'
    return href

# Refactored Output Section
st.subheader("⚙️ Refactored Output")

if st.button("🔧 Refactor Now"):
    if not code_input.strip():
        st.toast("⚠️ Please paste some Python code", icon="⚠️")
    else:
        with st.spinner("🔧 Refactoring code..."):
            cleaned_code, analysis = refactor_code(code_input)
            issues = count_issues(analysis)
            score = quality_score(issues)
            complexity = analyze_complexity(cleaned_code)

        # Refactored code
        st.markdown("#### ✅ Refactored Code")
        st.code(cleaned_code, language="python")
        st.markdown(download_button(cleaned_code), unsafe_allow_html=True)

        # Issue Stats
        st.markdown("#### 📊 Code Issue Summary")
        st.write(issues)

        # Complexity Stats
        st.markdown("#### ⚡ Function Complexity Analysis")
        st.write(complexity)

        # Bar Chart
        fig = go.Figure(data=[
            go.Bar(
                x=list(issues.keys()),
                y=list(issues.values()),
                text=list(issues.values()),
                textposition="auto",
                marker_color=["#3b82f6", "#34d399", "#fbbf24"]
            )
        ])
        fig.update_layout(title_text="Code Issue Breakdown", xaxis_title="Issue Type", yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)

        # Quality Score
        st.markdown(f"### 💯 Code Quality Score: `{score}/100`")
        st.progress(score)

        # Raw Analysis (Expanded View)
        with st.expander("🔍 Full Lint Analysis"):
            st.code(analysis)

# Footer
st.markdown("<div class='footer'>RefactorPro © 2025 — Built with ❤️ by Mehak Alamgir</div>", unsafe_allow_html=True)
