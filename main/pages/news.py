from newscatcherapi import NewsCatcherApiClient

api = NewsCatcherApiClient(x_api_key="YOUR_API_KEY")

# Example: get news about Apple
all_articles = api.get_search(q="Apple", lang="en", page_size=5)

for article in all_articles['articles']:
    print(article['title'], article['link'])
