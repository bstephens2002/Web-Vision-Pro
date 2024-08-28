import os
import dotenv
from groq import Groq

dotenv.load_dotenv()

config_list_gpt4 = [
    {
        "model": "gpt-4",
        "api_key": os.getenv("OPENAI_API_KEY"),
    }
]

config_list_gpt4_0125 = [
    {
        "model": "gpt-4-0125-preview",
        "api_key": os.getenv("OPENAI_API_KEY"),
    }
]


config_list_gpt4o_mini = [
    {
        "model": "gpt-4o-mini",
        "api_key": os.getenv("OPENAI_API_KEY"),
    }
]


config_list_gpt4_vision = [
    {
        "model": "gpt-4-vision-preview",
        "api_key": os.getenv("OPENAI_API_KEY"),
    }
]

config_list_claude3_sonnet = [
    {
        "model": "claude-3-sonnet-20240320",
        "api_key": os.getenv("ANTHROPIC_API_KEY"),
    }
]

config_list_groq_mixtral = [
    {
        "base_url": "https://api.groq.com/openai/v1",
        "model": "mixtral-8x7b-32768",
        "api_key": os.getenv("GROQ_API_KEY"),
    }
]

def get_groq_client():
    config = next(filter(lambda x: x['model'] == 'mixtral-8x7b-32768', config_list_groq_mixtral))
    api_key = config['api_key']
    client = Groq(api_key=api_key)
    return client

# http://postpilot.agency

# litellm --model ollama/mistral --port 8002
# litellm --model ollama/codellama --port 8004
# litellm --model ollama/dolphin-mistral --port 8006


config_list_mistral = [
    {
        'base_url': "http://127.0.0.1:11434/v1/",
        'api_key': "ollama",
        'model': "mistral:latest"
    }
]

config_list_codellama = [
    {
        'base_url': "http://127.0.0.1:11434/v1/",
        'api_key': "ollama",
        'model': "codellama:latest"
    }
]

config_list_dolphinmixtral = [
    {
        'base_url': "http://127.0.0.1:11434/v1/",
        'api_key': "ollama",
        'model': "dolphin-mixtral:latest"
    }
]

config_list_llama2 = [
    {
        'base_url': "http://127.0.0.1:11434/v1/",
        'api_key': "ollama",
        'model': "llama2"
    }
]

config_list_llava = [
    {
        'base_url': "http://127.0.0.1:11434/v1/",
        'api_key': "ollama",
        'model': "llava:7b"
    }
]

config_list_phi3 = [
    {
        'base_url': "http://127.0.0.1:11434/v1/",
        'api_key': "ollama",
        'model': "phi3:mini"
    }
]

llm_config_mistral = {
    "config_list": config_list_mistral,
    "timeout": 240,
}

llm_config_codellama = {
    "config_list": config_list_codellama,
    "timeout": 240,
}

llm_config_dolphinmixtral = {
    "config_list": config_list_dolphinmixtral,
    "timeout": 240,
}

llm_config_llama2 = {
    "config_list": config_list_llama2,
    "timeout": 240,
}

llm_config_llava = {
    "config_list": config_list_llava,
    "timeout": 240,
}

llm_config_gpt4 = {
    "config_list": config_list_gpt4,
    "timeout": 240,
}

llm_config_gpt4_0125 = {
    "config_list": config_list_gpt4_0125,
    "timeout": 240,
}

llm_config_gpt4o_mini = {
    "config_list": config_list_gpt4o_mini,
    "timeout": 240,
}

llm_config_gpt4_vision = {
    "config_list": config_list_gpt4_vision,
    "timeout": 240,
}

llm_config_groq = {
    "config_list": config_list_groq_mixtral,
    "timeout": 240,
}

llm_config_phi3 = {
    "config_list": config_list_phi3,
    "timeout": 240,
}

llm_config_claude3_sonnet = {
    "config_list": config_list_claude3_sonnet,
    "timeout": 240,
}

llm_config_test_model2 = {
    # "model": "mixtral-8x7b-32768",
    "model": "gemma-7b-it",
    "client": get_groq_client(),
}