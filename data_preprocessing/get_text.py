import re


def data_to_text(df):
	text_serie = data['text'].dropna()
	text_serie.apply(lambda x: x.rstrip())
	text = text_serie.to_string()
	text.lower()
	regex = re.compile('[^а-яА-я]')
	text = regex.sub(' ', text)
	text = re.sub(" +", " ", text)

	reply_text_serie = data['reply.text'].dropna()
	reply_text_serie.apply(lambda x: x.rstrip())
	reply_text = reply_text_serie.to_string()
	reply_text.lower()
	regex = re.compile('[^а-яА-я]')
	reply_text = regex.sub(' ', reply_text)
	reply_text = re.sub(" +", " ", reply_text)

	return reply_text + text

