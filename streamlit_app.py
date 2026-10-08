import streamlit as st
import os
import sys
import time
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Ensure backend directory is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.nlp.extractor import extract_text_from_pdf_bytes, clean_text, extract_skills_from_text
from app.nlp.matcher import HybridMatcher, get_transformer_model
from data.demo.demo_templates import DEMO_RESUME_TEXT, JOB_TEMPLATES

# Page Config
st.set_page_config(
    page_title="SKILLMATCH AI — Resume Intelligence & Skill Gap Analyzer",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Dark SaaS CSS matching the primary visual reference screenshot
CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background-color: #080c14;
        color: #f1f5f9;
    }
    
    /* Hide Streamlit Default Header/Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Persistent Top Header Bar */
    .top-header-bar {
        background: #0f172a;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding: 14px 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
        border-radius: 12px;
    }
    
    .top-brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .top-brand-title {
        font-size: 1.35rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #ffffff;
    }
    
    .top-brand-title span {
        background: linear-gradient(135deg, #00f2fe 0%, #9b51e0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .top-brand-sub {
        font-size: 0.72rem;
        color: #64748b;
    }
    
    /* Hero Banner */
    .hero-banner {
        text-align: center;
        padding: 15px 0 25px 0;
        max-width: 900px;
        margin: 0 auto;
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.8px;
        line-height: 1.2;
        margin-bottom: 8px;
        color: #ffffff;
    }
    
    .gradient-highlight {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 50%, #9b51e0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtitle {
        font-size: 0.98rem;
        color: #94a3b8;
        margin-bottom: 20px;
    }
    
    /* Dark Glass Cards */
    .saas-card {
        background: #101728;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        margin-bottom: 16px;
        height: 100%;
    }
    
    /* Feature Badges */
    .feature-card {
        background: #101728;
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 14px 16px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .feature-icon {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
    }
    
    /* Metric Card */
    .metric-card {
        background: #101728;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 18px;
        text-align: center;
    }
    
    .metric-val {
        font-size: 2.1rem;
        font-weight: 800;
        margin: 4px 0;
    }
    
    .metric-lbl {
        font-size: 0.75rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Formula Box */
    .formula-box {
        background: rgba(0, 242, 254, 0.03);
        border: 1px solid rgba(0, 242, 254, 0.2);
        border-radius: 12px;
        padding: 16px 20px;
        font-size: 0.88rem;
        color: #cbd5e1;
        line-height: 1.7;
        margin-bottom: 20px;
    }
    
    /* Pill Badges */
    .pill-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 14px;
        font-size: 0.78rem;
        font-weight: 600;
        margin: 3px 2px;
    }
    
    .pill-strong {
        background: rgba(16, 185, 129, 0.15);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .pill-partial {
        background: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    
    .pill-missing {
        background: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    .pill-additional {
        background: rgba(59, 130, 246, 0.15);
        color: #3b82f6;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
    
    /* Compact Chips Container for Additional Skills */
    .chips-container {
        display: flex;
        flex-wrap: wrap;
        gap: 4px;
        max-height: 180px;
        overflow-y: auto;
        padding: 4px;
    }
    
    /* Custom Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 50%, #9b51e0 100%) !important;
        color: #080c14 !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3) !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 242, 254, 0.5) !important;
    }
    
    /* Sidebar Styling */
    div[data-testid="stSidebar"] {
        background-color: #0a0e18;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    div[data-testid="stSidebar"] div[role="radiogroup"] > label {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 8px;
        padding: 8px 12px;
        margin-bottom: 5px;
        transition: all 0.2s ease;
    }
    
    div[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
        background: rgba(0, 242, 254, 0.12);
        border-color: rgba(0, 242, 254, 0.3);
    }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# Navigation Pages List
NAV_PAGES = [
    "🏠 Home / Dashboard",
    "📊 AI Job Match Score",
    "🎯 Skill Priorities & Roadmap",
    "💡 Explainable AI & Simulator",
    "📄 Resume Improvement Suggestions",
    "🔬 AI Model Evaluation",
    "📚 Methodology & Viva Guide",
    "ℹ About SKILLMATCH AI"
]

# ---------------------------------------------------------
# SESSION STATE INITIALIZATION
# ---------------------------------------------------------
if 'app_active_page' not in st.session_state:
    st.session_state['app_active_page'] = "🏠 Home / Dashboard"
if 'current_analysis' not in st.session_state:
    st.session_state['current_analysis'] = None
if 'resume_text' not in st.session_state:
    st.session_state['resume_text'] = ""
if 'job_desc' not in st.session_state:
    st.session_state['job_desc'] = JOB_TEMPLATES['junior_aiml']['description']
if 'job_title' not in st.session_state:
    st.session_state['job_title'] = JOB_TEMPLATES['junior_aiml']['title']

# Pre-load & cache SentenceTransformer model
@st.cache_resource
def cached_transformer_model():
    return get_transformer_model()

cached_transformer_model()

# ---------------------------------------------------------
# EARLY REQUEST PROCESSING (BEFORE RENDERING NAVIGATION WIDGET)
# ---------------------------------------------------------
if st.session_state.get("demo_requested"):
    st.session_state['resume_text'] = DEMO_RESUME_TEXT
    st.session_state['job_desc'] = JOB_TEMPLATES['junior_aiml']['description']
    st.session_state['job_title'] = JOB_TEMPLATES['junior_aiml']['title']
    
    # Run real NLP analysis pipeline
    res = HybridMatcher.analyze(
        st.session_state['resume_text'],
        st.session_state['job_desc'],
        st.session_state['job_title']
    )
    st.session_state['current_analysis'] = res
    st.session_state['app_active_page'] = "📊 AI Job Match Score"
    st.session_state['demo_requested'] = False

if st.session_state.get("analysis_requested"):
    if st.session_state['resume_text'].strip() and st.session_state['job_desc'].strip():
        res = HybridMatcher.analyze(
            st.session_state['resume_text'],
            st.session_state['job_desc'],
            st.session_state['job_title']
        )
        st.session_state['current_analysis'] = res
        st.session_state['app_active_page'] = "📊 AI Job Match Score"
    st.session_state['analysis_requested'] = False

# Sidebar Brand Header
st.sidebar.markdown("## ✦ SKILLMATCH AI")
st.sidebar.caption("Resume Intelligence & Skill Gap Analyzer")

# Sidebar Navigation Widget
page = st.sidebar.radio(
    "NAVIGATION MENU:",
    NAV_PAGES,
    key="app_active_page"
)

# Button Callbacks
def trigger_demo_callback():
    st.session_state["demo_requested"] = True

def trigger_analysis_callback():
    st.session_state["analysis_requested"] = True

# ---------------------------------------------------------
# TOP BRAND & HEADER BAR
# ---------------------------------------------------------
st.markdown("""
<div class="top-header-bar">
    <div class="top-brand">
        <div class="top-brand-title">✦ SKILLMATCH <span>AI</span></div>
        <div class="top-brand-sub">Resume Intelligence & Skill Gap Analyzer</div>
    </div>
    <div style="display:flex; align-items:center; gap:12px;">
        <span style="font-size:0.8rem; background:rgba(0,242,254,0.1); color:#00f2fe; padding:4px 10px; border-radius:12px; border:1px solid rgba(0,242,254,0.3);">
            384-D Vector Engine Active
        </span>
        <span style="font-weight:700; font-size:0.85rem; color:#f1f5f9;">👤 CANDIDATE PROFILE</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# PAGE 1: 🏠 HOME / DASHBOARD
# ---------------------------------------------------------
if page == "🏠 Home / Dashboard":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Discover Your Resume's True <span class="gradient-highlight">Skill Gap</span></div>
        <div class="hero-subtitle">AI-powered resume intelligence to match your skills with job requirements and get personalized career roadmaps.</div>
    </div>
    """, unsafe_allow_html=True)

    # Feature indicators matching visual reference
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon" style="background:rgba(0,242,254,0.15); color:#00f2fe;">⚡</div>
            <div>
                <div style="font-weight:700; font-size:0.85rem;">384-D Vector Engine</div>
                <div style="font-size:0.72rem; color:#64748b;">SentenceTransformer NLP</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon" style="background:rgba(155,81,224,0.15); color:#9b51e0;">📊</div>
            <div>
                <div style="font-weight:700; font-size:0.85rem;">Formula Transparency</div>
                <div style="font-size:0.72rem; color:#64748b;">Explicit Match Weights</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon" style="background:rgba(16,185,129,0.15); color:#10b981;">💡</div>
            <div>
                <div style="font-weight:700; font-size:0.85rem;">What-If Simulator</div>
                <div style="font-size:0.72rem; color:#64748b;">Dynamic Boost Projection</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon" style="background:rgba(245,158,11,0.15); color:#f59e0b;">🚀</div>
            <div>
                <div style="font-weight:700; font-size:0.85rem;">4–8 Week Roadmap</div>
                <div style="font-size:0.72rem; color:#64748b;">Targeted Skill Growth</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Input Section Cards
    in_col1, in_col2, in_col3 = st.columns([1.2, 1.2, 0.8])

    with in_col1:
        st.subheader("1. Resume Input")
        uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
        if uploaded_file is not None:
            pdf_bytes = uploaded_file.read()
            extracted_text = extract_text_from_pdf_bytes(pdf_bytes)
            st.session_state['resume_text'] = extracted_text
            st.success(f"Extracted {len(extracted_text.split())} words from PDF!")

        st.markdown("**OR Paste Resume Text:**")
        pasted_text = st.text_area(
            "Resume Plain Text",
            value=st.session_state['resume_text'],
            height=160,
            placeholder="Paste candidate resume content here...",
            key="home_resume_text_area"
        )
        if pasted_text != st.session_state['resume_text']:
            st.session_state['resume_text'] = pasted_text

    with in_col2:
        st.subheader("2. Target Job Description")
        template_keys = list(JOB_TEMPLATES.keys())
        selected_template = st.selectbox(
            "Choose Target Role Template:",
            options=["Custom Description"] + [JOB_TEMPLATES[k]['title'] for k in template_keys],
            key="home_template_selectbox"
        )

        if selected_template != "Custom Description":
            matched_key = [k for k in template_keys if JOB_TEMPLATES[k]['title'] == selected_template][0]
            st.session_state['job_title'] = JOB_TEMPLATES[matched_key]['title']
            st.session_state['job_desc'] = JOB_TEMPLATES[matched_key]['description']
            st.info(f"Loaded **{st.session_state['job_title']}** requirement template.")
            st.text_area("Job Description Preview", value=st.session_state['job_desc'], height=180, disabled=True)
        else:
            st.session_state['job_title'] = st.text_input("Job Title", value=st.session_state['job_title'], key="home_job_title_input")
            st.session_state['job_desc'] = st.text_area("Job Description", value=st.session_state['job_desc'], height=180, key="home_job_desc_textarea")

    with in_col3:
        st.subheader("★ Quick Options")
        st.markdown("""
        <div style="background:#101728; border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:16px; margin-bottom:16px;">
            <div style="font-weight:700; font-size:0.9rem; color:#00f2fe; margin-bottom:4px;">✨ Try Demo</div>
            <div style="font-size:0.75rem; color:#94a3b8; margin-bottom:12px;">Instant sample resume & Junior AI/ML job match analysis</div>
        </div>
        """, unsafe_allow_html=True)
        st.button("✨ TRY DEMO", on_click=trigger_demo_callback, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.button("✨ Analyze Resume →", on_click=trigger_analysis_callback, use_container_width=True)

# ---------------------------------------------------------
# PAGE 2: 📊 AI JOB MATCH SCORE
# ---------------------------------------------------------
elif page == "📊 AI Job Match Score":
    st.title("📊 AI Job Match Score Results")
    
    res = st.session_state['current_analysis']
    if not res:
        st.warning("No analysis available yet. Please go to '🏠 Home / Dashboard' or click '✨ TRY DEMO'.")
    else:
        st.caption(f"Target Role: **{res['job_title']}** | Evaluated in {res['latency_seconds']}s")

        # Top Row 3 Primary Cards matching visual reference layout
        top_c1, top_c2, top_c3 = st.columns([1.1, 1.1, 1.2])

        # CARD 1: AI JOB MATCH SCORE & GAUGE
        with top_c1:
            st.markdown("### 🔮 AI JOB MATCH SCORE")
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = res['overall_score'],
                number = {'suffix': "%", 'font': {'color': "#00f2fe", 'size': 38, 'family': 'Plus Jakarta Sans'}},
                title = {'text': f"{res['match_level'].upper()}", 'font': {'color': "#10b981" if res['overall_score']>=75 else "#f59e0b", 'size': 14}},
                gauge = {
                    'axis': {'range': [0, 100], 'tickcolor': "#94a3b8"},
                    'bar': {'color': "#00f2fe"},
                    'steps': [
                        {'range': [0, 40], 'color': "rgba(239, 68, 68, 0.2)"},
                        {'range': [40, 60], 'color': "rgba(245, 158, 11, 0.2)"},
                        {'range': [60, 75], 'color': "rgba(59, 130, 246, 0.2)"},
                        {'range': [75, 100], 'color': "rgba(16, 185, 129, 0.2)"}
                    ]
                }
            ))
            fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=220, margin=dict(l=20, r=20, t=30, b=10))
            st.plotly_chart(fig_gauge, use_container_width=True)

            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                st.markdown(f"<div class='metric-card'><div class='metric-lbl'>Total</div><div class='metric-val'>{res['total_skills_detected']}</div></div>", unsafe_allow_html=True)
            with m_col2:
                st.markdown(f"<div class='metric-card'><div class='metric-lbl'>Matching</div><div class='metric-val' style='color:#10b981;'>{res['matching_count']}</div></div>", unsafe_allow_html=True)
            with m_col3:
                st.markdown(f"<div class='metric-card'><div class='metric-lbl'>Missing</div><div class='metric-val' style='color:#ef4444;'>{res['missing_count']}</div></div>", unsafe_allow_html=True)

        # CARD 2: SKILL BREAKDOWN DONUT
        with top_c2:
            st.markdown("### 📌 SKILL BREAKDOWN")
            donut_data = {
                'Status': ['Matching Skills', 'Missing Skills', 'Additional Skills', 'Partial Match'],
                'Count': [res['matching_count'], res['missing_count'], res['additional_count'], res['partial_count']]
            }
            fig_pie = px.pie(
                donut_data,
                names='Status',
                values='Count',
                hole=0.55,
                color='Status',
                color_discrete_map={
                    'Matching Skills': '#10b981',
                    'Missing Skills': '#ef4444',
                    'Additional Skills': '#3b82f6',
                    'Partial Match': '#f59e0b'
                }
            )
            fig_pie.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#94a3b8',
                height=220,
                margin=dict(l=10, r=10, t=10, b=10),
                legend=dict(orientation="v", y=0.5)
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        # CARD 3: TOP MATCHING SKILLS PROGRESS BARS
        with top_c3:
            st.markdown("### 🏆 TOP MATCHING SKILLS")
            for s in res['top_matching_skills'][:5]:
                st.progress(s['similarity'] / 100.0, text=f"**{s['skill']}** ({s['similarity']}%)")

        st.markdown("<br>", unsafe_allow_html=True)

        # Bottom Row 4 Grid Cards matching reference image layout
        b_col1, b_col2, b_col3, b_col4 = st.columns([1, 1.1, 1.2, 1.1])

        # 1. MISSING SKILLS CARD
        with b_col1:
            st.markdown("### 🎯 MISSING SKILLS")
            if not res['missing_skills']:
                st.markdown("<div style='color:#10b981; font-weight:700;'>✓ No missing skills detected!</div>", unsafe_allow_html=True)
            else:
                for m in res['missing_skills']:
                    st.progress(m['similarity'] / 100.0, text=f"**{m['skill']}** ({m['similarity']}%)")

        # 2. ADDITIONAL SKILLS CARD (COMPACT CHIPS WRAPPING)
        with b_col2:
            st.markdown("### ⭐ ADDITIONAL SKILLS")
            add_skills = res['additional_skills']
            if not add_skills:
                st.caption("No extra skills detected.")
            else:
                display_skills = add_skills[:10]
                chips_html = "".join([f"<span class='pill-badge pill-additional'>{a['skill']}</span>" for a in display_skills])
                st.markdown(f"<div class='chips-container'>{chips_html}</div>", unsafe_allow_html=True)
                if len(add_skills) > 10:
                    with st.expander(f"+ {len(add_skills) - 10} more skills"):
                        more_chips = "".join([f"<span class='pill-badge pill-additional'>{a['skill']}</span>" for a in add_skills[10:]])
                        st.markdown(more_chips, unsafe_allow_html=True)

        # 3. WHAT-IF SIMULATOR CARD
        with b_col3:
            st.markdown("### ⚡ WHAT-IF SIMULATOR")
            st.caption("Select skills to project potential score:")
            available_missing = [m['skill'] for m in res['missing_skills']] + [p['skill'] for p in res['partial_matches']]
            if available_missing:
                selected_to_acquire = st.multiselect("Acquire Skills:", options=available_missing, key="results_whatif_multiselect")
                sim_res = HybridMatcher.simulate_what_if(selected_to_acquire, res)
                st.markdown(f"**Current:** {res['overall_score']}% ➔ **Projected:** <span style='color:#10b981; font-weight:800;'>{sim_res['projected_score']}% (+{sim_res['estimated_boost']}%)</span>", unsafe_allow_html=True)
            else:
                st.success("All required skills already matched!")

        # 4. LEARNING ROADMAP CARD
        with b_col4:
            st.markdown("### 🚀 LEARNING ROADMAP")
            if res['roadmap']:
                for week in res['roadmap'][:2]:
                    st.markdown(f"**{week['week_range']}:** {week['title']}")
                    st.caption(f"Target: {', '.join(week['skills'][:2])}")
            else:
                st.caption("Roadmap up to date.")

        st.markdown("<br>", unsafe_allow_html=True)

        # 2nd Results Row: SKILL COVERAGE ANALYSIS & KEY INSIGHTS
        sec_col1, sec_col2 = st.columns([1.2, 1])

        with sec_col1:
            st.markdown("### 📈 SKILL COVERAGE ANALYSIS")
            cat_df = pd.DataFrame(res['category_summary'])
            if not cat_df.empty:
                fig_cat = px.bar(
                    cat_df,
                    x='category',
                    y='match_percentage',
                    color='match_percentage',
                    color_continuous_scale=['#ef4444', '#f59e0b', '#10b981'],
                    labels={'match_percentage': 'Match %', 'category': 'Domain Category'},
                    range_y=[0, 100]
                )
                fig_cat.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#94a3b8', height=240, margin=dict(l=10,r=10,t=20,b=10))
                st.plotly_chart(fig_cat, use_container_width=True)

        with sec_col2:
            st.markdown("### 💡 KEY INSIGHTS")
            for insight in res['explainable_insights'][:3]:
                st.markdown(f"**{insight['title']}** (`{insight['badge']}`)")
                st.caption(insight['description'])

        st.markdown("<br>", unsafe_allow_html=True)

        # Formula Explanation Card
        st.subheader("SCORE CALCULATION EXPLANATION")
        st.markdown(f"""
        <div class="formula-box">
            • <b>35% Document Semantic Similarity:</b> {res['document_similarity']}%<br>
            • <b>45% Direct Skill Coverage:</b> {res['direct_skill_coverage']}%<br>
            • <b>20% Partial Concept Coverage:</b> {res['partial_concept_coverage']}%<br>
            <hr style="border-color:rgba(255,255,255,0.1); margin:8px 0;">
            <b>Formula Total:</b> {res['score_calculation']['document_similarity_weighted']}% + {res['score_calculation']['direct_coverage_weighted']}% + {res['score_calculation']['partial_coverage_weighted']}% = <span style="color:#00f2fe; font-weight:800;">{res['overall_score']}%</span>
        </div>
        """, unsafe_allow_html=True)

        # Skill Pills Summary
        st.markdown("### ✓ STRONG MATCHES (≥82% Similarity)")
        s_pills = "".join([f'<span class="pill-badge pill-strong">{s["skill"]} ({s["similarity"]}%)</span>' for s in res['strong_matches']])
        st.markdown(s_pills if s_pills else "*No direct strong matches*", unsafe_allow_html=True)

        st.markdown("### ~ PARTIAL MATCHES (45%–81% Concept Similarity)")
        p_pills = "".join([f'<span class="pill-badge pill-partial">{p["skill"]} ({p["similarity"]}% • {p["resume_concept"]})</span>' for p in res['partial_matches']])
        st.markdown(p_pills if p_pills else "*No partial matches*", unsafe_allow_html=True)

# ---------------------------------------------------------
# PAGE 3: 🎯 SKILL PRIORITIES & ROADMAP
# ---------------------------------------------------------
elif page == "🎯 Skill Priorities & Roadmap":
    st.title("🎯 Skill Priorities & Personalized Roadmap")
    
    res = st.session_state['current_analysis']
    if not res:
        st.warning("No analysis available yet. Please go to '🏠 Home / Dashboard' or click '✨ TRY DEMO'.")
    else:
        r_col1, r_col2 = st.columns([1, 2])

        with r_col1:
            st.subheader("Priority Classification")
            if not res['missing_skills']:
                st.success("No missing skills to prioritize!")
            else:
                for m in res['missing_skills']:
                    color_code = "🔴" if m['priority'] == "HIGH" else "🟠"
                    st.markdown(f"{color_code} **{m['skill']}** — `{m['priority']} PRIORITY` ({m['category']})")

        with r_col2:
            st.subheader("Personalized 4-8 Week Roadmap")
            for week in res['roadmap']:
                with st.expander(f"🚀 {week['week_range']}: {week['title']}", expanded=True):
                    st.write(f"**Target Skills:** {', '.join(week['skills'])}")
                    st.write(f"**Goal:** {week['goal']}")
                    st.write(f"**Focus:** {week['focus']}")
                    st.info(f"💡 **Practice:** {week['practice_recommendation']}")

# ---------------------------------------------------------
# PAGE 4: 💡 EXPLAINABLE AI & SIMULATOR
# ---------------------------------------------------------
elif page == "💡 Explainable AI & Simulator":
    st.title("💡 Explainable AI & Skill Improvement Simulator")
    
    res = st.session_state['current_analysis']
    if not res:
        st.warning("No analysis available. Please run an analysis on the Dashboard or click '✨ TRY DEMO'.")
    else:
        tab_exp, tab_sim = st.tabs(["💡 Explainable AI Reasoning", "⚡ What-If Skill Simulator"])

        with tab_exp:
            st.info("### AI Vector Embedding Architecture\n\nResume text and job requirements were mapped into 384-dimensional dense semantic vectors using `SentenceTransformer (all-MiniLM-L6-v2)` and compared via Cosine Distance.")

            for insight in res['explainable_insights']:
                with st.expander(f"📌 {insight['title']} ({insight['badge']})", expanded=True):
                    st.write(insight['description'])

        with tab_sim:
            st.subheader("⚡ Interactive What-If Simulator")
            st.caption("Select missing skills you plan to acquire to see your estimated match score boost:")

            available_missing = [m['skill'] for m in res['missing_skills']] + [p['skill'] for p in res['partial_matches']]

            if not available_missing:
                st.success("Awesome! You already match all required job skills.")
            else:
                selected_to_acquire = st.multiselect(
                    "Select Skills You Plan to Learn:",
                    options=available_missing,
                    key="tab_what_if_multiselect"
                )

                sim_result = HybridMatcher.simulate_what_if(selected_to_acquire, res)

                sc1, sc2, sc3 = st.columns(3)
                with sc1:
                    st.metric("CURRENT MATCH", f"{res['overall_score']}%")
                with sc2:
                    st.metric("PROJECTED MATCH", f"{sim_result['projected_score']}%", delta=f"+{sim_result['estimated_boost']}%")
                with sc3:
                    st.metric("SKILLS ACQUIRED", len(selected_to_acquire))

                st.caption(f"📌 *{sim_result['disclaimer']}*")

# ---------------------------------------------------------
# PAGE 5: 📄 RESUME IMPROVEMENT SUGGESTIONS
# ---------------------------------------------------------
elif page == "📄 Resume Improvement Suggestions":
    st.title("📄 Resume Improvement Suggestions")
    
    res = st.session_state['current_analysis']
    if not res:
        st.warning("No analysis available. Please run an analysis on the Dashboard or click '✨ TRY DEMO'.")
    else:
        cq = res['content_quality']
        st.markdown(f"""
        - **Action Verbs Detected:** {cq.get('action_verbs_detected', 0)}
        - **Quantifiable Metrics Found:** {cq.get('quantifiable_metrics_found', 0)}
        """)

        st.subheader("Bullet Optimization Templates")
        for b in res['bullet_rewrites']:
            st.markdown(f"**[{b['tag']}]**")
            st.error(f"Weak Bullet: \"{b['original_sample']}\"")
            st.success(f"Optimized Impact Bullet: \"{b['suggested_rewrite']}\"")
            st.caption(f"Why it works: {b['improvement_reason']}")
            st.markdown("---")

# ---------------------------------------------------------
# PAGE 6: 🔬 AI MODEL EVALUATION
# ---------------------------------------------------------
elif page == "🔬 AI Model Evaluation":
    st.title("🔬 AI Model Evaluation Framework")
    st.caption("Empirical runtime latency metrics and evaluation guidelines.")

    res = st.session_state['current_analysis']
    latency = res['latency_seconds'] if res else 0.31

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Pipeline Latency", f"{latency}s")
    with m2:
        st.metric("Embedding Dimension", "384")
    with m3:
        st.metric("Classification Logic", "Hybrid Vector")

    st.markdown("""
    ### Supervised Evaluation Framework
    - **Precision:** $\\text{TP} / (\\text{TP} + \\text{FP})$
    - **Recall:** $\\text{TP} / (\\text{TP} + \\text{FN})$
    - **F1 Score:** $2 \\times (P \\times R) / (P + R)$

    📌 *Benchmark evaluation dataset required for supervised precision/recall/F1 evaluation. The system currently evaluates skill similarity dynamically using real-time SentenceTransformer vectors.*
    """)

# ---------------------------------------------------------
# PAGE 7: 📚 METHODOLOGY & VIVA GUIDE
# ---------------------------------------------------------
elif page == "📚 Methodology & Viva Guide":
    st.title("📚 AI Methodology & Technical Viva Guide")
    st.markdown("""
    ### 1. Primary Semantic Model
    - **Model:** SentenceTransformer (`all-MiniLM-L6-v2`)
    - **Vector Dimensions:** 384-dimensional dense numerical vectors.

    ### 2. Mathematical Similarity Formula
    $$\\text{similarity}(A, B) = \\frac{A \\cdot B}{\\|A\\| \\|B\\|}$$

    ### 3. Classification Thresholds
    - **Strong Match:** $\\ge 82\\%$ or exact skill match
    - **Partial Match:** $45\\% - 81\\%$ concept similarity
    - **Missing Skill:** $< 45\\%$ similarity

    ### 4. Overall Match Score Formula
    $$\\text{Overall Score} = 35\\% \\times S_{\\text{doc}} + 45\\% \\times C_{\\text{direct}} + 20\\% \\times C_{\\text{partial}}$$
    """)

# ---------------------------------------------------------
# PAGE 8: ℹ ABOUT SKILLMATCH AI
# ---------------------------------------------------------
elif page == "ℹ About SKILLMATCH AI":
    st.title("ℹ About SKILLMATCH AI")
    st.markdown("""
    **SKILLMATCH AI** is an AI/ML Resume Intelligence application designed for B.Tech / M.Tech academic evaluation and career intelligence.
    
    - **Frontend:** Streamlit + Custom Dark SaaS CSS + Plotly
    - **Backend Engine:** Python + SentenceTransformers + PyMuPDF + Scikit-Learn
    - **Author:** SKILLMATCH AI Project Team
    """)
