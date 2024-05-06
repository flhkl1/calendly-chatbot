from openai import OpenAI
from fastapi import FastAPI, WebSocket
import asyncio
import requests

client = OpenAI(
    api_key="sk-proj-zmeIyR2zv79elIAcADLRT3BlbkFJSha8fwbGE8TaXk7NqbZX",
)

def generate_result(user_input, user_name="User"):
    messages = [
        {"role": "system", "content": "You are a helpful interactive chatbot that allows users to interact with their Calendly account directly through the chat interface."},
        {"role": "user", "content": "I am " + user_name + ", I want to interact with my Calendly account."},
        {"role": "user", "content": user_input}
    ]
    completion = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    reply = completion.choices[0].message.content
    return reply


def list_calendly_events(api_key):
    headers = {'Authorization': f'Bearer {api_key}'}
    url = 'https://api.calendly.com/scheduled_events'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        events = response.json().get('collection', [])
        events_info = "\n".join([f"Event: {event['name']} on {event['start_time']}, {event['uri']}" for event in events])
        return events_info if events_info else "No upcoming events."
    else:
        return "Failed to retrieve events. Error code" + str(response.status_code)

def cancel_event(api_key, event_uuid):
    headers = {'Authorization': f'Bearer {api_key}'}
    url = f'https://api.calendly.com/scheduled_events/{event_uuid}/cancellation'
    response = requests.post(url, headers=headers)
    if response.status_code == 204:
        return "Event cancelled successfully."
    else:
        return f"Failed to cancel event: {response.status_code}"