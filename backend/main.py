import uvicorn
from fastapi import WebSocketDisconnect
from fastapi import FastAPI, WebSocket, Request
from typing import List
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Список подключенных клиентов
connected_clients = []

# Очередь сообщений
message_queue = []

# WebSocket для веб-интерфейса чата
@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()
    # Добавляем клиента в список подключенных
    connected_clients.append({"websocket": websocket, "username": username})
    # Приветственное сообщение для нового клиента
    welcome_message = f"Привет, {username}! Добро пожаловать в чат Otus!"
    await websocket.send_text(welcome_message)
    
    # Отправляем сообщения из очереди (если они есть)
    for message in message_queue:
        await websocket.send_text(message)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = f"{username}: {data}"
            # Добавляем сообщение в очередь
            message_queue.append(message)
            # Отправляем сообщение всем подключенным клиентам
            for client in connected_clients:
                await client["websocket"].send_text(message)
    except WebSocketDisconnect:
        # Удаляем клиента из списка при отключении
        for client in connected_clients:
            if client["websocket"] == websocket:
                connected_clients.remove(client)
                break

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost",
        "http://176.114.79.182"
        # "http://31.129.43.117",
        # "https://site-test-deploy1.ru",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )