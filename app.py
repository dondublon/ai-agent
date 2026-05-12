import json

from logging_config import logger 
from chat_request import chatRequest 
from config import MODEL_NAME, URL
from text_prcessor import TextProcessor
from system_prompt import SYSTEM_PROMPT
from tools import TOOLS
def _bootstrap():
    textProcessor = TextProcessor.createTextProcessor()
    return textProcessor
def _finishProcess():
   print("Chat console exited. Thanks & bye")
def _get_response_from_tool(response):
    try:
        response_json = json.loads(response)
        tool_name = response_json.get("tool")
        arguments = response_json.get("arguments", {})
        response = None
        if tool_name in TOOLS:
            response = TOOLS[tool_name](arguments)
        else:
            logger.error(f"Tool '{tool_name}' not found in available tools.")
            response =  f"the tool '{tool_name}' is not available."
    except json.JSONDecodeError:
        pass
    return response
def _get_response(messages, textProcessor):
    response = textProcessor.get_answer(messages[-1]["content"])
    logger.debug(f"TextProcessor response: {response} on query: {messages[-1]['content']}")
    if not response:
        logger.debug("No relevant information found in TextProcessor. Falling back to chat model.") 
        response = chatRequest(MODEL_NAME, URL, messages)
        responseFromTool = _get_response_from_tool(response)
        role = "assistant"
        if responseFromTool:
            response = responseFromTool
            role = "tool"
    else: 
        response = "Travel agency: " + response
        role = "agent"
    return response, role
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
            response, role = _get_response(messages, testProcessor)
            print(f"{role.capitalize()}: {response}")
            messages.append({"role": role, "content": response})
        except KeyboardInterrupt:
            _finishProcess()
            break   
if __name__ == "__main__":
    main()