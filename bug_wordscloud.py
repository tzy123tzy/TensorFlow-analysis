# Import necessary libraries
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

# Step 1: Fetch HTML content from the URL
url = 'https://github.com/tensorflow/tensorflow/issues?q=is%3Aissue+is%3Aopen+bug'
response = requests.get(url, verify=False)
html_content = response.content
print(html_content)

# Step 2: Parse HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all issue titles and descriptions
issue_titles = soup.find_all('a', class_='Link--primary')
issue_descriptions = soup.find_all('div', class_='issue-body')

# Extract text from titles and descriptions
titles_text = [title.get_text().lower() for title in issue_titles]
descriptions_text = [desc.get_text().lower() for desc in issue_descriptions]

# Combine titles and descriptions into one text
combined_text = ' '.join(titles_text + descriptions_text)

# Step 3: Preprocess the text data
# Remove special characters and numbers
cleaned_text = re.sub(r'[^a-zA-Z ]', '', combined_text)
# Tokenize the text into words
words = cleaned_text.split()
# Remove stop words
stop_words = set(stopwords.words('english'))
filtered_words = [word for word in words if word not in stop_words]

# Step 4: Count word frequencies
word_counts = Counter(filtered_words)

# Step 5: Generate and display the word cloud
# Create a WordCloud object
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_counts)

# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
