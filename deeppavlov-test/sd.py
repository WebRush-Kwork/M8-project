import requests

def deep_pavlov_answer(question):
	try:
			API_URL = "https://7038.deeppavlov.ai/model"
			data = {"question_raw": [ question ]}
			res = requests.post(API_URL, json=data).json()
			res = res[0][0]
	except:
			res = "I don't know how to help"
	return res

print(deep_pavlov_answer('who is the first president of the US?'))
