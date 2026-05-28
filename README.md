# Gurukula AI - Advanced Intelligence Engine for Karnataka Government Exams

A complete, production-ready scraping, analytics, and AI preparation platform focused on **KAS, PSI, FDA, SDA, and PDO** Karnataka state exams.

---

## ✨ Features

### Multi-Exam Support
- **KAS (Karnataka Administrative Service)**: Advanced flagship exam with full intelligence
- **PSI (Police Sub-Inspector)**: Complete support
- **FDA (First Division Assistant)**: Complete support
- **SDA (Second Division Assistant)**: Complete support
- **PDO (Panchayat Development Officer)**: Complete support

### Core Capabilities
1. **Intelligent Web Scraping**:
   - Exam metadata, syllabus, patterns, subject weightage
   - Previous Year Question Papers (PYQs) with automatic PDF download (with URL validation)
2. **Analytics Engine**:
   - Subject priority ranking
   - Revision priority per topic
   - PYQ frequency analysis
   - Preparation difficulty categorization
   - AI readiness rules
3. **Live Update Monitoring**:
   - Monitor KPSC official website for new content
   - Detect new notifications, syllabi, and PYQs
   - Track update history
4. **AI Agent Context Builder**:
   - Research Agent context
   - Planning Agent context
   - Revision Agent context
   - Insight Agent context
   - Ready to use with Gemini/OpenAI APIs
5. **Dataset Management**:
   - Standardized multi-exam directory structure
   - Old dataset structure cleanup
   - URL validation for resources
   - PDF validity checking

---

## 📁 Project Structure

```
gurukula_scraper/
├── config/
│   ├── __init__.py
│   └── exams.py                 # Exam definitions (KAS, PSI, FDA, SDA, PDO)
├── datasets/
│   ├── KAS/                     # All KAS data
│   │   ├── exams/
│   │   ├── syllabus/
│   │   ├── weightage/
│   │   ├── patterns/
│   │   ├── pyqs/
│   │   ├── raw/
│   │   ├── analytics/
│   │   └── agent_contexts/
│   ├── PSI/                     # All PSI data
│   ├── FDA/                     # All FDA data
│   ├── SDA/                     # All SDA data
│   └── PDO/                     # All PDO data
├── scrapers/
│   ├── metadata_scraper.py      # Scrape exam metadata
│   ├── syllabus_scraper.py      # Scrape/prepare syllabus
│   ├── weightage_scraper.py     # Scrape subject weightage
│   ├── pattern_scraper.py       # Scrape exam pattern
│   ├── pyq_scraper.py           # Scrape PYQs
│   ├── update_checker.py        # Monitor KPSC for updates
│   ├── agent_context_builder.py # Generate AI agent contexts
│   └── exam_manager.py          # Master orchestrator
├── utils/
│   ├── json_utils.py            # JSON helpers
│   ├── pdf_utils.py             # PDF download/extraction
│   ├── scraper_utils.py         # Web scraping helpers
│   ├── analytics_utils.py       # Analytics generation
│   ├── dataset_manager.py       # Dataset path management, URL validation
│   └── logger.py
├── requirements.txt
├── main.py                      # Entry point
├── migrate_kas_datasets.py      # (One-time) Migrate old KAS data
├── cleanup_old_datasets.py      # (One-time) Remove old directory structure
└── README.md
```

---

## 🚀 Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Full Multi-Exam System
This processes all 5 exams in order:
```bash
python main.py
```

### 3. Run a Single Exam Pipeline
```bash
python scrapers/exam_manager.py --exam KAS
python scrapers/exam_manager.py --exam PSI
python scrapers/exam_manager.py --exam FDA
python scrapers/exam_manager.py --exam SDA
python scrapers/exam_manager.py --exam PDO
```

### 4. Run Individual Components
```bash
# Metadata only
python scrapers/metadata_scraper.py --exam KAS

# Syllabus
python scrapers/syllabus_scraper.py --exam KAS

# Agent Contexts only
python scrapers/agent_context_builder.py
```

### 5. Check for Updates
```bash
python scrapers/update_checker.py
```

### 6. Cleanup (if needed)
```bash
# Clean up old directory structure (only once)
python cleanup_old_datasets.py
```

---

## 📊 AI Readiness

All agent contexts in `datasets/<EXAM>/agent_contexts/` are directly usable with LLMs!

### Example with Gemini
```python
import google.generativeai as genai
import json

# Load planning agent context
with open("datasets/KAS/agent_contexts/planning_agent_context.json") as f:
    context = json.load(f)

# Prompt the AI
prompt = f"""
Use this context to create a 3-month KAS preparation roadmap:
{json.dumps(context)}
"""

model = genai.GenerativeModel("gemini-1.5-pro")
response = model.generate_content(prompt)
print(response.text)
```

---

## 📝 License
MIT
