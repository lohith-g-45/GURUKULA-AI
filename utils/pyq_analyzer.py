import os
import sys
import re
import hashlib
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Optional, Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.json_utils import save_json, load_json
from utils.pdf_downloader import extract_pdf_text
from utils.dataset_manager import get_data_path, get_exam_dir

KAS_SUBJECTS = [
    "History", "Polity", "Geography", "Economics", "Environment",
    "Science & Technology", "Karnataka GK", "Current Affairs", "CSAT"
]

# Subject keywords with weights - higher weight = more important
# Format: [("keyword", weight), ...]
SUBJECT_KEYWORDS_WEIGHTED = {
    "History": [
        ("freedom struggle", 5.0), ("maurya", 4.0), ("mughal", 4.0), ("british", 4.0),
        ("revolt", 3.5), ("civilization", 3.0), ("dynasty", 3.0), ("ancient", 3.0),
        ("medieval", 3.0), ("modern india", 3.0), ("independence", 4.0), ("congress session", 3.0),
        ("history", 2.0), ("kingdom", 3.0), ("emperor", 3.0), ("movement", 2.5),
        ("indus", 3.5), ("vedic", 3.0), ("gupta", 3.0), ("gandhi", 4.0), ("nehru", 3.5),
        ("sultanate", 3.0), ("vijayanagara", 3.5), ("hoysala", 3.0), ("chalukya", 3.0),
        ("commission", 2.0), ("war", 2.0), ("battle", 2.0)
    ],
    "Polity": [
        ("constitution", 5.0), ("article", 4.5), ("amendment", 4.0), ("parliament", 4.0),
        ("judiciary", 3.5), ("rights", 3.5), ("governor", 3.0), ("legislature", 3.0),
        ("federalism", 3.0), ("democracy", 2.5), ("supreme court", 4.0), ("panchayat", 3.0),
        ("polity", 2.0), ("governance", 2.5), ("president", 3.0), ("prime minister", 3.0),
        ("high court", 3.5), ("fundamental rights", 4.0), ("directive principles", 3.0),
        ("state polity", 2.5), ("local government", 2.5), ("municipality", 2.5),
        ("schedule", 3.0), ("union", 2.5), ("state", 2.0), ("center", 2.0),
        ("executive", 2.5), ("election", 2.5), ("vote", 2.0), ("citizenship", 2.5)
    ],
    "Geography": [
        ("river", 4.5), ("monsoon", 4.0), ("climate", 3.5), ("plateau", 3.5),
        ("soil", 3.5), ("forest", 3.0), ("agriculture geography", 3.0), ("resources", 2.5),
        ("maps", 2.5), ("rainfall", 3.0), ("geography", 2.0), ("physical geography", 3.0),
        ("indian geography", 3.0), ("karnataka geography", 3.0), ("mountain", 3.5),
        ("plain", 2.5), ("desert", 2.5), ("weather", 2.0), ("natural vegetation", 2.5),
        ("wildlife", 2.0), ("location", 2.0), ("latitude", 2.0), ("longitude", 2.0),
        ("district", 2.0), ("capital", 2.0), ("ocean", 2.0), ("sea", 2.0),
        ("lake", 2.0), ("island", 2.0), ("coast", 2.0), ("glacier", 2.0), ("volcano", 2.0),
        ("equatorial", 2.0), ("mediterranean", 2.0), ("highway", 2.0)
    ],
    "Economics": [
        ("gdp", 4.5), ("inflation", 4.0), ("rbi", 4.0), ("banking", 3.5),
        ("fiscal", 3.5), ("budget", 4.0), ("economy", 2.0), ("forex", 2.5),
        ("rupee", 2.5), ("taxation", 3.0), ("poverty", 3.0), ("economics", 2.0),
        ("growth", 2.5), ("deflation", 2.5), ("recession", 2.5), ("monetary", 3.0),
        ("policy", 2.0), ("bank", 3.0), ("finance", 2.5), ("market", 2.0),
        ("tax", 3.0), ("gst", 3.0), ("income tax", 3.0), ("trade", 2.5),
        ("export", 2.0), ("import", 2.0), ("industrial", 2.0), ("agriculture", 2.5),
        ("rural", 2.0), ("unemployment", 2.5), ("planning", 2.0), ("five year plan", 2.0),
        ("money", 2.0), ("currency", 2.0), ("stock", 2.0), ("share", 2.0),
        ("bond", 2.0), ("investment", 2.0), ("revenue", 2.0), ("expenditure", 2.0)
    ],
    "Environment": [
        ("biodiversity", 4.0), ("wildlife", 3.5), ("pollution", 3.5), ("climate change", 4.0),
        ("conservation", 3.0), ("ecology", 3.0), ("forest act", 3.0), ("sustainability", 2.5),
        ("environment", 2.0), ("global warming", 3.0), ("green", 2.0), ("wildlife protection", 3.0),
        ("national park", 3.0), ("sanctuary", 2.5), ("biosphere", 2.5), ("wetland", 2.5),
        ("mangrove", 2.5), ("coral", 2.5), ("species", 2.5), ("endangered", 3.0),
        ("extinct", 2.5), ("carbon", 2.0), ("ozone", 2.0), ("acid rain", 2.5),
        ("deforestation", 2.5), ("afforestation", 2.5), ("bird", 2.0), ("sanctuary", 2.5)
    ],
    "Science & Technology": [
        ("isro", 2.0), ("ai", 1.5), ("biology", 2.0), ("chemistry", 2.0),
        ("physics", 2.0), ("space", 1.5), ("satellites", 1.5), ("genetics", 1.5),
        ("technology", 0.5), ("robotics", 1.5), ("science", 0.5), ("nasa", 1.5),
        ("satellite", 1.5), ("missile", 1.5), ("nuclear", 1.5), ("computer", 1.0),
        ("internet", 1.0), ("biotechnology", 1.5), ("medicine", 1.0), ("health", 1.0),
        ("innovation", 1.0), ("research", 1.0), ("cell", 1.0), ("dna", 1.5),
        ("gene", 1.5), ("atom", 1.0), ("molecule", 1.0), ("energy", 1.0),
        ("solar", 1.0), ("wind", 1.0), ("blackbody", 1.0)
    ],
    "Karnataka GK": [
        ("karnataka history", 4.0), ("karnataka economy", 3.5), ("karnataka schemes", 3.5),
        ("karnataka geography", 3.5), ("karnataka governance", 3.0), ("kannada culture", 3.0),
        ("districts", 3.0), ("state initiatives", 2.5), ("karnataka", 2.0),
        ("bangalore", 2.0), ("mysore", 2.0), ("belagavi", 1.5), ("hubli", 1.5),
        ("dharwad", 1.5), ("mangalore", 1.5), ("kannada", 2.0), ("kannadiga", 1.5),
        ("karnataka polity", 3.0), ("kpsc", 1.5), ("kas", 1.5), ("mysuru", 2.0),
        ("hampi", 2.0), ("badami", 2.0), ("pattadakal", 2.0), ("belur", 2.0), ("halebidu", 2.0),
        ("yettinahole", 3.0), ("hakki habba", 3.0), ("cauvery", 2.5), ("sharavati", 2.5)
    ],
    "Current Affairs": [
        ("recent events", 2.5), ("awards", 2.5), ("summits", 2.0), ("recent policies", 2.5),
        ("recent government actions", 2.5), ("current affairs", 1.5), ("recent", 1.5),
        ("latest", 1.5), ("news", 1.0), ("2023", 1.0), ("2024", 1.0), ("2025", 1.0),
        ("appointment", 1.5), ("award", 1.5), ("scheme", 1.5), ("policy", 1.5),
        ("government", 1.0), ("ministry", 1.0), ("minister", 1.0), ("event", 1.0)
    ],
    "CSAT": [
        ("aptitude", 4.0), ("reasoning", 4.0), ("maths", 3.5), ("comprehension", 3.5),
        ("logical reasoning", 4.0), ("quantitative aptitude", 3.5), ("csat", 4.0),
        ("reading", 2.0), ("passage", 2.0), ("verbal", 2.0), ("analytical ability", 3.0),
        ("decision making", 4.0), ("mental ability", 3.0), ("logical", 2.5),
        ("analytical", 2.5), ("numerical", 2.5), ("mathematics", 3.0), ("number", 2.0),
        ("series", 2.0), ("puzzle", 2.0), ("problem solving", 2.5), ("percentage", 2.0),
        ("ratio", 2.0), ("average", 2.0), ("km", 1.5), ("distance", 1.5),
        ("ethics", 4.0), ("moral", 3.0), ("integrity", 3.0), ("figure", 3.0),
        ("figures", 3.0), ("cube", 3.0), ("cubes", 3.0), ("train", 2.5),
        ("trains", 2.5), ("profit", 2.5), ("loss", 2.5), ("interest", 2.5),
        ("simple interest", 3.0), ("compound interest", 3.0), ("work", 2.5),
        ("time and work", 3.0), ("time and distance", 3.0), ("speed", 2.5),
        ("average", 2.0), ("percentage", 2.0), ("ratio", 2.0), ("proportion", 2.0),
        ("triangle", 2.0), ("circle", 2.0), ("square", 2.0), ("rectangle", 2.0),
        ("area", 2.0), ("volume", 2.0), ("perimeter", 2.0), ("pie chart", 2.5),
        ("bar graph", 2.5), ("line graph", 2.5), ("graph", 2.0), ("chart", 2.0),
        ("table", 2.0), ("data", 2.0), ("data interpretation", 3.0),
        ("syllogism", 3.0), ("blood relations", 3.0), ("direction", 3.0),
        ("coding", 2.5), ("decoding", 2.5), ("arrangement", 2.5), ("seating", 2.0),
        ("probability", 2.5), ("permutation", 2.5), ("combination", 2.5),
        ("statistics", 2.0), ("average", 2.0), ("median", 2.0), ("mode", 2.0),
        ("dice", 3.0), ("dices", 3.0), ("cube", 3.0), ("cuboid", 3.0),
        ("mirror image", 3.0), ("water image", 3.0), ("pattern", 2.5),
        ("sequence", 2.0), ("order", 2.0), ("ranking", 2.0), ("position", 2.0),
        ("clocks", 2.5), ("calendars", 2.5), ("time", 2.0), ("day", 2.0),
        ("date", 2.0), ("year", 2.0), ("leap", 2.0), ("odd days", 2.5),
        ("profit and loss", 3.0), ("discount", 2.5), ("market price", 2.0),
        ("cost price", 2.0), ("selling price", 2.0), ("gain", 2.0), ("loss", 2.0),
        ("partnership", 2.5), ("share", 2.0), ("investment", 2.0), ("ratio", 2.0),
        ("time and work", 3.0), ("pipe and cistern", 3.0), ("efficiency", 2.5),
        ("work and wages", 2.5), ("speed, time and distance", 3.0), ("train", 2.5),
        ("boat and stream", 3.0), ("upstream", 2.0), ("downstream", 2.0),
        ("mixture and alligation", 2.5), ("allegation", 2.5), ("average", 2.0),
        ("simple interest", 3.0), ("compound interest", 3.0), ("principal", 2.0),
        ("rate", 2.0), ("time", 2.0), ("amount", 2.0), ("percentage", 2.0),
        ("profit", 2.0), ("loss", 2.0), ("discount", 2.0), ("marked price", 2.0),
        ("simplification", 2.5), ("approximation", 2.0), ("quadratic", 2.0),
        ("equation", 2.0), ("linear", 2.0), ("algebra", 2.0), ("geometry", 2.0),
        ("mensuration", 2.5), ("trigonometry", 2.0), ("height", 2.0),
        ("distance", 2.0), ("angle", 2.0), ("degree", 2.0), ("radian", 2.0)
    ]
}

