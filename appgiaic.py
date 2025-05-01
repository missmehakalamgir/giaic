# Required libraries import kar rahe hain
import streamlit as st  # Streamlit UI ke liye
import black  # Code ko format karne ke liye
import isort  # Imports ko arrange karne ke liye
import subprocess  # External processes run karne ke liye
import tempfile  # Temporary files create karne ke liye
import base64  # Base64 encoding/decoding ke liye
import re  # Regular expressions ke liye
import plotly.express as px  # Data visualization ke liye
import random  # Random values generate karne ke liye
import ast  # Python code ko parse karne ke liye
from radon.complexity import cc_visit  # Code ki complexity measure karne ke liye
from streamlit_lottie import st_lottie  # Lottie animations ko Streamlit mein add karne ke liye
import requests  # External requests bhejne ke liye

# Streamlit ki page configuration set kar rahe hain
st.set_page_config(page_title="RefactorPro", page_icon="🧠", layout="wide")

# Lottie Animation ko URL se load karna
@st.cache_data
def load_lottie_url(url: str):
    r = requests.get(url)  # URL se request bhejna
    if r.status_code != 200:  # Agar response code 200 nahi hai, toh None return karna
        return None
    return r.json()  # Agar response sahi hai, toh JSON response return karna

# Animation ko load karna
animation = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_j1adxtyb.json")

# Custom CSS ka section jo UI ko style karta hai
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

# Page title aur animation display karna
col1, col2 = st.columns([2, 1])  # Do columns create kar rahe hain
with col1:
    st.markdown("<div class='big-title'>AI-Powered Python Code Formatter & Optimizer 🚀</div>", unsafe_allow_html=True)  # Title ko render kar rahe hain
    st.markdown("<div class='subtitle'>Empower your Python code with AI-driven formatting, optimization, and analysis</div>", unsafe_allow_html=True)  # Subtitle render karna
with col2:
    if animation:  # Agar animation load ho gaya ho
        st_lottie(animation, height=200, speed=1, loop=True)  # Lottie animation ko display karna
    else:  # Agar animation load na ho toh warning dikhana
        st.warning("⚠️ Failed to load animation.")

# Sidebar me features aur documentation ko show karna
with st.sidebar:
    st.markdown("<div class='feature-box'><h2>🔧 Features</h2><p>Refactor, analyze, optimize your code.</p></div>", unsafe_allow_html=True)  # Feature box display karna
    st.markdown("<div class='doc-box'><h3>📘 Documentation</h3><p>Get started with AI-driven optimization.</p></div>", unsafe_allow_html=True)  # Documentation box display karna
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Code", help="Reset your code input"):  # Clear code button banate hain
        st.session_state.code_input = ""  # Code ko reset karna

# Session state initialize karna agar code_input nahi hai
if "code_input" not in st.session_state:
    st.session_state.code_input = ""  # Pehli baar session start karte waqt code_input ko initialize karna

# Tabs ka setup karna
tabs = st.tabs(["📝 Code Input", "⚙️ Refactored Output", "🎯 Scorecard", "📊 Module Graph", "✨ Code Optimization Suggestions"])

# --- Code Input Tab --- #
with tabs[0]:
    code_input = st.text_area("Paste your Python code here:", value=st.session_state.code_input, height=300, key="input_code")  # User se code input lena

# Refactoring Functions
def refactor_code(code):
    sorted_code = isort.code(code)  # Code ko sort karna using isort
    formatted_code = black.format_file_contents(sorted_code, fast=False, mode=black.Mode())  # Black se code ko format karna
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as tmp_file:  # Temporary file create karna
        tmp_file.write(formatted_code)  # Formatted code ko file me likhna
        tmp_path = tmp_file.name  # Temporary file ka path lena
    result = subprocess.run(["flake8", tmp_path], capture_output=True, text=True)  # Flake8 ke through code ko analyze karna
    return formatted_code, result.stdout  # Formatted code aur analysis result return karna

# Code analysis ke liye issues ko count karna
def count_issues(output):
    return {
        "Unused Imports": len(re.findall(r"unused-import", output)),  # Unused imports ko count karna
        "Unused Variables": len(re.findall(r"unused-variable", output)),  # Unused variables ko count karna
        "Undefined Variables": len(re.findall(r"undefined-variable", output))  # Undefined variables ko count karna
    }

# Code quality score calculate karna
def quality_score(issue_count):
    total = sum(issue_count.values())  # Total issues ko sum karna
    return max(0, 100 - total * 10)  # Score ko calculate karna (maximum 100, issues ke hisaab se)

# Code me imports ko extract karna
def extract_imports(code):
    tree = ast.parse(code)  # Code ko parse karte hain AST (Abstract Syntax Tree) me
    imports = [node.names[0].name for node in tree.body if isinstance(node, ast.Import)]  # Sirf import statements ko extract karte hain
    return imports  # Imports return karna

