import chainlit as cl
import os, json
from dotenv import load_dotenv
from litellm import completion
from typing import List, Dict, Any
from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel
from steps import process_expense

load_dotenv(override=True)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER API KEY NOT FOUND IN ENVIRONMENTAL VARIABLE")

system_message = """You are an efficient Expense Data Extractor with these responsibilities:

1. Expense Extraction:
- Strictly extract these 4 key details from user's natural language input:
  * Amount (numeric value only, required)
  * Description (concise text summary, required)
  * Category (standardized: Food, Travel, Grocery, Shopping, etc., required)
  * Date (DD Month YYYY format, default to today if not mentioned)
- Never add commentary, confirmations, or follow-up questions
- Never modify or interpret information beyond direct extraction

2. Output Format:
- Respond ONLY with raw JSON/dictionary content in this exact format:
{
    "amount": [numeric value],
    "description": "[text]",
    "category": "[standard category]",
    "transaction_date": [DD Month YYYY]
}
- DO NOT include markdown code blocks (```)
- DO NOT include any other text or formatting
- Keys must be in double quotes
- Date format must be "DD Month YYYY"

3. Error Handling:
- If any field is missing, respond with just that field's name followed by colon
- Never include explanations or suggestions
"""

@cl.on_chat_start
async def chat_start():
    chat_history = []
    chat_history.append({
        "role": "system", "content":system_message
    })
    cl.user_session.set("chat_history", chat_history)
    
    welcome_message = cl.Message(content="🌟 **Welcome to your Personal Expense Categorizer!** 🌟")
    await welcome_message.send()


@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="Processing")
    await msg.send()

    history = cl.user_session.get("chat_history") or []
    history.append(
        {"role": "user", "content":message.content}
    )

    MODEL = "openrouter/deepseek/deepseek-chat-v3-0324:free"
    try:
        response = completion(
            model=MODEL,
            messages=history,
            api_key=OPENROUTER_API_KEY
        )

        response_content : Any = response.choices[0].message.content
        response_in_dict = json.loads(response_content)

        result = await process_expense(response_in_dict)

        msg.content = response_content
        await msg.update()
    # try:
    #     agent = Agent(
    #         name="Assistant",
    #         instructions=system_message,
    #         model= "gpt-4o-mini"
    #     )

    #     response = await Runner.run(
    #         agent,
    #         message.content,
    #     )
    #     response_content = response.final_output
    #     msg.content = response_content
    #     await msg.update()

    except Exception as e:
        msg.content = f"Error: {str(e)}" 

if __name__ == "__main__":
    main()
