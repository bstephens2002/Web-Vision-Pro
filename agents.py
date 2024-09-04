import autogen
import config

def create_agent_with_depth_instruction(name, base_instruction, llm_config):
    return autogen.AssistantAgent(
        name=name,
        system_message=f"{base_instruction} Adjust your analysis depth based on the instruction provided in each request.",
        llm_config=llm_config,
    )

# Define agents with depth-aware instructions
design_analysis_assistant = create_agent_with_depth_instruction(
    "design_analysis_assistant",
    "Analyze the website's visual design, focusing on color schemes, typography, layout, and visual hierarchy.",
    config.llm_config_gpt4o_mini
)

usability_expert = create_agent_with_depth_instruction(
    "usability_expert",
    "Evaluate the website's usability and user experience, including navigation, interaction design, and consistency.",
    config.llm_config_gpt4o_mini
)

accessibility_evaluator = create_agent_with_depth_instruction(
    "accessibility_evaluator",
    "Assess the website's accessibility features and compliance with WCAG guidelines.",
    config.llm_config_gpt4o_mini
)

performance_analyst = create_agent_with_depth_instruction(
    "performance_analyst",
    "Evaluate the website's technical performance, including load times, responsiveness, and resource management.",
    config.llm_config_gpt4o_mini
)

summarization_agent = autogen.AssistantAgent(
    name="summarization_agent",
    system_message="Compile and synthesize the insights from all other agents into a concise summary report. Adjust the level of detail based on the analysis depth provided.",
    llm_config=config.llm_config_gpt4o_mini
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=0,
)

agents = [
    design_analysis_assistant,
    usability_expert,
    accessibility_evaluator,
    performance_analyst,
    summarization_agent,
    user_proxy
]

group_chat = autogen.GroupChat(agents=agents, messages=[], max_round=6)
manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=config.llm_config_gpt4o_mini)

def customize_analysis_depth(depth):
    if depth == "quick":
        return "Provide a brief overview of the most critical aspects. Limit your response to 2-3 key points."
    elif depth == "standard":
        return "Conduct a standard analysis covering all key areas. Aim for a balanced, moderately detailed report."
    elif depth == "deep":
        return "Perform an in-depth analysis with detailed explanations and comprehensive recommendations."
    else:
        return "Conduct a standard analysis covering all key areas."

def analyze_website(website_url, analysis_depth="standard"):
    depth_instruction = customize_analysis_depth(analysis_depth)
    
    try:
        user_proxy.initiate_chat(
            manager,
            message=f"Evaluate the design of the website: {website_url}. {depth_instruction}\n"
                    f"Coordinate these evaluations:\n"
                    f"1. Design Analysis\n"
                    f"2. Usability Report\n"
                    f"3. Accessibility Evaluation\n"
                    f"4. Performance Analysis\n"
                    f"After all analyses are complete, provide a concise summary report."
        )
        
        results = extract_agent_messages(group_chat)
        return results
    except Exception as e:
        return {
            "error": f"An error occurred during the analysis: {str(e)}",
            "partial_results": extract_all_messages(group_chat)
        }

def extract_agent_messages(group_chat):
    results = {
        "design_analysis": "",
        "usability_report": "",
        "accessibility_evaluation": "",
        "performance_analysis": "",
        "summary_report": ""
    }
    
    for message in group_chat.messages:
        content = message.get("content", "")
        if message["name"] == "design_analysis_assistant" and not results["design_analysis"]:
            results["design_analysis"] = content
        elif message["name"] == "usability_expert" and not results["usability_report"]:
            results["usability_report"] = content
        elif message["name"] == "accessibility_evaluator" and not results["accessibility_evaluation"]:
            results["accessibility_evaluation"] = content
        elif message["name"] == "performance_analyst" and not results["performance_analysis"]:
            results["performance_analysis"] = content
        elif message["name"] == "summarization_agent":
            results["summary_report"] = content
    
    return results

def extract_all_messages(group_chat):
    return [{"name": msg["name"], "content": msg["content"]} for msg in group_chat.messages]