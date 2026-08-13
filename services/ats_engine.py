import re
import json

# Skill synonym dictionary for robust ATS matching across tech domains
SKILL_ALIASES = {
    "cloud": ["aws", "azure", "gcp", "cloud computing", "infrastructure", "devops", "docker", "kubernetes", "linux", "server"],
    "aws": ["amazon web services", "cloud", "ec2", "s3", "cloud computing", "infrastructure"],
    "azure": ["microsoft azure", "cloud", "cloud computing"],
    "gcp": ["google cloud", "cloud", "cloud computing"],
    "linux": ["unix", "bash", "shell", "ubuntu", "system administration", "os"],
    "docker": ["containerization", "containers", "kubernetes", "devops"],
    "kubernetes": ["k8s", "container orchestration", "docker", "devops"],
    "terraform": ["infrastructure as code", "iac", "cloud engineering", "devops"],
    "python": ["py", "python3", "scripting", "pandas", "numpy"],
    "sql": ["database", "mysql", "postgresql", "oracle", "tsql", "querying", "data retrieval"],
    "data analysis": ["data analytics", "data visualization", "tableau", "power bi", "statistics", "pandas", "excel"],
    "web developer": ["web development", "javascript", "html", "css", "react", "full stack"],
    "javascript": ["js", "es6", "react", "node.js", "typescript"],
    "react": ["react.js", "reactjs", "frontend", "javascript"],
    "git": ["github", "gitlab", "version control", "gitflow"]
}

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

    # Calculate weights & scores
    total_core = len(core_skills) if core_skills else 1
    total_opt = len(optional_skills) if optional_skills else 1

    matched_core_cnt = len(matched_core)
    matched_opt_cnt = len(matched_optional)

    # Base match ratio
    core_ratio = matched_core_cnt / total_core
    opt_ratio = matched_opt_cnt / total_opt

    raw_score = int(round((core_ratio * 75.0) + (opt_ratio * 25.0)))

    # If candidate has solid core skills (e.g. SQL, Python, Git, Data Analysis, Linux), apply floor baseline score
    if matched_core_cnt >= 2 or (matched_core_cnt + matched_opt_cnt) >= 3:
        ats_score = max(raw_score, 72)
    elif matched_core_cnt >= 1 or (matched_core_cnt + matched_opt_cnt) >= 2:
        ats_score = max(raw_score, 60)
    else:
        ats_score = max(raw_score, 45)

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
    Check if a skill (single word, multi-word phrase, or domain alias) is present in text.
    """
    skill_clean = skill.strip().lower()
    
    # Direct boundary checking
    escaped = re.escape(skill_clean)
    pattern = r'(?:\b|_|^)' + escaped + r'(?:\b|_|$)'
    if re.search(pattern, text):
        return True
    
    if len(skill_clean) > 2 and skill_clean in text:
        return True

    # Check synonym / alias list
    if skill_clean in SKILL_ALIASES:
        for alias in SKILL_ALIASES[skill_clean]:
            alias_escaped = re.escape(alias)
            alias_pattern = r'(?:\b|_|^)' + alias_escaped + r'(?:\b|_|$)'
            if re.search(alias_pattern, text):
                return True

    return False
