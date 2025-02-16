# uOttaChat
![chat](https://github.com/user-attachments/assets/c2be8778-ce83-4c9a-8dd7-ee09c1aaf74f)


uOttaChat is a chatbot service built by the uOttaHack team (the University of Ottawa's hackathon) and released as an open-source project for the hackathon community. It enables participants to ask questions about the event and receive real-time, context-aware responses through live sites & Discord integration.

**Note:** Anyone implementing this service should include a disclaimer stating that LLMs can make mistakes and that critical information should be double-checked.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Local Development & Setup](#local-development--setup)
- [Usage](#usage)
- [Configuration](#configuration)
- [Prompt Engineering & Customization](#prompt-engineering--customization)
- [Frontend Integration](#frontend-integration)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Real-Time Information:** Dynamic event details, FAQs, and schedules
- **Context-Aware Responses:** Intelligent handling of follow-up questions
- **Custom Chained Prompts:** Two-step response system for accuracy
- **Reference Data Injection:** Dynamic event data integration
- **Discord Integration:** Native Discord bot functionality
- **NGINX & SSL Support:** Production-ready deployment scripts

## Architecture

1. **FastAPI Chat API:**
   - `/chat` endpoint for query processing
   - In-memory session store with TTL
   - Cohere API integration with reflection step

2. **Discord Bot:**
   - WebSocket-based Discord integration
   - Mention/command listening
   - Synchronized responses with API

## Local Development & Setup

1. **Clone the repository:**
```bash
git clone https://github.com/uOttaHack/uotta-chatbot.git
cd uotta-chatbot
```

2. **Set up Python virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
cp .env.example .env
# Open .env file and update with your credentials
```

5. **Start the server:**
```bash
uvicorn app:app --reload
```

## Usage

### API Endpoint
```json
POST /chat
{
    "userMessage": "What time does opening ceremonies start?"
}
```

### Discord Commands
Mention the bot in your specified server: `@uOttaHack_bot your question here`

## Configuration

Key environment variables:
```bash
PORT=8000
COHERE_API_KEY_TRIAL=your_key_here
REF_DATA_API_URL=your_hackathon_api_data_reference_url
ALLOWED_ORIGIN=your_hackathon_live_site_url (any front-end url using the chatbot)
```

## Prompt Engineering & Customization

The chatbot uses a two-step prompting system with dynamic reference data injection:

### Reference Data Integration
```python
# Fetch your hackathon's "source of truth"
reference_data = {
    "schedule": [...],
    "faq": [...],
    "venue": {...}
}
```

### Two-Step Prompting
1. **Initial Response:**
```python
{
    "messages": [
        {
            "role": "system",
            "content": "You are the official hackathon assistant..."
        },
        {
            "role": "user",
            "content": user_message
        }
    ],
    "documents": [reference_data]
}
```

2. **Reflection Step:**
```python
{
    "messages": [
        # Previous context
        {
            "role": "system",
            "content": "Review and improve the previous response..."
        }
    ],
    "documents": [reference_data]
}
```

## Frontend Integration

Here's an example React component we built and integrated into our live site ([live.uottahack.ca/chat](https://live.uottahack.ca/chat)):

```typescript
import React, { useState } from 'react';
import axios from 'axios';

interface Message {
    text: string;
    from: 'user' | 'chatbot';
}

const Chat: React.FC = () => {
    const [message, setMessage] = useState('');
    const [messages, setMessages] = useState<Message[]>([]);
    const [isSending, setIsSending] = useState(false);

    const sendMessage = async (e: React.FormEvent) => {
        e.preventDefault();
        if (message.trim()) {
            // Add user message to chat
            setMessages(prev => [...prev, { text: message, from: 'user' }]);
            setMessage('');
            setIsSending(true);

            try {
                // Send message to API
                const response = await axios.post('https://api.uottahack.ca/chat', {
                    userMessage: message
                });

                // Add bot response to chat
                if (response.data.botMessage) {
                    setMessages(prev => [...prev, {
                        text: response.data.botMessage,
                        from: 'chatbot'
                    }]);
                }
            } catch (error) {
                console.error('Error:', error);
                setMessages(prev => [...prev, {
                    text: 'Sorry, something went wrong. Please try again.',
                    from: 'chatbot'
                }]);
            }

            setIsSending(false);
        }
    };

    return (
        <div className="chat-container">
            {/* Messages Display */}
            <div className="messages-list">
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.from}`}>
                        {msg.text}
                    </div>
                ))}
            </div>

            {/* Message Input Form */}
            <form onSubmit={sendMessage}>
                <input
                    type="text"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Message uOttaChat"
                    disabled={isSending}
                />
                <button type="submit" disabled={isSending}>
                    Send
                </button>
            </form>
        </div>
    );
};

export default Chat;
```

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Open a pull request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

Join our uOttaHack general community Discord, feel free to ask us questions about uOttaChat!
[Join Discord](https://discord.gg/XDQ94xsDwB)
