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

# Dark Mode Toggle with Session State
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True  # Default to dark mode

toggle_text = "🌙 Enable Dark Mode" if not st.session_state.dark_mode else "☀️ Enable Light Mode"
if st.button(toggle_text):
    st.session_state.dark_mode = not st.session_state.dark_mode

dark_mode_css = """
<style>
body { background-color: #1e293b; color: white; }
.sidebar .sidebar-content { background-color: #0f172a; }
.stButton>button { background-color: #3b82f6; color: white; border-radius: 8px; }
.download-btn { background-color: #10b981; padding: 10px 20px; border-radius: 8px; color: white; text-align: center; font-weight: bold; }
.metric-box { border-radius: 8px; padding: 15px; text-align: center; font-weight: bold; }
</style>
"""

light_mode_css = """
<style>
body { background-color: white; color: black; }
.sidebar .sidebar-content { background-color: #e2e8f0; }
.stButton>button { background-color: #2563eb; color: white; border-radius: 8px; }
.download-btn { background-color: #059669; padding: 10px 20px; border-radius: 8px; color: white; text-align: center; font-weight: bold; }
.metric-box { border-radius: 8px; padding: 15px; text-align: center; font-weight: bold; }
</style>
"""

st.markdown(dark_mode_css if st.session_state.dark_mode else light_mode_css, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4711/4711987.png", width=100)
    st.title("RefactorPro")
    st.markdown("🚀 Clean your Python code with AI\n🔍 Analyze & visualize issues\n📥 Export clean code")
    if st.button("Clear Code"):
        st.session_state.code_input = ""

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

    result = subprocess.run(["flake8", tmp_path], capture_output=True, text=True)
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
    return f'<div class="download-btn"><a href="data:file/txt;base64,{b64}" download="refactored.py">📥 Download Refactored Code</a></div>'

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

        # **Improved Code Quality Score UI**
        st.markdown("""
            <div class="metric-box">
                <div class="metric-title">💯 Code Quality Score</div>
                <div class="metric-score">{}</div>
            </div>
        """.format(score), unsafe_allow_html=True)
        st.progress(score)

        # **Issue Breakdown Updated**
        st.markdown("#### 🚀 Code Issue Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric(label="📌 Unused Imports", value=issues["Unused Imports"])
        col2.metric(label="⚠️ Unused Variables", value=issues["Unused Variables"])
        col3.metric(label="🚨 Undefined Variables", value=issues["Undefined Variables"])

        # **Pie Chart for Code Issues**
        total_issues = sum(issues.values())
        percentages = [round((v / total_issues) * 100, 2) if total_issues else 0 for v in issues.values()]
        fig = go.Figure(data=[go.Pie(labels=list(issues.keys()), values=percentages, hole=0.4)])
        fig.update_layout(title="📊 Issue Breakdown (Percentage)", template="plotly_dark" if st.session_state.dark_mode else "plotly_white")
        st.plotly_chart(fig, use_container_width=True)

        # **Expanded Full Lint Analysis**
        st.subheader("🔍 Full Lint Analysis")
        with st.expander("Click to View Detailed Report"):
            st.code(analysis)

# Footer
st.markdown("<div class='footer'>RefactorPro © 2025 — Built with ❤️ by Mehak Alamgir</div>", unsafe_allow_html=True)
