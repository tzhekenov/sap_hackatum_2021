import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")


#
# # Opening JSON file
# f = open('input_text.json',) #
#
# # returns JSON object as a dictionary
# data = json.load(f)
# input_text = data["input_text"]
# # Closing file
# f.close() #

#Function which returns trend of the interval
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

#Function which returns trend of the interval
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

#Function which returns combined dictionary of time interval and trend (aka direction of the graph in that interval)
def comb_result(input_text):
    time_interval = extract_time_interval(input_text)
    trend = extract_trend(input_text)
    interval = time_interval.split()
    trend_map = {'decline':-1,'increase':1, 'steep':0}
    return {'trend': trend_map[trend.strip().lower()], 'start_date': int(interval[0]), 'end_date': int(interval[1])}

# # the json file where the output must be stored
# out_file = open("result.json", "w")
# json.dump(comb_result(input_text), out_file)
# out_file.close()
