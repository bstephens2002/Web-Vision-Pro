import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import anthropic
import base64
import os
from dotenv import load_dotenv

load_dotenv()

def analyze_website(url):
    # Ensure the URL has a scheme
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    # Fetch the webpage content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract text from the webpage
    text = soup.get_text(separator=' ', strip=True)

    # Take a screenshot using Playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        screenshot_path = "screenshot.png"
        page.screenshot(path=screenshot_path)
        browser.close()

    # Read the screenshot and encode it to base64
    with open(screenshot_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    # Initialize the Anthropic client
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Prepare the message for Claude
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Please analyze this website and provide a detailed description. Here's the text content:\n\n{text[:15000]}"  # Truncate to 15000 chars to avoid token limits
                },
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": encoded_image
                    }
                }
            ],
        }
    ]

    # Send the request to Claude
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        messages=messages
    )

    # Return Claude's analysis
    return response.content[0].text

# Example usage
if __name__ == "__main__":
    website_url = "https://stackoverflow.com/"
    analysis = analyze_website(website_url)
    print(analysis)