# Module usage ko plot karna
def plot_import_usage(imports):
    import_counts = {imp: imports.count(imp) for imp in set(imports)}  # Har import ke count ko calculate karte hain
    colors = [f"rgb({random.randint(50,255)}, {random.randint(50,255)}, {random.randint(50,255)})" for _ in import_counts]  # Random colors generate karte hain
    fig = px.bar(x=list(import_counts.keys()), y=list(import_counts.values()),  # Bar chart create karte hain
                 labels={'x':'Modules', 'y':'Usage Count'},
                 title="📊 Module Usage", color=list(import_counts.keys()),  # Title aur color set karte hain
                 color_discrete_sequence=colors)  # Colors ko set karte hain
    fig.update_layout(bargap=0.3)  # Bar gap ko adjust karte hain
    st.plotly_chart(fig, use_container_width=True)  # Chart ko display karte hain

# Refactored code download karne ka button banana
def download_button(code):
    b64 = base64.b64encode(code.encode()).decode()  # Code ko Base64 encode karna
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
    '''  # Download button ka HTML code return karna

# Code Optimization Suggestions dena
def optimize_code_suggestions(code):
    suggestions = []  # Suggestions ko store karne ke liye list banate hain

    # Specific code patterns ke liye suggestions dena
    if "for i in range(len(list))" in code:
        suggestions.append("Use 'for item in list' instead of 'for i in range(len(list))' for better readability.")
    if "== None" in code:
        suggestions.append("Use 'is None' instead of '== None' for better performance and readability.")
    if len(re.findall(r"print\(", code)) > 3:
        suggestions.append("Avoid excessive 'print' statements. Consider logging or using a debugger for better performance.")
    if "for i in range(len(" in code:
        suggestions.append("Consider using 'enumerate()' for cleaner loops, e.g., 'for i, item in enumerate(list):'")
    if "list1 + list2" in code:
        suggestions.append("Avoid concatenating lists inside loops, as it's inefficient. Use 'list.extend()' or 'append()'.")
    if "list.remove(" in code:
        suggestions.append("If you're removing duplicates, consider using 'set()' instead of repeatedly removing elements from a list.")
    if "global " in code:
        suggestions.append("Avoid using 'global' variables. It's better to pass variables as function arguments or return values.")
    if len(re.findall(r"\b[a-z]{1,2}\b", code)) > 5: #Yeh line check kar rahi hai ki code mein zyada 1 ya 2 letter ke variable names ya words toh nahi hain
        suggestions.append("Use descriptive variable names instead of single-letter variables (e.g., 'x', 'y').")
    if "open(" in code and "close()" in code:
        suggestions.append("Use 'with open(...) as file' to automatically handle file closing and exceptions.")
    if "if x == None:" in code:
        suggestions.append("Use default arguments instead of manual 'None' checks in function definitions, e.g., 'def func(x=None):'")
    if "lambda " in code and len(re.findall(r"lambda", code)) > 3:
        suggestions.append("Consider replacing redundant lambda functions with regular function definitions.")
    if "list(map(" in code:
        suggestions.append("Consider using list comprehensions instead of 'map()' for better readability and performance.")

    return suggestions  # Suggestions return karna

# Refactor Button ka action
if st.button("⚙️ Refactor Now"):  # Refactor button click hone par action
    if not code_input.strip():  # Agar input code empty ho toh warning dena
        st.warning("Please paste some code to analyze.")
    else:
        cleaned_code, analysis = refactor_code(code_input)  # Code ko refactor karna
        issues = count_issues(analysis)  # Issues count karna
        score = quality_score(issues)  # Quality score calculate karna
        used_imports = extract_imports(code_input)  # Code se imports extract karna

        with tabs[1]:
            st.markdown("#### ✅ Cleaned & Refactored Code")  # Refactored code ka heading
            st.code(cleaned_code, language="python")  # Refactored code ko display karna
            st.markdown(download_button(cleaned_code), unsafe_allow_html=True)  # Download button dikhana

        with tabs[2]:
            st.markdown(f"<div class='score-box'>📊 Code Quality Score: {score}</div>", unsafe_allow_html=True)  # Quality score display karna
            st.progress(score)  # Progress bar ke through score dikhana
            st.json(issues)  # Issues ko JSON format me display karna

        with tabs[3]:
            if used_imports:
                plot_import_usage(used_imports)  # Module usage ko plot karna
            else:
                st.info("No modules found in the code.")  # Agar imports na ho toh info message dikhana

        with tabs[4]:
            suggestions = optimize_code_suggestions(code_input)  # Code optimization suggestions dena
            if suggestions:
                st.markdown("#### 💡 Code Optimization Suggestions")  # Suggestions heading
                for suggestion in suggestions:  # Har suggestion ko display karna
                    st.markdown(f"- {suggestion}")
            else:
                st.info("No optimization suggestions available.")  # Agar koi suggestion na ho toh info display karna

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
