from ai71 import AI71
import openai

AI71_API_KEY = "api71-api-12c8b014-623e-425f-89ef-d4131414361e"
AI71_BASE_URL = "https://api.ai71.ai/v1/"

client = AI71(AI71_API_KEY)

# Simple invocation
print(
    client.chat.completions.create(
        model="tiiuae/falcon-180B-chat",
        messages=[
            # {"role": "system", "content": "You are a helpful assistant."},
            # {"role": "user", "content": "Hello!"},
        ],
    )
)
