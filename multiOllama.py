import chainlit as cl
import ollama
from chainlit.input_widget import Select

@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name="phi3",
            markdown_description="The underlying LLM model is **GPT-3.5**.",
            icon="https://picsum.photos/200",
        ),
        cl.ChatProfile(
            name="tinyllama",
            markdown_description="The underlying LLM model is **GPT-4**.",
            icon="https://picsum.photos/250",
        ),
        cl.ChatProfile(
            name="tinydolphin",
            markdown_description="The underlying LLM model is **GPT-4**.",
            icon="https://picsum.photos/300",
        ),
    ]

@cl.on_chat_start
async def on_chat_start():
    chat_profile = cl.user_session.get("chat_profile")
    await cl.Message(
        content=f"Starting chat using the {chat_profile} chat profile"
    ).send()

async def get_response_from_ollama(prompt):
    chat_profile = cl.user_session.get("chat_profile")
    response = ollama.generate(model=chat_profile, prompt=prompt)
    return response['response']

@cl.step(type="tool")
async def tool(prompt: str):
    # Get the response from ollama
    response = await get_response_from_ollama(prompt)
    return response

@cl.on_message  # This function will be called every time a user inputs a message in the UI
async def main(message: cl.Message):
    """
    This function is called every time a user inputs a message in the UI.
    It sends back an intermediate response from the tool, followed by the final answer.

    Args:
        message: The user's message.

    Returns:
        None.
    """

    # Initial response to the user
    final_answer = await cl.Message(content="Generating response...").send()

    # Call the tool with the user's message
    response = await tool(message.content)

    # Update the message with the actual response from ollama
    final_answer.content = response
    await final_answer.update()