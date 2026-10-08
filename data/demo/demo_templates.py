"""
Predefined Job Description Templates & Demo Data for SKILLMATCH AI
"""

DEMO_RESUME_TEXT = """
MEGANA V.
AI & Machine Learning Software Engineer
Email: megana@example.com | GitHub: github.com/megana-ai | LinkedIn: linkedin.com/in/megana

PROFESSIONAL SUMMARY:
Results-driven AI/ML Engineer with strong foundation in Python, Machine Learning, Data Structures, and SQL. Experienced in developing predictive machine learning models using Scikit-learn, data analysis with Pandas and NumPy, and version control with Git & GitHub. Passionate about artificial intelligence, model optimization, and scalable backend services.

TECHNICAL SKILLS:
• Programming Languages: Python, JavaScript, SQL, C++
• AI / Machine Learning: Machine Learning, Deep Learning, Scikit-learn, Neural Networks
• Data Science & Analytics: NumPy, Pandas, Matplotlib, Data Analysis, Data Visualization
• Developer Tools: Git, GitHub, Jupyter Notebook, VS Code
• Web & Backend: FastAPI, REST API, HTML, CSS
• Methodologies: Agile, OOP, System Design

PROJECTS:
1. Predictive Machine Learning Classification Pipeline (Python, Scikit-learn, Pandas)
   - Engineered a supervised classification model to analyze customer churn datasets with 88.5% accuracy across 10,000+ data samples.
   - Performed feature selection and exploratory data analysis using Pandas, NumPy, and Matplotlib.

2. RESTful Sentiment Analysis Service (FastAPI, Python, Git)
   - Built an asynchronous REST API using FastAPI to serve machine learning inference predictions.
   - Containerized application code and pushed version-controlled updates via Git and GitHub Actions.

EDUCATION:
B.Tech in Computer Science & Engineering (Artificial Intelligence & Machine Learning)
CGPA: 8.9/10.0
"""

