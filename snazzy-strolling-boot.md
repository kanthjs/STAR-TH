# STAR-TH: Modern Statistical Tool for Thai Agricultural Research

## Context

**What is STAR?**
STAR (Statistical Tool for Agricultural Research) is a 2014 software by IRRI built on Eclipse RCP + Java + R. It provides experimental design generation (CRD, RCBD, Latin Square, Alpha Lattice, Split Plot, etc.) and ANOVA analysis for crop breeding trials. It is no longer updated but is valued for its ease of use.

**Goal**
Build **STAR-TH** — a modernized web app version for Thai agricultural researchers (university/graduate level), focusing on rice (ข้าว) with Thai language UI and reports, plus modern features: AI result interpretation in Thai, cloud storage, interactive charts, and Excel/PDF export.

**Developer level:** Beginner (little/no coding experience)

---

## Recommended Tech Stack

| Layer | Tool | Reason |
|---|---|---|
| Web Framework | **Streamlit** | Python → web app with zero HTML/CSS needed |
| Statistics | **statsmodels + scipy + pingouin** | Replaces R backend; simple Python functions |
| Charts | **Plotly Express** | Interactive charts, one line per chart |
| AI Interpretation | **Claude API** (`claude-sonnet-4-6`) | Best Thai language support for result explanation |
| Cloud Storage | **Supabase** (free tier) | PostgreSQL DB with simple Python SDK |
| PDF Export | **ReportLab** | Thai font (THSarabunNew) support |
| Excel Export | **openpyxl** | Standard Python Excel library |
| Hosting | **Streamlit Community Cloud** | Free, deploy from GitHub in minutes |

---

## Project File Structure

```
STAR-TH/
├── app.py                          # Main Streamlit entry point
├── requirements.txt
├── .streamlit/secrets.toml         # API keys (NOT committed to git)
├── config/
│   ├── settings.py                 # App constants, crop types, design types
│   └── thai_translations.py        # All Thai UI strings
├── modules/
│   ├── data_manager.py             # CSV import/export, data validation
│   ├── experimental_design.py      # CRD, RCBD, Latin Square, Alpha Lattice generators
│   ├── anova.py                    # ANOVA analysis (RCBD, CRD, Latin Square, Split Plot)
│   ├── mean_comparison.py          # LSD, Tukey HSD, Duncan's DMRT
│   └── gxe_analysis.py             # Combined ANOVA + Eberhart-Russell stability
├── ai/
│   └── claude_interpreter.py       # Claude API: Thai result interpretation
├── visualization/
│   └── charts.py                   # Plotly bar charts, box plots, GxE heatmap
├── export/
│   ├── pdf_report.py               # ReportLab PDF with Thai font
│   └── excel_export.py             # openpyxl Excel export
├── storage/
│   └── supabase_client.py          # Save/load projects to cloud
├── pages/
│   ├── 01_home.py                  # Thai landing page
│   ├── 02_data_input.py            # File upload and data preview
│   ├── 03_experimental_design.py   # Design generator UI
│   ├── 04_anova.py                 # Main ANOVA analysis page (central workflow)
│   ├── 05_visualization.py         # Charts page
│   └── 06_reports.py               # Export and cloud save
├── assets/fonts/THSarabunNew.ttf   # Thai font for PDF
└── data/sample_rice_data.csv       # Sample rice trial data
```

---

## Phased Implementation Plan

### Phase 1 — MVP (Weeks 1–8): Core working app

**Goal:** Import rice trial data → run ANOVA → see Thai results + charts

**Steps:**

1. **Setup (Week 1–2)**
   - Install: Python 3.11, VS Code, Git
   - `pip install streamlit pandas scipy statsmodels plotly pingouin`
   - Create `app.py` with Thai title and layout
   - Run: `streamlit run app.py`

2. **Data Import Module (Week 3–4)** → `modules/data_manager.py`
   - `load_csv_file(uploaded_file)` — reads CSV, returns DataFrame + error
   - `validate_rcbd_data(df, treatment_col, rep_col, response_col)` — checks columns/nulls
   - `get_summary_stats(df, response_col)` — Thai-labeled descriptive stats
   - Page: `pages/02_data_input.py` — `st.file_uploader()` + data preview table

3. **ANOVA Module (Week 5–6)** → `modules/anova.py`
   - `run_rcbd_anova(df, treatment_col, rep_col, response_col)` — uses `statsmodels.formula.api.ols`
   - Returns: ANOVA table, treatment means, CV, F-value, P-value, significance flag
   - Formula: `response ~ C(treatment) + C(rep)`

4. **Charts + First Deploy (Week 7–8)** → `visualization/charts.py`
   - `create_means_bar_chart()` — Plotly bar chart with Thai labels
   - `create_box_plot()` — distribution check
   - Deploy to Streamlit Community Cloud (free) via GitHub

---

### Phase 2 — Full Features (Weeks 9–16): All STAR features + cloud

5. **Experimental Design Generator (Week 9–10)** → `modules/experimental_design.py`
   - `generate_crd(treatments, replications)` — shuffled plot list
   - `generate_rcbd(treatments, replications)` — blocks with randomized treatments (most common for Thai rice trials)
   - `generate_latin_square(treatments)` — permuted n×n square
   - `generate_alpha_lattice(treatments, replications, block_size)` — for large trials (50+ genotypes)
   - Page: `pages/03_experimental_design.py` — input form → show layout table → download CSV

