import speech_recognition as sr
from pieces_os_client.wrapper import PiecesClient
from pieces_os_client.wrapper.basic_identifier.chat import BasicChat
from pieces_os_client.api_client import ApiClient
from pieces_os_client.api.conversations_api import ConversationsApi
from pieces_os_client.models.seeded_conversation import SeededConversation

api_client = ApiClient.get_default()
host_url = "http://127.0.0.1:39300"
pieces_client = PiecesClient(host=host_url)
conversations_api = ConversationsApi(api_client)
seeded_conversation = SeededConversation(
    type="COPILOT",
    initial_message="You are an AI assistant that helps people with their work and can send emails for them by triggering specific functions."
)
conversation = conversations_api.conversations_create_specific_conversation(
    transferables=True,
    seeded_conversation=seeded_conversation
)

print("New conversation created:", conversation)
chat_id = "8ece170c-2c20-40b4-abc5-4d02d6aba951"
pieces_client.copilot.chat = BasicChat(chat_id)
pieces_client.copilot.chat.name = "System: Pieces-Assistant"

def listen_and_respond():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Use the microphone as the source for input
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            # Convert audio to text
            question = recognizer.recognize_google(audio)
            print(f"You said: {question}")

            # Ask the question to the copilot and stream the response
            for response in pieces_client.copilot.stream_question(question):
                if response.question:
                    answers = response.question.answers.iterable
                    for answer in answers:
                        print(answer.text, end="")

        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

# Call the function
listen_and_respond()
# Close the client
pieces_client.close()