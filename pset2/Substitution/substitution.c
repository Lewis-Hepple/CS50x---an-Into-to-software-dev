#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    string PT;
    const int offset = 'A';
    int counter[26] = {0};
    void change(char *T, char *K);

    if (argc != 2)
    {
        printf("Usage:  ./substitution key\n");
        return 1;
    }

    int x = strlen(argv[1]);

   if (x != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    else
    {
        for (int i = 0; i < 26; i++)
        {
            if (isalpha(argv[1][i]) == 0)
            {
                printf("Key must only contain alphabetical letters\n");
                return 1;
            }

            counter[toupper(argv[1][i]) - offset]++;
        }

    }
    for (int k = 0; k < 26; k++)
    {
        if (counter[k] > 1)
        {
            printf("Key cannot have repeating charectors\n");
            return 1;
        }
    }
    PT = get_string("plaintext: ");
    printf("ciphertext: ");
    change(PT, argv[1]);
    return 0;
}

void change(char *T, char *K)
{
    for (int j = 0; j < strlen(T); j++)
    {
        if (isalpha(T[j]) != 0)
        {
            if (isupper(T[j]) != 0)
            {
                int number = T[j] - 'A';
                printf("%C", toupper(K[number]));
            }
            else
            {
                int number = T[j] - 'a';
                printf("%C", tolower(K[number]));
            }
        }
        else
        {
            printf("%C", T[j]);
        }
    }
    printf("\n");
}