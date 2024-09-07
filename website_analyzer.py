import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import base64
import os
from dotenv import load_dotenv
from datetime import datetime
from PIL import Image
import io
from groq import Groq

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
        
        page.set_viewport_size({"width": 1920, "height": 1080})
        page.screenshot(path=screenshot_path, full_page=False)
        
        browser.close()

    with Image.open(screenshot_path) as img:
        img.thumbnail((400, 300))
        img.save(thumbnail_path, "PNG")
        
        if img.width > 1920 or img.height > 1080:
            img.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
        
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG', optimize=True, quality=85)
        img_byte_arr = img_byte_arr.getvalue()

    encoded_image = base64.b64encode(img_byte_arr).decode('utf-8')

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    llava_model = 'llava-v1.5-7b-4096-preview'

    prompt = f"""Please analyze this website and provide a detailed description. 
    Consider the visual layout, color scheme, and main elements visible in the image. 
    Also analyze the following text content from the website:

    {text[:15000]}

    Provide a comprehensive analysis of both the visual and textual elements."""

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{encoded_image}",
                        },
                    },
                ],
            }
        ],
        model=llava_model,
        max_tokens=1000
    )

    analysis = chat_completion.choices[0].message.content

    return analysis, thumbnail_path

# Example usage
if __name__ == "__main__":
    website_url = "https://stackoverflow.com/"
    analysis, thumbnail_path = analyze_website(website_url)
    print(analysis)
    print(f"Thumbnail saved at: {thumbnail_path}")