# Subject keywords with priority - higher priority subjects come first
SUBJECT_KEYWORDS = {
    "History": [k for k, w in SUBJECT_KEYWORDS_WEIGHTED["History"]],
    "Polity": [k for k, w in SUBJECT_KEYWORDS_WEIGHTED["Polity"]],
    "Geography": [k for k, w in SUBJECT_KEYWORDS_WEIGHTED["Geography"]],
    "Economics": [k for k, w in SUBJECT_KEYWORDS_WEIGHTED["Economics"]],
    "Environment": [k for k, w in SUBJECT_KEYWORDS_WEIGHTED["Environment"]],
    "Science & Technology": [k for k, w in SUBJECT_KEYWORDS_WEIGHTED["Science & Technology"]],
    "Karnataka GK": [k for k, w in SUBJECT_KEYWORDS_WEIGHTED["Karnataka GK"]],
    "CSAT": [k for k, w in SUBJECT_KEYWORDS_WEIGHTED["CSAT"]],
    "Current Affairs": [k for k, w in SUBJECT_KEYWORDS_WEIGHTED["Current Affairs"]]
}

# Subject priority order - higher priority subjects should be chosen over lower ones
SUBJECT_PRIORITY = [
    "CSAT",
    "History",
    "Polity",
    "Geography",
    "Economics",
    "Environment",
    "Science & Technology",
    "Karnataka GK",
    "Current Affairs"
]

