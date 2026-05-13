import json
from typing import Any
from channels.generic.websocket import AsyncWebsocketConsumer

online_count = 0


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket консьюмер для чату з підтримкою push-сповіщень.

    Attributes:
        room_group_name: Назва групи каналів для broadcast.
    """

    async def connect(self) -> None:
        """Обробляє нове WebSocket підключення.

        Збільшує лічильник онлайн-користувачів та повідомляє всіх підключених.
        """
        global online_count
        online_count += 1

        self.room_group_name = 'chat_room'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'online_count_update',
                'count': online_count,
            }
        )

    async def disconnect(self, close_code: int) -> None:
        """Обробляє відключення WebSocket.

        Args:
            close_code: Код закриття WebSocket з'єднання.
        """
        global online_count
        online_count -= 1

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'online_count_update',
                'count': online_count,
            }
        )

    async def receive(self, text_data: str) -> None:
        """Обробляє вхідне повідомлення від клієнта.

        Args:
            text_data: JSON-рядок з типом та даними повідомлення.
        """
        data = json.loads(text_data)
        msg_type = data.get('type')

        user = self.scope['user']

        if msg_type == 'chat_message':
            if not user.is_authenticated:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'Увійдіть, щоб писати повідомлення'
                }))
                return

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': data['message'],
                    'username': user.username,
                }
            )

        elif msg_type == 'push_notification':
            if not user.is_staff:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'Тільки адміністратор може надсилати push-сповіщення'
                }))
                return

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'push_notification',
                    'message': data['message'],
                    'from_user': user.username if user.is_authenticated else 'Гість',
                }
            )

    async def chat_message(self, event: dict[str, Any]) -> None:
        """Надсилає повідомлення чату конкретному клієнту.

        Args:
            event: Словник з полями message та username.
        """
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'username': event['username'],
        }))

    async def online_count_update(self, event: dict[str, Any]) -> None:
        """Надсилає оновлений лічильник онлайн-користувачів клієнту.

        Args:
            event: Словник з полем count.
        """
        await self.send(text_data=json.dumps({
            'type': 'online_count',
            'count': event['count'],
        }))

    async def push_notification(self, event: dict[str, Any]) -> None:
        """Надсилає push-сповіщення конкретному клієнту.

        Args:
            event: Словник з полями message та from_user.
        """
        await self.send(text_data=json.dumps({
            'type': 'push_notification',
            'message': event['message'],
            'from_user': event['from_user'],
        }))