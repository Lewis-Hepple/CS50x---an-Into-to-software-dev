#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float change;
    do
    {
        change = get_float("Change owed: ");
    }
    while (change < 0);

    int count = 0;
    int cents = round(change * 100);

    while (cents >= 25)
    {
        cents = cents - 25;
        count++;
    }

    while (cents >= 10)
    {
        cents = cents - 10;
        count++;
    }

    while (cents >= 5)
    {
        cents = cents - 5;
        count++;
    }

    while (cents >= 1)
    {
        cents = cents - 1;
        count ++;
    }
    printf("%i\n", count);
}