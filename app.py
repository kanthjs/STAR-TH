"""
STAR-TH: Modern Statistical Tool for Thai Agricultural Research
Main Streamlit Application Entry Point - Phase 1 MVP
"""

import streamlit as st
import pandas as pd
import numpy as np
from config.settings import PAGE_CONFIG, APP_VERSION, APP_TITLE
from config.thai_translations import THAI
from modules.data_manager import (
    load_csv_file, validate_rcbd_data, get_summary_stats, get_design_info
)
from modules.anova import run_rcbd_anova, get_cv_quality, get_significance_stars
from visualization.charts import (
    create_means_bar_chart, create_box_plot, create_means_with_error_bars
)

# Configure Streamlit page
st.set_page_config(**PAGE_CONFIG)

# Custom CSS
st.markdown("""
    <style>
    .title {
        text-align: center;
        color: #2D5016;
        font-size: 2.5em;
        margin-bottom: 0.2em;
    }
    .subtitle {
        text-align: center;
        color: #5A7A3A;
        font-size: 1.2em;
        margin-bottom: 1em;
    }
    .footer {
        text-align: center;
        color: #999;
        font-size: 0.85em;
        margin-top: 3em;
        padding-top: 1em;
        border-top: 1px solid #eee;
    }
    .metric-card {
        background-color: #f0f7f0;
        padding: 1em;
        border-radius: 0.5em;
        border-left: 4px solid #2D5016;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'anova_results' not in st.session_state:
    st.session_state.anova_results = None
if 'means_table' not in st.session_state:
    st.session_state.means_table = None
if 'treatment_col' not in st.session_state:
    st.session_state.treatment_col = None
if 'replication_col' not in st.session_state:
    st.session_state.replication_col = None
if 'response_col' not in st.session_state:
    st.session_state.response_col = None

# Main header
st.markdown(f"""
<div class="title">🌾 {APP_TITLE}</div>
<div class="subtitle">{THAI['home_subtitle']}</div>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("### 📋 " + THAI['nav_home'])
    st.markdown(f"**{THAI['footer_version']}:** {APP_VERSION}")
    st.divider()

    page = st.radio(
        label="Navigation",
        options=[
            THAI['nav_home'],
            THAI['nav_data_input'],
            THAI['nav_anova'],
            THAI['nav_visualization'],
        ],
        label_visibility="collapsed"
    )

    st.divider()

    # Quick stats
    if st.session_state.df is not None:
        st.markdown("### 📊 " + THAI['data_summary'])
        col1, col2 = st.columns(2)
        with col1:
            st.metric(THAI['data_rows'], len(st.session_state.df))
        with col2:
            st.metric(THAI['data_cols'], len(st.session_state.df.columns))

        if st.session_state.anova_results is not None:
            st.markdown("### 📈 ANOVA")
            st.metric("CV", f"{st.session_state.anova_results['cv']:.2f}%")
            st.metric("F-value", f"{st.session_state.anova_results['f_treatment']:.2f}")

    st.divider()
    st.markdown('<div class="footer">' + THAI['footer_made_with'] + '</div>', unsafe_allow_html=True)

# Main content
if page == THAI['nav_home']:
    # ============= HOME PAGE =============
    st.markdown(f"### {THAI['home_welcome']}")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"#### {THAI['home_description']}")
        st.markdown(f"{THAI['home_features']}")
        st.markdown(f"""
- {THAI['home_feature_design']}
- {THAI['home_feature_analysis']}
- {THAI['home_feature_charts']}
- {THAI['home_feature_export']}
- {THAI['home_feature_ai']}
        """)

    with col2:
        st.info("""
        **🚀 เริ่มต้นใช้งาน:**

        1️⃣ ไปที่ "นำเข้าข้อมูล" และอัปโหลดไฟล์ CSV
        2️⃣ เลือกคอลัมน์ที่ถูกต้อง
        3️⃣ ไปที่ "การวิเคราะห์ ANOVA" เพื่อวิเคราะห์
        4️⃣ ดูผลลัพธ์ในหน้า "แสดงผลข้อมูล"
        5️⃣ ส่งออก PDF หรือ Excel ในหน้า "รายงาน"
        """)

    st.divider()
    st.markdown("#### 📝 " + THAI['data_upload_help'])
    st.info("""
    ไฟล์ CSV ควรมีคอลัมน์:
    - **GEN** (Genotype/Treatment)
    - **REP** (Replication/Block)
    - **Y1** (Response/Yield)

    ตัวอย่าง:
    ```
    GEN,REP,Y1
    V1,1,45.2
    V2,1,48.5
    V1,2,46.1
    V2,2,49.3
    ```
    """)

