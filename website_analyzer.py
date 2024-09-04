import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import anthropic
import base64
import os
from dotenv import load_dotenv
from datetime import datetime
from PIL import Image
import io

load_dotenv()

def analyze_website(url):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"screenshots/screenshot_{timestamp}.png"
    thumbnail_path = f"thumbnails/thumbnail_{timestamp}.png"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        
        # Set viewport size to a more reasonable size (1920x1080)
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        # Capture the viewport
        page.screenshot(path=screenshot_path, full_page=False)
        
        browser.close()

    # Create a thumbnail
    with Image.open(screenshot_path) as img:
        # Create a thumbnail
        img.thumbnail((400, 300))
        img.save(thumbnail_path, "PNG")
        
        # Resize the original screenshot if it's too large
        if img.width > 1920 or img.height > 1080:
            img.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
        
        # Save with compression
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG', optimize=True, quality=85)
        img_byte_arr = img_byte_arr.getvalue()

    # Encode the compressed image to base64
    encoded_image = base64.b64encode(img_byte_arr).decode('utf-8')

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Please analyze this website and provide a detailed description. Here's the text content:\n\n{text[:15000]}"
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

    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        messages=messages
    )

    analysis = response.content[0].text

    # Clean up the screenshot file, but keep the thumbnail
    #os.remove(screenshot_path)

    return analysis, thumbnail_path

# Example usage
if __name__ == "__main__":
    website_url = "https://stackoverflow.com/"
    analysis, thumbnail_path = analyze_website(website_url)
    print(analysis)
    print(f"Thumbnail saved at: {thumbnail_path}")