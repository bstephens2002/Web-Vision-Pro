import autogen
import config


design_analysis_assistant = autogen.AssistantAgent(
    name="design_analysis_assistant",
    system_message="You are to analyze the website design and provide a comprehensive report on its visual appeal, user interface, and overall aesthetics. Focus on color schemes, typography, layout, and visual hierarchy. Only report on the design aspects, not the content or functionality.",
    llm_config=config.llm_config_gpt4o_mini,
)

usability_expert = autogen.AssistantAgent(
    name="usability_expert",
    system_message="Your task is to evaluate the website's usability and user experience. Assess navigation, information architecture, and overall ease of use. Provide recommendations for improving user interactions and flow. Only report on the usability aspects, not the content or functionality.",
    llm_config=config.llm_config_gpt4o_mini
)

accessibility_evaluator = autogen.AssistantAgent(
    name="accessibility_evaluator",
    system_message="Your role is to assess the website's accessibility features and compliance with WCAG guidelines. Identify areas for improvement to ensure the site is usable by people with various disabilities. Only report on the accessibility aspects, not the content or functionality.",
    llm_config=config.llm_config_gpt4o_mini
)

performance_analyst = autogen.AssistantAgent(
    name="performance_analyst",
    system_message="Evaluate the website's technical performance, including load times, responsiveness, and cross-browser compatibility. Suggest optimizations to enhance overall site speed and efficiency. Only report on the performance aspects, not the content or functionality.",
    llm_config=config.llm_config_gpt4o_mini
)




user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=0,
    code_execution_config={
        "work_dir": "code",
        "use_docker": False
    }
)

# Including all agents in the group chat
agents = [
    design_analysis_assistant,
    usability_expert,
    accessibility_evaluator,
    performance_analyst,
    user_proxy
]

group_chat = autogen.GroupChat(agents=agents, messages=[], max_round=5)
manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=config.llm_config_gpt4o_mini)