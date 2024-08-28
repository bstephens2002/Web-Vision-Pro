import agents
from website_analyzer import analyze_website
import gradio as gr


title = "Website Design Evaluation"

def evaluate_website_design(website_url):
    analysis = analyze_website(website_url)
    
    # Initiate a chat with the agency's assistants
    agents.user_proxy.initiate_chat(
        agents.manager,
        message=f"We need to evaluate the design of the website: {website_url}. Here's the initial analysis: {analysis}. "
                f"Please coordinate the following evaluations, ensuring each agent focuses solely on their area of expertise:\n"
                f"1. Design Analyst: Provide a Design Analysis\n"
                f"2. Usability Expert: Deliver a Usability Report\n"
                f"3. Accessibility Specialist: Conduct an Accessibility Evaluation\n"
                f"4. Performance Analyst: Perform a Performance Analysis\n"
                f"Ensure that each analysis appears in its own separate message and is limited to the agent's specific area of expertise."
    )

    # Extract responses from the assistants
    design_analysis = "No design analysis provided."
    usability_report = "No usability report provided."
    accessibility_evaluation = "No accessibility evaluation provided."
    performance_analysis = "No performance analysis provided."


    # Iterate through the chat messages to extract the latest response from each agent
    for message in reversed(agents.group_chat.messages):
        if message["role"] == "user":
            if message["name"] == "design_analysis_assistant" and design_analysis.startswith("No design analysis"):
                design_analysis = message["content"]
            elif message["name"] == "usability_expert" and usability_report.startswith("No usability report"):
                usability_report = message["content"]
            elif message["name"] == "accessibility_evaluator" and accessibility_evaluation.startswith("No accessibility evaluation"):
                accessibility_evaluation = message["content"]
            elif message["name"] == "performance_analyst" and performance_analysis.startswith("No performance analysis"):
                performance_analysis = message["content"]


    return analysis, design_analysis, usability_report, accessibility_evaluation, performance_analysis


with gr.Blocks(theme=gr.themes.Monochrome(), title="Website Design Evaluator") as page:
    gr.Image("images/Web-Vision-Pro-sm.jpg", show_label=False, interactive=False, show_download_button=False)
    
    # Inputs
    website_url = gr.Textbox(value="Enter a URL (e.g., https://example.com)", label="Website URL", info="Enter the website URL to evaluate")
    
    # Button to submit inputs
    submit_button = gr.Button("WebVision Go!")
    
    # Outputs
    initial_analysis = gr.Markdown(label="Initial Analysis")
    design_analysis = gr.Markdown(label="Design Analysis")
    usability_report = gr.Markdown(label="Usability Report")
    accessibility_evaluation = gr.Markdown(label="Accessibility Evaluation")
    performance_analysis = gr.Markdown(label="Performance Analysis")

    
    submit_button.click(
        fn=evaluate_website_design,
        inputs=[website_url],
        outputs=[initial_analysis, design_analysis, usability_report, accessibility_evaluation, performance_analysis]
    )

if __name__ == "__main__":
    page.launch(share=True,allowed_paths=["Web-Rating/images/"])
