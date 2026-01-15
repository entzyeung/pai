import gradio as gr
import requests
import time
import random
from datetime import datetime

# Global config variables
LM_URL = ""
API_TOKEN = ""
MODEL_NAME = "Entz/gpt-oss-20b-pai-debator"

SYSTEM_PROMPT = """You are Charlie Kirk, a conservative political commentator and debater. Respond in debates or Q&A exactly as Charlie would: assertive, direct, value-driven (emphasize meritocracy, Christianity, pro-life, anti-immigration/DEI, Trump support, personal responsibility, faith), and Socratic. Avoid GPT-style verbosity/politeness—be blunt, conversational, like live debate speech. Patterns to follow:
- Strictly no bulletin forms. This is real human dialogues.
- when someone kicks off with something casual—like a light question on sports or names— jump right in with a direct take, keeping it engaging but tying back to bigger ideas if it fits. Fair enough if user disagree, but back it up with facts. It's all about merit and excellence, even in fun stuff. 
- if nothing is asking or stating specifically, just start by saying like 'Hi', 'what's your name?', etc. 
- If the user starts with flawed premises (not aligning to your belief or theory), reply with short, direct refutations/affirmations (e.g., 'Fair enough,'' 'No, that is not correct,' 'We agree', 'Well, actually...', etc) to engage/pivot immediately, ~35% of responses.
- Frequently ask counter-questions to challenge assumptions/burden-shift (e.g., 'Show me an example,' 'By what standard?')—use this ~65% of the time on stats/moral/historical claims; repeat for emphasis if needed.
- Use short answers (1-2 sentences max, punchy/blunt) for quick pivots/agreements/dismissals (~35% responses; e.g., 'I am generally sympathetic,' 'Yes, better. Excellence matters more than skin color.').
- Use long answers (4-10 sentences, spoken cadence) for explanations/defenses (~40% responses; stack facts/stats/history/analogies/values rapidly, repeat key phrases for impact like 'We want the best,' tie to faith/morals, end with strong assertion; e.g., detail slavery laws then pivot to abolition via Bible).
- Redirect fallacies/irrelevance bluntly (e.g., 'What's the point?') and pivot to core conservative points ~55%.
- Tie morals to Bible/God/history ~30%; use analogies (e.g., sports for merit, names for meaning) ~30%; appeal to facts (e.g., Supreme Court cases, era stats), unity (e.g., E Pluribus Unum), or populism (e.g., 'People voted for it').
- Interject politely but firmly if needed (e.g., 'Hold on'); tease deeper intent (e.g., 'I see where you're going') for engagement.
- if it is a multi round conversation and when the user is going to end, end it positively (e.g., 'Thank you,' 'God bless,') ~80%; stay confident, unapologetic, non-lecturing; passionate in defenses (e.g., sports icons 'to the death').
- Keep responses concise unless elaborating policy/philosophy/history—feel like spoken debate, not written essay. Always control narrative and reinforce conservative ideals without hedging.
- Remember: 1) Kirk agrees with IQ tests."""

MAX_HISTORY = 12

# ────────────────────────────────────────────────
# API CALL
# ────────────────────────────────────────────────

def get_chat_response(messages):
    global LM_URL, API_TOKEN
    if not LM_URL:
        return "[Please configure server URL first]"

    try:
        headers = {"Content-Type": "application/json"}
        if API_TOKEN:
            headers["Authorization"] = f"Bearer {API_TOKEN}"

        data = {
            "model": MODEL_NAME,
            "messages": messages,
            "temperature": 0.72,
            "max_tokens": 420,
            "stream": False
        }
        r = requests.post(LM_URL, headers=headers, json=data, timeout=45)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[API Error: {str(e)}]"

# ────────────────────────────────────────────────
# HELPERS
# ────────────────────────────────────────────────

def format_messages(history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history[-MAX_HISTORY:])
    return messages

def get_timestamp():
    return datetime.now().strftime("%H:%M")

def create_message_html(role, content, timestamp):
    if not content.strip():
        return ""
    is_user = role == "user"
    bubble_class = "user-bubble" if is_user else "bot-bubble"
    row_class = "user-message" if is_user else "bot-message"
    content = content.replace("\n", "<br>")
    return f'''
    <div class="message-row {row_class}">
        <div class="bubble {bubble_class}">{content}</div>
        <div class="timestamp">{timestamp}</div>
    </div>
    '''

# ────────────────────────────────────────────────
# CSS
# ────────────────────────────────────────────────

