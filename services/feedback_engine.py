def generate_smart_feedback(parsed_data, ats_result, score_result, ai_result, target_role="Web Developer"):
    """
    Generate deep Pros, Cons, Verdict, prioritize suggestions, Executive Summary,
    and recommended portfolio projects + curated learning resources.
    """
    pros = []
    cons = []
    suggestions = []
    
    cleaned_text = parsed_data.get("cleaned_text", "")
    contact = parsed_data.get("contact_info", {})
    sections = parsed_data.get("sections", {})
    word_count = parsed_data.get("word_count", 0)
    
    overall_score = score_result.get("overall_score", 0)
    ats_score = ats_result.get("ats_score", 0)
    ai_percentage = ai_result.get("ai_percentage", 0)
    ai_risk = ai_result.get("risk_level", "Natural Phrasing")
    
    matched_skills = ats_result.get("matched_skills", [])
    missing_core = ats_result.get("missing_core", [])
    missing_optional = ats_result.get("missing_optional", [])

    # 1. Evaluate Pros (Strengths)
    if contact.get("email"):
        pros.append(f"Direct Contact Info: Valid email ({contact['email']}) detected.")
    if contact.get("phone"):
        pros.append(f"Phone Contact Provided: Contact phone ({contact['phone']}) available for recruiter calls.")
    if contact.get("linkedin"):
        pros.append("Verified Professional Identity: LinkedIn profile link provided for background verification.")
    if contact.get("github") or contact.get("portfolio"):
        pros.append("Portfolio Presence: Live code repository or personal portfolio link detected.")

    if 300 <= word_count <= 700:
        pros.append(f"Optimal Resume Length: {word_count} words fits standard 1-2 page recruiter standards.")

    if ai_percentage < 25:
        pros.append(f"Authentic Content & Phrasing: Text appears natural, well-formatted, and free from generic clichés.")

    if len(matched_skills) >= 4:
        matched_str = ", ".join([s.title() for s in matched_skills[:5]])
        pros.append(f"Strong Technical Keyword Alignment: Found key industry competencies ({matched_str}).")

    if sections.get("experience") and sections.get("projects"):
        pros.append("Well-Structured Experience & Projects: Clear distinction between practical projects and work history.")

    # 2. Evaluate Cons (Weaknesses & Risk Factors)
    if not contact.get("phone"):
        cons.append("Missing Phone Number: Omission of contact phone number prevents immediate recruiter screening calls.")
    if not contact.get("linkedin"):
        cons.append("Missing LinkedIn Profile: Omitting LinkedIn URL reduces recruiter trust and verification speed.")
    if not (contact.get("github") or contact.get("portfolio")):
        cons.append("Missing Code Repository Links: No GitHub or personal portfolio link detected to verify projects.")

    if word_count < 250:
        cons.append(f"Under-elaborated Document: Resume length is short ({word_count} words). Lacks detailed project descriptions.")
    elif word_count > 800:
        cons.append(f"Excessive Length ({word_count} words): May exceed recruiter attention spans; condense irrelevant filler.")

    if missing_core:
        missing_str = ", ".join([s.title() for s in missing_core[:4]])
        cons.append(f"Missing Essential ATS Keywords: Resume lacks core required skills for {target_role}: {missing_str}.")

    if ai_percentage >= 50:
        cons.append(f"Overused Buzzwords Risk: Contains heavy buzzword patterns and repetitive phrasing that may flag recruiter filters.")

    if not sections.get("summary"):
        cons.append("Missing Professional Summary: Lacks an introductory elevator pitch tailored to target roles.")

    # 3. Formulate Prioritized Improvement Suggestions
    if missing_core:
        missing_str = ", ".join([s.title() for s in missing_core])
        suggestions.append({
            "priority": "HIGH",
            "title": f"Integrate Missing Core Competencies for {target_role}",
            "description": f"Target role demands core expertise in: {missing_str}. Your resume currently omits these exact keywords.",
            "action": f"Naturally incorporate these keywords into your Project and Work Experience bullet points: {missing_str}."
        })

    if not contact.get("phone"):
        suggestions.append({
            "priority": "HIGH",
            "title": "Add Contact Phone Number",
            "description": "Recruiters and ATS screening bots require a phone number for scheduling initial phone interviews.",
            "action": "Place your phone number in international format (+1-xxx-xxx-xxxx) in the top header."
        })

    if not contact.get("linkedin"):
        suggestions.append({
            "priority": "HIGH",
            "title": "Add Clickable LinkedIn URL",
            "description": "Over 85% of technical recruiters verify candidate profiles on LinkedIn prior to scheduling interviews.",
            "action": "Add your customized LinkedIn profile link (e.g., linkedin.com/in/yourname) in the header section."
        })

    if not (contact.get("github") or contact.get("portfolio")):
        suggestions.append({
            "priority": "MEDIUM",
            "title": "Include GitHub or Portfolio Link",
            "description": "Technical roles require proof of execution. Lacking project links reduces recruiter confidence.",
            "action": "Add your GitHub URL (github.com/username) or personal portfolio website near your contact info."
        })

    if ai_percentage >= 40:
        suggestions.append({
            "priority": "MEDIUM",
            "title": "Refine Cliché & Buzzword Phrasing",
            "description": "High density of generic buzzwords ('spearheaded groundbreaking paradigm shifts') detected.",
            "action": "Replace vague buzzwords with specific technical tools used, metric achievements, and personal contributions."
        })

    # 4. Formulate Executive Verdict
    if overall_score >= 80 and ai_percentage < 30:
        verdict_status = "Highly Competitive & Authentic"
        badge_color = "emerald"
        icon = "fa-circle-check"
    elif overall_score >= 65:
        verdict_status = "Solid Foundation - Moderate ATS Alignment"
        badge_color = "amber"
        icon = "fa-triangle-exclamation"
    else:
        verdict_status = "Requires Strategic Optimization"
        badge_color = "rose"
        icon = "fa-circle-xmark"

    verdict = {
        "status": verdict_status,
        "badge_color": badge_color,
        "icon": icon
    }

    # 5. Formulate Executive Summary Narrative
    para1 = (
        f"Executive Evaluation Report for {target_role}: Your document achieved an overall score of {overall_score}/100 "
        f"with a {ats_score}% ATS Keyword Match and a Content Authenticity Rating of {100 - ai_percentage}%. "
        f"The candidate's profile demonstrates strongest alignment in {matched_skills[0].title() if matched_skills else 'general technical communication'}, "
        f"auditing at a total word count of {word_count} words across {sum(sections.values())} identified structural sections."
    )

    if cons:
        para2 = (
            f"Strategic Gap Analysis: The primary bottlenecks hindering recruiter callback rates are: {cons[0]} "
            f"{cons[1] if len(cons) > 1 else ''} Addressing these specific gaps will significantly improve ATS parsing fidelity."
        )
    else:
        para2 = "Strategic Gap Analysis: Your document presents strong alignment across all audited structural and keyword criteria."

    para3 = (
        f"Recommended Action Plan: Focus immediately on integrating the missing core skills ({', '.join([s.title() for s in missing_core[:3]]) if missing_core else 'advanced framework specializations'}) "
        f"and verifying all professional social links. Implementing the prioritized recommendations below will optimize your resume for tier-1 ATS screening software."
    )

    executive_summary = f"{para1}\n\n{para2}\n\n{para3}"

    # 6. Formulate Recommended Projects & Learning Resources Roadmap
    learning_roadmap = generate_learning_roadmap(target_role, missing_core, matched_skills)

    return {
        "pros": pros,
        "cons": cons,
        "suggestions": suggestions,
        "verdict": verdict,
        "executive_summary": executive_summary,
        "learning_roadmap": learning_roadmap
    }