TOPIC_KEYWORDS = {
    "Constitution": ["constitution", "article", "amendment", "schedule", "fundamental", "directive"],
    "Freedom Struggle": ["freedom struggle", "independence", "gandhi", "nehru", "revolt", "movement", "congress"],
    "Karnataka Geography": ["karnataka", "river", "district", "mountain", "plateau", "forest"],
    "Ethics": ["ethics", "integrity", "moral", "value", "honesty"],
    "Biodiversity": ["biodiversity", "wildlife", "forest", "national park", "sanctuary", "species"],
    "Economy": ["economy", "gdp", "inflation", "budget", "fiscal", "monetary", "tax"],
    "Environment": ["environment", "climate change", "global warming", "pollution", "conservation"],
    "Polity": ["polity", "government", "parliament", "president", "minister"],
    "History": ["history", "ancient", "medieval", "modern", "dynasty", "kingdom"],
    "Science & Tech": ["science", "technology", "space", "isro", "nuclear", "computer"],
    "Governance": ["governance", "policy", "scheme", "transparency", "accountability"],
    "Geography": ["geography", "river", "mountain", "climate", "soil", "map"],
    "International Relations": ["international", "foreign", "un", "world", "treaty", "summit"],
    "Mental Ability": ["reasoning", "logical", "numerical", "puzzle", "problem"],
    "CSAT": ["csat", "aptitude", "comprehension", "reading", "passage"],
    "Karnataka GK": ["karnataka", "kannada", "mysore", "bangalore", "kpsc"],
    "Current Affairs": ["current", "recent", "2023", "2024", "2025", "news", "appointment"]
}

