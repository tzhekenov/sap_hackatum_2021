import json
import os
import openai


openai.api_key = os.getenv('OPENAI_KEY')


# Function which returns trend of the interval
def extract_trend(input_text):
    base = "Extract the trend up or down:\n\n"
    request = "trend is: "
    prompt = base+input_text+request
    response1 = openai.Completion.create(
      engine="davinci-instruct-beta",
      prompt=prompt,
      temperature=0,
      max_tokens=64,
      top_p=1,
      frequency_penalty=2, #50
      presence_penalty=0
    )
    trend = response1['choices'][0]['text']
    return trend


# Function which returns trend of the interval
def extract_time_interval(input_text):
    base = "Extract the start and end dates: \n\n"
    request = "the start and end dates are: "
    prompt = base+input_text+request
    response1 = openai.Completion.create(
      engine="davinci-instruct-beta",
      prompt=prompt,
      temperature=0,
      max_tokens=64,
      top_p=1,
      frequency_penalty=2, #50
      presence_penalty=0
    )
    dates = response1['choices'][0]['text']
    return dates


# Function which returns combined dictionary of time interval and trend (aka direction of the graph in that interval)
def comb_result(input_text):
    time_interval = extract_time_interval(input_text)
    trend = extract_trend(input_text)
    interval = time_interval.split()

    return {'trend': get_trend(trend), 'start_date': int(interval[0]), 'end_date': int(interval[1])}


def get_trend(trend_message):
    down_messages = ['down', 'decreas', 'fall']
    up_messages = ['up', 'increa', 'rise', 'ris']
    for d in down_messages:
        if d in trend_message.lower():
            return -1
    for d in up_messages:
        if d in trend_message.lower():
            return 1
    return 0

# # the json file where the output must be stored
# out_file = open("result.json", "w")
# json.dump(comb_result(input_text), out_file)
# out_file.close()


class DataVisualizer:

    @staticmethod
    def visualize_time_series(data, text: str, timeout: int = 2):
        # 1) get sentiment
        # 2) build graph from data
        # 3) generate visuals

        trend = comb_result(text)
        left, r = None, None
        for i in range(len(data[0])):
            if data[0][i] == trend['start_date'] and left is None:
                left = i
            if data[0][i] == trend['end_date']:
                r = i
        d = {
            'original': {
                'x': data[0],
                'y': data[1],
            },
            'left_index': left,
            'right_index': r,
            'timeout': timeout,
            'text': text
        }
        with open('data.json', 'w') as f:
            json.dump(d, f)
