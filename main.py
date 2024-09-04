import agents
from website_analyzer import analyze_website
import gradio as gr
import os

def evaluate_website_design(website_url, analysis_depth):
    initial_analysis, thumbnail_path = analyze_website(website_url)
    
    # Use the new analyze_website function from agents.py
    results = agents.analyze_website(website_url, analysis_depth)
    
    if "error" in results:
        return (
            gr.update(visible=True, value=thumbnail_path),
            f"Error: {results['error']}",
            "N/A",
            "N/A",
            "N/A",
            "N/A"
        )
    
    return (
        gr.update(visible=True, value=thumbnail_path),
        results["design_analysis"],
        results["usability_report"],
        results["accessibility_evaluation"],
        results["performance_analysis"],
        results["summary_report"]
    )

custom_css = """
footer.svelte-1rjryqp {display: none !important;}
.gradio-container {min-height: 0 !important;}

/* Target the image container */
.image-container.svelte-1p15vfy {
    background-color: #030a3e !important;
}

/* Target the button containing the image */
.image-container.svelte-1p15vfy button.svelte-1p15vfy {
    background-color: #030a3e !important;
}

/* Target the image frame */
.image-frame.svelte-1p15vfy {
    background-color: #030a3e !important;
}

/* Target the image itself */
.image-frame.svelte-1p15vfy img.svelte-1pijsyv {
    background-color: #030a3e !important;
}
"""

with gr.Blocks(theme=gr.themes.Monochrome(), title="Website Design Evaluator", css=custom_css) as page:
    gr.Image("images/Web-Vision-Pro-sm.jpg", show_label=False, interactive=False, show_download_button=False,show_fullscreen_button=False, elem_id="logo-image")

    # Inputs
    website_url = gr.Textbox(placeholder="Enter a URL (e.g., https://example.com)", label="Website URL", info="Enter the website URL to evaluate")
    analysis_depth = gr.Radio(["quick", "standard", "deep"], label="Analysis Depth", value="quick")

    # Button to submit inputs
    submit_button = gr.Button("WebVision Go!")

    # Outputs
    with gr.Column():
        screenshot_thumbnail = gr.Image(label="Website Thumbnail", visible=False, show_label=False, interactive=False, show_download_button=False,show_fullscreen_button=False)
        design_analysis = gr.Markdown(label="Design Analysis")
        usability_report = gr.Markdown(label="Usability Report")
        accessibility_evaluation = gr.Markdown(label="Accessibility Evaluation")
        performance_analysis = gr.Markdown(label="Performance Analysis")
        summary_report = gr.Markdown(label="Summary Report")

    submit_button.click(
        fn=evaluate_website_design,
        inputs=[website_url, analysis_depth],
        outputs=[screenshot_thumbnail, design_analysis, usability_report, accessibility_evaluation, performance_analysis, summary_report]
    )

if __name__ == "__main__":
    page.launch(share=True, allowed_paths=["Web-Rating/images/", "./"])

# Clean up thumbnails after the Gradio app is closed
def cleanup_thumbnails():
    for file in os.listdir():
        if file.startswith("thumbnail_") and file.endswith(".png"):
            os.remove(file)

import atexit
atexit.register(cleanup_thumbnails)