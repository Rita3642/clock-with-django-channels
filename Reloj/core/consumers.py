import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import requests
from datetime import datetime
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Myconsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.id = self.scope['url_route']['kwargs']['option']

        option = self.id.replace('/', '-')

        self.clock_group_name = 'clock_%s' % option

        # Imprime mensajes de depuración para verificar la conexión y el grupo
        # print(f'Conectado a WebSocket para opción {option}')
        # print(f'Nombre del grupo: {self.clock_group_name}')

        await self.channel_layer.group_add(
            self.clock_group_name, 
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.clock_group_name, 
            self.channel_name
        )


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        option = text_data_json['option']
        
        country_code = option


        api_url = f'http://worldtimeapi.org/api/timezone/{country_code}'




        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            time_str = data['datetime']

            time = datetime.fromisoformat(time_str)

            hr = time.strftime('%H')
            mn = time.strftime('%M')
            sc = time.strftime('%S')

        else:
            print('Error?????????????????')


        await self.channel_layer.group_send(
            self.clock_group_name, {
                'type': 'clock_country',
                'option': option,
                'hr': hr,
                'mn': mn,
                'sc': sc,
            }
        )

    async def clock_country(self, event):
        option = event['option']
        hr = event['hr']
        mn = event['mn']
        sc = event['sc']

        await self.send(text_data=json.dumps({"message": option, 'hr': hr, 'mn': mn, 'sc': sc}))


    