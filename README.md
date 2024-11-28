# **uOttaChat**

uOttaChat is uOttaHack's fine-tuned LLM! This repo is the FastAPI backend that allows uOttaChat to be live on the internet via REST API.

## **About**

Built with **Python** and **FastAPI**, uOttaChat runs on an **EC2 instance** and uses a fine-tuned pre-trained LLM (Open AI's GPT-4) to answer event-related questions quickly. It handles queries about challenges, schedules, floor info, and food options, helping reduce people asking organizer Qs.

Use Case: We integrated it into the live site via a chat page!

## **Architecture**

<img width="1793" alt="design" src="https://github.com/user-attachments/assets/ea7a6cac-3bc1-45af-8f76-15bb673c1b24">

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
