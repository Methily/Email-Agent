import smtplib
import requests
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

def get_github_trending():
    """Fetch trending repositories from GitHub"""
    try:
        # Backend, DevOps, AI/ML focused languages
        languages = ['python', 'go', 'rust', 'java']
        lang = random.choice(languages)
        
        url = f"https://api.github.com/search/repositories"
        params = {
            'q': f'language:{lang} stars:>100',
            'sort': 'stars',
            'order': 'desc',
            'per_page': 5
        }
        
        response = requests.get(url, params=params, timeout=10)
        repos = response.json().get('items', [])
        
        trending = []
        for repo in repos[:3]:
            trending.append({
                'name': repo['name'],
                'description': repo['description'] or 'No description',
                'stars': repo['stargazers_count'],
                'language': repo['language'],
                'url': repo['html_url']
            })
        
        return trending
    except Exception as e:
        print(f"Error fetching GitHub trending: {e}")
        return []

def get_devto_articles():
    """Fetch latest dev.to articles on backend/devops/AI"""
    try:
        tags = ['docker', 'kubernetes', 'python', 'devops', 'machinelearning', 'backend']
        tag = random.choice(tags)
        
        url = f"https://dev.to/api/articles?tag={tag}&per_page=5"
        response = requests.get(url, timeout=10)
        articles = response.json()
        
        tech_news = []
        for article in articles[:3]:
            tech_news.append({
                'title': article['title'],
                'description': article['description'],
                'url': article['url'],
                'tags': article['tag_list']
            })
        
        return tech_news
    except Exception as e:
        print(f"Error fetching dev.to articles: {e}")
        return []

def get_project_suggestion():
    """Suggest a project based on backend/devops/AI topics"""
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
    
    return random.choice(projects)

def create_email_content():
    """Generate the email HTML content"""
    
    trending_repos = get_github_trending()
    tech_articles = get_devto_articles()
    project = get_project_suggestion()
    
    current_date = datetime.now().strftime("%B %d, %Y")
    
    # Build trending repos section
    repos_html = ""
    for repo in trending_repos:
        repos_html += f"""
        <div style="margin-bottom: 15px; padding: 10px; background: #f8f9fa; border-radius: 5px;">
            <strong style="color: #2563eb;">{repo['name']}</strong> ⭐ {repo['stars']:,}
            <br>
            <span style="color: #6b7280; font-size: 14px;">{repo['description'][:150]}...</span>
            <br>
            <span style="background: #dbeafe; color: #1e40af; padding: 2px 8px; border-radius: 3px; font-size: 12px; margin-top: 5px; display: inline-block;">
                {repo['language']}
            </span>
            <br>
            <a href="{repo['url']}" style="color: #2563eb; font-size: 14px;">View on GitHub →</a>
        </div>
        """
    
    # Build tech news section
    news_html = ""
    for idx, article in enumerate(tech_articles, 1):
        tags_html = " ".join([f'<span style="background: #e0e7ff; color: #4338ca; padding: 2px 6px; border-radius: 3px; font-size: 11px;">#{tag}</span>' for tag in article['tags'][:3]])
        news_html += f"""
        <div style="margin-bottom: 15px;">
            <strong style="color: #1f2937;">{idx}. {article['title']}</strong>
            <br>
            <span style="color: #6b7280; font-size: 14px;">{article['description'][:200]}...</span>
            <br>
            <div style="margin-top: 5px;">{tags_html}</div>
            <a href="{article['url']}" style="color: #2563eb; font-size: 14px;">Read more →</a>
        </div>
        """
    
    # Build project section
    tech_stack_html = " • ".join(project['tech_stack'])
    learn_items = "<br>".join([f"        • {item}" for item in project['learn']])
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 700px; margin: 0 auto; padding: 20px;">
        
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 30px;">
            <h1 style="margin: 0; font-size: 28px;">🚀 Weekly Tech Updates</h1>
            <p style="margin: 10px 0 0 0; opacity: 0.9;">{current_date}</p>
        </div>
        
        <div style="margin-bottom: 30px;">
            <p style="font-size: 16px; color: #4b5563;">Hi there! 👋</p>
            <p style="font-size: 16px; color: #4b5563;">Here's your weekly dose of backend, DevOps, and AI inspiration!</p>
        </div>
        
        <!-- Tech News Section -->
        <div style="margin-bottom: 40px;">
            <h2 style="color: #1f2937; border-bottom: 3px solid #667eea; padding-bottom: 10px; margin-bottom: 20px;">
                📰 TRENDING TECH NEWS
            </h2>
            {news_html}
        </div>
        
        <!-- Project of the Week -->
        <div style="margin-bottom: 40px; background: #f0f9ff; padding: 20px; border-radius: 10px; border-left: 5px solid #0ea5e9;">
            <h2 style="color: #0c4a6e; margin-top: 0;">
                🚀 PROJECT OF THE WEEK
            </h2>
            <h3 style="color: #0369a1; margin-bottom: 10px;">{project['title']}</h3>
            <p style="color: #475569; font-size: 15px;">{project['description']}</p>
            
            <div style="margin: 20px 0;">
                <div style="margin-bottom: 10px;">
                    <span style="background: #22c55e; color: white; padding: 5px 12px; border-radius: 5px; font-weight: bold; font-size: 14px;">
                        💰 {project['cost']}
                    </span>
                    <span style="background: #f59e0b; color: white; padding: 5px 12px; border-radius: 5px; font-weight: bold; font-size: 14px; margin-left: 10px;">
                        ⏱️ {project['time']}
                    </span>
                    <span style="background: #8b5cf6; color: white; padding: 5px 12px; border-radius: 5px; font-weight: bold; font-size: 14px; margin-left: 10px;">
                        🎯 {project['level']}
                    </span>
                </div>
            </div>
            
            <div style="margin-bottom: 15px;">
                <strong style="color: #1e293b;">Tech Stack:</strong>
                <br>
                <span style="color: #475569; font-size: 14px;">{tech_stack_html}</span>
            </div>
            
            <div>
                <strong style="color: #1e293b;">What you'll learn:</strong>
                <br>
                <span style="color: #475569; font-size: 14px;">
{learn_items}
                </span>
            </div>
        </div>
        
        <!-- Trending Repositories -->
        <div style="margin-bottom: 40px;">
            <h2 style="color: #1f2937; border-bottom: 3px solid #667eea; padding-bottom: 10px; margin-bottom: 20px;">
                🔥 TRENDING REPOSITORIES
            </h2>
            {repos_html}
        </div>
        
        <!-- Footer -->
        <div style="text-align: center; padding: 20px; background: #f9fafb; border-radius: 10px; margin-top: 40px;">
            <p style="color: #6b7280; font-size: 14px; margin: 0;">
                Happy coding! 🎉
            </p>
            <p style="color: #9ca3af; font-size: 12px; margin: 10px 0 0 0;">
                You're receiving this because you signed up for weekly tech updates.
            </p>
        </div>
        
    </body>
    </html>
    """
    
    return html_content

def send_email(sender_email, sender_password, recipient_email):
    """Send the email using Gmail SMTP"""
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🚀 Weekly Tech Updates - {datetime.now().strftime('%B %d, %Y')}"
        msg['From'] = sender_email
        msg['To'] = recipient_email
        
        # Generate email content
        html_content = create_email_content()
        
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
    
    if not all([SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL]):
        print("❌ Error: Missing environment variables!")
        print("Please set: SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL")
        exit(1)
    
    print("Starting Tech Email Agent...")
    print(f"Sending to: {RECIPIENT_EMAIL}")
    
    send_email(SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL)