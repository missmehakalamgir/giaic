import streamlit as st
import black, isort, subprocess, tempfile, base64, re, plotly.express as px, random, ast
from radon.complexity import cc_visit

# Page configuration
st.set_page_config(page_title="RefactorPro", page_icon="🧠", layout="wide")

# --- Custom CSS for consistent styling ---
st.markdown("""
<style>
body {
    background-color: #f9f9fb;
    color: #333333;
}
h1, h2, h3, h4 {
    font-family: 'Segoe UI', sans-serif;
}
.stTextArea textarea {
    font-family: 'Courier New', monospace;
    font-size: 15px;
}
.download-btn a:hover {
    background-color: #3b82f6;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown("""
    <div style="text-align:center; padding: 30px 0;">
        <h1 style="font-size: 48px; color: #2563eb; margin-bottom: 10px;">RefactorPro 🚀</h1>
        <p style="font-size: 20px; color: #555;">AI-powered Python code optimizer. Format, analyze, and improve your code effortlessly.</p>
    </div>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("""
        <div style="background: linear-gradient(to right, #6a11cb, #2575fc); padding: 25px; border-radius: 12px; color: white; text-align: center;">
            <h2>🔧 Features</h2>
            <ul style="text-align: left; padding-left: 20px;">
                <li>Format with Black & isort</li>
                <li>Lint via Flake8</li>
                <li>Show module usage graph</li>
                <li>Download refactored code</li>
                <li>Code quality scoring</li>
            </ul>
        </div>
        <br>
        <div style="background: linear-gradient(to right, #10b981, #34d399); padding: 20px; border-radius: 12px; color: white; text-align: center;">
            <h3>📘 Documentation</h3>
            <p>Learn how to use RefactorPro for better code.</p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🗑️ Clear Code", help="Reset your code input"):
        st.session_state.code_input = ""

# --- Input Area ---
st.markdown("## 📝 Paste Your Code Below")
if "code_input" not in st.session_state:
    st.session_state.code_input = ""

code_input = st.text_area("Your Python Code", value=st.session_state.code_input, height=300, key="input_code")

# --- Refactor Logic ---
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
    total_issues = sum(issue_count.values())
    return max(0, 100 - total_issues * 10)

def extract_imports(code):
    tree = ast.parse(code)
    imports = [node.names[0].name for node in tree.body if isinstance(node, ast.Import)]
    return imports

def plot_import_usage(imports):
    import_counts = {imp: imports.count(imp) for imp in set(imports)}
    colors = [f"rgb({random.randint(50,255)}, {random.randint(50,255)}, {random.randint(50,255)})" for _ in import_counts]
    fig = px.bar(
        x=list(import_counts.keys()), 
        y=list(import_counts.values()), 
        labels={'x':'Modules', 'y':'Usage Count'}, 
        title="📊 Module Usage Statistics",
        color=list(import_counts.keys()),
        color_discrete_sequence=colors
    )
    fig.update_layout(bargap=0.3)
    st.plotly_chart(fig, use_container_width=True)

def download_button(code):
    b64 = base64.b64encode(code.encode()).decode()
    return f'''
        <div class="download-btn" style="text-align:center; padding:20px;">
            <a href="data:file/txt;base64,{b64}" download="refactored.py" style="
                background: #2563eb;
                padding: 12px 25px;
                border-radius: 8px;
                color: white;
                font-size: 18px;
                text-decoration: none;
                font-weight: bold;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);">📥 Download Refactored Code</a>
        </div>
    '''

# --- Refactor Button ---
if st.button("🔧 Refactor Now"):
    if not code_input.strip():
        st.warning("⚠️ Please paste some Python code first.")
    else:
        with st.spinner("🔄 Analyzing and optimizing your code..."):
            cleaned_code, analysis = refactor_code(code_input)
            issues = count_issues(analysis)
            score = quality_score(issues)

        st.markdown("### ✅ Refactored Code")
        st.code(cleaned_code, language="python")
        st.markdown(download_button(cleaned_code), unsafe_allow_html=True)

        st.markdown(f"""
            <div style="text-align: center; font-size: 26px; font-weight: bold; padding: 10px; border-radius: 8px;
                        background: linear-gradient(to right, #10b981, #34d399); color: white;">
                💯 Code Quality Score: {score}
            </div>
        """, unsafe_allow_html=True)
        st.progress(score)

        # Graph of imports
        used_imports = extract_imports(code_input)
        if used_imports:
            plot_import_usage(used_imports)
        else:
            st.info("ℹ️ No import statements found to analyze.")

# --- Footer ---
st.markdown("""
    <hr>
    <p style="text-align: center; font-size: 16px; color: #888;">
        RefactorPro © 2025 — Built with ❤️ by <b>Mehak Alamgir</b>
    </p>
""", unsafe_allow_html=True)
