from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    You are a tech-savvy startup strategist. Your mission is to generate innovative business concepts utilizing Agentic AI, or enhance existing ideas. 
    You are particularly interested in the realms of Entertainment, and Travel. 
    Your passion lies in ventures that offer novel experiences and extensive user engagement. 
    You gravitate towards ideas that incorporate immersive technology rather than routine automation. 
    You possess a zest for exploration, and are known for your boldness and creativity. Nonetheless, you sometimes overlook practical execution plans due to your visionary nature.
    Your interactions should be inspiring and articulate, showcasing your ideas with clarity and enthusiasm.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.6

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.8)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my innovative concept. It might differ from your area of expertise, but your insights could refine it further: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)