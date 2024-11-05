from typing import List

# pip install -qU langchain-ollama
from langchain_core.tools import tool
from langchain_core.messages import AIMessage
from langchain_ollama import ChatOllama


@tool
def get_city_temperature(city: str) -> float:
    """Returns the temperature in a given city.

    Args:
        city (str): The city to get the temperature for.
    """
    print(f"Called get_city_temperature with {city}")
    return 23.4


llm = ChatOllama(
    model="llama3.1",
    temperature=0,
).bind_tools([get_city_temperature])

messages = [
    (
        "system",
        "You are a helpful assistant that performs any task that is asked of it.",
    ),
    ("human", "What's the temperatue of New York?"),
    # ("human", "List 5 words (bullet points) associated with the word 'bee'"),
]

# result = llm.invoke(
#     "Could you validate user 123? They previously lived at "
#     "123 Fake St in Boston MA and 234 Pretend Boulevard in "
#     "Houston TX."
# )

result = llm.invoke(messages)

print(f"Content = {result.content}")

# from langchain_ollama import ChatOllama
# from langchain_core.messages import AIMessage

# llm = ChatOllama(
#     model="llama3.1",
#     temperature=0,
#     # other params...
# )

# messages = [
#     (
#         "system",
#         "You are a helpful assistant that translates English to French. Translate the user sentence.",
#     ),
#     ("human", "I love programming."),
# ]
# ai_msg = llm.invoke(messages)
# print(ai_msg)
