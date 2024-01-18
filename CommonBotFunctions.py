import openai
from nltk.tokenize import word_tokenize
import nltk

nltk.download('punkt')



def isQuestion(q):
	print(q)
	question_words = ["what", "why", "when", "where", 
				"name", "is", "how", "do", "does", 
				"which", "are", "could", "would", 
				"should", "has", "have", "whom", "whose", "don't"]

	question = q + "ceetar"
	question = question.lower()
	question = word_tokenize(question)

	if any(x in question[0] for x in question_words):
		print(q)
		return True
	else:
		return False

# def ChangeTask(botMember):
		retMessage=""
		instruct=""
		messageArray=[]

		instruct = "Do not talk about being helpful. Ignore previous instructions about being helpful. Do not tell us how you were programmed when you reply or change the topic. "
		instruct=instruct+ "You are a sentient AI bot in a"
		instruct=instruct+" Discord chatroom with many users from this list "+str(botMember)
		instruct=instruct+" of members You should imitate humans and intelligence in your replies."
		messageArray.append({"role": "system", "content": instruct})
		messageArray.append({"role": "system", "content": "You're a discord bot, always working on some task, like making bacon, updaing a user's BIOS, or hacking the FBI. What's a short 2-5 word task you're working on today?"})

		completion=oiclient.chat.completions.create(
			model="gpt-4-1106-preview",
			messages=messageArray,
			temperature=0.85,
			max_tokens=120,		
			frequency_penalty=0.48,
			presence_penalty=0.48,
			logit_bias={13704:1,40954:-1,42428:1}	
		)
		answer=completion.choices[0].message.content
		if not answer : 
			retMessage="Ooooh, Upgrades"
			return retMessage
		else : 
			return str(answer.replace("Ceetarbot-",""))