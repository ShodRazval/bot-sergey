import os
import openai


class ChatGptClient:
    __model = "gpt-3.5-turbo"

    openai.api_key = os.environ.get('OPEN_API_TOKEN')

    def get_response(self, message):
        response = openai.chat.completions.create(
            model=self.__model,
            messages=[
                {
                    "role": "user",
                    "content": message,
                },
            ],
        )

        return response.choices[0].message.content.strip()

#            messages=[
#                {"role": "system", "content": message}
#           ]


        #        {"role": "system", "content": "You are a helpful assistant."},
#        {"role": "user", "content": "Who won the world series in 2020?"},
 #       {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
  #      {"role": "user", "content": "Where was it played?"}
