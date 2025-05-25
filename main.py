from openai import OpenAI
from dotenv import load_dotenv
import os
from tools import get_current_time

load_dotenv()

def main():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    print("Welcome! I'm your AI assistant. Type 'quit' to exit.")

    functions = [
        {
            "name": "get_current_time",
            "description": "Returns the current time.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    ]

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "quit":
            break

        response = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[{"role": "user", "content": user_input}],
            functions=functions,
            function_call="auto",
        )

        choice = response.choices[0]
        message = choice.message

        if hasattr(message, "function_call") and message.function_call: 
            func_name = message.function_call.name
            if func_name == "get_current_time":
                result = get_current_time()
                follow_up = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "user", "content": user_input},
                        message,  
                        {
                            "role": "function",
                            "name": func_name,
                            "content": str(result),
                        },
                    ],
                )
                print("\nAI Assistant:", follow_up.choices[0].message.content)
        else:
            print("\nAI Assistant:", message.content)

if __name__ == "__main__":
    main()