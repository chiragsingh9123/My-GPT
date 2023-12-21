import tkinter as tk
from tkinter import scrolledtext,messagebox,filedialog
import google.generativeai as genai
import requests
from PIL import Image, ImageTk
GOOGLE_API_KEY='YOUR_GIMINI_API_KEY'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])


# models = {
#     'gemini-pro': genai.GenerativeModel('gemini-pro'),
#     'gemini-pro-vision': genai.GenerativeModel('gemini-pro-vision')
# }
# current_model = 'gemini-pro'
# chat = models[current_model].start_chat(history=[])  

# def switch_model():
#     global current_model, chat
#     current_model = 'gemini-pro' if current_model == 'gemini-pro' else 'gemini-pro-vision'
#     chat = models[current_model].start_chat(history=[])
#     clear_conversation()
#     model_label.config(text=f"Current Model: {current_model}")


def is_internet_available():
    try:
        # Attempt to make a simple HTTP request to check internet connectivity
        response = requests.get("http://www.google.com", timeout=5)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False

def show_no_internet_popup():
    messagebox.showerror("No Internet", "Please check your internet connection and try again.")

def regenerate_response():
    user_input = "Regenerate Response"
    conversation_text.config(state=tk.NORMAL)
    conversation_text.insert(tk.END, f"User: {user_input}\n", "user")
    conversation_text.config(state=tk.DISABLED)

    # Simulate response animation
    response = get_response(user_input)
    animate_response(response)




def get_response(input_text):
    # Placeholder function; replace with ChatGPT API call
    q = str(input_text)
    response = chat.send_message(q, stream=True)
    response.resolve()
    return response.text

def send_message():
    user_input = input_text.get("1.0", tk.END).strip()
    if is_internet_available():
        if user_input:
            conversation_text.config(state=tk.NORMAL)
            conversation_text.insert(tk.END, f"User: {user_input}\n", "user")
            conversation_text.config(state=tk.DISABLED)
            input_text.delete("1.0", tk.END)

            # Simulate response animation
            response = get_response(user_input)
            animate_response(response)
    else:
        show_no_internet_popup()

def animate_response(response):
    words = response.split()
    conversation_text.config(state=tk.NORMAL)

    def insert_word(i=0):
        if i < len(words):
            conversation_text.insert(tk.END, words[i] + " ", "AI")
            conversation_text.see(tk.END)  # Scroll to the bottom
            root.after(20, insert_word, i+1)
        else:
            conversation_text.insert(tk.END, "\n")
            conversation_text.config(state=tk.DISABLED)

    insert_word()


def clear_conversation():
    conversation_text.config(state=tk.NORMAL)
    conversation_text.delete("1.0", tk.END)
    conversation_text.config(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
root.title("My GPT")

# Configure row and column weights for responsiveness
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=0)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)
root.grid_columnconfigure(2, weight=0)



# # Label for current model name
# model_label = tk.Label(root, text=f"Current Model: {current_model}", font=('Arial', 12, 'bold'))
# model_label.grid(row=5, column=2, columnspan=3, pady=(10, 0))


# Create Text and Scrollbar widgets
input_text = tk.Text(root, height=3, width=50, wrap="word", font=('Arial', 12))
scrollbar = tk.Scrollbar(root, command=input_text.yview)
input_text.config(yscrollcommand=scrollbar.set)

# Create Send button
send_button = tk.Button(root, text="Send", command=send_message, font=('Arial', 12), bg='#4CAF50', fg='white')
clear_button = tk.Button(root, text="Clear Chat", command=clear_conversation, font=('Arial', 12), bg='#FF5252', fg='white')

# Create a Text widget for displaying the conversation
conversation_text = scrolledtext.ScrolledText(root, height=20, width=50, wrap="word", state=tk.DISABLED, font=('Arial', 12))

# Regen Button
regenerate_response_button = tk.Button(root, text="Regenerate Response", command=regenerate_response, font=('Arial', 12), bg='#2196F3', fg='white')


# # Switch Model button
# switch_model_button = tk.Button(root, text="Switch Model", command=switch_model, font=('Arial', 12), bg='#FFC107', fg='black')


# Tag configurations for different text styles
conversation_text.tag_configure("user", foreground="red")
conversation_text.tag_configure("chatgpt", foreground="#000000")

# Grid layout
input_text.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
scrollbar.grid(row=1, column=1, sticky="ns")
send_button.grid(row=1, column=2, padx=10, pady=10, sticky="ew")
clear_button.grid(row=2, column=2, padx=20, pady=(0, 1), sticky="ew")
conversation_text.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
regenerate_response_button.grid(row=5, column=2, pady=(1, 0))
# switch_model_button.grid(row=5, column=2, pady=(10, 0))

# Bind the Enter key to the send_message function
input_text.bind('<Return>', lambda event=None: send_message())


# Start the Tkinter event loop
root.mainloop()