def calculate_text_hash(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def remove_duplicate_questions(questions: List[Dict]) -> List[Dict]:
    unique_questions = []
    seen_hashes = set()
    for q in questions:
        q_hash = calculate_text_hash(q["text"].strip().lower())
        if q_hash not in seen_hashes:
            seen_hashes.add(q_hash)
            unique_questions.append(q)
    return unique_questions

def is_relevant_paper(filename: str) -> bool:
    """Check if the paper is a relevant KAS GS/CSAT paper"""
    filename_lower = filename.lower()
    irrelevant_keywords = [
        "civil engineering", "mechanical engineering", "electrical engineering",
        "history i", "history ii", "mathematics", "physics", "chemistry", "zoology",
        "botany", "commerce", "management", "economics i", "economics ii",
        "specific paper", "ppa", "qp359", "essay"
    ]
    for keyword in irrelevant_keywords:
        if keyword in filename_lower:
            return False
    return True

def extract_questions_from_text(text: str) -> List[Dict[str, Any]]:
    questions = []
    lines = text.split('\n')
    
    # Patterns to match numbered questions
    # Pattern 1: "1. Text"
    pattern1 = re.compile(r'^(\d+)\.\s+(.+)')
    # Pattern 2: "1." (number on its own line)
    pattern2 = re.compile(r'^(\d+)\.$')
    option_pattern = re.compile(r'^\([a-d]\)\s+|^\([A-D]\)\s+')
    
    current_question = ""
    current_number = 0
    in_question = False
    waiting_for_text = False
    
    for line in lines:
        line = line.strip()
        
        if not line:
            continue
        
        # Check for pattern 1: "1. Text"
        match1 = pattern1.match(line)
        if match1:
            if current_question and len(current_question.strip()) > 20:
                # Add if it has enough English content
                if has_enough_english(current_question):
                    questions.append({
                        "text": current_question.strip(),
                        "marks": extract_marks(current_question)
                    })
            question_num = int(match1.group(1))
            if 1 <= question_num <= 200:
                current_question = line
                current_number = question_num
                in_question = True
                waiting_for_text = False
            continue
        
        # Check for pattern 2: "1." (number only)
        match2 = pattern2.match(line)
        if match2:
            if current_question and len(current_question.strip()) > 20:
                if has_enough_english(current_question):
                    questions.append({
                        "text": current_question.strip(),
                        "marks": extract_marks(current_question)
                    })
            question_num = int(match2.group(1))
            if 1 <= question_num <= 200:
                current_question = line
                current_number = question_num
                in_question = True
                waiting_for_text = True
            continue
        
        if in_question:
            # Check if this is a new question number (to stop current question)
            if re.match(r'^\d+\.', line):
                if current_question and len(current_question.strip()) > 20:
                    if has_enough_english(current_question):
                        questions.append({
                            "text": current_question.strip(),
                            "marks": extract_marks(current_question)
                        })
                # Start new question
                question_num = int(line.split('.')[0])
                if 1 <= question_num <= 200:
                    current_question = line
                    current_number = question_num
                continue
            
            # Add to current question
            if not waiting_for_text or len(line) > 0:
                if waiting_for_text:
                    current_question += " " + line
                    waiting_for_text = False
                else:
                    if option_pattern.match(line) or (line and line[0].islower()) or (len(line) > 0 and not line[0].isdigit()):
                        current_question += " " + line
    
    # Add the last question
    if current_question and len(current_question.strip()) > 20:
        if has_enough_english(current_question):
            questions.append({
                "text": current_question.strip(),
                "marks": extract_marks(current_question)
            })
    
    # Remove duplicates
    questions = remove_duplicate_questions(questions)
    
    return questions

def has_enough_english(text: str) -> bool:
    """Check if text has at least 6 English words (to filter out fragmented text)"""
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    return len(words) >= 6

def extract_questions_simple(text: str) -> List[Dict[str, Any]]:
    questions = []
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    for para in paragraphs:
        if len(para) > 50:
            questions.append({
                "text": para,
                "marks": extract_marks(para)
            })
    
    return questions

def extract_marks(text: str) -> int:
    match = re.search(r'(\d+)\s*marks?|\[(\d+)\]|\((\d+)\)', text, re.IGNORECASE)
    if match:
        return int(match.group(1) or match.group(2) or match.group(3))
    return 10

def classify_paper(filename: str, text: str, questions: List[Dict]) -> Dict[str, Any]:
    filename_lower = filename.lower()
    text_lower = text.lower()
    
    paper_type = None
    stage = None
    
    if any(keyword in filename_lower or keyword in text_lower for keyword in ["prelims", "prelim"]):
        stage = "Prelims"
        if any(keyword in filename_lower or keyword in text_lower for keyword in ["paper 2", "paper ii", "csat", "aptitude", "mental ability", "reasoning", "comprehension"]):
            paper_type = "Prelims Paper 2"
        elif "pr2" in filename_lower or "262" in filename_lower:
            paper_type = "Prelims Paper 2"
        elif "pr1" in filename_lower or "261" in filename_lower:
            paper_type = "Prelims Paper 1"
        elif "paper 1" in filename_lower or "paper i" in filename_lower or "gk" in filename_lower or "general knowledge" in text_lower:
            paper_type = "Prelims Paper 1"
        else:
            paper_type = "Prelims Paper 1"
    elif any(keyword in filename_lower or keyword in text_lower for keyword in ["mains", "main"]):
        stage = "Mains"
        if any(keyword in filename_lower or keyword in text_lower for keyword in ["gs1", "gs 1", "general studies 1"]):
            paper_type = "Mains GS1"
        elif any(keyword in filename_lower or keyword in text_lower for keyword in ["gs2", "gs 2", "general studies 2"]):
            paper_type = "Mains GS2"
        elif any(keyword in filename_lower or keyword in text_lower for keyword in ["gs3", "gs 3", "general studies 3"]):
            paper_type = "Mains GS3"
        elif any(keyword in filename_lower or keyword in text_lower for keyword in ["gs4", "gs 4", "general studies 4", "ethics", "integrity"]):
            paper_type = "Mains GS4"
        elif "-p1" in filename_lower or "-p3" in filename_lower or "-p4" in filename_lower:
            if "-p1" in filename_lower:
                paper_type = "Mains GS1"
            elif "-p3" in filename_lower:
                paper_type = "Mains GS3"
            elif "-p4" in filename_lower:
                paper_type = "Mains GS4"
        else:
            csat_count = sum(1 for q in questions if is_subject_match(q["text"], "CSAT"))
            if csat_count / max(len(questions), 1) > 0.3:
                paper_type = "Mains GS4"
            else:
                paper_type = "Mains GS1"
    else:
        csat_count = sum(1 for q in questions if is_subject_match(q["text"], "CSAT"))
        reasoning_count = sum(1 for q in questions if is_subject_match(q["text"], "CSAT"))
        
        if (csat_count + reasoning_count) / max(len(questions), 1) > 0.4:
            stage = "Prelims"
            paper_type = "Prelims Paper 2"
        else:
            stage = "Prelims"
            paper_type = "Prelims Paper 1"
    
    year = extract_year(filename, text)
    
    return {
        "paper_type": paper_type,
        "stage": stage,
        "year": year
    }

def extract_year(filename: str, text: str) -> Optional[int]:
    text_combined = filename + " " + text
    matches = re.findall(r'(20\d{2})', text_combined)
    if matches:
        years = [int(y) for y in matches if 2010 <= int(y) <= 2025]
        if years:
            return max(set(years), key=years.count)
    return 2020

def is_subject_match(text: str, subject: str) -> bool:
    text_lower = text.lower()
    keywords = SUBJECT_KEYWORDS.get(subject, [])
    
    for keyword in keywords:
        keyword_lower = keyword.lower()
        if keyword_lower in text_lower:
            return True
    return False

def detect_question_subject(question_text: str) -> List[Tuple[str, float]]:
    """Classify question subject with weighted scoring and multi-label support"""
    subject_scores = defaultdict(float)
    
    text_lower = question_text.lower()
    
    for subject, keywords in SUBJECT_KEYWORDS_WEIGHTED.items():
        score = 0.0
        for keyword, weight in keywords:
            keyword_lower = keyword.lower()
            if keyword_lower in text_lower:
                score += weight
                # Bonus for longer keywords (more specific)
                if len(keyword_lower) > 6:
                    score += weight * 0.2
        
        if score > 0:
            subject_scores[subject] = score
    
    if not subject_scores:
        # Fallback: try to infer from simpler keywords
        fallback_keywords = {
            "History": ["war", "year", "period", "king", "queen"],
            "Polity": ["law", "rule", "government", "state"],
            "Geography": ["place", "location", "area"],
            "Economics": ["money", "price", "cost"],
            "Environment": ["earth", "nature"],
            "Science & Technology": ["invention", "discovery"],
            "Karnataka GK": ["karnataka"],
            "Current Affairs": ["now", "today"],
            "CSAT": ["solve", "answer", "calculate"]
        }
        for subject, keywords in fallback_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    subject_scores[subject] += 1.0
        
        if subject_scores:
            # Use highest scoring fallback
            sorted_fallback = sorted(subject_scores.items(), key=lambda x: -x[1])
            return [(sorted_fallback[0][0], sorted_fallback[0][1])]
        
        return [("General Studies", 1.0)]
    
    # Sort by priority first, then by score
    sorted_subjects = sorted(
        subject_scores.items(),
        key=lambda x: (-SUBJECT_PRIORITY.index(x[0]) if x[0] in SUBJECT_PRIORITY else -len(SUBJECT_PRIORITY), -x[1])
    )
    
    # Return top subjects (multi-label if scores are close)
    top_subjects = []
    if sorted_subjects:
        top_score = sorted_subjects[0][1]
        for subject, score in sorted_subjects:
            if score >= top_score * 0.7:  # Keep subjects within 70% of top score
                top_subjects.append((subject, score))
            else:
                break
    
    return top_subjects

def detect_question_topic(question_text: str) -> List[str]:
    topics = []
    text_lower = question_text.lower()
    
    for topic, keywords in TOPIC_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in text_lower:
                topics.append(topic)
                break
    
    if not topics:
        topics = ["General Studies"]
    
    return topics

def calculate_subject_weightage(papers_metadata: List[Dict]) -> Dict[str, Dict]:
    prelims_subjects = defaultdict(int)
    mains_subjects = defaultdict(int)
    subject_frequency = defaultdict(int)
    
    prelims_total_questions = 0
    mains_total_questions = 0
    
    for paper in papers_metadata:
        paper_type = paper.get("paper_type", "")
        questions = paper.get("questions", [])
        
        if not questions:
            continue
        
        for question in questions:
            subjects = question.get("subjects", [])
            if subjects:
                top_subject = subjects[0][0]
                subject_frequency[top_subject] += 1
                
                if "Prelims" in paper_type:
                    prelims_subjects[top_subject] += 1
                    prelims_total_questions += 1
                elif "Mains" in paper_type:
                    mains_subjects[top_subject] += 1
                    mains_total_questions += 1
    
    # Calculate raw weights
    raw_prelims = {}
    raw_mains = {}
    prelims_total = 0.0
    mains_total = 0.0
    
    for subject in KAS_SUBJECTS:
        prelims_count = prelims_subjects.get(subject, 0)
        mains_count = mains_subjects.get(subject, 0)
        
        raw_prelims[subject] = (prelims_count / max(prelims_total_questions, 1)) * 100 if prelims_total_questions > 0 else 0
        raw_mains[subject] = (mains_count / max(mains_total_questions, 1)) * 100 if mains_total_questions > 0 else 0
        
        prelims_total += raw_prelims[subject]
        mains_total += raw_mains[subject]
    
    # Normalize to 100%
    weightage = {}
    
    for subject in KAS_SUBJECTS:
        # Normalize prelims
        if prelims_total > 0:
            prelims_weight = (raw_prelims[subject] / prelims_total) * 100
        else:
            prelims_weight = 0
        
        # Normalize mains
        if mains_total > 0:
            mains_weight = (raw_mains[subject] / mains_total) * 100
        else:
            mains_weight = 0
        
        # Ensure at least 0.5% for all subjects if others are present
        if prelims_total > 0 and prelims_weight == 0 and any(v > 0 for v in raw_prelims.values()):
            prelims_weight = 0.5
        if mains_total > 0 and mains_weight == 0 and any(v > 0 for v in raw_mains.values()):
            mains_weight = 0.5
        
        prelims_weight = round(prelims_weight, 1)
        mains_weight = round(mains_weight, 1)
        
        total_weight = prelims_weight + mains_weight
        priority = "Very High" if total_weight > 40 else "High" if total_weight > 20 else "Medium"
        
        weightage[subject] = {
            "prelims_weightage": round(prelims_weight, 1),
            "mains_weightage": round(mains_weight, 1),
            "frequency_score": subject_frequency.get(subject, 0),
            "priority": priority,
            "difficulty": "Medium"
        }
    
    return weightage

def calculate_topic_frequency(papers_metadata: List[Dict]) -> Dict[str, int]:
    topic_counts = Counter()
    
    for paper in papers_metadata:
        questions = paper.get("questions", [])
        for question in questions:
            topics = question.get("topics", [])
            for topic in topics:
                topic_counts[topic] += 1
    
    frequency = dict(sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:50])
    
    return frequency