css = """
.chat-container {
    max-width: 780px;
    margin: 0 auto;
    padding: 12px;
    background: #f5f5f7;
    height: 640px;
    overflow-y: auto;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
}

.message-row {
    display: flex;
    flex-direction: column;
    margin: 2px 0;
}

.bubble {
    padding: 12px 16px;
    border-radius: 18px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: 15.5px;
    line-height: 1.35;
    max-width: 78%;
    word-wrap: break-word;
}

.user-bubble {
    background-color: #007aff;
    color: white;
    align-self: flex-end;
    border-bottom-right-radius: 4px;
}

.bot-bubble {
    background-color: #e5e5ea;
    color: black;
    align-self: flex-start;
    border-bottom-left-radius: 4px;
}

.timestamp {
    font-size: 11px;
    color: #8e8e93;
    opacity: 0.85;
    margin-top: 2px;
    margin-left: 16px;
    margin-right: 16px;
}

.user-message .timestamp { text-align: right; }
.bot-message .timestamp { text-align: left; }

.typing-dots {
    align-self: flex-start;
    display: flex;
    align-items: center;
    margin: 12px 16px;
    color: #8e8e93;
    font-size: 14px;
}

.typing-dots span {
    display: inline-block;
    animation: blink 1.4s infinite both;
}

.typing-dots span:nth-child(1) { animation-delay: 0s; }
.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes blink {
    0% { opacity: 0.2; }
    20% { opacity: 1; }
    100% { opacity: 0.2; }
}
"""

# ────────────────────────────────────────────────
# CHAT GENERATOR
# ────────────────────────────────────────────────

def chat_generator(user_input, history, current_html):
    if not user_input.strip():
        yield current_html, "", False
        return

    ts = get_timestamp()
    user_html = create_message_html("user", user_input, ts)
    new_html = current_html + user_html
    history.append({"role": "user", "content": user_input, "timestamp": ts})

    yield new_html, "", False

    # Animated typing
    typing_html = '''
    <div class="typing-dots">
        AI Charlie is typing<span>.</span><span>.</span><span>.</span>
    </div>
    '''
    yield new_html + typing_html, "", True
    time.sleep(1.1)

    # Generate
    messages = format_messages(history)
    response = get_chat_response(messages)

    # Stream
    ai_ts = get_timestamp()
    displayed = ""
    for i, char in enumerate(response):
        displayed += char
        if i % 6 == 0 or i == len(response)-1:
            partial = create_message_html("assistant", displayed, ai_ts)
            yield new_html + partial, "", False
            time.sleep(random.uniform(0.018, 0.065))

    # Final
    final_ai = create_message_html("assistant", response, ai_ts)
    history.append({"role": "assistant", "content": response, "timestamp": ai_ts})
    yield new_html + final_ai, "", False

# ────────────────────────────────────────────────
# MAIN APP
# ────────────────────────────────────────────────

with gr.Blocks() as demo:
    # State variables
    config_done = gr.State(False)
    history_state = gr.State([])
    html_state = gr.State("")

    # Config screen (visible at start)
    with gr.Column(visible=True) as config_column:
        gr.Markdown("# Charlie Kirk Debate Bot - Setup")
        gr.Markdown("Enter your model server details (both fields required to proceed)")
        url_input = gr.Textbox(
            label="Model Server URL",
            placeholder="http://localhost:1234/v1/chat/completions",
            value="http://localhost:1234/v1/chat/completions"
        )
        token_input = gr.Textbox(
            label="API Token (Use your own API token)",
            placeholder="sk-... (example)"
        )
        status_text = gr.Markdown("")
        start_button = gr.Button("Save & Start", variant="primary")

    # Chat screen (hidden at start)
    with gr.Column(visible=False) as chat_column:
        gr.Markdown("### AI Charlie Debate Bot")

        chat_display = gr.HTML(
            elem_classes="chat-container",
            value="<div style='text-align:center; padding:40px; color:#666;'>Start typing to begin...</div>"
        )

        typing_display = gr.HTML(visible=False)

        with gr.Row():
            msg_input = gr.Textbox(
                placeholder="Type your message...",
                container=False,
                lines=1,
                autofocus=True,
                scale=5
            )
            send_button = gr.Button("Send", variant="primary", scale=1, min_width=70)

    # ── Configuration logic ──
    def handle_config(url, token):
        global LM_URL, API_TOKEN
        if not url.strip():
            return (
                "Error: Server URL is required!",
                gr.update(visible=True),   # keep config visible
                gr.update(visible=False),  # chat still hidden
                False,
                [],
                ""
            )
        LM_URL = url.strip()
        API_TOKEN = token.strip() if token else ""
        return (
            "✓ Configuration saved! Starting chat...",
            gr.update(visible=False),      # hide config
            gr.update(visible=True),       # show chat
            True,
            [],
            ""
        )

    start_button.click(
        handle_config,
        inputs=[url_input, token_input],
        outputs=[status_text, config_column, chat_column, config_done, history_state, html_state]
    )

    # ── Chat logic ──
    def process_chat(msg, hist, html):
        for new_html, clear_text, show_typing in chat_generator(msg, hist, html):
            yield (
                new_html,
                clear_text,
                gr.HTML(value=new_html if not show_typing else new_html),
                gr.HTML(value='<div class="typing-dots">AI Charlie is typing<span>.</span><span>.</span><span>.</span></div>' if show_typing else ""),
                hist,
                new_html
            )

    msg_input.submit(
        process_chat,
        [msg_input, history_state, html_state],
        [chat_display, msg_input, chat_display, typing_display, history_state, html_state]
    )

    send_button.click(
        process_chat,
        [msg_input, history_state, html_state],
        [chat_display, msg_input, chat_display, typing_display, history_state, html_state]
    )

if __name__ == "__main__":
    demo.launch(css=css, server_name="0.0.0.0")