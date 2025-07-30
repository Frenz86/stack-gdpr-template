from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
import asyncio

router = APIRouter()

# WebSocket endpoint per notifiche real-time
@router.websocket("/ws/notifications")
async def websocket_notifications(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Echo per demo, sostituire con logica notifiche
            await websocket.send_text(f"Notifica ricevuta: {data}")
    except WebSocketDisconnect:
        pass

# SSE endpoint per live dashboard updates
@router.get("/sse/dashboard")
async def sse_dashboard():
    async def event_generator():
        for i in range(10):
            await asyncio.sleep(1)
            yield f"data: update {i}\n\n"
    return StreamingResponse(event_generator(), media_type="text/event-stream")
