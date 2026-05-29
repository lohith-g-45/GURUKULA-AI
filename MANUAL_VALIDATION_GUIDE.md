
# GURUKULA AI - Manual Validation Guide
This guide provides step-by-step instructions to manually validate the complete GURUKULA AI KAS preparation platform.

---

## 1. Project Structure Validation
- [ ] Verify the project root directory contains `datasets/KAS/`
- [ ] Check that all expected subdirectories exist under `datasets/KAS/`:
  - [ ] `agent_contexts/`
  - [ ] `analytics/`
  - [ ] `exams/`
  - [ ] `intelligence/`
  - [ ] `patterns/`
  - [ ] `planning/`
  - [ ] `prompts/`
  - [ ] `pyqs/`
  - [ ] `raw/`
  - [ ] `recommendations/`
  - [ ] `syllabus/`
  - [ ] `weightage/`

---

## 2. JSON File Validation (Manual Spot-Check)
For each JSON file in `datasets/KAS/`, perform these checks:
1. Open the file in a text editor or JSON viewer
2. Verify it's valid JSON (no syntax errors)
3. Spot-check the content for reasonableness

### Key Files to Validate:
#### Analytics:
- [ ] `kas_pyq_metadata.json`: Check it contains real PYQ data
- [ ] `kas_question_distribution.json`: Verify question counts per subject/year
- [ ] `kas_subject_weightage.json`: Check subject weightages add up logically
- [ ] `kas_topic_frequency.json`: Verify topic frequencies are reasonable

#### Intelligence:
- [ ] `consistency_rules.json`: Check daily streak rules
- [ ] `readiness_rules.json`: Verify study hour rules
- [ ] `risk_rules.json`: Check risk factor calculations
- [ ] `scoring_formulas.json`: Verify formulas make sense

#### Recommendations:
- [ ] `recommendation_engine.json`: Check student type recommendations are logical
- [ ] `recommendation_priority_rules.json`: Verify priority scoring thresholds

#### Planning:
- [ ] `roadmap_rules.json`: Check roadmap phases
- [ ] `study_planning_rules.json`: Verify daily schedule templates
- [ ] `revision_cycles.json`: Check spaced repetition intervals

---

## 3. Prompt File Validation
For each prompt in `datasets/KAS/prompts/`:
- [ ] Open the file and read it carefully
- [ ] Verify it has a clear role definition
- [ ] Check it contains critical instructions
- [ ] Verify it has a JSON output format specified
- [ ] Confirm it lists key focus areas and tasks

#### Prompt Files:
- [ ] `insight_prompt.txt`: Insight Agent
- [ ] `planning_prompt.txt`: Planning Agent
- [ ] `research_prompt.txt`: Research Agent
- [ ] `revision_prompt.txt`: Revision Agent

---

## 4. Data Consistency Validation
### Subject Weightage Consistency
Compare these three files to ensure they have the same subject weightages:
- [ ] `datasets/KAS/analytics/kas_subject_weightage.json`
- [ ] `datasets/KAS/weightage/kas_weightage.json`
- [ ] `datasets/KAS/recommendations/recommendation_engine.json` (subject_weightage section)

### Priority Label Consistency
Verify all files use the same priority labels:
- [ ] "Very High"
- [ ] "High"
- [ ] "Medium"
- [ ] "Low"

### Exam Stage Consistency
Check files clearly separate Prelims and Mains:
- [ ] `analytics/kas_question_distribution.json`
- [ ] `planning/study_planning_rules.json`
- [ ] `recommendations/recommendation_engine.json`

---

## 5. Adaptive Logic Validation
### Readiness Engine
- [ ] Check readiness rules account for study hours, consistency, and weak subjects
- [ ] Verify scoring formulas include diminishing returns

### Recommendation Engine
- [ ] Check recommendations vary by student type (weak/average/strong/burnout risk)
- [ ] Verify recommendations prioritize high-weightage subjects
- [ ] Check burnout recovery rules exist

### Planning Engine
- [ ] Verify roadmap phases adjust based on readiness/consistency
- [ ] Check subject interleaving rules prevent consecutive heavy subjects
- [ ] Verify fatigue-aware scheduling includes breaks

---

## 6. PYQ & Syllabus Validation
- [ ] Check `pyqs/KAS_pyqs.json` contains real KAS previous year questions
- [ ] Verify `syllabus/kas_syllabus.json` covers all KAS subjects
- [ ] Check `raw/KAS_syllabus_raw.json` is present as a backup

---

## 7. Backend Compatibility Check
- [ ] All JSON files use consistent schemas
- [ ] All prompts output JSON for easy backend integration
- [ ] No hardcoded values that would break backend systems
- [ ] All files are UTF-8 encoded

---

## 8. Final Overall Check
- [ ] No dummy or hallucinated data (all based on real KAS PYQs)
- [ ] All adaptive systems preserved
- [ ] No broken links or invalid references
- [ ] Project is well-organized and easy to navigate

---

## Validation Complete!
If all checks pass, the project is ready for integration!