elif page == THAI['nav_data_input']:
    # ============= DATA INPUT PAGE =============
    st.markdown(f"### {THAI['data_upload_title']}")

    uploaded_file = st.file_uploader(
        THAI['data_upload_label'],
        type=['csv'],
        help=THAI['data_upload_help']
    )

    if uploaded_file is not None:
        try:
            df, error = load_csv_file(uploaded_file)
            if error:
                st.error(f"{THAI['data_error']} {error}")
            else:
                st.session_state.df = df
                st.success(THAI['data_success'])

                st.markdown(f"#### {THAI['data_preview']}")
                st.dataframe(df.head(15), use_container_width=True)

                st.markdown(f"#### {THAI['data_summary']}")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(THAI['data_rows'], len(df))
                with col2:
                    st.metric(THAI['data_cols'], len(df.columns))
                with col3:
                    st.metric("Columns", ", ".join(df.columns.tolist()))

                st.divider()
                st.markdown("### " + THAI['col_treatment'])

                col1, col2, col3 = st.columns(3)

                with col1:
                    treatment_col = st.selectbox(
                        THAI['col_treatment'],
                        df.columns,
                        key="treatment_select",
                        label_visibility="collapsed"
                    )

                with col2:
                    replication_col = st.selectbox(
                        THAI['col_replication'],
                        df.columns,
                        key="replication_select",
                        label_visibility="collapsed"
                    )

                with col3:
                    response_col = st.selectbox(
                        THAI['col_response'],
                        df.columns,
                        key="response_select",
                        label_visibility="collapsed"
                    )

                if st.button(THAI['btn_submit'], key="validate_button"):
                    # Validate
                    is_valid, message = validate_rcbd_data(df, treatment_col, replication_col, response_col)

                    if is_valid:
                        st.session_state.treatment_col = treatment_col
                        st.session_state.replication_col = replication_col
                        st.session_state.response_col = response_col
                        st.success(message)

                        # Get design info
                        design_info = get_design_info(df, treatment_col, replication_col)
                        st.markdown("#### 📋 Design Information")
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Treatments", design_info['num_treatments'])
                        with col2:
                            st.metric("Replications", design_info['num_reps'])
                        with col3:
                            st.metric("Total Plots", design_info['total_plots'])
                        with col4:
                            st.metric("Balanced", "✓ Yes" if design_info['is_balanced'] else "✗ No")

                        if not design_info['is_balanced']:
                            st.warning("⚠️ ข้อมูลไม่สมดุล - อาจส่งผลต่อการวิเคราะห์")

                        # Summary stats
                        st.markdown("#### 📊 Summary Statistics")
                        stats = get_summary_stats(df, response_col, treatment_col)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Overall Mean", f"{stats['mean']:.2f}")
                        with col2:
                            st.metric("Std Dev", f"{stats['std']:.2f}")
                        with col3:
                            st.metric("SE", f"{stats['se']:.4f}")

                    else:
                        st.error(message)

        except Exception as e:
            st.error(f"{THAI['data_error']} {str(e)}")

