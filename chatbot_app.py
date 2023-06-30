import openai
import gradio as gr

openai.api_key = "YOUR OPENAI API KEY"

message_history = [
    {"role": "user", "content": "You are a helpful assistant. I want to know about Large Language Models"},
    {"role": "assistant", "content": "Large language models are advanced AI models that have been trained on massive "
                                     "amounts of text data. "},
]


def predict(user_input):
    global message_history
    message_history.append({"role": "user", "content": user_input})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history
    )

    reply_content = completion.choices[0].message.content
    message_history.append({"role": "user", "content": reply_content})

    response = [(message_history[i]["content"], message_history[i + 1]["content"]) for i in
                range(2, len(message_history) - 1, 2)]
    return response


with gr.Blocks(theme=gr.themes.base) as demo:
    chatbot = gr.Chatbot()
    with gr.Row():
        text_box = gr.Textbox(show_label=False, placeholder="Type your message here").style(container=False)
        text_box.submit(predict, text_box, chatbot)
        text_box.submit(lambda: "", None, text_box)

demo.launch()
