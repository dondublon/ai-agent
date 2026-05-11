from logging_config import logger 
from chat_request import chatRequest 
from config import MODEL_NAME, URL
from text_prcessor import TextProcessor
from system_prompt import SYSTEM_PROMPT
def _bootstrap():
    textProcessor = TextProcessor.createTextProcessor()
    return textProcessor
def _finishProcess():
   print("Chat console exited. Thanks & bye")
def _get_response(messages, textProcessor):
    response = textProcessor.get_answer(messages[-1]["content"])
    logger.debug(f"TextProcessor response: {response} on query: {messages[-1]['content']}")
    if not response:
        logger.debug("No relevant information found in TextProcessor. Falling back to chat model.") 
        response = chatRequest(MODEL_NAME, URL, messages)
    else: response = "Travel agency " + response
    return response
def main():
    testProcessor = _bootstrap()
    print(f"{MODEL_NAME} chat console started. Type 'exit' to quit.")
    messages = [
        {"role": "system", 
         "content": SYSTEM_PROMPT
         }
    ]
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                _finishProcess()
                break
            messages.append({"role": "user", "content": user_input})
            response = _get_response(messages, testProcessor)
            print(f"Assistant: {response}")
            messages.append({"role": "assistant", "content": response})
        except KeyboardInterrupt:
            _finishProcess()
            break   
if __name__ == "__main__":
    main()