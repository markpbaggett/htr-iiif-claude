import anthropic
import json


class ClaudeRequest:
    def __init__(self, model, key, prompt, image):
        self.model = model
        self.prompt = prompt
        self.content = self.__add_prompt(image, prompt)
        self.client = self.__create_client(key)
        self.output = self.__request()
        self.cost = self.__determine_cost()
        self.text = self.__get_htr_text()

    def __get_htr_text(self):
        try:
            text = json.loads(self.output['content'][0]['text'])
            return text.get('htr', text)
        except json.decoder.JSONDecodeError:
            return self.output['content'][0]['text']

    @staticmethod
    def __create_client(apikey):
        return anthropic.Anthropic(
            api_key=apikey,
        )

    @staticmethod
    def __add_prompt(image, user_prompt):
        image.append(
            {
                "type": "text",
                "text": user_prompt
            }
        )
        return image

    def __request(self):
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": self.content
                }
            ],
        )
        return json.loads(response.json())

    def __determine_cost(self):
        known_models = {
            "claude-3-haiku-20240307": {
                "input": .25,
                "output": 1.25
            },
            "claude-3-5-sonnet-20240620": {
                "input": 3.00,
                "output": 15.00
            },
            "claude-3-sonnet-20240229": {
                "input": 3.00,
                "output": 15.00
            },
            "claude-3-opus-20240229": {
                "input": 15.00,
                "output": 75.00
            }
        }
        input_cost = self.output['usage']['input_tokens'] / 1000000 * known_models[self.model]['input']
        output_cost = self.output['usage']['output_tokens'] / 1000000 * known_models[self.model]['output']
        return {
            'input': input_cost,
            'output': output_cost,
            'total': input_cost + output_cost
        }
