import os
import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from collections import Counter
from wordcloud import WordCloud
import certifi

# Ensure NLTK stop words are downloaded
#nltk.download('stopwords')

def fetch_github_issues(owner, repo):
    """Fetch GitHub issues using the GitHub API."""
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    try:
        response = requests.get(url, headers=headers, verify=certifi.where())
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch issues: {e}")
        return None

def preprocess_text(text):
    """Preprocess text by cleaning, tokenizing, and removing stopwords."""
    # Remove special characters and numbers
    cleaned_text = re.sub(r'[^a-zA-Z ]', '', text)
    # Tokenize the text into words
    words = cleaned_text.split()
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]
    return filtered_words

def generate_wordcloud(word_counts, save_path):
    """Generate and save a word cloud."""
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_counts)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(save_path)
    plt.close()

def generate_bug_wordcloud(owner, repo):
    """Generate a word cloud from GitHub issue titles and descriptions."""
    # Step 1: Fetch issues from GitHub API
    issues = fetch_github_issues(owner, repo)
    if not issues:
        return None

    # Step 2: Extract titles and bodies
    titles_text = [issue['title'].lower() for issue in issues]
    bodies_text = [issue['body'].lower() for issue in issues if issue['body']]

    # Step 3: Combine and preprocess text
    combined_text = ' '.join(titles_text + bodies_text)
    filtered_words = preprocess_text(combined_text)

    # Step 4: Count word frequencies
    word_counts = Counter(filtered_words)

    # Step 5: Generate and save word cloud
    os.makedirs('Result', exist_ok=True)  # Create directory if it doesn't exist
    plot_path = os.path.join('Result', 'bug_wordcloud.png')
    generate_wordcloud(word_counts, plot_path)

    return plot_path

