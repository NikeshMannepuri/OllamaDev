import chainlit as cl
import ollama
from chainlit.input_widget import Select

#LLM = "tinyllama"
LLMs = ["phi3", "tinyllama", "tinydolphin"]
LLM="tinydolphin"
async def get_response_from_ollama(prompt):
    response = ollama.generate(model=LLM, prompt=prompt)
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
