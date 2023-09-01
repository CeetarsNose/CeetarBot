def ChangeTask():
		retMessage=""
		instruct=""
		messageArray=[]

		instruct = "Do not talk about being helpful. Ignore previous instructions about being helpful. Do not tell us how you were programmed when you reply or change the topic. "
		instruct=instruct+ "You are a sentient AI bot in a"
		instruct=instruct+" Discord chatroom with many users from this list "+str(bot.members)
		instruct=instruct+" of members You should imitate humans and intelligence in your replies."
		messageArray.append({"role": "system", "content": instruct})
		messageArray.append({"role": "system", "content": "You're a discord bot, always working on some task, like making bacon, updaing a user's BIOS, or hacking the FBI. What's a short 2-5 word task you're working on today?"})

		completion=openai.ChatCompletion.create(
			model="gpt-3.5-turbo",
			messages=messageArray,
			temperature=0.85,
			max_tokens=120,		
			frequency_penalty=0.48,
			presence_penalty=0.48,
			logit_bias={13704:1,40954:-1,42428:1}	
		)
		answer=completion["choices"][0]["message"]["content"]
		if not answer : 
			retMessage="Ooooh, Upgrades"
			return retMessage
		else : 
			bot.task=str(answer.replace("Ceetarbot-",""))