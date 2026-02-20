# STAR-TH Development Guide

## Quick Start

### 1. Environment Setup
```bash
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the App
```bash
streamlit run app.py
```

### 3. Deploy to Streamlit Cloud
- Push to GitHub
- Connect repo at https://share.streamlit.io
- Deploy from branch `main`

---

## Project Architecture at a Glance

### Tech Stack (Why Each?)
- **Streamlit** — Zero HTML/CSS needed, perfect for beginners + interactive data apps
- **pandas/statsmodels/scipy** — Python replaces R for statistics
- **Plotly Express** — Interactive charts, minimal code
- **Claude API** — Thai language AI interpretation of results
- **ReportLab + openpyxl** — PDF/Excel export with Thai font support

### Core Modules (Development Order)

| Module | Purpose | Phase | Status |
|--------|---------|-------|--------|
| `config/settings.py` | Constants, Thai text, design types | Setup | - |
| `modules/data_manager.py` | CSV load/validate | Phase 1 | - |
| `modules/anova.py` | RCBD/CRD/Latin Square ANOVA | Phase 1 | - |
| `visualization/charts.py` | Plotly bar/box charts | Phase 1 | - |
| `pages/02_data_input.py` | File upload UI | Phase 1 | - |
| `pages/04_anova.py` | Main analysis workflow | Phase 1–2 | - |
| `modules/experimental_design.py` | Design generators | Phase 2 | - |
| `modules/mean_comparison.py` | Tukey/Duncan/LSD | Phase 2 | - |
| `export/pdf_report.py` | ReportLab PDF with IBM Plex Sans Thai font | Phase 2 | - |
| `export/excel_export.py` | openpyxl export | Phase 2 | - |
| `ai/claude_interpreter.py` | Claude API Thai interpretation | Phase 3 | - |
| `modules/gxe_analysis.py` | Multi-site stability analysis | Phase 3 | - |

---

## Development Phases

### Phase 1 (Weeks 1–8): MVP
**Goal:** Import rice data → ANOVA → Thai results + charts

**Key Files to Create:**
1. `app.py` — Streamlit entry point
2. `config/settings.py` — App constants
3. `config/thai_translations.py` — All Thai UI strings
4. `modules/data_manager.py` — CSV validation
5. `modules/anova.py` — RCBD ANOVA calculation
6. `visualization/charts.py` — Basic charts
7. `pages/02_data_input.py` — Upload interface
8. `pages/04_anova.py` — Analysis page

**Test with:** Sample RCBD rice data (treatment×rep → response)

---

### Phase 2 (Weeks 9–14): Full Features
Add design generators, mean comparison tests, PDF/Excel export

---

### Phase 3 (Weeks 15–22): AI Features
Add Claude Thai interpretation, GxE analysis, stability parameters

---

## Critical Functions by Module

### `modules/data_manager.py`
```python
load_csv_file(uploaded_file)
validate_rcbd_data(df, treatment_col, rep_col, response_col)
get_summary_stats(df, response_col)
```

### `modules/anova.py`
```python
run_rcbd_anova(df, treatment_col, rep_col, response_col)
# Returns: anova_table, treatment_means, CV, F-value, P-value
```

### `visualization/charts.py`
```python
create_means_bar_chart(means_df)
create_box_plot(df, response_col)
```

### `ai/claude_interpreter.py`
```python
interpret_anova_results_thai(anova_results, means_table, trait_name, design_type)
# Returns: 3–5 paragraphs Thai academic interpretation
```

---

## File Structure

```
STAR-TH/
├── app.py                          # Streamlit entry point
├── requirements.txt
├── .streamlit/secrets.toml         # API keys (NOT in git)
│
├── config/
│   ├── settings.py                 # App constants, crop types, designs
│   └── thai_translations.py        # All Thai strings
│
├── modules/
│   ├── data_manager.py             # CSV load/validate
│   ├── anova.py                    # ANOVA calculation
│   ├── experimental_design.py       # CRD/RCBD/Latin Square/Alpha Lattice
│   ├── mean_comparison.py           # LSD/Tukey/Duncan
│   └── gxe_analysis.py              # Multi-site stability
│
├── ai/
│   └── claude_interpreter.py        # Claude API integration
│
├── visualization/
│   └── charts.py                    # Plotly charts
│
├── export/
│   ├── pdf_report.py                # ReportLab PDF
│   └── excel_export.py              # openpyxl Excel
│
├── pages/
│   ├── 01_home.py                   # Landing page
│   ├── 02_data_input.py             # Upload & preview
│   ├── 03_experimental_design.py     # Design generator
│   ├── 04_anova.py                  # Main analysis
│   ├── 05_visualization.py          # Charts
│   └── 06_reports.py                # Export PDF/Excel
│
├── assets/fonts/
│   └── IBMPlexSansThai-Regular.ttf  # Thai font for PDF
│
└── data/
    └── sample_rice_data.csv         # Sample RCBD data