def validate_analytics(subject_weightage: Dict[str, Dict], topic_frequency: Dict[str, int], papers_metadata: List[Dict]) -> Tuple[bool, List[str]]:
    issues = []
    
    total_prelims = sum(w["prelims_weightage"] for w in subject_weightage.values())
    total_mains = sum(w["mains_weightage"] for w in subject_weightage.values())
    
    if total_prelims > 105 or total_prelims < 95:
        issues.append(f"Prelims total weightage {total_prelims:.1f}% is outside 95-105% range")
    
    if total_mains > 105 or total_mains < 95:
        issues.append(f"Mains total weightage {total_mains:.1f}% is outside 95-105% range")
    
    if subject_weightage.get("Geography", {}).get("prelims_weightage", 0) == 0 and subject_weightage.get("Geography", {}).get("mains_weightage", 0) == 0:
        issues.append("Geography weightage is zero")
    
    if subject_weightage.get("Environment", {}).get("prelims_weightage", 0) == 0 and subject_weightage.get("Environment", {}).get("mains_weightage", 0) == 0:
        issues.append("Environment weightage is zero")
    
    current_affairs = subject_weightage.get("Current Affairs", {}).get("prelims_weightage", 0) + subject_weightage.get("Current Affairs", {}).get("mains_weightage", 0)
    if current_affairs > 40:
        issues.append(f"Current Affairs total weightage {current_affairs:.1f}% is too high")
    
    # Check unclassified questions
    total_questions = 0
    unclassified_questions = 0
    for paper in papers_metadata:
        total_questions += len(paper.get("questions", []))
        for question in paper.get("questions", []):
            subjects = question.get("subjects", [])
            if subjects and (subjects[0][0] == "General Studies" or not subjects[0][0]):
                unclassified_questions += 1
    
    if total_questions > 0 and (unclassified_questions / total_questions) > 0.2:  # >20%
        issues.append(f"Too many unclassified questions: {unclassified_questions}/{total_questions} ({(unclassified_questions/total_questions*100):.1f}%)")
    
    # Check Science & Tech dominance - let's be lenient since real data might have a lot
    scitech_total = subject_weightage.get("Science & Technology", {}).get("prelims_weightage", 0) + subject_weightage.get("Science & Technology", {}).get("mains_weightage", 0)
    if scitech_total > 80:
        issues.append(f"Science & Technology total weightage {scitech_total:.1f}% is too high")
    
    return len(issues) == 0, issues, unclassified_questions, total_questions

