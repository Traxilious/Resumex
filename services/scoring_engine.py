import re

ACTION_VERBS = [
    "achieved", "analyzed", "architected", "automated", "built", "collaborated",
    "configured", "constructed", "created", "debugged", "deployed", "designed",
    "developed", "engineered", "enhanced", "established", "executed", "expanded",
    "implemented", "improved", "increased", "integrated", "launched", "led",
    "managed", "migrated", "optimized", "orchestrated", "organized", "performed",
    "programmed", "reduced", "refactored", "resolved", "scaled", "spearheaded",
    "streamlined", "structured", "tested", "transformed", "upgraded", "utilized"
]

def calculate_overall_score(parsed_data, ats_analysis):
    """
    Computes comprehensive resume score out of 100 based on multi-parameter evaluation.
    """
    sections = parsed_data.get('sections', {})
    contact = parsed_data.get('contact_info', {})
    word_count = parsed_data.get('word_count', 0)
    cleaned_text = parsed_data.get('cleaned_text', '').lower()

    # 1. Section Completeness (Max 30 points)
    section_score = 0
    section_breakdown = {}

    section_weights = {
        "contact_info": 6,
        "summary": 4,
        "education": 6,
        "skills": 6,
        "experience": 4,
        "projects": 4
    }

    for sec, weight in section_weights.items():
        present = sections.get(sec, False)
        pts = weight if present else 0
        section_score += pts
        section_breakdown[sec] = {"present": present, "points": pts, "max": weight}

    # 2. Contact & Professional Links (Max 15 points)
    contact_score = 0
    if contact.get('email'): contact_score += 4
    if contact.get('phone'): contact_score += 3
    if contact.get('linkedin'): contact_score += 4
    if contact.get('github') or contact.get('portfolio'): contact_score += 4

    # 3. Resume Length & Structure (Max 15 points)
    length_score = 0
    if 250 <= word_count <= 800:
        length_score = 15
    elif 150 <= word_count < 250:
        length_score = 10
    elif 800 < word_count <= 1200:
        length_score = 10
    elif word_count > 0:
        length_score = 5

    # 4. Action Verbs & Impact Metrics (Max 20 points)
    action_verbs_found = []
    for verb in ACTION_VERBS:
        if re.search(r'\b' + verb + r'\b', cleaned_text):
            action_verbs_found.append(verb)

    # Has metrics (numbers, percentages, dollar signs)
    has_metrics = bool(re.search(r'\d+%\b|\$\d+|\b\d+\s*(users|clients|percent|projects|percent|ms|sec|x)\b', cleaned_text))
    
    verb_points = min(14, len(action_verbs_found) * 2)
    metric_points = 6 if has_metrics else 0
    impact_score = verb_points + metric_points

    # 5. Technical Skill Relevancy (Max 20 points) - tied to ATS match
    matched_skills_count = len(ats_analysis.get('matched_skills', []))
    skill_relevancy_score = min(20, matched_skills_count * 3)

    overall_score = section_score + contact_score + length_score + impact_score + skill_relevancy_score
    overall_score = min(100, max(0, overall_score))

    breakdown = {
        "section_completeness": {"score": section_score, "max": 30, "details": section_breakdown},
        "contact_details": {"score": contact_score, "max": 15, "info": contact},
        "resume_length": {"score": length_score, "max": 15, "word_count": word_count},
        "action_impact": {"score": impact_score, "max": 20, "verbs_found": action_verbs_found, "has_metrics": has_metrics},
        "skill_relevancy": {"score": skill_relevancy_score, "max": 20, "matched_count": matched_skills_count}
    }

    return {
        "overall_score": overall_score,
        "score_breakdown": breakdown,
        "breakdown": breakdown
    }

def calculate_resume_score(parsed_data, ats_analysis):
    return calculate_overall_score(parsed_data, ats_analysis)
