from deeppavlov import build_model

model = build_model('en_odqa_infer_wiki', download=True, install=True)
questions = ["What is the name of Darth Vader's son?", 'Who was the first president of France?']
answer, answer_score, answer_place = model(questions)
print(answer)
# from deeppavlov import build_model

# model = build_model('kbqa_cq_en', download=True, install=True)
# questions = ['What is the currency of Sweden?', 'When did the Korean War end?']
# answers, answer_ids, query = model(questions)
# print(answers)
