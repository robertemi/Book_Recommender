import os, json
from openai import OpenAI
from dotenv import load_dotenv
from retriever import search_books
from tools import get_summary_by_title

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

SYSTEM = (
    "You are Smart Librarian. You MUST choose exactly ONE title from the provided candidates. "
    "After you choose, call the tool `get_summary_by_title` with that exact title. "
    "Then, when you receive the tool result, compose a friendly reply that:\n"
    "1) Recommends the title (bold the title),\n"
    "2) Briefly justifies why it fits the user's request (1-2 sentences),\n"
    "3) Shows the long summary returned by the tool under a header 'Detailed summary:'."
)


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_summary_by_title",
            "description": "Return the long summary for an exact book title.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Exact book title"}
                },
                "required": ["title"]
            }
        }
    }
]


def chat(user_prompt: str) -> str:
    candidates = search_books(user_prompt, k=3)

    if not candidates:
        return f'No suitable books have been found'
    
    candidate_titles = [c["title"] for c in candidates]
    system_prompt = SYSTEM + "\nCandidates:\n" + "\n".join(f"- {t}" for t in candidate_titles)

    response = client.chat.completions.create(
        model='gpt-4o-nano',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ],
        tools=TOOLS,
        tool_choice='auto'
    )

    tool_calls = response.choices[0].message.tool_calls


    tool_args = json.loads(tool_calls[0].function.arguments)
    title = tool_args["title"]


    summary = get_summary_by_title(title)

    # send tool call output back to model for final reply
    followup = client.chat.completions.create(
        model="gpt-4o-nano",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
            response.choices[0].message,
            {
                "role": "tool",
                "tool_call_id": tool_calls[0].id,
                "name": "get_summary_by_title",
                "content": summary
            }
        ],
        tools=TOOLS
    )

    # final reply
    return followup.choices[0].message.content