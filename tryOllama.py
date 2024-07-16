# import chainlit as cl


# @cl.step(type="tool")
# async def tool():
#     # Fake tool
#     await cl.sleep(2)
#     return "Response from the tool!"


# @cl.on_message  # this function will be called every time a user inputs a message in the UI
# async def main(message: cl.Message):
#     """
#     This function is called every time a user inputs a message in the UI.
#     It sends back an intermediate response from the tool, followed by the final answer.

#     Args:
#         message: The user's message.

#     Returns:
#         None.
#     """

#     final_answer = await cl.Message(content="").send()

#     # Call the tool
#     final_answer.content = await tool()

#     await final_answer.update()

import chainlit as cl
import ollama

# Define the model to use
LLM = "phi3"

# Function to generate a response using the Ollama API
def generate_response(prompt):
    response = ollama.generate(model=LLM, prompt=prompt)
    return response['text']

# Define the chatbot logic using Chainlit
@cl.on_message
def on_message(message):
    user_input = message.content
    response_text = generate_response(user_input)
    message.reply(response_text)

if __name__ == "__main__":
    cl.run()