def generate_learning_roadmap(target_role, missing_skills, matched_skills):
    """
    Generate tailored recommended portfolio projects and curated learning resources (YouTube, Docs, Guides)
    based on the candidate's target role and identified missing skills.
    """
    role_lower = target_role.lower()

    # Default / Software Engineering / Web Dev Projects & Resources
    projects = []
    resources = []

    if any(k in role_lower for k in ["web", "frontend", "backend", "full stack", "software"]):
        projects = [
            {
                "title": "Full-Stack SaaS Platform with User Auth & REST API",
                "difficulty": "Intermediate / Advanced",
                "tech_stack": ["React", "Node.js", "Express", "PostgreSQL", "Tailwind CSS"],
                "description": "Build a production-ready SaaS web application featuring JWT authentication, state management, RESTful API endpoints, and database CRUD operations.",
                "resume_impact": "Demonstrates end-to-end full stack architecture, API design, and database modeling."
            },
            {
                "title": "Real-Time Collaborative Dashboard / Messaging App",
                "difficulty": "Advanced",
                "tech_stack": ["TypeScript", "WebSockets / Socket.io", "React", "Docker"],
                "description": "Develop a real-time multi-user application such as a live collaborative document editor, chat platform, or real-time data monitoring dashboard.",
                "resume_impact": "Highlights asynchronous JavaScript, WebSocket protocol mastery, and containerization."
            }
        ]
        resources = [
            {
                "title": "freeCodeCamp - Full Stack Web Development Course",
                "type": "YouTube Video",
                "url": "https://www.youtube.com/watch?v=nu_pCVPKzTk",
                "source": "freeCodeCamp",
                "description": "Comprehensive 12-hour video tutorial covering modern JavaScript, React, Node.js, and API architecture."
            },
            {
                "title": "MDN Web Docs - Modern JavaScript & Web APIs",
                "type": "Documentation",
                "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
                "source": "Mozilla Developer Network",
                "description": "Official reference guide for async/await, ES6+ syntax, DOM manipulation, and browser APIs."
            },
            {
                "title": "React Official Learn & Interactive Documentation",
                "type": "Official Guide",
                "url": "https://react.dev/learn",
                "source": "React Core Team",
                "description": "Modern React guides covering hooks, component lifecycle, state management, and server components."
            }
        ]

    elif any(k in role_lower for k in ["data analyst", "data scientist", "analytics", "business intelligence"]):
        projects = [
            {
                "title": "Customer Churn & E-Commerce RFM Segmentation Model",
                "difficulty": "Intermediate",
                "tech_stack": ["Python", "Pandas", "Scikit-Learn", "Seaborn", "Jupyter"],
                "description": "Perform exploratory data analysis (EDA) on a 100k+ transaction dataset. Build predictive classification models to forecast customer churn.",
                "resume_impact": "Proves data wrangling, statistical hypothesis testing, and business impact modeling."
            },
            {
                "title": "Interactive Executive Sales Dashboard",
                "difficulty": "Beginner / Intermediate",
                "tech_stack": ["SQL", "Power BI / Tableau", "Excel", "Data Modeling"],
                "description": "Architect a multi-page interactive dashboard calculating KPIs, revenue growth rates, regional sales trends, and profit margins.",
                "resume_impact": "Demonstrates business intelligence visualization and complex SQL aggregation."
            }
        ]
        resources = [
            {
                "title": "Alex The Analyst - Data Analyst Complete Portfolio Project",
                "type": "YouTube Video",
                "url": "https://www.youtube.com/watch?v=r-uOLxNrNk8",
                "source": "Alex The Analyst",
                "description": "Step-by-step video guide building a complete end-to-end data analytics project using SQL, Excel, and Tableau."
            },
            {
                "title": "Kaggle - Datasets, Notebooks & Predictive Analytics Competitions",
                "type": "Reference Platform",
                "url": "https://www.kaggle.com/",
                "source": "Kaggle / Google",
                "description": "World's largest data science hub featuring open-source datasets, starter notebooks, and code tutorials."
            },
            {
                "title": "freeCodeCamp - SQL & Relational Database Certification",
                "type": "Interactive Course",
                "url": "https://www.youtube.com/watch?v=HXV3zeQKqGY",
                "source": "freeCodeCamp",
                "description": "4-hour SQL tutorial covering joins, GROUP BY aggregations, window functions, and subqueries."
            }
        ]

    elif any(k in role_lower for k in ["predictive modeling", "analytics", "data science"]):
        projects = [
            {
                "title": "Document Information Retrieval System",
                "difficulty": "Advanced",
                "tech_stack": ["Python", "FAISS", "Streamlit", "NLTK"],
                "description": "Build a document retrieval application that ingests custom PDF/markdown documents and performs vector similarity search.",
                "resume_impact": "Showcases text processing, vector search, and API orchestration."
            }
        ]
        resources = [
            {
                "title": "Kaggle - Practical Data Science & Predictive Analytics",
                "type": "Free Course",
                "url": "https://www.kaggle.com/learn",
                "source": "Kaggle",
                "description": "Hands-on predictive analytics course teaching data science, visualization, and model deployment."
            }
        ]

    elif any(k in role_lower for k in ["cloud", "devops", "kubernetes", "docker", "infrastructure"]):
        projects = [
            {
                "title": "Automated Multi-Environment CI/CD Infrastructure on AWS",
                "difficulty": "Advanced",
                "tech_stack": ["Terraform", "AWS", "GitHub Actions", "Docker", "Kubernetes"],
                "description": "Provision AWS cloud infrastructure (VPC, EKS, RDS) using Terraform Infrastructure as Code. Build automated GitHub Actions CI/CD pipelines.",
                "resume_impact": "Proves enterprise cloud automation, IaC proficiency, and container orchestration."
            },
            {
                "title": "Cloud-Native Observability & Monitoring Suite",
                "difficulty": "Intermediate",
                "tech_stack": ["Docker", "Prometheus", "Grafana", "Linux"],
                "description": "Deploy a distributed monitoring stack to track CPU, memory, API latency, and container health metrics with custom Grafana alerts.",
                "resume_impact": "Demonstrates Site Reliability Engineering (SRE) and cloud infrastructure monitoring."
            }
        ]
        resources = [
            {
                "title": "TechWorld with Nana - Docker & Kubernetes Full Course",
                "type": "YouTube Video",
                "url": "https://www.youtube.com/watch?v=X48VuDVv0do",
                "source": "TechWorld with Nana",
                "description": "Comprehensive tutorial covering containerization, Dockerfiles, Kubernetes pods, deployments, and services."
            },
            {
                "title": "AWS Skill Builder & Cloud Practitioner Training",
                "type": "Official Platform",
                "url": "https://aws.amazon.com/skill-builder/",
                "source": "Amazon Web Services",
                "description": "Official AWS digital courses and hands-on cloud architecture labs."
            },
            {
                "title": "DevOps Roadmap & Interactive Learning Paths",
                "type": "Interactive Guide",
                "url": "https://roadmap.sh/devops",
                "source": "roadmap.sh",
                "description": "Step-by-step learning path covering CI/CD, Linux administration, Cloud, and IaC."
            }
        ]

    else:
        # General Professional / Other Roles
        projects = [
            {
                "title": "Cross-Functional Project Optimization Charter & Case Study",
                "difficulty": "Intermediate",
                "tech_stack": ["Project Charter", "Risk Register", "Excel / Sheets", "Process Mapping"],
                "description": "Draft a comprehensive project management framework containing stakeholder analysis, risk registers, Gantt charts, and quantitative ROI deliverables.",
                "resume_impact": "Demonstrates strategic project governance, leadership, and structured problem-solving."
            }
        ]
        resources = [
            {
                "title": "Google Professional Career Certificates & Case Studies",
                "type": "Video Course",
                "url": "https://www.youtube.com/user/google",
                "source": "Google",
                "description": "Official foundational training in project management, data analysis, and professional strategy."
            },
            {
                "title": "Harvard Business Review - Effective Communication & Leadership",
                "type": "Reference Guide",
                "url": "https://hbr.org/",
                "source": "Harvard Business Review",
                "description": "Articles and guides on executive presentation skills, cross-functional leadership, and strategic planning."
            }
        ]

    return {
        "projects": projects,
        "resources": resources
    }