elif page == THAI['nav_anova']:
    # ============= ANOVA ANALYSIS PAGE =============
    st.markdown(f"### {THAI['anova_title']}")

    if st.session_state.df is None:
        st.warning(THAI['msg_data_required'])
    elif st.session_state.treatment_col is None:
        st.warning("⚠️ ต้องทำให้ข้อมูลพร้อมใช้งานจากหน้า 'นำเข้าข้อมูล' ก่อน")
    else:
        st.success("✅ ข้อมูลพร้อมใช้งาน")

        # ANOVA settings
        col1, col2 = st.columns(2)
        with col1:
            alpha = st.slider("ระดับนัยสำคัญ (α):", 0.01, 0.20, 0.05, 0.01)

        if st.button(THAI['anova_table'], key="run_anova"):
            try:
                with st.spinner(THAI['msg_processing']):
                    results = run_rcbd_anova(
                        st.session_state.df,
                        st.session_state.treatment_col,
                        st.session_state.replication_col,
                        st.session_state.response_col,
                        alpha=alpha
                    )
                    st.session_state.anova_results = results

                st.success(THAI['msg_success'])

                # Display ANOVA table
                st.markdown("#### ANOVA Table")
                anova_display = results['anova_table'].copy()
                st.dataframe(anova_display, use_container_width=True)

                # Display statistics
                st.markdown("#### 📊 Statistical Summary")
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    sig = "***" if results['p_treatment'] < 0.001 else (
                        "**" if results['p_treatment'] < 0.01 else (
                            "*" if results['p_treatment'] < 0.05 else "ns"
                        )
                    )
                    st.metric("F-value", f"{results['f_treatment']:.2f} {sig}")

                with col2:
                    st.metric("P-value", f"{results['p_treatment']:.4f}")

                with col3:
                    st.metric("CV", f"{results['cv']:.2f}%")

                with col4:
                    quality = get_cv_quality(results['cv'])
                    st.metric("CV Quality", quality)

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Grand Mean", f"{results['grand_mean']:.2f}")
                with col2:
                    st.metric("MSE", f"{results['mse']:.4f}")
                with col3:
                    st.metric("LSD (0.05)", f"{results['lsd']:.2f}")

                # Significance interpretation
                st.markdown("#### 📈 Interpretation")
                if results['is_significant']:
                    st.success(f"✓ Treatment มีนัยสำคัญที่ α = {alpha} (P = {results['p_treatment']:.4f})")
                else:
                    st.info(f"✗ Treatment ไม่มีนัยสำคัญที่ α = {alpha} (P = {results['p_treatment']:.4f})")

                # Treatment means table
                st.markdown("#### ตารางค่าเฉลี่ย Treatment")
                means_display = results['treatment_means'].copy()
                means_display = means_display.round(4)
                st.dataframe(means_display, use_container_width=True)

            except Exception as e:
                st.error(f"{THAI['msg_error']}: {str(e)}")
                import traceback
                st.error(traceback.format_exc())

elif page == THAI['nav_visualization']:
    # ============= VISUALIZATION PAGE =============
    st.markdown(f"### {THAI['nav_visualization']}")

    if st.session_state.anova_results is None:
        st.warning("⚠️ ต้องทำการวิเคราะห์ ANOVA ก่อน")
    else:
        st.success("✅ ข้อมูลพร้อมแสดงผล")

        results = st.session_state.anova_results
        means_df = results['treatment_means']

        # Chart 1: Treatment means with error bars
        st.markdown("#### Mean Treatment with Standard Error")
        try:
            fig1 = create_means_with_error_bars(
                means_df,
                title=f"ค่าเฉลี่ย Treatment (ด้วย SE)",
                x_label=st.session_state.treatment_col,
                y_label=st.session_state.response_col
            )
            st.plotly_chart(fig1, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating chart: {str(e)}")

        # Chart 2: Box plot
        st.markdown("#### Distribution by Treatment")
        try:
            fig2 = create_box_plot(
                st.session_state.df,
                st.session_state.treatment_col,
                st.session_state.response_col,
                title="Box Plot ข้อมูล",
                x_label=st.session_state.treatment_col,
                y_label=st.session_state.response_col
            )
            st.plotly_chart(fig2, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating chart: {str(e)}")

        # Chart 3: Simple bar chart
        st.markdown("#### Treatment Means")
        try:
            fig3 = create_means_bar_chart(
                means_df,
                title="ค่าเฉลี่ย Treatment",
                x_label=st.session_state.treatment_col,
                y_label=st.session_state.response_col
            )
            st.plotly_chart(fig3, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating chart: {str(e)}")

# Footer
st.divider()
st.markdown(f"<div class='footer'>{THAI['footer_made_with']} | {THAI['footer_version']} {APP_VERSION}</div>", unsafe_allow_html=True)
