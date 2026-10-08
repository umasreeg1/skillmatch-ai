"""
Comprehensive Skill Taxonomy & Alias Mapping for SKILLMATCH AI
"""

SKILL_TAXONOMY = {
    "Programming": [
        "Python", "Java", "C++", "JavaScript", "TypeScript", "Go", "Rust", "C#", "Ruby", "PHP", "Swift", "Kotlin"
    ],
    "AI/ML": [
        "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "TensorFlow", "PyTorch", "Scikit-learn", 
        "Keras", "HuggingFace", "LLM", "Generative AI", "OpenCV", "Reinforcement Learning", "XGBoost", "Neural Networks"
    ],
    "Data": [
        "NumPy", "Pandas", "Matplotlib", "Seaborn", "SQL", "Data Analysis", "Data Visualization", "PostgreSQL", 
        "MySQL", "MongoDB", "Redis", "Data Engineering", "ETL", "Apache Spark", "Hadoop", "Tableau", "Power BI"
    ],
    "Cloud": [
        "AWS", "Azure", "GCP", "Cloud Computing", "Serverless", "Lambda", "S3", "EC2"
    ],
    "DevOps": [
        "Docker", "Kubernetes", "CI/CD", "GitHub Actions", "Terraform", "Jenkins", "Ansible", "Linux", "Bash"
    ],
    "Web": [
        "React", "Node.js", "FastAPI", "Flask", "Django", "REST API", "GraphQL", "HTML", "CSS", "Tailwind CSS", "Vue.js", "Angular"
    ],
    "Tools": [
        "Git", "GitHub", "Jupyter", "VS Code", "Postman", "JIRA"
    ],
    "Methodologies": [
        "Agile", "Scrum", "Kanban", "TDD", "Microservices", "System Design", "OOP"
    ]
}

# Mapping of aliases/variations to standard skill name
SKILL_ALIASES = {
    "python3": "Python",
    "js": "JavaScript",
    "ts": "TypeScript",
    "golang": "Go",
    "ml": "Machine Learning",
    "dl": "Deep Learning",
    "natural language processing": "NLP",
    "cv": "Computer Vision",
    "sklearn": "Scikit-learn",
    "tf": "TensorFlow",
    "large language models": "LLM",
    "genai": "Generative AI",
    "amazon web services": "AWS",
    "google cloud platform": "GCP",
    "google cloud": "GCP",
    "microsoft azure": "Azure",
    "postgres": "PostgreSQL",
    "spark": "Apache Spark",
    "k8s": "Kubernetes",
    "continuous integration": "CI/CD",
    "continuous deployment": "CI/CD",
    "reactjs": "React",
    "react.js": "React",
    "nodejs": "Node.js",
    "node": "Node.js",
    "restful api": "REST API",
    "rest apis": "REST API",
    "restful apis": "REST API",
    "rest": "REST API",
    "object oriented programming": "OOP",
    "test driven development": "TDD",
    "bash scripting": "Bash",
    "shell scripting": "Bash",
    "jupyter notebook": "Jupyter",
    "jupyter notebooks": "Jupyter",
    "github action": "GitHub Actions",
}

# Reverse lookup dictionary: skill -> category
SKILL_TO_CATEGORY = {}
for category, skills in SKILL_TAXONOMY.items():
    for skill in skills:
        SKILL_TO_CATEGORY[skill.lower()] = category

def get_skill_category(skill_name: str) -> str:
    return SKILL_TO_CATEGORY.get(skill_name.lower(), "General Technical")

def get_all_canonical_skills() -> list:
    all_skills = []
    for category, skills in SKILL_TAXONOMY.items():
        all_skills.extend(skills)
    return all_skills
