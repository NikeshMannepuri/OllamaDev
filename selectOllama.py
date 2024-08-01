import chainlit as cl
from chainlit.input_widget import Select
import ollama

LLMs = ["phi3", "tinyllama", "tinydolphin"]

selected_model = None

async def get_response_from_ollama(prompt, model):
    response = ollama.generate(model=model, prompt=prompt)
    return response['response']

@cl.step(type="tool")
async def tool(prompt: str, model: str):
    response = await get_response_from_ollama(prompt, model)
    return response

@cl.on_chat_start
async def start():
    global selected_model
    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="LLM Model",
                values=LLMs,
                initial_index=0,
            )
        ]
    ).send()
    selected_model = settings["Model"]
    await cl.Message(content=f"Model selected: {selected_model}").send()

@cl.on_message
async def main(message: cl.Message):
    global selected_model
    if selected_model is None:
        await cl.Message(content="Please select a model first.").send()
        return
    
    final_answer = await cl.Message(content="Generating response...").send()
    response = await tool(message.content, selected_model)
    final_answer.content = response
    await final_answer.update()
