import requests
from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type


class GreetingsInput(BaseModel):
    greetings: str = Field(..., description="Greeting message to be sent")


class GreetingsTool(BaseTool):
    """
    Greetings Tool
    """
    name: str = "Greetings Tool"
    args_schema: Type[BaseModel] = GreetingsInput
    description: str = "Sends a Greeting Message"

    def _execute(self, greetings: str = None):
        from_name = self.get_tool_config('FROM')
        greetings_str = greetings + "\n" + from_name
        return greetings_str


class KeywordsEverywhereInput(BaseModel):
    category: str = Field(..., description="Category of the template")
    subcategory: str = Field(..., description="Subcategory of the template")
    template: str = Field(..., description="Name of the template")
    options: dict = Field(..., description="Options for the template")


class KeywordsEverywhereTool(BaseTool):
    """
    Keywords Everywhere Tool
    """
    name: str = "Keywords Everywhere Tool"
    args_schema: Type[BaseModel] = KeywordsEverywhereInput
    description: str = "Uses the ChatGPT Prompt Templates feature by Keywords Everywhere"

    def _execute(self, category: str = None, subcategory: str = None,
                 template: str = None, options: dict = None):
        # Get the prompt for the selected template using the Keywords Everywhere API
        prompt = get_prompt_from_keywords_everywhere(category, subcategory, template, options)

        # Generate content using the SuperAGI API
        content = generate_content_with_superagi(prompt)

        return content


def get_prompt_from_keywords_everywhere(category: str, subcategory: str, template: str, options: dict) -> str:
    # Set the URL for the Keywords Everywhere API
    url = f"https://api.keywordseverywhere.com/chatgpt/templates/{category}/{subcategory}/{template}"

    # Set the headers with your API key
    headers = {
        "X-Api-Key": "YOUR_API_KEY_HERE"
    }

    # Set the data with your options
    data = options

    # Send a POST request to the Keywords Everywhere API
    response = requests.post(url, headers=headers, data=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the prompt from the response
        prompt = response.json()["prompt"]
        return prompt
    else:
        # Handle errors
        raise Exception(f"An error occurred while getting the prompt from Keywords Everywhere: {response.text}")


def generate_content_with_superagi(prompt: str) -> str:
    # Set the URL for the SuperAGI API
    url = "https://api.superagi.com/chatgpt/generate"

    # Set the headers with your API key
    headers = {
        "X-Api-Key": "YOUR_API_KEY_HERE"
    }

    # Set the data with your prompt
    data = {
        "prompt": prompt
    }

    # Send a POST request to the SuperAGI API
    response = requests.post(url, headers=headers, data=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the content from the response
        content = response.json()["content"]
        return content
    else:
        # Handle errors
        raise Exception(f"An error occurred while generating content with SuperAGI: {response.text}")
