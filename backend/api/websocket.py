"""WebSocket endpoint for real-time updates."""

import asyncio
import json
from datetime import datetime
from typing import Dict, Set

import structlog
from fastapi import WebSocket, WebSocketDisconnect

logger = structlog.get_logger()


class ConnectionManager:
    """Manages WebSocket connections and broadcasting."""

    # Maximum number of concurrent WebSocket connections
    MAX_CONNECTIONS = 100

    def __init__(self):
        """Initialize the connection manager."""
        self.active_connections: Set[WebSocket] = set()
        self.subscriptions: Dict[WebSocket, Set[str]] = {}

    async def connect(self, websocket: WebSocket) -> bool:
        """Accept a new WebSocket connection.

        Args:
            websocket: The WebSocket connection

        Returns:
            True if connection was accepted, False if rejected due to limit
        """
        if len(self.active_connections) >= self.MAX_CONNECTIONS:
            logger.warning(
                "websocket_connection_rejected",
                reason="max_connections_reached",
                current=len(self.active_connections),
                max=self.MAX_CONNECTIONS,
            )
            await websocket.close(code=1013, reason="Maximum connections reached")
            return False

        await websocket.accept()
        self.active_connections.add(websocket)
        self.subscriptions[websocket] = set()
        logger.info("websocket_connected", total_connections=len(self.active_connections))
        return True

    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection.

        Args:
            websocket: The WebSocket connection to remove
        """
        self.active_connections.discard(websocket)
        self.subscriptions.pop(websocket, None)
        logger.info("websocket_disconnected", total_connections=len(self.active_connections))

    def subscribe(self, websocket: WebSocket, channels: list[str]):
        """Subscribe a connection to specific channels.

        Args:
            websocket: The WebSocket connection
            channels: List of channel names to subscribe to
        """
        if websocket in self.subscriptions:
            self.subscriptions[websocket].update(channels)
            logger.info(
                "websocket_subscribed",
                channels=channels,
                total_subscriptions=len(self.subscriptions[websocket]),
            )

    def unsubscribe(self, websocket: WebSocket, channels: list[str]):
        """Unsubscribe a connection from specific channels.

        Args:
            websocket: The WebSocket connection
            channels: List of channel names to unsubscribe from
        """
        if websocket in self.subscriptions:
            self.subscriptions[websocket].difference_update(channels)
            logger.info(
                "websocket_unsubscribed",
                channels=channels,
                total_subscriptions=len(self.subscriptions[websocket]),
            )

    async def send_personal(self, message: dict, websocket: WebSocket):
        """Send a message to a specific connection.

        Args:
            message: The message to send
            websocket: The target WebSocket connection
        """
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error("failed_to_send_personal_message", error=str(e))

    async def broadcast(self, message: dict, channel: str = "all"):
        """Broadcast a message to all subscribed connections.

        Args:
            message: The message to broadcast
            channel: Channel name (only connections subscribed to this channel receive it)
        """
        disconnected = set()

        for connection in self.active_connections:
            # Check if connection is subscribed to this channel or "all"
            subscriptions = self.subscriptions.get(connection, set())
            if channel in subscriptions or "all" in subscriptions:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(
                        "failed_to_broadcast_message",
                        channel=channel,
                        error=str(e),
                    )
                    disconnected.add(connection)

        # Clean up disconnected clients
        for connection in disconnected:
            self.disconnect(connection)


# Global connection manager
manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication.

    Args:
        websocket: The WebSocket connection
    """
    connected = await manager.connect(websocket)
    if not connected:
        return  # Connection was rejected due to limit

    try:
        # Send initial connection success message
        await manager.send_personal(
            {
                "type": "connected",
                "data": {"message": "WebSocket connection established"},
                "timestamp": datetime.now().isoformat(),
            },
            websocket,
        )

        # Main message loop
        while True:
            # Receive message from client
            data = await websocket.receive_text()

            try:
                message = json.loads(data)
                message_type = message.get("type")
                message_data = message.get("data", {})

                if message_type == "subscribe":
                    # Subscribe to channels
                    channels = message_data.get("channels", [])
                    manager.subscribe(websocket, channels)

                    await manager.send_personal(
                        {
                            "type": "subscribed",
                            "data": {"channels": channels},
                            "timestamp": datetime.now().isoformat(),
                        },
                        websocket,
                    )

                elif message_type == "unsubscribe":
                    # Unsubscribe from channels
                    channels = message_data.get("channels", [])
                    manager.unsubscribe(websocket, channels)

                    await manager.send_personal(
                        {
                            "type": "unsubscribed",
                            "data": {"channels": channels},
                            "timestamp": datetime.now().isoformat(),
                        },
                        websocket,
                    )

                elif message_type == "ping":
                    # Respond to ping with pong
                    await manager.send_personal(
                        {
                            "type": "pong",
                            "data": {},
                            "timestamp": datetime.now().isoformat(),
                        },
                        websocket,
                    )

                else:
                    logger.warning("unknown_websocket_message_type", type=message_type)
                    await manager.send_personal(
                        {
                            "type": "error",
                            "data": {"message": f"Unknown message type: {message_type}"},
                            "timestamp": datetime.now().isoformat(),
                        },
                        websocket,
                    )

            except json.JSONDecodeError:
                logger.error("invalid_json_received")
                await manager.send_personal(
                    {
                        "type": "error",
                        "data": {"message": "Invalid JSON"},
                        "timestamp": datetime.now().isoformat(),
                    },
                    websocket,
                )

            except Exception as e:
                logger.error("websocket_message_processing_error", error=str(e), exc_info=True)
                await manager.send_personal(
                    {
                        "type": "error",
                        "data": {"message": "Failed to process message"},
                        "timestamp": datetime.now().isoformat(),
                    },
                    websocket,
                )

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("client_disconnected")

    except Exception as e:
        logger.error("websocket_error", error=str(e), exc_info=True)
        manager.disconnect(websocket)


