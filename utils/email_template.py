"""
Email template generator for newsletters
"""

from datetime import datetime
from typing import List, Dict


class NewsletterTemplate:
    """Generates HTML email templates for newsletters."""
    
    @staticmethod
    def generate_html(summary: str, articles: List[Dict]) -> str:
        """
        Generate a beautiful HTML email template.
        
        Template structure:
        1. Header - Purple gradient with title and date
        2. Summary - AI-generated analysis in a highlighted box
        3. Articles - Top 10 recent articles with links
        4. Footer - Branding and info
        """
        current_date = datetime.now().strftime("%B %d, %Y")
        
        # Build articles HTML
        articles_html = ""
        for article in articles[:10]:
            articles_html += f"""
            <div class="article">
                <div class="article-title">{article['title']}</div>
                <div class="article-meta">{article['source']} • {article['published'].strftime('%B %d, %Y at %H:%M')}</div>
                <a href="{article['link']}" class="article-link" target="_blank">Read more →</a>
            </div>"""
        
        # Complete HTML template
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 8px 8px 0 0;
            margin: -30px -30px 30px -30px;
            text-align: center;
        }}
        .header h1 {{ margin: 0; font-size: 28px; font-weight: 600; }}
        .header p {{ margin: 10px 0 0 0; opacity: 0.9; font-size: 14px; }}
        .summary {{
            background-color: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        .summary pre {{
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: inherit;
            margin: 0;
        }}
        .articles {{ margin-top: 30px; }}
        .articles h2 {{
            color: #667eea;
            font-size: 20px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e9ecef;
        }}
        .article {{
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 6px;
            background-color: #f8f9fa;
        }}
        .article:hover {{
            transform: translateX(5px);
            background-color: #e9ecef;
        }}
        .article-title {{
            font-weight: 600;
            color: #2c3e50;
            font-size: 16px;
            margin-bottom: 8px;
        }}
        .article-meta {{
            color: #6c757d;
            font-size: 13px;
            margin-bottom: 8px;
        }}
        .article-link {{
            color: #667eea;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
        }}
        .article-link:hover {{ text-decoration: underline; }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e9ecef;
            text-align: center;
            color: #6c757d;
            font-size: 13px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 KeepMePosted</h1>
            <p>Your AI-Powered Tech Newsletter • {current_date}</p>
        </div>
        
        <div class="summary">
            <pre>{summary}</pre>
        </div>
        
        <div class="articles">
            <h2>📰 Recent Articles</h2>
            {articles_html}
        </div>
        
        <div class="footer">
            <p>Powered by Google Gemini • Generated with KeepMePosted</p>
            <p>You're receiving this because you subscribed to tech news updates</p>
        </div>
    </div>
</body>
</html>"""
