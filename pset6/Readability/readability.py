from cs50 import get_string

def main():
    while True:
        text = get_string("Text: ")
        if len(text) > 0:
            break

    lettercount = 0
    wordcount = 1
    sentencecount = 0

    for i in text:
        if i.isalpha() == True:
            lettercount += 1
        if i in ['.', '!', '?']:
            sentencecount += 1
        if i == ' ':
            wordcount += 1

    index = 0.0588 * lettercount * 100 / wordcount - 0.296 * sentencecount * 100 / wordcount - 15.8

    if index < 16 and index > 1:
        print(f"Grade {round(index)}")

    elif index >= 16:
        print(f"Grade 16+")

    elif index <= 1:
        print("Before Grade 1")




main()