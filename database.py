import sqlite3
import json
import os

# Use /tmp directory on Vercel serverless environment
DB_NAME = os.path.join("/tmp", "database.db") if os.environ.get("VERCEL") else "database.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create job_roles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_title TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            core_skills TEXT NOT NULL,
            optional_skills TEXT NOT NULL
        )
    ''')

    # Create evaluation_history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS evaluation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            target_role TEXT NOT NULL,
            overall_score INTEGER NOT NULL,
            ats_score INTEGER NOT NULL,
            section_scores TEXT NOT NULL,
            matched_skills TEXT NOT NULL,
            missing_skills TEXT NOT NULL,
            feedback TEXT NOT NULL,
            analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Comprehensive Expanded Job Roles & Qualifications Database
    roles = [
        # Software Engineering
        ("Web Developer", "Software Engineering", "Builds dynamic web applications using modern HTML, CSS, JavaScript, and frameworks.", 
         ["javascript", "html", "css", "react", "git", "node.js", "rest api"], 
         ["typescript", "vue", "next.js", "docker", "tailwind"]),

        ("Frontend Developer", "Software Engineering", "Specializes in client-side web interfaces, user experience, and responsive design.",
         ["javascript", "html", "css", "react", "typescript", "git", "responsive design"],
         ["redux", "tailwind", "next.js", "webpack", "jest"]),

        ("Backend Engineer", "Software Engineering", "Engineers server-side business logic, databases, APIs, and microservices.",
         ["python", "node.js", "sql", "rest api", "git", "database design", "docker"],
         ["postgressql", "mongodb", "redis", "graphql", "aws"]),

        ("Full Stack Developer", "Software Engineering", "Develops both frontend user interfaces and backend server infrastructure.",
         ["javascript", "react", "node.js", "sql", "git", "rest api", "html", "css"],
         ["typescript", "docker", "mongodb", "aws", "graphql"]),

        ("Mobile App Developer", "Software Engineering", "Creates native and cross-platform mobile applications for iOS and Android.",
         ["mobile app development", "react native", "flutter", "swift", "kotlin", "git", "rest api"],
         ["ios", "android", "firebase", "sqlite", "ci/cd"]),

        ("Cybersecurity Analyst", "Security & IT", "Monitors networks, identifies vulnerabilities, and enforces digital security policies.",
         ["cybersecurity", "network security", "linux", "firewalls", "vulnerability management", "siem", "incident response"],
         ["python", "penetration testing", "wireshark", "ethical hacking", "cissp"]),

        # Data & Machine Learning
        ("Data Analyst", "Data & Analytics", "Extracts actionable business insights using SQL, Python, Excel, and visualization dashboards.", 
         ["python", "sql", "excel", "tableau", "power bi", "data visualization", "statistics"], 
         ["r", "pandas", "numpy", "jira", "etl"]),

        ("Data Scientist", "Data & Analytics", "Builds predictive statistical models, machine learning algorithms, and deep analytics.", 
         ["python", "machine learning", "statistics", "sql", "pandas", "scikit-learn", "data modeling"], 
         ["spark", "hadoop", "cloud", "a/b testing"]),

        ("ML Engineer", "Machine Learning", "Develops machine learning models, neural networks, and NLP pipelines.", 
         ["python", "pytorch", "tensorflow", "machine learning", "nlp"], 
         ["scikit-learn", "opencv", "transformers", "langchain", "api"]),

        ("Data Engineer", "Data & Infrastructure", "Constructs scalable data pipelines, data warehouses, and ETL workflows.",
         ["python", "sql", "etl", "data warehousing", "spark", "docker", "git"],
         ["airflow", "snowflake", "bigquery", "kafka", "aws"]),

        ("Business Intelligence Analyst", "Data & Business", "Translates raw data into strategic business dashboards and KPIs.",
         ["sql", "power bi", "tableau", "excel", "data analysis", "reporting", "business intelligence"],
         ["python", "dbt", "data modeling", "etl", "kpis"]),

        # Cloud & Operations
        ("Cloud Engineer", "Cloud & Infrastructure", "Architects scalable cloud infrastructure on AWS, Azure, or GCP.", 
         ["aws", "azure", "gcp", "docker", "kubernetes", "terraform", "linux"], 
         ["bash", "python", "ansible", "ci/cd", "iam"]),

        ("DevOps Engineer", "Operations & Automation", "Automates CI/CD deployment pipelines and container orchestration systems.", 
         ["docker", "kubernetes", "ci/cd", "git", "linux", "jenkins", "terraform"], 
         ["python", "bash", "prometheus", "grafana", "aws"]),

        ("Network / Systems Administrator", "IT & Infrastructure", "Configures enterprise server hardware, networks, Active Directory, and system uptime.",
         ["linux", "windows server", "networking", "tcp/ip", "active directory", "troubleshooting", "system administration"],
         ["powershell", "bash", "dns", "vmware", "cisco"]),

        # Product, Design & Business
        ("Product Manager", "Product & Management", "Drives product vision, roadmap planning, user research, and cross-functional execution.",
         ["product management", "agile", "scrum", "product roadmap", "user research", "data analysis", "jira"],
         ["wireframing", "sql", "a/b testing", "stakeholder management", "kpis"]),

        ("Project Manager", "Product & Management", "Oversees project scope, schedules, risk mitigation, and team deliverables.",
         ["project management", "agile", "scrum", "pmp", "risk management", "budgeting", "jira"],
         ["trello", "confluence", "stakeholder management", "ms project", "leadership"]),

        ("Business Analyst", "Product & Management", "Gathers business requirements, maps process flows, and bridging IT with business stakeholders.",
         ["business analysis", "requirements gathering", "process mapping", "sql", "excel", "agile", "jira"],
         ["tableau", "visio", "scrum", "use cases", "stakeholder management"]),

        ("UI/UX Designer", "Design & Creative", "Designs intuitive digital interfaces, wireframes, visual prototypes, and design systems.",
         ["ui/ux design", "figma", "wireframing", "prototyping", "user research", "visual design", "design systems"],
         ["adobe xd", "illustrator", "html", "css", "usability testing"]),

        ("Digital Marketing Specialist", "Marketing & Growth", "Executes SEO, PPC ad campaigns, content marketing, and conversion funnel optimizations.",
         ["digital marketing", "seo", "sem", "google analytics", "content marketing", "social media marketing", "email marketing"],
         ["copywriting", "hubspot", "wordpress", "ppc", "a/b testing"]),

        ("Financial / Business Analyst", "Finance & Strategy", "Performs financial modeling, forecasting, budgeting, and corporate valuation.",
         ["financial modeling", "excel", "financial analysis", "forecasting", "budgeting", "data analysis", "valuation"],
         ["stakeholder management", "power bi", "sap", "accounting", "corporate finance"]),

        # Universal Fallback Option
        ("Other / Custom Role", "General Professional", "Universal assessment for custom job roles, non-tech majors, and specialized fields.",
         ["communication", "problem solving", "leadership", "project management", "teamwork", "time management", "analytical thinking", "adaptability"],
         ["microsoft office", "data analysis", "presentation", "critical thinking", "budgeting", "organization"])
    ]

    for title, cat, desc, core, opt in roles:
        cursor.execute('''
            INSERT OR REPLACE INTO job_roles (role_title, category, description, core_skills, optional_skills)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, cat, desc, json.dumps(core), json.dumps(opt)))

    conn.commit()
    conn.close()
    print("Database successfully initialized & pre-seeded with 21+ job roles!")

if __name__ == '__main__':
    init_db()
