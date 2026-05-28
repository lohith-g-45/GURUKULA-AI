# Gurukula AI - Advanced Intelligence Engine for Karnataka Government Exams

A complete, production-ready scraping, analytics, and AI preparation platform focused on Karnataka Administrative Service (KAS) and other state government exams.

---

## ✨ Features

1. **Intelligent Web Scraping**:
   - KAS Metadata (from official KPSC and reliable sources)
   - Comprehensive Syllabus (with subjects, topics, subtopics)
   - Subject Weightage & Exam Pattern
   - Previous Year Question Papers (PDFs included)

2. **Analytics Engine**:
   - Subject Priority Ranking
   - Revision Priority per Topic
   - PYQ Frequency Analysis
   - Preparation Difficulty Categorization
   - Readiness Rules for AI Agents

3. **Live Update Monitoring**:
   - Monitor KPSC website for new notifications
   - Detect new syllabus/PYQ PDFs
   - Keep track of update history
   - Generate alerts when new content is available

4. **AI Agent Context Builder**:
   - Research Agent Context (for syllabus & pattern analysis)
   - Planning Agent Context (for roadmap generation)
   - Revision Agent Context (for practice scheduling)
   - Insight Agent Context (for trend analysis)
   - Full Agent Context (complete dataset)

---

## 📁 Project Structure

```
gurukula_scraper/
├── datasets/
│   ├── exams/                 # Exam metadata (kas_metadata.json)
│   ├── syllabus/              # Structured syllabus (json + optional pdf)
│   ├── weightage/             # Subject weightage per stage
│   ├── patterns/              # Exam pattern details
│   ├── pyqs/                  # PYQ PDFs + metadata (kas_pyqs.json)
│   ├── raw/                   # Raw extracted syllabus text
│   ├── analytics/             # AI-ready analytics datasets
│   ├── updates/               # Update monitoring history + new content
│   └── agent_contexts/        # AI agent contexts for Gemini/OpenAI
├── scrapers/
│   ├── metadata_scraper.py
│   ├── syllabus_scraper.py
│   ├── weightage_scraper.py
│   ├── pattern_scraper.py
│   ├── pyq_scraper.py
│   ├── update_checker.py
│   └── agent_context_builder.py
├── utils/
│   ├── json_utils.py
│   ├── pdf_utils.py
│   ├── scraper_utils.py
│   ├── analytics_utils.py
│   └── logger.py
├── requirements.txt
├── main.py
└── README.md
```

---

## 🚀 Quick Start Guide

### 1. Install Dependencies
First, ensure you have Python 3.8+ installed, then run:
```bash
pip install -r requirements.txt
```

### 2. Run the Full System
This performs **all steps** in order: update check → scraping → analytics → agent context generation!
```bash
python main.py
```

---

## 📖 Individual Usage Guides

### A. Update Monitoring
Check KPSC website for new notifications, syllabi, or PYQs:
```bash
python scrapers/update_checker.py
```
This will:
- Look for new content
- Compare with previous state
- Generate alerts
- Save update history in `datasets/updates/`

### B. Run a Specific Scraper
Run any scraper individually if you only need to update one dataset:
```bash
python scrapers/metadata_scraper.py
python scrapers/syllabus_scraper.py
python scrapers/weightage_scraper.py
python scrapers/pattern_scraper.py
python scrapers/pyq_scraper.py
```

### C. Build AI Agent Contexts
Generate structured context ready for AI APIs (Gemini/OpenAI):
```bash
python scrapers/agent_context_builder.py
```
This creates:
- `research_agent_context.json`: For syllabus & pattern research
- `planning_agent_context.json`: For roadmap generation
- `revision_agent_context.json`: For practice scheduling
- `insight_agent_context.json`: For trend analysis
- `full_agent_context.json`: Complete combined dataset

---

## 🔧 Configuration & Customization

### Adding New Exams
The system is modular! To add support for other Karnataka exams (PSI, FDA, SDA, PDO):
1. Create new scraper files in `scrapers/` (copy existing ones and adjust)
2. Add corresponding analytics/context builders
3. Update `main.py` to include the new exam

### Modifying Scraping Sources
Check the individual scraper files and update the `url` variables to point to your preferred sources.

---

## 📊 AI Readiness

All datasets in `datasets/agent_contexts/` are **directly usable** as context for LLMs!

### Example Use with Gemini API
```python
import google.generativeai as genai
import json

# Load planning agent context
with open("datasets/agent_contexts/planning_agent_context.json") as f:
    context = json.load(f)

# Prompt the AI
prompt = f"""
Use this context to generate a 3-month KAS preparation roadmap:
{json.dumps(context, indent=2)}
"""

model = genai.GenerativeModel("gemini-1.5-pro")
response = model.generate_content(prompt)
print(response.text)
```

---

## 📝 Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Commit and push
5. Open a Pull Request

---

## 📜 License
MIT

---

## 🤝 Acknowledgements
- KPSC (Karnataka Public Service Commission) for official content
- Reliable educational platforms for reference material
- Open-source community for libraries used

---

## 🛠️ Troubleshooting
- If scraping fails, check your internet connection or update the source URLs
- If PDFs don't download, verify the PDF links are still active
- For any other issues, open a GitHub Issue!
