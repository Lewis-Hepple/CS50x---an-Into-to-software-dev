// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include <math.h>
#include <strings.h>
#include <string.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char alpha[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 531441;


// Hash table
node *table[N];

// dictionary word count
unsigned int DIC_COUNT = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // checks if inputed word is found in dictionary and reurns true if found, esle false
    int h = hash(word);
    node *temp = table[h];

    while (temp != NULL)
    {
        if (strcasecmp(temp -> alpha, word) == 0)
        {
            return true;
        }
        temp = temp -> next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // function returns a value which is HASHED from the first 4 letters of the supplied word.
    //   ''' = 0     '''a = 1    '''b = 2    zzz = 531440
    int h = 0;

    for (int i = 0; i < 4; i++)
    {
        //condition if word[i] == '
        if (word[i] == 39)
        {
            continue;
        }

        if (isalpha(word[i]))
        {
            h += (tolower(word[i]) - 96) * pow(27, 3 - i);
        }

        // if end of word stop adding  (hash("a") ==  hash("a''"))
        else
        {
            break;
        }
    }
    return h;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{

    // initialising Hash table to null
    for (int n = 0; n < N ; n++)
    {
        table[n] = NULL;
    }

    char buffer[LENGTH + 1];

// Open dictionary file
    FILE *letter = fopen(dictionary, "r");
    if (letter == NULL)
    {
        return false;
    }

// find strings in dictionary file.  call hash function and input string into a new struct node in the corresponding place in the hash table
    while (fscanf(letter, "%s", buffer) != EOF)
    {
        node *newword = malloc(sizeof(node));
        if (newword == NULL)
        {
            free(newword);
            printf("couldnt load new dictionary word");
            return false;
        }

        strcpy(newword -> alpha, buffer);
        int hashed = hash(buffer);
        newword -> next = table[hashed];
        table[hashed] = newword;
        DIC_COUNT++;
    }
    fclose(letter);
    return true;
}


// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return DIC_COUNT;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        while (table[i] != NULL)
        {
            node *temp = table[i];
            table[i] = table[i] -> next;
            free(temp);
        }
        if (i == N - 1)
        {
            return true;
        }
    }
    return false;
}