```

---

## Key Design Decisions

### 1. **RCBD is the default** for Thai rice trials
   - Blocks = replications (4 typical)
   - Treatments = rice varieties (8–15 typical)
   - Formula: `response ~ C(treatment) + C(rep)`

### 2. **Thai language everywhere**
   - UI labels, column headers, chart axes, PDF/Excel
   - All strings in `config/thai_translations.py` for i18n

### 3. **Streamlit session state** for data persistence
   ```python
   if 'df' not in st.session_state:
       st.session_state.df = None
   ```

### 4. **Claude API for Thai academic interpretation**
   - Use `claude-sonnet-4-6` (best Thai support, cost-effective)
   - Prompt: "You are a Thai agricultural scientist. Interpret these results..."
   - Cost: ~฿0.10 per interpretation (acceptable for university use)

### 5. **Supabase for cloud storage**
   - Free tier: 500MB DB, 50MB storage (enough for 1000+ projects)
   - Schema: `projects(id, project_name, user_id, created_at, data_json, results_json)`

---

## Testing Checklist

### Phase 1 MVP Test
- [ ] Upload sample RCBD CSV (8 treatments × 4 reps)
- [ ] Select correct columns (GEN, REP, Y1)
- [ ] ANOVA runs and F-value matches manual calculation
- [ ] Thai labels appear in all UI elements
- [ ] Download CSV of means works
- [ ] Bar chart and box plot render correctly

### Phase 2 Test
- [ ] Generate RCBD layout (8 treatments, 4 reps) → verify each block has 8 plots
- [ ] Run Duncan test → verify letter groupings (e.g., A, AB, BC, C)
- [ ] Download PDF → verify Thai font (IBM Plex Sans Thai) renders correctly
- [ ] Download Excel → verify sheets (raw data, means, ANOVA table)

### Phase 3 Test
- [ ] Run Claude AI interpretation → verify Thai academic text
- [ ] Upload multi-site RCBD (3 provinces) → verify GxE heatmap
- [ ] Stability analysis → verify bi ≈ 1 varieties labeled as stable

---

## Dependencies Reference

```
streamlit==1.31.0          # Web framework
pandas==2.1.4              # Data manipulation
numpy==1.26.3              # Arrays
scipy==1.11.4              # Stats functions (distributions, etc.)
statsmodels==0.14.1        # ANOVA, regressions
pingouin==0.5.3            # Pairwise tests
plotly==5.18.0             # Interactive charts
anthropic==0.18.1          # Claude API
reportlab==4.1.0           # PDF with Thai font
openpyxl==3.1.2            # Excel export
scikit-posthocs==0.8.1     # Duncan, Dunn, etc.
python-dotenv==1.0.0       # .env file support
```

---

## API Keys & Configuration

### Streamlit Secrets (`.streamlit/secrets.toml`)
```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

### GitHub Secrets (for CI/CD)
- `ANTHROPIC_API_KEY`

---

## Common Commands

```bash
# Create pages directory
mkdir -p pages

# Create config directory
mkdir -p config modules visualization export ai assets/fonts

# Run app locally
streamlit run app.py

# Lint code (optional)
pip install black flake8
black . --line-length=100
flake8 .

# Requirements snapshot
pip freeze > requirements.txt

# Deploy updates
git add .
git commit -m "Phase 1: MVP ANOVA"
git push origin main
# Streamlit Cloud auto-deploys from main
```

---

## Next Steps

1. **Create `app.py`** — Streamlit title, sidebar, page navigation
2. **Create `config/settings.py`** — App constants and design types
3. **Create `config/thai_translations.py`** — All Thai text strings
4. **Create `modules/data_manager.py`** — CSV loading and validation
5. **Create `modules/anova.py`** — RCBD ANOVA calculation (statsmodels)
6. **Test Phase 1** with sample rice data

---

## Resources

- **Streamlit** — https://docs.streamlit.io
- **statsmodels ANOVA** — https://www.statsmodels.org/stable/generated/statsmodels.formula.api.ols.html
- **Plotly** — https://plotly.com/python/
- **Claude API** — https://docs.anthropic.com/claude/reference/getting-started-with-the-api
- **ReportLab Thai** — https://www.reportlab.com/docs/reportlab-userguide.pdf
