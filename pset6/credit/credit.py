from cs50 import get_string

def main():

    while True:
        number = get_string("Number: ")

        if len(number) in range(13, 17):
            break
    add = 0

    for i in range(len(number) - 2, -1, -2):
        if int(number[i]) * 2 < 10:
            add += int(number[i]) * 2

        if int(number[i]) * 2 >= 10:
            add += (int(number[i]) * 2) % 10
            add += 1

    for i in range(len(number) - 1, -1, -2):
        add += int(number[i])

    if add % 10 == 0:
        if number[0] == '3' and number[1] in ['4', '7']:
            print("AMEX")

        if number[0] == '5' and number[1] in range('1', '6'):
            print("MASTERCARD")

        if number[0] == '4':
            print("VISA")

    else:
        print("INVALID")


main()