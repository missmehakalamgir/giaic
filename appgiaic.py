import streamlit as st
import black
import subprocess
import tempfile
import base64
import re
import plotly.graph_objects as go

# Set up page configuration
st.set_page_config(page_title="RefactorPro", page_icon="🧠", layout="wide")

# Custom CSS for modern UI
st.markdown("""
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
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4711/4711987.png", width=100)
    st.title("RefactorPro")
    st.markdown("🚀 Clean your Python code with AI\n\n🔍 Analyze & visualize issues\n\n📥 Export clean code")
    
    # Added options in the sidebar for extra functionality
    if st.button("Clear Code"):
        st.session_state.code_input = ""

# Title
st.markdown("<h1 style='text-align:center;'>RefactorPro - Python Code Refactoring Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Paste your code, refactor it, and analyze it like a pro developer.</p>", unsafe_allow_html=True)

# Input Code Section
st.subheader("📝 Input Code")
if 'code_input' not in st.session_state:
    st.session_state.code_input = ""  # Initialize input code state
code_input = st.text_area("Paste your messy Python code below", value=st.session_state.code_input, height=300, key="input_code")

# Refactor Code Function
def refactor_code(code):
    try:
        formatted = black.format_str(code, mode=black.FileMode())
    except Exception as e:
        formatted = code

    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as tmp_file:
        tmp_file.write(formatted)
        tmp_path = tmp_file.name

    result = subprocess.run(
        ["pylint", tmp_path, "--disable=all", "--enable=unused-import,unused-variable,undefined-variable"],
        capture_output=True, text=True
    )
    return formatted, result.stdout

# Count issues from the lint result
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

# Function to create download button
def download_button(code):
    b64 = base64.b64encode(code.encode()).decode()
    href = f'<div class="download"><a href="data:file/txt;base64,{b64}" download="refactored.py">📥 Download Refactored Code</a></div>'
    return href

# Refactored Output Section
st.subheader("⚙️ Refactored Output")

if st.button("🔧 Refactor Now"):
    if not code_input.strip():
        st.warning("Please paste some Python code.")
    else:
        cleaned_code, analysis = refactor_code(code_input)
        issues = count_issues(analysis)
        score = quality_score(issues)

        # Refactored code
        st.markdown("#### ✅ Refactored Code")
        st.code(cleaned_code, language="python")
        st.markdown(download_button(cleaned_code), unsafe_allow_html=True)

        # Issue Stats
        st.markdown("#### 📊 Code Issue Summary")
        st.write(issues)

        # Bar Chart
        fig = go.Figure(data=[
            go.Bar(
                x=list(issues.keys()),
                y=list(issues.values()),
                text=list(issues.values()),
                textposition='auto',
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
