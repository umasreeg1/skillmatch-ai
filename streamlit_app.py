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

# Injected Custom Dark SaaS CSS
CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
    }
    
    /* Hide Streamlit Default Header/Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Header Gradient Banner */
    .brand-header {
        background: linear-gradient(135deg, rgba(0, 242, 254, 0.1) 0%, rgba(155, 81, 224, 0.1) 100%);
        border: 1px solid rgba(79, 172, 254, 0.25);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 25px;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    .gradient-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 50%, #9b51e0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }
    
    .subtitle {
        font-size: 1rem;
        color: #94a3b8;
    }
    
    /* Metric Cards */
    .metric-card {
        background: #141c2e;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(0, 242, 254, 0.3);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        margin: 6px 0;
    }
    
    .metric-label {
        font-size: 0.78rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Pill Badges */
    .pill-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        margin: 4px;
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
    
    /* Formula Box */
    .formula-box {
        background: rgba(14, 20, 34, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px;
        font-family: monospace;
        font-size: 0.85rem;
        margin: 12px 0;
    }

    /* Custom Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        color: #0b0f19 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.4) !important;
    }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# Pre-load & cache SentenceTransformer model
@st.cache_resource
def cached_transformer_model():
    return get_transformer_model()

# Warmup model
cached_transformer_model()

# Session State Initialization
if 'current_analysis' not in st.session_state:
    st.session_state.current_analysis = None
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'job_desc' not in st.session_state:
    st.session_state.job_desc = JOB_TEMPLATES['junior_aiml']['description']
if 'job_title' not in st.session_state:
    st.session_state.job_title = JOB_TEMPLATES['junior_aiml']['title']

# Sidebar Navigation
st.sidebar.markdown("## ✦ SKILLMATCH AI")
st.sidebar.caption("Resume Intelligence & Skill Gap Analyzer")

page = st.sidebar.radio(
    "Navigation Menu",
    [
        "🏠 Dashboard & Input",
        "📊 AI Job Match Score",
        "🧠 Skill Analysis & Breakdown",
        "💡 Explainable AI Insights",
        "⚡ What-If Skill Simulator",
        "🎯 Skill Priorities & Roadmap",
        "📄 Resume Suggestions",
        "📚 Methodology & Viva Guide",
        "ℹ About System"
    ]
)

# Helper Function to Run Analysis
def run_analysis_pipeline(resume_txt, job_txt, j_title):
    with st.spinner("🧠 Running SentenceTransformer embeddings (384-D) & Cosine Matcher..."):
        res = HybridMatcher.analyze(resume_txt, job_txt, j_title)
        st.session_state.current_analysis = res
        return res

# ---------------------------------------------------------
# PAGE 1: DASHBOARD & INPUT
# ---------------------------------------------------------
if page == "🏠 Dashboard & Input":
    st.markdown("""
    <div class="brand-header">
        <div class="gradient-title">✦ SKILLMATCH AI</div>
        <div class="subtitle">Discover your resume's true skill gap using 384-D semantic embeddings.</div>
    </div>
    """, unsafe_allow_html=True)

    # Feature indicators
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info("⚡ **Accurate Matching**\n\nNLP + Semantic Vectors")
    with col2:
        st.info("📊 **Gap Analysis**\n\nIdentify missing skills")
    with col3:
        st.info("💡 **Learning Roadmap**\n\nPersonalized 4-8 wk plan")
    with col4:
        st.info("💼 **Career Boost**\n\nBe job-ready")

    st.markdown("---")

    # Quick Demo Option
    demo_col1, demo_col2 = st.columns([3, 1])
    with demo_col1:
        st.subheader("⚡ Quick Start")
        st.caption("Click '✨ TRY DEMO' to immediately analyze a realistic sample resume against Junior AI/ML Engineer requirements.")
    with demo_col2:
        if st.button("✨ TRY DEMO", use_container_width=True):
            st.session_state.resume_text = DEMO_RESUME_TEXT
            st.session_state.job_desc = JOB_TEMPLATES['junior_aiml']['description']
            st.session_state.job_title = JOB_TEMPLATES['junior_aiml']['title']
            run_analysis_pipeline(DEMO_RESUME_TEXT, st.session_state.job_desc, st.session_state.job_title)
            st.success("Demo analysis completed! Go to '📊 AI Job Match Score' tab.")

    st.markdown("---")

    # Input Cards
    in_col1, in_col2 = st.columns(2)

    with in_col1:
        st.subheader("📄 YOUR RESUME")
        input_type = st.radio("Resume Mode", ["Upload PDF", "Paste Raw Text"], horizontal=True)

        if input_type == "Upload PDF":
            uploaded_pdf = st.file_uploader("Upload PDF Resume (Max 5MB)", type=["pdf"])
            if uploaded_pdf is not None:
                pdf_bytes = uploaded_pdf.read()
                extracted = extract_text_from_pdf_bytes(pdf_bytes)
                if extracted:
                    st.session_state.resume_text = extracted
                    st.success(f"✓ PDF extracted successfully ({len(extracted)} characters).")
                else:
                    st.error("Unable to extract text from this PDF. Please try another PDF or paste text.")
        else:
            st.session_state.resume_text = st.text_area(
                "Paste Resume Text",
                value=st.session_state.resume_text,
                height=250,
                placeholder="Paste work experience, skills, projects..."
            )

    with in_col2:
        st.subheader("💼 TARGET JOB REQUIREMENT")
        job_type = st.radio("Job Mode", ["Select Role Template", "Paste Job Description"], horizontal=True)

        if job_type == "Select Role Template":
            template_options = {t['title']: t for t in JOB_TEMPLATES.values()}
            selected_name = st.selectbox("Select Target Role Template", list(template_options.keys()))
            selected_t = template_options[selected_name]
            st.session_state.job_title = selected_t['title']
            st.session_state.job_desc = selected_t['description']
            st.text_area("Template Description", value=st.session_state.job_desc, height=200, disabled=True)
        else:
            st.session_state.job_title = st.text_input("Job Title", value=st.session_state.job_title)
            st.session_state.job_desc = st.text_area("Job Description", value=st.session_state.job_desc, height=200)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 ANALYZE RESUME NOW", use_container_width=True):
        if not st.session_state.resume_text.strip():
            st.error("Please upload a PDF resume or paste resume text.")
        elif not st.session_state.job_desc.strip():
            st.error("Please select a job template or paste a target job description.")
        else:
            run_analysis_pipeline(st.session_state.resume_text, st.session_state.job_desc, st.session_state.job_title)
            st.success("Analysis complete! Select '📊 AI Job Match Score' in the sidebar.")

# ---------------------------------------------------------
# PAGE 2: AI JOB MATCH SCORE
# ---------------------------------------------------------
elif page == "📊 AI Job Match Score":
    st.title("📊 AI Job Match Score Results")
    
    res = st.session_state.current_analysis
    if not res:
        st.warning("No analysis available yet. Please go to '🏠 Dashboard & Input' to run an analysis.")
    else:
        st.caption(f"Target Role: **{res['job_title']}** | Evaluated in {res['latency_seconds']}s")

        # Top Cards
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Overall Match</div>
                <div class="metric-value" style="color:#00f2fe;">{res['overall_score']}%</div>
                <div style="font-size:0.8rem; color:#10b981; font-weight:700;">{res['match_level']}</div>
            </div>
            """, unsafe_allow_html=True)
        with m_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Strong Matches</div>
                <div class="metric-value" style="color:#10b981;">{res['matching_count']}</div>
                <div style="font-size:0.75rem; color:#94a3b8;">&ge;82% Similarity</div>
            </div>
            """, unsafe_allow_html=True)
        with m_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Partial Matches</div>
                <div class="metric-value" style="color:#f59e0b;">{res['partial_count']}</div>
                <div style="font-size:0.75rem; color:#94a3b8;">45% - 81% Similarity</div>
            </div>
            """, unsafe_allow_html=True)
        with m_col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Missing Skills</div>
                <div class="metric-value" style="color:#ef4444;">{res['missing_count']}</div>
                <div style="font-size:0.75rem; color:#94a3b8;">&lt;45% Similarity</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        g_col1, g_col2 = st.columns([1, 1])

        # Plotly Score Gauge
        with g_col1:
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = res['overall_score'],
                number = {'suffix': "%", 'font': {'color': "#00f2fe", 'size': 44}},
                title = {'text': "Resume-Job Match Score", 'font': {'color': "#f1f5f9", 'size': 18}},
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
            fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=280)
            st.plotly_chart(fig_gauge, use_container_width=True)

        # Formula Explanation Card
        with g_col2:
            st.subheader("SCORE CALCULATION EXPLANATION")
            st.caption("Transparent weighted scoring equation:")
            st.markdown(f"""
            <div class="formula-box">
                • <b>35% Document Similarity:</b> {res['document_similarity']}%<br>
                • <b>45% Direct Skill Coverage:</b> {res['direct_skill_coverage']}%<br>
                • <b>20% Partial Concept Coverage:</b> {res['partial_concept_coverage']}%<br>
                <hr style="border-color:rgba(255,255,255,0.1);">
                <b>Formula Total:</b> {res['score_calculation']['document_similarity_weighted']}% + {res['score_calculation']['direct_coverage_weighted']}% + {res['score_calculation']['partial_coverage_weighted']}% = <span style="color:#00f2fe; font-weight:800;">{res['overall_score']}%</span>
            </div>
            """, unsafe_allow_html=True)

        # Skill Pills
        st.markdown("### ✓ STRONG MATCHES (≥82% Similarity)")
        s_pills = "".join([f'<span class="pill-badge pill-strong">{s["skill"]} ({s["similarity"]}%)</span>' for s in res['strong_matches']])
        st.markdown(s_pills if s_pills else "*No direct strong matches*", unsafe_allow_html=True)

        st.markdown("### ~ PARTIAL MATCHES (45%–81% Concept Similarity)")
        p_pills = "".join([f'<span class="pill-badge pill-partial">{p["skill"]} ({p["similarity"]}% • {p["resume_concept"]})</span>' for p in res['partial_matches']])
        st.markdown(p_pills if p_pills else "*No partial matches*", unsafe_allow_html=True)

        st.markdown("### ✕ MISSING SKILLS (<45% Similarity)")
        m_pills = "".join([f'<span class="pill-badge pill-missing">{m["skill"]} ({m["similarity"]}% • {m["priority"]} Priority)</span>' for m in res['missing_skills']])
        st.markdown(m_pills if m_pills else "*No missing skills*", unsafe_allow_html=True)

# ---------------------------------------------------------
# PAGE 3: SKILL ANALYSIS
# ---------------------------------------------------------
elif page == "🧠 Skill Analysis & Breakdown":
    st.title("🧠 AI Skill Analysis & Categorization")
    
    res = st.session_state.current_analysis
    if not res:
        st.warning("No analysis available. Please run an analysis on the Dashboard.")
    else:
        c1, c2 = st.columns(2)

        with c1:
            st.subheader("Domain Category Visualization")
            cat_df = pd.DataFrame(res['category_summary'])
            if not cat_df.empty:
                fig_bar = px.bar(
                    cat_df,
                    x='category',
                    y='match_percentage',
                    color='match_percentage',
                    color_continuous_scale=['#ef4444', '#f59e0b', '#10b981'],
                    labels={'match_percentage': 'Match %', 'category': 'Domain'},
                    range_y=[0, 100]
                )
                fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#94a3b8')
                st.plotly_chart(fig_bar, use_container_width=True)

        with c2:
            st.subheader("Skill Status Distribution")
            donut_data = {
                'Status': ['Matching', 'Partial', 'Missing', 'Additional'],
                'Count': [res['matching_count'], res['partial_count'], res['missing_count'], res['additional_count']]
            }
            fig_pie = px.pie(
                donut_data,
                names='Status',
                values='Count',
                hole=0.5,
                color='Status',
                color_discrete_map={'Matching': '#10b981', 'Partial': '#f59e0b', 'Missing': '#ef4444', 'Additional': '#3b82f6'}
            )
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#94a3b8')
            st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown("### Top Ranked Matching Skills")
        for s in res['top_matching_skills']:
            st.progress(s['similarity'] / 100.0, text=f"**{s['skill']}** ({s['similarity']}%) — {s['category']}")

# ---------------------------------------------------------
# PAGE 4: EXPLAINABLE AI
# ---------------------------------------------------------
elif page == "💡 Explainable AI Insights":
    st.title("💡 Explainable AI Insights")
    
    res = st.session_state.current_analysis
    if not res:
        st.warning("No analysis available.")
    else:
        st.info("### AI Vector Embedding Architecture\n\nResume text and job requirements were mapped into 384-dimensional dense semantic vectors using `SentenceTransformer (all-MiniLM-L6-v2)` and compared via Cosine Distance.")

        for insight in res['explainable_insights']:
            with st.expander(f"📌 {insight['title']} ({insight['badge']})"):
                st.write(insight['description'])

# ---------------------------------------------------------
# PAGE 5: WHAT-IF SIMULATOR
# ---------------------------------------------------------
elif page == "⚡ What-If Skill Simulator":
    st.title("⚡ Skill Improvement Simulator")
    st.caption("What-If Analysis: Select missing skills you plan to acquire to calculate projected match score boost.")

    res = st.session_state.current_analysis
    if not res:
        st.warning("No analysis available.")
    else:
        available_missing = [m['skill'] for m in res['missing_skills']] + [p['skill'] for p in res['partial_matches']]

        if not available_missing:
            st.success("Awesome! You already match all required job skills.")
        else:
            selected_to_acquire = st.multiselect(
                "Select Skills You Plan to Learn:",
                options=available_missing
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
# PAGE 6: LEARNING ROADMAP
# ---------------------------------------------------------
elif page == "🎯 Skill Priorities & Roadmap":
    st.title("🎯 Skill Priorities & Personalized Roadmap")
    
    res = st.session_state.current_analysis
    if not res:
        st.warning("No analysis available.")
    else:
        r_col1, r_col2 = st.columns([1, 2])

        with r_col1:
            st.subheader("Priority Classification")
            for m in res['missing_skills']:
                color_code = "🔴" if m['priority'] == "HIGH" else "🟠"
                st.markdown(f"{color_code} **{m['skill']}** — `{m['priority']} PRIORITY` ({m['category']})")

        with r_col2:
            st.subheader("Personalized 4-8 Week Roadmap")
            for week in res['roadmap']:
                with st.expander(f"🚀 {week['week_range']}: {week['title']}"):
                    st.write(f"**Target Skills:** {', '.join(week['skills'])}")
                    st.write(f"**Goal:** {week['goal']}")
                    st.write(f"**Focus:** {week['focus']}")
                    st.info(f"💡 **Practice:** {week['practice_recommendation']}")

# ---------------------------------------------------------
# PAGE 7: RESUME SUGGESTIONS
# ---------------------------------------------------------
elif page == "📄 Resume Suggestions":
    st.title("📄 Resume Improvement Suggestions")
    
    res = st.session_state.current_analysis
    if not res:
        st.warning("No analysis available.")
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
# PAGE 8: METHODOLOGY
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
# PAGE 9: ABOUT SYSTEM
# ---------------------------------------------------------
elif page == "ℹ About System":
    st.title("ℹ About SKILLMATCH AI")
    st.markdown("""
    **SKILLMATCH AI** is an AI/ML Resume Intelligence application designed for B.Tech / M.Tech academic evaluation and career intelligence.
    
    - **Frontend:** Streamlit + Custom Dark SaaS CSS + Plotly
    - **Backend Engine:** Python + SentenceTransformers + PyMuPDF + Scikit-Learn
    - **Author:** Megana V.
    """)
