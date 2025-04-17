from textblob import TextBlob


def getPolarity(text):
    sen = TextBlob(text).sentiment.polarity
    print(text, " : ", sen)
    return sen


texts = ["We don’t have rides in space ships (yet), but it could be an option to explore, right?", "I absolutely love this product, it's amazing!",
         "This is a terrible experience, I'm really disappointed.", "It's okay, not too bad but not great either.", "Average", "Brilliant", "Ek dam dami"]


for text in texts:
    getPolarity(text)

# getPolarity("Hello")
