import asyncio
import aiohttp
import requests
from transformers import AutoTokenizer, pipeline
import gradio as gr
import re
from datetime import datetime, timezone

# -------------------------------
# 🔹 Load Models & Tokenizers
# -------------------------------
templateId = "{B4E6C442-2F61-4926-9E5A-A4E5150C5EB6}"
parentId = "{72171220-15C0-4901-9146-759FA5564008}"
# XM Cloud GraphQL API details
GRAPHQL_URL = ""
API_KEY = ""  # Replace with your actual API key

#AI Models
model_name = "jy46604790/Fake-News-Bert-Detect"
tokenizer = AutoTokenizer.from_pretrained(model_name)
fake_news_classifier = pipeline(
    "text-classification", model=model_name, tokenizer=tokenizer)
sentiment_analyzer = pipeline("sentiment-analysis")
news_classifier = pipeline("zero-shot-classification",
                           model="facebook/bart-large-mnli")

# Predefined Categories
CATEGORIES = ["Politics", "Technology", "Sports",
              "Health", "Entertainment", "Finance"]

# -------------------------------
# 🔹 Helper Functions
# -------------------------------

articles = []


def fetch_rss_articles(feed_url):
    """Fetch articles from an RSS feed"""
    feed = requests.get(feed_url)
    response = feed.json()

    for entry in response['articles']:  # Limit to first 5 articles
        title = entry['title']
        link = f"<link text='' linktype='external' url='{entry['url']}' target='_blank' />"
        content = entry['content']
        name = re.sub(r'[^A-Za-z0-9\s]', '', entry['title'])[:50]
        author = entry['author']
        description = entry['description']
        pubdateNotFormat = entry['publishedAt']
        publishDate = datetime.strptime(pubdateNotFormat, "%Y-%m-%dT%H:%M:%SZ")
        # Convert to Sitecore format
        sitecore_format = publishDate.strftime("%Y%m%dT%H%M%S")

        if content:
            articles.append({"title": title, "description":description, "link": link, "content": content, "authenticity": "", "name": name, "author": author,
                            "authscore": "", "sentiment": "", "sentimentscore": "", "category": "", "categoryscore": "","publishdate":sitecore_format})

    return articles


def split_text(text, chunk_size=512):
    """Splits text into 512-token chunks properly."""
    tokens = tokenizer.encode(text, add_special_tokens=True)

    if len(tokens) == 0:
        return []

    chunks = [tokens[i:i + chunk_size]
              for i in range(0, len(tokens), chunk_size)]
    return [" ".join(tokenizer.convert_ids_to_tokens(chunk)) for chunk in chunks]


def check_authenticity(text):
    """Checks if news is fake or real"""
    results = fake_news_classifier(text)

    real_score = sum(res['score']
                     for res in results if res['label'] == 'LABEL_1') / len(results)
    fake_score = sum(res['score']
                     for res in results if res['label'] == 'LABEL_0') / len(results)

    return ('real', real_score) if real_score > fake_score else ('fake', fake_score)


def analyze_sentiment(text):
    """Runs sentiment analysis on the article"""
    result = sentiment_analyzer(text[:512])[0]  # Limit to first 512 tokens
    return result['label'], result['score']


def classify_article(text):
    """Classifies news into predefined categories"""
    result = news_classifier(
        text[:512], candidate_labels=CATEGORIES)  # Limit to first 512 tokens
    # Return highest confidence category
    return result['labels'][0], result['scores'][0]


rss_url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=095392c11b2945928e1d34da0db48c10"

fetch_rss_articles(rss_url)

if articles:
    for article in articles:
        authenticity, auth_score = check_authenticity(article['content'])
        sentiment, sentiment_score = analyze_sentiment(article['content'])
        category, category_score = classify_article(article['content'])
        print(
            f"📰 **Authenticity:** {authenticity} (Confidence: {auth_score:.2f})")
        article['authenticity'] = authenticity
        article['authscore'] = round(auth_score, 2)
        print(
            f"😊 **Sentiment:** {sentiment} (Confidence: {sentiment_score:.2f})")
        article['sentiment'] = sentiment
        article['sentimentscore'] = round(sentiment_score, 2)
        print(
            f"🏷️ **Category:** {category} (Confidence: {category_score:.2f})")
        article['category'] = category
        article['categoryscore'] = round(category_score, 2)
        print("---")
else:
    print("No articles found. Try another RSS feed.")


# *********************************************************************************************
# Define GraphQL mutation
async def create_content(session, article):
    """ Sends a GraphQL mutation request to create an article """
    inputParam = {
        "name": article["name"],
        "templateId": templateId,
        "parent": parentId,
        "language": "en",
        "fields": [
            {"name": "Title", "value": f"{article["title"]}"},
            {"name": "Author", "value": f"{article["author"]}"},
            {"name": "Description", "value": f"{article["description"]}"},
            {"name": "Url", "value": f"{article["link"]}"},
            {"name": "Authenticity" ,"value":f"{article["authenticity"]}"},
            {"name": "Authenticity Score" ,"value":f"{article["authscore"]}"},
            {"name": "Sentiment" ,"value":f"{article["sentiment"]}"},
            {"name": "Sentiment Score" ,"value":f"{article["sentimentscore"]}"},
            {"name": "Category" ,"value":f"{article["category"]}"},
            {"name": "Category Score" ,"value":f"{article["categoryscore"]}"},
            {"name": "PublishedAt" ,"value":f"{article["publishdate"]}"}
        ]
    }
    MUTATION_QUERY = """
mutation($input: CreateItemInput!) {
    createItem(input: $input) {
        item{
            itemId
            name
            path
        }
    }
}
"""
    headers = {"Authorization": f"Bearer {API_KEY}",
               "Content-Type": "application/json"}

    async with session.post(GRAPHQL_URL, json={"query": MUTATION_QUERY, "variables": {"input": inputParam}}, headers=headers) as response:
        result = await response.json()
    if response.status == 200:
        print(f"✅ Created: {result}")
    else:
        print(f"❌ Failed: {result}")


async def main():
    """ Runs all GraphQL requests in parallel """
    try:
        async with aiohttp.ClientSession() as session:
            tasks = [create_content(session, article) for article in articles]
            await asyncio.gather(*tasks)  # Equivalent to Task.WhenAll()
    except Exception as ex:
        print(ex)

# Run the async event loop
asyncio.run(main())
