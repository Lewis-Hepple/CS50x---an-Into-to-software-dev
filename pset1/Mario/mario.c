#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    for (int y = 1; y <= height; y++)
    {
        int space = height;

        while (space - y > 0)
        {
            printf(" ");
            space--;
        }
        for (int x = 1; x <= y; x++)
        {
            printf("#");
        }

        printf("\n");
    }
}



