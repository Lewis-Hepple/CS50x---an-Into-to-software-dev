#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>


int main(void)
{
    // t = text     w = words       l = letters
    string t = get_string("Text: ");
    int w = 1;
    int l;
    int lc = 0;
    int s = 0;

    for (l = 0; t[l] != '\0'; l++)
    {
        if (t[l] == ' ')
        {
            w++;
        }

        if (isalpha(t[l]) != 0)
        {
            lc++;
        }
        if (t[l] == '.' || t[l] == '?' || t[l] == '!')
        {
            s++;
        }

    }
    float index = 0.0588 * lc / w * 100 - 0.296 * s / w * 100 - 15.8;
    int indexr = round(index);
    if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", indexr);
    }

}
