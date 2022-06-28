from textblob import TextBlob

def analysize_comment(comment_text):
    return TextBlob(comment_text).polarity
