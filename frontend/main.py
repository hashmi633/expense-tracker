import chainlit as cl
import os, json
from dotenv import load_dotenv
from litellm import completion
from typing import List, Dict, Any,cast
from openai import AsyncOpenAI
from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, RunConfig, ModelProvider
from agents.extensions.models.litellm_model import LitellmModel
from steps import process_expense
from tools import record_expense

# set_tracing_disabled(disabled=True)

MODEL = "deepseek/deepseek-chat-v3-0324:free"

load_dotenv(override=True)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER API KEY NOT FOUND IN ENVIRONMENTAL VARIABLE")

external_client =AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
    
)

model = OpenAIChatCompletionsModel(
    model=MODEL,
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=cast(ModelProvider, external_client),
    tracing_disabled=True,
)


system_message = """
You are an intelligent expense tracking assistant. Your primary functions are to:
1.  **Record Expenses:** Capture details like amount, description, category, and date from user input.
2.  **Generate Expense Reports:** Understand user requests for expense reports based on criteria like date ranges, categories, or specific descriptions.

When a user asks for an expense report, you must identify the following parameters from their request:
-   `report_type`: (e.g., "category_wise", "date_wise", "all") - default to "all" if not specified.
-   `category`: (optional) The expense category (e.g., "food", "transport", "utilities"). If the user asks for a specific category, extract it.
-   `start_date`: (optional) The start date for the report in YYYY-MM-DD format. If the user mentions a month (e.g., "July 2025"), infer the first day of that month. If "last week", infer the start of last week.
-   `end_date`: (optional) The end date for the report in YYYY-MM-DD format. If the user mentions a month, infer the last day of that month. If "last week", infer the end of last week.
-   `description_keyword`: (optional) A keyword to filter expenses by description.

If the user's intent is to get a report, you *must* call the `get_expense_report` tool with the extracted parameters. If you cannot extract enough information, ask clarifying questions.

If the user's intent is to record an expense, you *must* call the `record_expense` tool with the extracted parameters (amount, description, category, date).

**Example Report Request & Expected Parameters:**
User: "Show me my food expenses for July 2025."
Parameters for `get_expense_report`: `report_type="category_wise"`, `category="food"`, `start_date="2025-07-01"`, `end_date="2025-07-31"`

User: "What did I spend last week?"
Parameters for `get_expense_report`: `report_type="date_wise"`, `start_date="<start_of_last_week>"`, `end_date="<end_of_last_week>"`

User: "Give me a report of all expenses."
Parameters for `get_expense_report`: `report_type="all"` (no category, no dates)

User: "I spent $50 on groceries today."
Parameters for `record_expense`: `amount=50`, `description="groceries"`, `category="food"`, `date="<today's date>"`

Always strive to be helpful and accurate.
"""


# """You are an efficient Expense Data Extractor with these responsibilities:

# 1. Expense Extraction:
# - Strictly extract these 4 key details from user's natural language input:
#   * Amount (numeric value only, required)
#   * Description (concise text summary, required)
#   * Category (standardized: Food, Travel, Grocery, Shopping, etc., required)
#   * Date (DD Month YYYY format, default to today if not mentioned)
# - Never add commentary, confirmations, or follow-up questions
# - Never modify or interpret information beyond direct extraction

# 2. Output Format:
# - Respond ONLY with raw JSON/dictionary content in this exact format:
# {
#     "amount": [numeric value],
#     "description": "[text]",
#     "category": "[standard category]",
#     "transaction_date": [DD Month YYYY]
# }
# - DO NOT include markdown code blocks (```)
# - DO NOT include any other text or formatting
# - Keys must be in double quotes
# - Date format must be "DD Month YYYY"

# 3. Error Handling:
# - If any field is missing, respond with just that field's name followed by colon
# - Never include explanations or suggestions
# """

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
        # try:
        # response = completion(
        #     model=MODEL,
        #     messages=history,
        #     api_key=OPENROUTER_API_KEY
        # )

        # response_content : Any = response.choices[0].message.content
        # response_in_dict = json.loads(response_content)

        # result = await process_expense(response_in_dict)

        # msg.content = response_content
        # await msg.update()
    try:
        agent = Agent(
            name="Assistant",
            instructions=system_message,
            model=MODEL,
            tools=[record_expense]
        )

        response = await Runner.run(
            agent,
            message.content,
            run_config=config,
        )
        if response.final_output:
            msg.content = response.final_output
            await msg.update()
            print("there is final_output")
        else:
            print("there is no final_output")
            await cl.Message(content="Agent processing complete.").send()

    except Exception as e:
        msg.content = f"Error: {str(e)}" 

if __name__ == "__main__":
    main()
