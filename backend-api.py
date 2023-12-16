import requests
import uuid
import json


class PandoraNextClient():
    def __init__(self, endpoint, prefix, token):
        self.base_url = f"{endpoint}/{prefix}"
        self.session = requests.Session()
        self.session.headers = {
            "Authorization": f"Bearer {token}",
        }

    def get_arkose_token(self, model):
        if not model.startswith('gpt-4'):
            return None
        arkose_token = self.session.post(
            f"{self.base_url}/api/arkose/token",
            data={'type': 'gpt-4'}
        ).json().get('token')
        return arkose_token

    def start(self, conversation_id=None, parent_message_id=None, model="text-davinci-002-render-sha", gizmo_id=None):
        self.conversation_id = conversation_id
        self.parent_message_id = parent_message_id
        self.model = model
        self.conversation_mode = self.session.get(
            f'{self.base_url}/backend-api/gizmos/{gizmo_id}'
        ).json() if gizmo_id else None

    def ask(self, content):
        data = {
            'action': 'next',
            'messages': [
                {
                    'id': str(uuid.uuid4()),
                    'author': {
                        'role': 'user',
                    },
                    'content': {
                        'content_type': 'text',
                        'parts': [
                            content,
                        ],
                    },
                    'metadata': {},
                },
            ],
            'conversation_id': self.conversation_id or None,
            'parent_message_id': self.parent_message_id or str(uuid.uuid4()),
            'model': self.model,
            'arkose_token': self.get_arkose_token(self.model),
            'conversation_mode': self.conversation_mode
        }
        resp = self.session.post(
            f'{self.base_url}/backend-api/conversation',
            json=data
        )
        answer = None
        for line in resp.text.split('\n'):
            if not line:
                continue
            try:
                item = json.loads(line[5:])
                if not item.get('is_completion'):
                    answer = item
            except:
                continue
        self.conversation_id = answer['conversation_id']
        self.parent_message_id = answer['message']['id']
        return answer

    def end(self):
        if not self.conversation_id:
            return {
                "error": "conversation_id is not exist"
            }
        resp = self.session.patch(
            f'{self.base_url}/backend-api/conversation/{self.conversation_id}',
            json={'is_visible': False},
        ).json()
        self.conversation_id = None
        self.parent_message_id = None
        self.conversation_mode = None
        return resp


client = PandoraNextClient(
    endpoint="",
    prefix="",
    token=""
)

client.start()
print(client.ask("你好"))
print(client.ask("我叫小强，你叫什么名字？"))
print(client.ask("我叫什么名字？"))
client.end()

client.start(model="gpt-4")
print(client.ask("最近发生了哪些大事情？"))
client.end()

# GPTs例子
client.start(model="gpt-4-gizmo", gizmo_id="g-CFsXuTRfy-pandoranextzhu-shou")
answer = client.ask("PandoraNext 里 proxy_api_prefix 有哪些配置要求")
client.end()

print(answer)