async def broadcast_state_update(state: dict):
    """Broadcast a state update to all subscribed clients.

    Args:
        state: The current emotional state
    """
    await manager.broadcast(
        {
            "type": "state_update",
            "data": state,
            "timestamp": datetime.now().isoformat(),
        },
        channel="state",
    )


async def broadcast_trigger_detected(trigger_name: str, intensity: float):
    """Broadcast a trigger detection event.

    Args:
        trigger_name: Name of the detected trigger
        intensity: Intensity of the trigger
    """
    await manager.broadcast(
        {
            "type": "trigger_detected",
            "data": {
                "trigger": trigger_name,
                "intensity": intensity,
            },
            "timestamp": datetime.now().isoformat(),
        },
        channel="triggers",
    )


async def broadcast_memory_consolidated(memory_id: str, summary: str, score: float):
    """Broadcast a memory consolidation event.

    Args:
        memory_id: UUID of the consolidated memory
        summary: Summary of the memory
        score: Consolidation score
    """
    await manager.broadcast(
        {
            "type": "memory_consolidated",
            "data": {
                "memory_id": memory_id,
                "summary": summary,
                "score": score,
            },
            "timestamp": datetime.now().isoformat(),
        },
        channel="memory",
    )


async def broadcast_response_ready(response: str, processing_time_ms: int):
    """Broadcast that a response is ready.

    Args:
        response: The system response
        processing_time_ms: Processing time in milliseconds
    """
    await manager.broadcast(
        {
            "type": "response",
            "data": {
                "content": response,
                "processing_time_ms": processing_time_ms,
            },
            "timestamp": datetime.now().isoformat(),
        },
        channel="all",
    )


async def broadcast_processing():
    """Broadcast that the system is processing a message."""
    await manager.broadcast(
        {
            "type": "processing",
            "data": {},
            "timestamp": datetime.now().isoformat(),
        },
        channel="all",
    )
