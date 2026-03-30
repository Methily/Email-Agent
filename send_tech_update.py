import smtplib
import requests
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import os

def get_github_repositories():
    """Fetch good/new GitHub repositories for requested topics, prioritizing major orgs."""
    try:
        topics = [
            "Neural network",
            "Quantum Computing",
            "DevSecOps",
            "Docker",
            "CI/CD",
            "Spiking Neural Network"
        ]

        preferred_orgs = [
            "google", "google-deepmind", "tensorflow",
            "meta", "facebookresearch", "pytorch"
        ]
        preferred_tokens = {"google", "meta", "facebook", "deepmind", "tensorflow", "pytorch"}
        recent_date = (datetime.utcnow() - timedelta(days=180)).strftime("%Y-%m-%d")

        candidates = {}
        base_url = "https://api.github.com/search/repositories"

        for topic in topics:
            general_query = f'"{topic}" in:name,description,readme stars:>50 archived:false'
            params = {
                "q": general_query,
                "sort": "updated",
                "order": "desc",
                "per_page": 5
            }
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            for repo in response.json().get("items", []):
                candidates[repo["full_name"]] = repo

            for org in preferred_orgs:
                org_query = f'org:{org} "{topic}" in:name,description,readme archived:false'
                org_params = {
                    "q": org_query,
                    "sort": "updated",
                    "order": "desc",
                    "per_page": 2
                }
                org_response = requests.get(base_url, params=org_params, timeout=10)
                org_response.raise_for_status()
                for repo in org_response.json().get("items", []):
                    candidates[repo["full_name"]] = repo

        scored = []
        for repo in candidates.values():
            owner = repo.get("owner", {}).get("login", "").lower()
            description = (repo.get("description") or "").lower()
            language = (repo.get("language") or "").lower()
            full_text = f"{owner} {description} {language}"
            preferred = any(token in full_text for token in preferred_tokens)
            recently_active = (repo.get("pushed_at") or "")[:10] >= recent_date
            score = (
                (3 if preferred else 0)
                + (2 if recently_active else 0)
                + min(int(repo.get("stargazers_count", 0) / 1000), 5)
            )
            scored.append((score, repo))

        scored.sort(key=lambda x: (x[0], x[1].get("stargazers_count", 0)), reverse=True)
        top_repos = scored[:3]

        repositories = []
        for score, repo in top_repos:
            repositories.append({
                "name": repo.get("full_name", "unknown/repo"),
                "description": repo.get("description") or "No description",
                "stars": repo.get("stargazers_count", 0),
                "language": repo.get("language") or "N/A",
                "url": repo.get("html_url", ""),
                "pushed_at": (repo.get("pushed_at") or "")[:10],
                "score": score
            })

        return repositories
    except Exception as e:
        print(f"Error fetching GitHub repositories: {e}")
        return []

