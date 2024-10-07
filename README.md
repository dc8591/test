<p>
  <div align="center">
  <h1>
<br >
  Exa AI <br /> <br />
  </h1>
  </div>
  </p>
 

Exa AI leverages advanced embeddings-based search technology to precisely locate the content you need on the web. It provides three main functionalities through its API:

1. **Search for Pages**: Utilize natural language queries or Google-style keyword searches to find any page on the web.

2. **Get Contents from Pages**: Extract clean, up-to-date, and parsed HTML from Exa search results. The 'highlights' feature allows for semantically targeted content extraction.

3. **Find Similar Pages**: Identify and return pages that are similar in meaning based on a provided link.

### Basic Code Snippet

Below is a basic example to illustrate how to use the Exa AI API to search for pages:

```python
import requests
import json

url = "https://api.exa.ai/search"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-api-key": "your_api_key_here",
}

query = "what is black forest flux text to image model?"
payload = {
    "query": query,
    "type": "neural",
    "useAutoprompt": True,
    "numResults": 5,
    "excludeDomains": ["en.wikipedia.org"],
    "contents": {"text": True, "summary": True},
}

response = requests.post(url, headers=headers, json=payload).json()

# Print the JSON response
print(json.dumps(response, indent=2))

# Save the response to a file
with open("response.json", "w") as file:
    json.dump(response, file, indent=4)
```

### Key Features:
- Use of advanced neural search technology.
- Ability to exclude specific domains from search results.
- Option to obtain both text and summary through the 'contents' parameter.

Ensure you replace `"your_api_key_here"` with your actual API key when making requests.