JOB_TEMPLATES = {
    "junior_aiml": {
        "id": "junior_aiml",
        "title": "Junior AI/ML Engineer",
        "category": "AI/ML",
        "description": """
We are seeking a motivated Junior AI/ML Engineer to join our Artificial Intelligence team. 

Key Requirements:
• Strong proficiency in Python programming and SQL.
• Experience building machine learning models using Scikit-learn and TensorFlow or PyTorch.
• Solid background in Data Analysis using Pandas, NumPy, and Matplotlib.
• Familiarity with NLP (Natural Language Processing) concepts and Computer Vision.
• Experience with cloud platforms such as AWS or Azure.
• Knowledge of containerization with Docker and version control with Git/GitHub.
• Understanding of Agile software development methodologies.
"""
    },
    "data_analyst": {
        "id": "data_analyst",
        "title": "Data Analyst",
        "category": "Data",
        "description": """
Looking for a detail-oriented Data Analyst to analyze complex datasets and create actionable insights.

Requirements:
• Advanced SQL and Python skills for data manipulation and querying.
• Hands-on experience with Pandas, NumPy, and Data Analysis techniques.
• Expertise in Data Visualization using Matplotlib, Seaborn, and Tableau or Power BI.
• Ability to communicate insights to technical and non-technical stakeholders.
• Knowledge of Git and Jupyter Notebooks.
"""
    },
    "python_developer": {
        "id": "python_developer",
        "title": "Python Developer",
        "category": "Backend",
        "description": """
We are looking for a skilled Python Developer to build high-performance web applications and backend APIs.

Requirements:
• Expert knowledge of Python and object-oriented programming (OOP).
• Experience building web frameworks with FastAPI or Flask / Django.
• Strong experience designing REST APIs and working with PostgreSQL or MySQL databases.
• Proficient with Git, Docker, and CI/CD pipelines.
• Familiarity with Linux environments and unit testing (TDD).
"""
    },
    "ml_engineer": {
        "id": "ml_engineer",
        "title": "Machine Learning Engineer",
        "category": "AI/ML",
        "description": """
Seeking a Machine Learning Engineer to design, train, and deploy scalable ML models to production.

Requirements:
• Proficiency in Python, PyTorch, TensorFlow, and Scikit-learn.
• In-depth understanding of Deep Learning, Neural Networks, and NLP.
• Experience with MLOps, Docker, Kubernetes, and AWS (SageMaker, S3, EC2).
• Strong skills in SQL, Apache Spark, and big data processing.
• Experience with CI/CD and GitHub Actions for automated deployment.
"""
    },
    "frontend_developer": {
        "id": "frontend_developer",
        "title": "Frontend Developer",
        "category": "Web",
        "description": """
Looking for a creative Frontend Developer to craft intuitive user experiences.

Requirements:
• Strong mastery of JavaScript, TypeScript, HTML, and CSS / Tailwind CSS.
• Hands-on experience with React, Vue.js, or Next.js.
• Experience consuming REST API and GraphQL endpoints.
• Proficiency with Git, VS Code, and responsive UI design principles.
• Familiarity with Agile workflows and UI performance optimization.
"""
    },
    "backend_developer": {
        "id": "backend_developer",
        "title": "Backend Developer",
        "category": "Web",
        "description": """
Seeking a Backend Developer to design scalable microservices and server infrastructure.

Requirements:
• Proficiency in Python, Node.js, Java, or Go.
• Experience building REST API and GraphQL microservices with FastAPI or Express.js.
• Database expertise in PostgreSQL, MySQL, Redis, and MongoDB.
• Hands-on experience with Docker, Kubernetes, AWS, and CI/CD.
• Solid grasp of System Design, Data Structures, and Agile.
"""
    },
    "fullstack_developer": {
        "id": "fullstack_developer",
        "title": "Full Stack Developer",
        "category": "Web",
        "description": """
We are hiring a Full Stack Developer to build modern end-to-end web applications.

Requirements:
• Frontend: JavaScript, TypeScript, React, HTML, CSS.
• Backend: Python, Node.js, FastAPI, REST API.
• Database: SQL, PostgreSQL, MongoDB, Redis.
• DevOps: Docker, Git, GitHub Actions, AWS.
• Methodologies: Agile, System Design, OOP.
"""
    },
    "data_scientist": {
        "id": "data_scientist",
        "title": "Data Scientist",
        "category": "AI/ML",
        "description": """
Seeking a Data Scientist to extract intelligence from structured and unstructured data.

Requirements:
• High proficiency in Python, SQL, and R.
• Machine Learning expertise with Scikit-learn, XGBoost, and TensorFlow.
• Deep expertise in Data Analysis, Pandas, NumPy, and statistical modeling.
• Experience with NLP, LLM concepts, and Data Visualization tools.
• Ability to present data stories to executive leadership.
"""
    },
    "cloud_engineer": {
        "id": "cloud_engineer",
        "title": "Cloud Engineer",
        "category": "Cloud",
        "description": """
Looking for a Cloud Engineer to architect and manage secure cloud infrastructure.

Requirements:
• Expertise in AWS, Azure, or GCP cloud platforms.
• Strong experience with Infrastructure as Code using Terraform.
• Advanced Docker, Kubernetes, and Linux administration skills.
• Solid background in Python, Bash scripting, and Networking.
• Proficient in CI/CD, GitHub Actions, and cloud security best practices.
"""
    },
    "devops_engineer": {
        "id": "devops_engineer",
        "title": "DevOps Engineer",
        "category": "DevOps",
        "description": """
We are hiring a DevOps Engineer to automate build, test, and release pipelines.

Requirements:
• Hands-on mastery of Docker, Kubernetes, and CI/CD.
• Experience with GitHub Actions, Jenkins, and Ansible.
• Expertise in Cloud Computing (AWS, GCP) and Terraform.
• Strong scripting skills in Python, Bash, and Linux systems.
• Knowledge of Agile, Microservices monitoring, and Git.
"""
    }
}
