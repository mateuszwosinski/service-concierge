from concierge.memory.internal import Memory
from concierge.datatypes.chat_types import RoleMessage, Role
from concierge.agent.understanding import Understanding


class Agent():
    
    def __init__(self):
        self.memory = Memory(init_with_mock_data=True)
        self.understanding = Understanding()
        
    def process_message(self, conversation_id: str, message: str) -> str:
        self.memory.add_message(conversation_id, RoleMessage(role=Role.USER, message=message))
        
        response = self.understanding.process(message)
        answer = response.choices[0].message.content
        
        self.memory.add_message(conversation_id, RoleMessage(role=Role.ASSISTANT, message=answer))
        return answer