6. **Mean Comparison Tests (Week 11–12)** → `modules/mean_comparison.py`
   - `run_tukey_hsd()` — `statsmodels.stats.multicomp.pairwise_tukeyhsd`
   - `run_duncan_test()` — via `scikit-posthocs`
   - `run_lsd_test()` — via `pingouin.pairwise_tests()`
   - `create_means_table_with_letters()` — standard Thai journal format (mean + letter grouping + SE)

7. **Cloud Storage (Week 13–14)** → `storage/supabase_client.py`
   - `save_project(project_name, df, results)` — JSON serialize to Supabase `projects` table
   - `load_project(project_id)` — restore df + results from cloud
   - `list_user_projects()` — show saved projects sidebar
   - Supabase SQL schema: `projects(id, project_name, user_id, created_at, data_json, results_json)`

8. **PDF + Excel Export (Week 15–16)** → `export/pdf_report.py`, `export/excel_export.py`
   - Register `THSarabunNew.ttf` for Thai text in ReportLab
   - `generate_anova_report()` — full PDF: project info → ANOVA table → means table → CV + significance
   - Excel: raw data sheet + means sheet + ANOVA table sheet

---

### Phase 3 — AI Features (Weeks 17–24): Claude integration + GxE

9. **Claude AI Interpretation (Week 17–18)** → `ai/claude_interpreter.py`
   - `interpret_anova_results_thai(anova_results, means_table, trait_name, design_type, crop_type)`
     - Sends structured Thai prompt with all numerical results to `claude-sonnet-4-6`
     - Prompt instructs: interpret significance, rank varieties, assess CV quality, give Thai research-paper-style text
     - Returns 3–5 paragraph Thai academic interpretation
   - `get_design_recommendation_thai(num_treatments, num_replications, field_conditions)`
     - AI recommends which design to use based on conditions
   - `explain_statistical_concept_thai(concept)` — in-app help/tutorial in Thai

10. **GxE Analysis (Week 19–20)** → `modules/gxe_analysis.py`
    - `run_combined_anova(df, site_col, gen_col, rep_col, response_col)` — across multiple provinces
    - `calculate_stability_parameters(df, ...)` — Eberhart-Russell bi and S²d
    - `interpret_stability(bi, s2d)` — Thai stability label per variety
    - `create_gxe_heatmap()` — Plotly heatmap (varieties × environments)

11. **Complete ANOVA Page Integration (Week 21–22)** → `pages/04_anova.py`
    - Full workflow in one page: column selection → run ANOVA → view table → charts → AI interpretation → export
    - Uses `st.session_state` to pass data between pages

12. **Polish + Settings (Week 23–24)** → `config/settings.py`
    - Thai province list for site names
    - CV quality thresholds (excellent <10%, good 10–15%, acceptable 15–20%, poor >20%)
    - Crop type list, design type labels (Thai + English)
    - App version, Claude model constant (`claude-sonnet-4-6`)

---

## STAR Feature → STAR-TH Mapping

| STAR (Java/R) | STAR-TH (Python) |
|---|---|
| CRD / RCBD / Latin Square design | `modules/experimental_design.py` |
| Alpha Lattice design | `modules/experimental_design.py` |
| ANOVA (all designs) | `modules/anova.py` via statsmodels |
| LSD / Tukey / Duncan | `modules/mean_comparison.py` |
| GxE / Combined ANOVA | `modules/gxe_analysis.py` |
| CSV import | `st.file_uploader()` |
| PDF report | `export/pdf_report.py` ReportLab |
| Static bar charts | Plotly interactive charts |
| **NEW** Thai AI interpretation | `ai/claude_interpreter.py` Claude API |
| **NEW** Cloud project save | `storage/supabase_client.py` Supabase |
| **NEW** Excel export | `export/excel_export.py` openpyxl |

---

## Key Dependencies (requirements.txt)

```
streamlit==1.31.0
pandas==2.1.4
numpy==1.26.3
scipy==1.11.4
statsmodels==0.14.1
pingouin==0.5.3
plotly==5.18.0
anthropic==0.18.1
supabase==2.3.4
reportlab==4.1.0
openpyxl==3.1.2
scikit-posthocs==0.8.1
python-dotenv==1.0.0
```

---

## Cost (Free for University Use)

| Service | Free Tier |
|---|---|
| Streamlit Community Cloud | 1 app, unlimited users |
| Supabase | 500MB DB, 50MB storage |
| GitHub | Free public/private repos |
| Claude API | Pay-per-use ~฿0.10/interpretation |

---

## Verification (How to Test Each Phase)

**Phase 1:**
- Upload `C:\STAR\Projects\SampleProject\Data\MasterData.csv`
- Select: GEN=treatment, REP=rep, Y1=response
- Run ANOVA → verify F-value and P-value match known results
- Confirm Thai labels appear correctly in all UI elements

**Phase 2:**
- Generate RCBD with 8 treatments, 4 reps → verify each block has 8 plots, all treatments present
- Run Duncan's test → verify letter groupings match manual calculation
- Save project to Supabase → reload and verify data integrity
- Download PDF → open and verify Thai font renders correctly

**Phase 3:**
- Run AI interpretation → verify response is in Thai academic style
- Test with multi-environment data (MasterData.csv has 3 sites) → verify GxE heatmap shows
- Run stability analysis → verify bi≈1 varieties are labeled as stable

---

## Learning Path for Beginner

1. **Python basics** — python.org/about/gettingstarted
2. **Streamlit** — docs.streamlit.io (30-min quickstart)
3. **Pandas** — pandas.pydata.org/docs/getting_started
4. **Git** — learngitbranching.js.org
5. **Claude API** — docs.anthropic.com
6. **Thai community** — Facebook group "Python Thailand"
