import re
import json

def analyze_ats_match(cleaned_text, core_skills, optional_skills):
    """
    Compares resume text against target role skills.
    Calculates ATS compatibility score, matched skills, and skill gaps.
    """
    text_lower = cleaned_text.lower()

    matched_core = []
    missing_core = []
    
    for skill in core_skills:
        if is_skill_present(skill, text_lower):
            matched_core.append(skill)
        else:
            missing_core.append(skill)

    matched_optional = []
    missing_optional = []

    for skill in optional_skills:
        if is_skill_present(skill, text_lower):
            matched_optional.append(skill)
        else:
            missing_optional.append(skill)

    # Score calculation
    core_weight = 75.0
    optional_weight = 25.0

    core_score = (len(matched_core) / len(core_skills) * core_weight) if core_skills else 0
    optional_score = (len(matched_optional) / len(optional_skills) * optional_weight) if optional_skills else 0

    ats_score = int(round(core_score + optional_score))
    ats_score = min(100, max(0, ats_score))

    return {
        "ats_score": ats_score,
        "matched_skills": matched_core + matched_optional,
        "matched_core": matched_core,
        "missing_core": missing_core,
        "matched_optional": matched_optional,
        "missing_optional": missing_optional,
        "total_required_core": len(core_skills),
        "total_matched_core": len(matched_core)
    }

def analyze_ats(cleaned_text, target_role_data):
    core_skills = target_role_data.get('core_skills', [])
    optional_skills = target_role_data.get('optional_skills', [])
    return analyze_ats_match(cleaned_text, core_skills, optional_skills)

def is_skill_present(skill, text):
    """
    Check if a skill (single word or multi-word phrase) is present in text using boundary-aware regex.
    Handles special characters like C++, Node.js, CI/CD, .NET.
    """
    skill_clean = skill.strip().lower()
    
    # Escape regex special characters except letters and spaces
    escaped = re.escape(skill_clean)
    
    # Word boundary checking
    pattern = r'(?:\b|_|^)' + escaped + r'(?:\b|_|$)'
    
    if re.search(pattern, text):
        return True
    
    # Fallback substring check for multi-word or special skills (e.g., node.js, c++, power bi)
    if len(skill_clean) > 2 and skill_clean in text:
        return True

    return False