def get_learning_articles(youtube_api_key):
    """Fetch 3 learning resources from 3 different requested topics."""
    try:
        if not youtube_api_key:
            print("YOUTUBE_API_KEY is missing. Skipping YouTube section.")
            return []

        all_topics = [
            "Docker",
            "CI/CD",
            "LangChain",
            "DevOps",
            "quantum computing",
            "neuromorphic computing"
        ]
        selected_topics = random.sample(all_topics, 3)
        resources = []
        url = "https://www.googleapis.com/youtube/v3/search"

        for topic in selected_topics:
            params = {
                "part": "snippet",
                "q": topic,
                "type": "video",
                "order": "date",
                "maxResults": 1,
                "key": youtube_api_key
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            items = response.json().get("items", [])

            if not items:
                continue

            item = items[0]
            snippet = item.get("snippet", {})
            video_id = item.get("id", {}).get("videoId")
            if not video_id:
                continue

            resources.append({
                "topic": topic,
                "title": snippet.get("title", "Untitled Video"),
                "description": snippet.get("description", "No description"),
                "channel": snippet.get("channelTitle", "Unknown Channel"),
                "published_at": snippet.get("publishedAt", ""),
                "url": f"https://www.youtube.com/watch?v={video_id}"
            })

        return resources
    except Exception as e:
        print(f"Error fetching learning resources: {e}")
        return []

def get_project_suggestions():
    """Return 3 project suggestions."""
    projects = [
        {
            'title': 'Build a REST API with FastAPI + PostgreSQL',
            'description': 'Create a production-ready REST API with user authentication, database migrations, and Docker deployment',
            'tech_stack': ['Python', 'FastAPI', 'PostgreSQL', 'Docker', 'SQLAlchemy'],
            'time': '6-8 hours',
            'level': 'Intermediate',
            'cost': '100% FREE',
            'learn': ['API design', 'Database modeling', 'Authentication', 'Containerization']
        },
        {
            'title': 'DevOps CI/CD Pipeline with GitHub Actions',
            'description': 'Set up automated testing, building, and deployment pipeline for a Python application',
            'tech_stack': ['GitHub Actions', 'Docker', 'Python', 'pytest', 'YAML'],
            'time': '4-5 hours',
            'level': 'Beginner-Intermediate',
            'cost': '100% FREE',
            'learn': ['CI/CD concepts', 'Automated testing', 'Docker builds', 'Deployment automation']
        },
        {
            'title': 'Build a CLI Tool with Python',
            'description': 'Create a command-line tool for automating daily tasks (file operations, API calls, data processing)',
            'tech_stack': ['Python', 'Click/Typer', 'Requests', 'JSON'],
            'time': '3-4 hours',
            'level': 'Beginner',
            'cost': '100% FREE',
            'learn': ['CLI design', 'Argument parsing', 'File handling', 'API integration']
        },
        {
            'title': 'Dockerize a Multi-Service Application',
            'description': 'Use Docker Compose to orchestrate a multi-container app (API + Database + Redis cache)',
            'tech_stack': ['Docker', 'Docker Compose', 'Python/Node.js', 'PostgreSQL', 'Redis'],
            'time': '5-6 hours',
            'level': 'Intermediate',
            'cost': '100% FREE',
            'learn': ['Docker networking', 'Container orchestration', 'Service communication', 'Environment configuration']
        },
        {
            'title': 'Machine Learning Model Deployment API',
            'description': 'Train a simple ML model and deploy it as an API using Flask/FastAPI',
            'tech_stack': ['Python', 'scikit-learn', 'Flask/FastAPI', 'Docker', 'pandas'],
            'time': '6-7 hours',
            'level': 'Intermediate',
            'cost': '100% FREE',
            'learn': ['ML basics', 'Model serialization', 'API deployment', 'Prediction endpoints']
        },
        {
            'title': 'Build a Job Queue System with Redis',
            'description': 'Create a background job processing system using Redis Queue (RQ)',
            'tech_stack': ['Python', 'Redis', 'RQ (Redis Queue)', 'Docker'],
            'time': '4-5 hours',
            'level': 'Intermediate',
            'cost': '100% FREE',
            'learn': ['Async processing', 'Task queues', 'Worker processes', 'Job scheduling']
        },
        {
            'title': 'Infrastructure as Code with Terraform',
            'description': 'Provision cloud resources using Terraform (works with free tiers of AWS/Azure)',
            'tech_stack': ['Terraform', 'AWS Free Tier', 'HCL', 'Git'],
            'time': '5-6 hours',
            'level': 'Intermediate',
            'cost': '100% FREE (with AWS Free Tier)',
            'learn': ['IaC concepts', 'Resource provisioning', 'State management', 'Cloud basics']
        },
        {
            'title': 'Log Aggregation System with ELK Stack',
            'description': 'Set up Elasticsearch, Logstash, and Kibana for log analysis using Docker',
            'tech_stack': ['Docker', 'Elasticsearch', 'Logstash', 'Kibana', 'Python'],
            'time': '6-8 hours',
            'level': 'Intermediate-Advanced',
            'cost': '100% FREE (local Docker)',
            'learn': ['Log aggregation', 'Data visualization', 'Search engines', 'Monitoring']
        }
    ]
    
    return random.sample(projects, 3)

def create_email_content(youtube_api_key):
    """Generate the email HTML content"""
    
    learning_articles = get_learning_articles(youtube_api_key)
    github_repositories = get_github_repositories()
    projects = get_project_suggestions()
    
    current_date = datetime.now().strftime("%B %d, %Y")
    
    # Build learning articles section
    articles_html = ""
    for idx, article in enumerate(learning_articles, 1):
        published_text = article['published_at'][:10] if article['published_at'] else "N/A"
        articles_html += f"""
        <div style="margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid #dddddd;">
            <strong>{idx}. Topic: {article['topic']}</strong>
            <br>
            <span>{article['title']}</span>
            <br>
            <span>{article['description'][:180]}...</span>
            <br>
            <span>Source: YouTube ({article['channel']}) | Published: {published_text}</span>
            <br>
            <a href="{article['url']}">Open resource</a>
        </div>
        """
    
    # Build projects section
    projects_html = ""
    for idx, project in enumerate(projects, 1):
        tech_stack_html = ", ".join(project['tech_stack'])
        learn_items = ", ".join(project['learn'])
        projects_html += f"""
        <div style="margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid #dddddd;">
            <strong>{idx}. {project['title']}</strong>
            <br>
            <span>{project['description']}</span>
            <br>
            <span>Time: {project['time']} | Level: {project['level']} | Cost: {project['cost']}</span>
            <br>
            <span>Tech stack: {tech_stack_html}</span>
            <br>
            <span>You will learn: {learn_items}</span>
        </div>
        """

    # Build GitHub repositories section
    repos_html = ""
    for idx, repo in enumerate(github_repositories, 1):
        repos_html += f"""
        <div style="margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid #dddddd;">
            <strong>{idx}. {repo['name']}</strong>
            <br>
            <span>{repo['description'][:180]}...</span>
            <br>
            <span>Language: {repo['language']} | Stars: {repo['stars']:,} | Last update: {repo['pushed_at']}</span>
            <br>
            <a href="{repo['url']}">Open repository</a>
        </div>
        """
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.5; color: #222; max-width: 700px; margin: 0 auto; padding: 16px;">
        <h1 style="margin-bottom: 0;">Weekly Tech Update</h1>
        <p style="margin-top: 4px;">{current_date}</p>

        <h2>3 Learning Articles</h2>
        {articles_html}

        <h2>3 Project Ideas</h2>
        {projects_html}

        <h2>3 GitHub Repositories</h2>
        {repos_html}

        <p style="margin-top: 24px;">Happy coding.</p>
    </body>
    </html>
    """
    
    return html_content

def send_email(sender_email, sender_password, recipient_email, youtube_api_key):
    """Send the email using Gmail SMTP"""
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🚀 Weekly Tech Updates - {datetime.now().strftime('%B %d, %Y')}"
        msg['From'] = sender_email
        msg['To'] = recipient_email
        
        # Generate email content
        html_content = create_email_content(youtube_api_key)
        
        # Attach HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Send email via Gmail SMTP
        print("Connecting to Gmail SMTP server...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        print("Logging in...")
        server.login(sender_email, sender_password)
        
        print("Sending email...")
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Email sent successfully to {recipient_email}!")
        
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        raise

if __name__ == "__main__":
    # Get credentials from environment variables (set in GitHub Secrets)
    SENDER_EMAIL = os.getenv('SENDER_EMAIL')
    SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
    RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
    
    if not all([SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL, YOUTUBE_API_KEY]):
        print("❌ Error: Missing environment variables!")
        print("Please set: SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL, YOUTUBE_API_KEY")
        exit(1)
    
    print("Starting Tech Email Agent...")
    print(f"Sending to: {RECIPIENT_EMAIL}")
    
    send_email(SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL, YOUTUBE_API_KEY)