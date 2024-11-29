# **uOttaChat**

uOttaChat is uOttaHack's fine-tuned LLM! This repo is the FastAPI backend that allows uOttaChat to be live on the internet via REST API.

## **About**

Built with **Python** and **FastAPI**, uOttaChat runs on an **EC2 instance** and uses a fine-tuned pre-trained LLM (Open AI's GPT-4) to answer event-related questions quickly. It handles queries about challenges, schedules, floor info, and food options, helping reduce people asking organizer Qs.

Use Case: We integrated it into the live site via a chat page!

## **Architecture**
<img width="1991" alt="Screen Shot 2024-11-28 at 5 51 58 PM" src="https://github.com/user-attachments/assets/b58f2840-306d-410b-974b-1d8c2b9cf5c9">


- **Backend**: 
  - **FastAPI** REST API.
  - Hosted on **EC2** instance.
  - Calling our custom trained version on OpenAI's server via API call.

- **Frontend**:
  - Integrated into the live site.


## **Screenshots**
<img width="1809" alt="Screen Shot 2024-11-28 at 12 06 31 AM" src="https://github.com/user-attachments/assets/242464a0-e7c3-4161-b479-89949b5b7611">


## **Deployment**
TODO!

## **Future Improvements**

We should open-source this for other hackathons to deploy and use :)



Finetuning:

- https://platform.openai.com/docs/guides/fine-tuning/


you have to train with somehting like this: 
{"prompt": "What is uOttaHack?", "completion": " uOttaHack is a hackathon part of the Major League Hacking 2025 Hackathon Season. It runs from January 17-19, 2025, at the University of Ottawa (CRX)."}
{"prompt": "Where is uOttaHack 7 held?", "completion": " uOttaHack 7 will be held in person at the Learning Crossroads (CRX) at the University of Ottawa. Address: 100 Louis-Pasteur Private, Ottawa, ON K1N 9N3."}
{"prompt": "Who are the sponsors of uOttaHack?", "completion": " The sponsors for uOttaHack 7 include Solace, Nav Canada, Survey Monkey, CSE Canada, DEEPCODE, IPSG, Deloitte, Red Bull, Warp, Elegoo, Huion, and Long & McQuade."}
{"prompt": "What are the challenges at uOttaHack?", "completion": " uOttaHack 7 includes several challenges: Solace PubSub+ Challenge, Enhancing the EV Experience, Office of The President Challenge, CSE Machine Learning Challenge, Best Sustainability Hackathon, Scoreboard Challenge, Best Carleton x uOttawa Collab, and many more."}
{"prompt": "What prizes are available for uOttaHack winners?", "completion": " Prizes include Meta Quest 2 headsets, Apple Airpods, Google Nest Minis, $500 tuition credits, and more. Each challenge has specific prizes for winners."}
{"prompt": "What is the food menu at uOttaHack?", "completion": " The menu includes:\n- Friday Dinner: Burrito bowls\n- Saturday Breakfast: Baked goods, coffee, fruit, and yogurt\n- Saturday Lunch: Korean bowls (chicken, beef, vegetarian)\n- Saturday Dinner: Shawarma\n- Sunday Breakfast: Baked goods, coffee, fruit, and yogurt."}
{"prompt": "What are the building floor details for uOttaHack?", "completion": " The building floors include:\n- Floor 1: Career Fair, Lobby, Registration, Washrooms\n- Floor 2: Hacker Rooms, Space, Washrooms\n- Floor 3: Food Room, Hacker Rooms, Individual Hacker Rooms\n- Floor 4: Sleep Room, Dishwashing Station, Washrooms\n- Floor 5: Common Area, Team Formation Room, Individual Hacker Rooms."}
{"prompt": "Tell me about the Solace PubSub+ Challenge.", "completion": " The Solace PubSub+ Challenge requires building a project with multiple applications communicating through a Solace Event Broker. Judging criteria include innovation and effective use of Event-Driven Architecture. Prizes include 4 x $250 gift cards."}
{"prompt": "What is the Office of The President Challenge?", "completion": " The challenge involves developing a tool that replicates a study hall for students to collaborate online. Features include chatting (text/audio), sharing insights, and asking questions. Prizes: 4 x $500 tuition credits."}
{"prompt": "What is the food menu for Saturday dinner?", "completion": " Saturday Dinner: Shawarma."}


