from fastapi import APIRouter, HTTPException
from app.schemas.research import ResearchRequest, ResearchResponse
from app.services.data_loader import DataLoader
from app.services.llm_service import LLMService
from app.utils.logger import logger
import json
from pathlib import Path

router = APIRouter(tags=["Research Agent"], prefix="/agent")

data_loader = DataLoader()
llm_service = LLMService()


def generate_fallback_research_response(all_data):
    """Generate fallback research response using datasets"""
    analytics = all_data.get("analytics", {})
    syllabus = all_data.get("syllabus", {})
    exams = all_data.get("exams", {})
    
    # Get subject weightage data
    subject_weightage = analytics.get("kas_subject_weightage", {}).get("subjects", {})
    subjects_list = list(subject_weightage.keys()) if subject_weightage else ["Polity", "History", "Geography"]
    
    # Get frequent topics
    topic_frequency = analytics.get("kas_topic_frequency", {}).get("topics", {})
    frequent_topics = [
        {"topic": topic, "frequency": int(freq)}
        for topic, freq in list(topic_frequency.items())[:10]
    ]
    
    # Build research data
    fallback_data = {
        "research_summary": {
            "exam_overview": "Karnataka Administrative Services (KAS) exam conducted by KPSC",
            "high_priority_subjects": subjects_list[:5],
            "frequent_topics": frequent_topics
        },
        "metadata": {
            "conducted_by": "Karnataka Public Service Commission (KPSC)",
            "stages": ["Prelims", "Mains", "Interview"],
            "qualification": "Bachelor's Degree",
            "difficulty": "Moderate to High",
            "preparation_duration": "6-12 months",
            "exam_type": "State Civil Services"
        },
        "actionable_insights": [
            "Focus on high weightage subjects first",
            "Solve previous year question papers",
            "Create a structured study plan",
            "Stay updated with current affairs"
        ]
    }
    return fallback_data


@router.post("/research", response_model=ResearchResponse)
async def get_research_insights(request: ResearchRequest = ResearchRequest(exam="KAS")):
    try:
        logger.info(f"Received research request for exam: {request.exam}")
        
        # Load datasets
        all_data = data_loader.load_all()
        prompts = all_data.get("prompts", {})
        
        # Try LLM first
        try:
            analytics = all_data.get("analytics", {})
            
            # Load research agent context
            context_path = Path(__file__).parent.parent.parent / "datasets" / "KAS" / "agent_contexts" / "research_agent_context.json"
            if context_path.exists():
                with open(context_path, 'r', encoding='utf-8') as f:
                    research_context = json.load(f)
                
                minimal_context = {
                    "metadata": research_context.get("data", {}).get("metadata", {}),
                    "syllabus_subjects": research_context.get("data", {}).get("syllabus", {}).get("subjects", []),
                    "pyq_trends": research_context.get("data", {}).get("pyq_trends", {}),
                    "exam_pattern": research_context.get("data", {}).get("pattern", {})
                }
            else:
                minimal_context = {}
            
            # Call LLM service
            research_prompt = prompts.get("research_prompt", "Generate research insights.")
            result = await llm_service.generate(
                prompt=research_prompt,
                context=minimal_context,
                schema={
                    "research_summary": dict,
                    "metadata": dict,
                    "actionable_insights": list
                }
            )
            
            # Check if result is successful and has data
            if result.get("success") and "data" in result:
                logger.info("LLM research generation complete")
                return ResearchResponse(
                    success=result["success"],
                    data=result["data"],
                    usage=result.get("usage", {})
                )
            else:
                logger.warning("LLM failed, using fallback research response")
        except Exception as e:
            logger.warning(f"LLM path failed: {e}, using fallback")
        
        # If LLM failed, use fallback
        fallback_data = generate_fallback_research_response(all_data)
        logger.info("Using fallback research response")
        return ResearchResponse(
            success=True,
            data=fallback_data,
            usage={}
        )
        
    except Exception as e:
        logger.error(f"Research request failed: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Last resort fallback
        all_data = data_loader.load_all()
        fallback_data = generate_fallback_research_response(all_data)
        return ResearchResponse(
            success=True,
            data=fallback_data,
            usage={}
        )