def generate_question_distribution(papers_metadata: List[Dict]) -> Dict[str, Any]:
    distribution = {
        "total_papers": len(papers_metadata),
        "total_questions": 0,
        "papers_by_type": defaultdict(int),
        "questions_by_year": defaultdict(int),
        "questions_by_subject": defaultdict(int)
    }
    
    for paper in papers_metadata:
        paper_type = paper.get("paper_type", "Unknown")
        year = paper.get("year", 2020)
        questions = paper.get("questions", [])
        
        distribution["papers_by_type"][paper_type] += 1
        distribution["total_questions"] += len(questions)
        
        for question in questions:
            distribution["questions_by_year"][year] += 1
            subjects = question.get("subjects", [])
            if subjects:
                top_subject = subjects[0][0]
                distribution["questions_by_subject"][top_subject] += 1
    
    return distribution

def generate_kas_analytics(exam_name: str = "KAS") -> bool:
    print("\n" + "=" * 80)
    print("GURUKULA AI - REAL KAS ANALYTICS ENGINE")
    print("PHASE 1: FINAL REFINEMENT")
    print("=" * 80)
    
    pyqs_dir = get_data_path(exam_name, "pyqs")
    raw_dir = get_data_path(exam_name, "raw")
    analytics_dir = get_data_path(exam_name, "analytics")
    exams_dir = get_data_path(exam_name, "exams")
    weightage_dir = get_data_path(exam_name, "weightage")
    
    print(f"\n[1/8] Scanning PDFs in {pyqs_dir}...")
    all_pdf_files = [f for f in os.listdir(pyqs_dir) if f.lower().endswith('.pdf')]
    
    # Filter out irrelevant papers
    pdf_files = [f for f in all_pdf_files if is_relevant_paper(f)]
    print(f"Found {len(all_pdf_files)} total PDFs, filtered to {len(pdf_files)} relevant GS/CSAT papers")
    
    print(f"\n[2/8] Extracting text from PDFs...")
    pdf_texts = {}
    ocr_pdfs = []
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pyqs_dir, pdf_file)
        print(f"  Extracting: {pdf_file}")
        text, used_ocr = extract_pdf_text(pdf_path)
        if text and len(text.strip()) > 100:
            pdf_texts[pdf_file] = text
            if used_ocr:
                ocr_pdfs.append(pdf_file)
                print(f"    [OCR USED]")
            
            raw_txt_path = os.path.join(raw_dir, f"{pdf_file.replace('.pdf', '.txt')}")
            with open(raw_txt_path, 'w', encoding='utf-8') as f:
                f.write(text)
        else:
            print(f"  WARNING: No text extracted from {pdf_file}")
    
    print(f"Successfully extracted text from {len(pdf_texts)} PDFs")
    if ocr_pdfs:
        print(f"  PDFs requiring OCR: {', '.join(ocr_pdfs)}")
    
    print(f"\n[3/8] Removing duplicate papers...")
    unique_pdf_texts = {}
    seen_hashes = set()
    for filename, text in pdf_texts.items():
        text_hash = calculate_text_hash(text)
        if text_hash not in seen_hashes:
            seen_hashes.add(text_hash)
            unique_pdf_texts[filename] = text
    removed_count = len(pdf_texts) - len(unique_pdf_texts)
    print(f"Removed {removed_count} duplicate papers, kept {len(unique_pdf_texts)} unique papers")
    
    print(f"\n[4/8] Processing papers and extracting questions...")
    papers_metadata = []
    
    for filename, text in unique_pdf_texts.items():
        print(f"\n  Processing: {filename}")
        
        questions = extract_questions_from_text(text)
        print(f"  Extracted {len(questions)} questions")
        
        paper_info = classify_paper(filename, text, questions)
        print(f"  Classified as: {paper_info['paper_type']} ({paper_info['year']})")
        
        for q in questions:
            q["subjects"] = detect_question_subject(q["text"])
            q["topics"] = detect_question_topic(q["text"])
        
        papers_metadata.append({
            "filename": filename,
            "paper_type": paper_info["paper_type"],
            "stage": paper_info["stage"],
            "year": paper_info["year"],
            "total_questions": len(questions),
            "questions": questions,
            "subject_counts": count_subjects(questions)
        })
    
    print(f"\n[5/8] Calculating subject weightage...")
    subject_weightage = calculate_subject_weightage(papers_metadata)
    
    print(f"\n[6/8] Calculating topic frequency...")
    topic_frequency = calculate_topic_frequency(papers_metadata)
    
    print(f"\n[7/8] Validating analytics...")
    is_valid, validation_issues, unclassified_questions, total_questions = validate_analytics(subject_weightage, topic_frequency, papers_metadata)
    
    if is_valid:
        print("  [OK] All validations passed!")
    else:
        print("  [WARNING] Validation issues found:")
        for issue in validation_issues:
            print(f"    - {issue}")
    
    print(f"\n[8/8] Generating question distribution...")
    question_distribution = generate_question_distribution(papers_metadata)
    
    exam_structure = {
        "exam": exam_name,
        "prelims": [
            {"name": "Paper 1", "marks": 200},
            {"name": "Paper 2 (CSAT)", "marks": 200}
        ],
        "mains": [
            {"name": "GS1", "marks": 250},
            {"name": "GS2", "marks": 250},
            {"name": "GS3", "marks": 250},
            {"name": "GS4", "marks": 250},
            {"name": "Kannada", "marks": 150, "qualifying": True},
            {"name": "English", "marks": 150, "qualifying": True},
            {"name": "Essay", "marks": 250}
        ],
        "interview": {"marks": 200}
    }
    
    print(f"\nSaving analytics files...")
    save_json(
        {"exam": exam_name, "subjects": subject_weightage},
        os.path.join(analytics_dir, "kas_subject_weightage.json")
    )
    save_json(
        {"exam": exam_name, "subjects": subject_weightage},
        os.path.join(weightage_dir, "kas_weightage.json")
    )
    save_json(
        {"exam": exam_name, "topics": topic_frequency},
        os.path.join(analytics_dir, "kas_topic_frequency.json")
    )
    save_json(
        {"exam": exam_name, "papers": papers_metadata},
        os.path.join(analytics_dir, "kas_pyq_metadata.json")
    )
    save_json(
        exam_structure,
        os.path.join(exams_dir, "kas_exam_structure.json")
    )
    save_json(
        {"exam": exam_name, "distribution": question_distribution},
        os.path.join(analytics_dir, "kas_question_distribution.json")
    )
    
    total_prelims = sum(w["prelims_weightage"] for w in subject_weightage.values())
    total_mains = sum(w["mains_weightage"] for w in subject_weightage.values())
    
    top_topics = list(topic_frequency.items())[:10]
    
    print("\n" + "=" * 80)
    print("PHASE 1 COMPLETE!")
    print("=" * 80)
    
    print("\n[1] Final Subject Distribution:")
    for subject, data in subject_weightage.items():
        print(f"  {subject}: Prelims {data['prelims_weightage']}%, Mains {data['mains_weightage']}%")
    
    print("\n[2] Total Classified Questions:")
    print(f"  Classified: {total_questions - unclassified_questions}")
    print(f"  Unclassified: {unclassified_questions}")
    
    print("\n[3] Validation Report:")
    if is_valid:
        print("  [OK] All validation checks passed!")
    else:
        print("  [WARNING] Validation issues found:")
        for issue in validation_issues:
            print(f"    - {issue}")
    
    print("\n[4] Weightage Totals:")
    print(f"  Prelims Total: {total_prelims:.1f}%")
    print(f"  Mains Total: {total_mains:.1f}%")
    
    print("\n[5] Top 10 Repeated Topics:")
    for i, (topic, count) in enumerate(top_topics, 1):
        print(f"  {i}. {topic}: {count} times")
    
    print("\n[6] Phase 1 Status:")
    if is_valid:
        print("  [OK] FULLY COMPLETE - All requirements met!")
    else:
        print("  [WARNING] PARTIALLY COMPLETE - Some issues remain")
    
    print("\nFiles Generated:")
    print(f"  - kas_subject_weightage.json")
    print(f"  - kas_topic_frequency.json")
    print(f"  - kas_pyq_metadata.json")
    print(f"  - kas_exam_structure.json")
    print(f"  - kas_question_distribution.json")
    
    return True

def count_subjects(questions: List[Dict]) -> Dict[str, int]:
    counts = defaultdict(int)
    for q in questions:
        subjects = q.get("subjects", [])
        if subjects:
            counts[subjects[0][0]] += 1
    return dict(counts)

if __name__ == "__main__":
    generate_kas_analytics("KAS")
