#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t  BYTE;


int main(int argc, char *argv[])
{
    // Input error checking
    if (argc != 2)
    {
        printf("usage ./recover DATA.raw\n");
        return 1;
    }

    FILE *file = fopen(argv[1], "r");

    if (file == NULL)
    {
        printf("couldn't read DATA\n");
        return 1;
    }

    // allocating memory for buffer
    BYTE *buffer;
    buffer = malloc(512);

    // initialising checks
    BYTE header[3] = {0xff, 0xd8, 0xff};
    char filename[8];
    int i = -1;
    FILE *destination;

// itterating over entire file and making jpgs
    while (fread(buffer, 1, 512, file) == 512)
    {
        if(buffer[0] == header[0] && buffer[1] == header[1] && buffer[2] == header[2] && (buffer[3] & 0xf0) == 0xe0)
        {
            if (i != -1)
            {
                fclose(destination);
            }

            i++;
            sprintf(filename, "%03i.jpg", i);
            destination = fopen(filename, "w");

            if (destination == NULL)
            {
                fclose(destination);
                fclose(file);
                free(buffer);
                printf("Unable to create image file %s", filename);
                return 2;
            }
        }

        if (i == -1)
            {
            continue;
            }

        fwrite(buffer, 1, 512, destination);

    }
    
    fclose(file);
    fclose(destination);
    free(buffer);
    return 0;
}