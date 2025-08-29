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


async def chat(user_prompt: str) -> str:
    candidates = await search_books(user_prompt, k=3)

    if not candidates:
        return f'No suitable books have been found'
    
    context = "Candidates:\n" + "\n".join(
        f"- {candidate['title']}: {candidate['text'][:280]}..." for candidate in candidates
    )
    
    candidate_titles = [c["title"] for c in candidates]
    system_prompt = SYSTEM + "\nCandidates:\n" + "\n".join(f"- {t}" for t in candidate_titles)

    first_response = client.chat.completions.create(
        model='gpt-4.1-nano',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt},
            {'role': 'assistant', 'content': context}
        ],
        tools=TOOLS,
        tool_choice='auto',
        temperature=0.2
    )

    message = first_response.choices[0].message
    tool_calls = message.tool_calls if message.tool_calls else []


    # extract chosen title
    chosen_title = None
    if tool_calls:
        try:
            args = json.loads(tool_calls[0].function.arguments or "{}")
            chosen_title = (args.get("title") or "").strip()
        except Exception:
            chosen_title = None

    # fallback if no/invalid tool call or hallucinated title
    if not chosen_title or chosen_title not in candidate_titles:
        chosen_title = candidate_titles[0]

    # run the tool locally
    summary = await get_summary_by_title(chosen_title)
    if not summary or summary == "Summary not found.":
        # second fallback: return a simple recommendation without long summary
        return f"I recommend **{chosen_title}**. It fits your request based on semantic search, " \
               f"but I couldn't retrieve the long summary right now."

    # return tool result to model to create the final answer
    final = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": context},
            message,
            {
                "role": "tool",
                "tool_call_id": tool_calls[0].id if tool_calls else "manual_fallback",
                "name": "get_summary_by_title",
                "content": summary,
            },
        ],
        temperature=0.2,
    )
    return final.choices[0].message.content.strip()