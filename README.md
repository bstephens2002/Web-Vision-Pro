# WebVisionPro: AI-Powered Site Analysis Suite 🚀🔍

![WebVisionPro Logo](images/Web-Vision-Pro-sm.jpg)

WebVisionPro is an advanced, AI-powered website analysis tool that provides comprehensive insights into various aspects of web design and functionality. Leveraging Microsoft's Autogen framework and Groq's high-speed inference capabilities, WebVisionPro offers a multi-faceted evaluation of websites, making it an invaluable resource for web developers, designers, and digital marketers.

## ✨ Features

- **Design Analysis** 🎨: Evaluates the website's visual appeal, color schemes, typography, and layout.
- **Usability Report** 🖱️: Assesses navigation, information architecture, and overall user experience.
- **Accessibility Evaluation** ♿: Checks compliance with WCAG guidelines and identifies areas for improvement.
- **Performance Analysis** ⚡: Examines load times, responsiveness, and cross-browser compatibility.
- **Comprehensive Summary** 📊: Provides a concise overview of all analyzed aspects.

## 🛠️ Technology Stack

- **Framework**: Microsoft Autogen
- **Language Models**: Groq (llava-v1.5-7b-4096-preview and llama3-70b-8192)
- **Web Scraping**: BeautifulSoup, Playwright
- **UI**: Gradio

## 🚀 Installation

1. Clone the repository:
   ```
   git clone https://github.com/bstephens2002/Web-Vision-Pro.git
   cd Web-Vision-Pro
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
   ```
   playwright install
   ```

3. Set up your environment variables:
   - Copy the `.env.example` file to `.env`
   - Fill in your API key for Groq

## 🖥️ Usage

1. Run the main application:
   ```
   python main.py
   ```

2. Open the provided Gradio interface URL in your web browser.

3. Enter the URL of the website you want to analyze and choose the analysis depth (quick, standard, or deep).

4. Click "Evaluate Website" to start the analysis.

5. View the comprehensive analysis across multiple categories.

## 🤝 Contributing

We welcome contributions to WebVisionPro! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, or request features.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Microsoft Autogen team for their powerful conversational AI framework
- Groq for their high-speed inference capabilities
- The open-source community for various tools and libraries used in this project

## 📬 Contact

For any questions or feedback, please open an issue on this GitHub repository or contact [braddstephens@gmail.com](mailto:braddstephens@gmail.com).

---

WebVisionPro - Empowering web professionals with AI-driven insights. 💻🧠✨
