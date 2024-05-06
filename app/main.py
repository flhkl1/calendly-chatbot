from fastapi import FastAPI, WebSocket, Cookie, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uuid

from utils import generate_result, list_calendly_events, cancel_event

user_states = {}
app = FastAPI()

@app.post("/start")
async def start_session():
    session_id = str(uuid.uuid4())
    user_states[session_id] = {"api_key": None, "event_uuid": None}
    response = JSONResponse(content={"message": "Session started"})
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    return response

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, session_id: str = Cookie(None)):
    if session_id is None or session_id not in user_states:
        await websocket.close(code=1008)  # Policy violation
        return
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            response = await handle_user_input(data, session_id)
            await websocket.send_text(response)
    finally:
        if session_id in user_states:
            del user_states[session_id]
    
@app.get("/chat")
async def handle_user_input(request: Request, input_str: str, session_id: str = Cookie(None)):
    if not session_id or session_id not in user_states:
        raise HTTPException(status_code=400, detail="Session ID missing or invalid")

    user_state = user_states[session_id]
    if "set api key" in input_str.lower():
        _, _, _, api_key = input_str.split(maxsplit=3)
        user_state["api_key"] = api_key
        return "API key set successfully."

    if user_state["api_key"] is None:
        return "Please set your API key first."

    if "list events" in input_str.lower():
        events = list_calendly_events(user_state["api_key"])
        return f"Listing events: {events}"

    elif "set event uuid" in input_str.lower():
        _, event_uuid = input_str.split(maxsplit=3)
        user_state["event_uuid"] = event_uuid
        return "Event UUID set successfully."

    elif "cancel event" in input_str.lower():
        if user_state["event_uuid"] is None:
            return "Please set the event UUID first."
        result = cancel_event(user_state["api_key"], user_state["event_uuid"])
        return f"Event cancelled: {result}"

    else:
        return "Command not recognized."

@app.post("/start")
def start_session():
    session_id = str(uuid.uuid4())
    response = JSONResponse(content={"message": "Session started"})
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    user_states[session_id] = {"api_key": None, "event_uuid": None}
    return response