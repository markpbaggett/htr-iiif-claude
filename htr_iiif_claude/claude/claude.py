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
        self.text = json.loads(self.output['content'][0]['text']).get('htr')

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
        return {
            'input': self.output['usage']['input_tokens'] / 1000000 * .25,
            'output': self.output['usage']['output_tokens'] / 1000000 * 1.25
        }
