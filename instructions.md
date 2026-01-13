# pAI Setup Instructions: Charlie Kirk AI Debate Bot

This guide will help you set up and run the Charlie Kirk AI Debate Bot, part of the Personality AI (pAI) project. The bot simulates engaging debates in Kirk's style, drawing from his public ideas to foster critical thinking and truth-seeking dialogues. Follow these steps to get started.

<!-- Block for Infinite Looping GIF: 
    GIFs loop infinitely by default if created that way; added CSS for smooth playback and full width. -->
![Kirk Demo Animation](materials/kirk%20demo%20100%25size.gif)

*Welcome to pAI: Preserving the spirit of debate through AI. Dive into thoughtful conversations inspired by Charlie Kirk's ideas, fostering critical thinking for a better society.*

## 1. Download and Set Up LM Studio
The bot requires a local language model server. We recommend LM Studio for its ease of use. It will host the fine-tuned model and provide the API endpoint.

1. Download LM Studio from the official website: [https://lmstudio.ai/](https://lmstudio.ai/). Choose the version for your operating system (Windows, macOS, or Linux).
2. Install LM Studio by following the on-screen instructions. Once installed, open the application.
3. In LM Studio's search bar (usually at the top), type "Entz/gpt-oss-20b-pai-debator" to find the model.
4. Click on the model in the search results and select "Download".
5. Wait for the download to complete (it may take time depending on your internet; the model is ~13 GB).
6. Once downloaded, go to the "Local Inference Server" tab (or similar—look for the server icon in the sidebar).
7. Load the model: Select "Entz/gpt-oss-20b-pai-debator" from your downloaded models.
8. Start the server: Click "Start Server" (default port is 1234). Note the API URL—it should be something like `http://localhost:1234/v1/chat/completions`. You'll use this when the app is loaded.
9. Keep LM Studio running in the background while using the bot.

> **Note:** If the model isn't found, ensure you're searching the exact name. No API token is needed for local LM Studio servers—leave it blank when the app is loaded.

## 2. Install Python Dependencies
The script requires a few Python libraries for the web interface and API calls.

1. Ensure Python is installed (version 3.8+). Download from [python.org](https://www.python.org/) if needed.
2. Create a file named `requirements.txt` with the following content:

   ```
   gradio
   requests
   ```

3. In your terminal/command prompt, run:
   ```
   pip install -r requirements.txt
   ```
4. Alternatively, install directly:
   ```
   pip install gradio requests
   ```

## 3. Download and Run the Script
1. Download the script file `ai_charlie_kirk.py` from this GitHub repository (click "Raw" and save as .py).
2. Open a terminal/command prompt and navigate to the directory containing the script (e.g., `cd path/to/folder`).
3. Run the script:
   ```
   python ai_charlie_kirk.py
   ```
4. The script will launch a configuration screen in your browser (e.g., at http://127.0.0.1:7860). Enter your LM Studio API URL (from Step 1, e.g., "http://localhost:1234/v1/chat/completions") and leave the API Token blank (or enter if required by your setup).
5. Click "Save & Start" to proceed to the chat interface.

## 4. Use the Chat Interface
1. Once the chat loads, you'll see "Debate AI Charlie Kirk • Classic Messenger Style" with a chat window.
2. Type your message in the bottom text box (e.g., a debate opener like "What's your view on meritocracy?").
3. Press Enter or click "Send". Your message appears on the right (blue bubble) with a timestamp.
4. A "Typing..." indicator shows while the AI generates a response.
5. The AI's reply appears on the left (gray bubble), building the conversation vertically.
6. Continue the dialogue—history is maintained for context.

<!-- Block for Several Pictures: Insert this where you want a gallery of images (e.g., in a new section). 
    This creates a responsive grid (adjusts to screen size). 
    Add/remove <img> tags as needed for more/fewer pictures. -->
![Description of Picture 1](materials/demo.png)
![Description of Picture 2](materials/demo2.png)

*These images highlight the model successfully captured Charlie's confidence in his speech, and some phrases Charlie loves to say, e.g. "God bless!".*

> **Note:** Responses align with Kirk's public ideas; test on familiar topics for best results. Report misalignments via GitHub issues.

## 5. Troubleshooting and Tips
- If the API fails, check LM Studio is running and the URL is correct. Error messages will appear in the chat.
- Conversation history: Up to 12 messages for context; clears on restart.
- Stop the server: Press Ctrl+C in the terminal.
- Customize: Edit SYSTEM_PROMPT in the script for tweaks.
- For remote access: In the script, change `demo.launch()` to `demo.launch(server_name="0.0.0.0", share=True)` (use cautiously).

Enjoy your debates! This is a tool for truth-seeking and cultural preservation—feedback welcome on GitHub.