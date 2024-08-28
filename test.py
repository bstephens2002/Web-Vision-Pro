import autogen

BASE_URL = "http://0.0.0.0:15429/chat/completions"

config_list_mistral = [
    {
        'base_url': BASE_URL,
        'api_key': "NULL",
        'model': "dolphin-mistral"
    }
]

llm_config_mistral = {
    "config_list": config_list_mistral
}

coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config_mistral,
    code_execution_config={"work_dir": "web", "use_docker": False}
)

# Use the agent to interact with Ollama
response = coder.initiate_chat(coder, "Can you create an dirty ad idea for a craft coffee company called Great Outdoors Coffee Company?")
print(response)


# curl -X POST -H "Content-Type: application/json" -d '{"messages": [{"role": "user", "content": "Can you create an dirty ad idea for a craft coffee company called Great Outdoors Coffee Company?"}]}' http://0.0.0.0:11434/v1/chat/completions
# curl -X POST -H "Content-Type: application/json" -d '{"prompt": "Your prompt here"}' http://127.0.0.1:60192/v1/completions


# curl --location 'http://0.0.0.0:15429/chat/completions' \
# --header 'Content-Type: application/json' \
# --data ' {
#       "model": "dolphin-mistral",
#       "messages": [
#         {
#           "role": "user",
#           "content": "Can you create an dirty ad idea for a craft coffee company called Great Outdoors Coffee Company?"
#         }
#       ],
#     }
# '
