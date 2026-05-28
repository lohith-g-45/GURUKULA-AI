# Gurukula AI - Advanced Intelligence Engine for Karnataka Government Exams

A complete, production-ready scraping, analytics, and AI preparation platform focused on **KAS, PSI, FDA, SDA, and PDO** Karnataka state exams.

---

## ✨ Features

### Multi-Exam Support
- **KAS (Karnataka Administrative Service)** - Advanced flagship exam
- **PSI (Police Sub-Inspector)** - Full support
- **FDA (First Division Assistant)** - Full support
- **SDA (Second Division Assistant)** - Full support
- **PDO (Panchayat Development Officer)** - Full support

### Core Capabilities
1. **Intelligent Web Scraping**
   - Exam metadata, syllabus, patterns, subject weightage
   - Previous Year Question Papers (PYQs) with automatic PDF download
2. **Analytics Engine**
   - Subject priority ranking
   - Revision priority per topic
   - PYQ frequency analysis
   - Preparation difficulty categorization
   - AI readiness rules
3. **Live Update Monitoring**
   - Monitor KPSC official website for new content
   - Detect new notifications, syllabi, and PYQs
   - Track update history
4. **AI Agent Context Builder**
   - Research Agent context
   - Planning Agent context
   - Revision Agent context
   - Insight Agent context
   - Ready to use with Gemini/OpenAI APIs

---

## 📁 Project Structure

```
gurukula_scraper/
├── config/
│   ├── __init__.py
│   └── exams.py                 # Exam definitions (KAS, PSI, FDA, SDA, PDO)
├── datasets/
│   ├── KAS/
│   │   ├── exams/
│   │   ├── syllabus/
│   │   ├── weightage/
│   │   ├── patterns/
│   │   ├── pyqs/
│   │   ├── raw/
│   │   ├── analytics/
│   │   └── agent_contexts/
│   ├── PSI/
│   ├── FDA/
│   ├── SDA/
│   └── PDO/
├── scrapers/
│   ├── metadata_scraper.py
│   ├── syllabus_scraper.py
│   ├── weightage_scraper.py
│   ├── pattern_scraper.py
│   ├── pyq_scraper.py
│   ├── update_checker.py
│   ├── agent_context_builder.py
│   └── exam_manager.py          # Master orchestrator
├── utils/
│   ├── json_utils.py
│   ├── pdf_utils.py
│   ├── scraper_utils.py
│   ├── analytics_utils.py
│   └── logger.py
├── requirements.txt
├── main.py                      # Entry point (runs all exams)
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

### 3. Run a Specific Exam
Process only a single exam:
```bash
# Metadata only
python scrapers/metadata_scraper.py --exam KAS
python scrapers/metadata_scraper.py --exam PSI
python scrapers/metadata_scraper.py --exam FDA
python scrapers/metadata_scraper.py --exam SDA
python scrapers/metadata_scraper.py --exam PDO

# Syllabus
python scrapers/syllabus_scraper.py --exam PSI

# Full pipeline for one exam
# (use exam_manager programmatically)
```

---

## 📖 Usage Guides

### Update Monitoring
Check for new KPSC content:
```bash
python scrapers/update_checker.py
```

### AI Agent Contexts
Generate AI-ready context for Gemini/OpenAI:
```bash
python scrapers/agent_context_builder.py
```

---

## 🔧 Configuration & Customization

### Adding New Exams
1. Add exam definition to `config/exams.py`
2. Add curated data in respective scraper files
3. The system will automatically include it in the pipeline!

---

## 📊 AI Readiness

All agent contexts in `datasets/<exam>/agent_contexts/` are directly usable with LLMs!

### Example with Gemini
```python
import google.generativeai as genai
import json

with open("datasets/KAS/agent_contexts/planning_agent_context.json") as f:
    context = json.load(f)

prompt = f"Use this data to create a KAS study plan:\n{json.dumps(context)}"
model = genai.GenerativeModel("gemini-1.5-pro")
response = model.generate_content(prompt)
print(response.text)
```

---

## 📝 License
MIT
