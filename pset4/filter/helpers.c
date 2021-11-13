#include "helpers.h"
#include "math.h"
#include "stdio.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int grey = (int)nearbyint(((float)image[i][j].rgbtRed + (float)image[i][j].rgbtBlue + (float)image[i][j].rgbtGreen) / 3);
            image[i][j].rgbtRed = grey;
            image[i][j].rgbtBlue = grey;
            image[i][j].rgbtGreen = grey;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{

    for (int i = 0; i < height; i++)
    {
        RGBTRIPLE temp[1][1] = {0};
        int count = 0;
        do
        {
            temp[0][0].rgbtRed = image[i][count].rgbtRed;
            image[i][count].rgbtRed = image[i][width - 1 - count].rgbtRed;
            image[i][width - 1 - count].rgbtRed = temp[0][0].rgbtRed;

            temp[0][0].rgbtBlue = image[i][count].rgbtBlue;
            image[i][count].rgbtBlue = image[i][width - 1 - count].rgbtBlue;
            image[i][width - 1 - count].rgbtBlue = temp[0][0].rgbtBlue;

            temp[0][0].rgbtGreen = image[i][count].rgbtGreen;
            image[i][count].rgbtGreen = image[i][width - 1 - count].rgbtGreen;
            image[i][width - 1 - count].rgbtGreen = temp[0][0].rgbtGreen;

            count++;

        }
        while (count < width - count);
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int count = 0;
            int red = 0;
            int blue = 0;
            int green = 0;

            for (int k = -1; k < 2; k++)
            {
                for (int l = -1; l < 2; l++)
                {
                    if (i + k >= 0 && j + l >= 0 && i + k < height && j + l < width)
                    {
                        red += copy[i + k][j + l].rgbtRed;
                        blue +=  copy[i + k][j + l].rgbtBlue;
                        green += copy[i + k][j + l].rgbtGreen;
                        count++;

                    }
                }
            }
            image[i][j].rgbtRed = (int)round((float)red / count);
            image[i][j].rgbtBlue = (int)round((float)blue / count);
            image[i][j].rgbtGreen = (int)round((float)green / count);
        }
    }
    void free(void *copy);
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int gxred = 0;
            int gyred = 0;
            int gxblue = 0;
            int gyblue = 0;
            int gxgreen = 0;
            int gygreen = 0;

            for (int k = -1; k < 2; k++)
            {
                for (int l = -1; l < 2; l++)
                {
                    if (i + k >= 0 && j + l >= 0 && i + k < height && j + l < width)
                    {
                        if (k == 0 || l == 0)
                        {
                            gxred += copy[i + k][j + l].rgbtRed * 2 * l;
                            gxblue += copy[i + k][j + l].rgbtBlue * 2 * l;
                            gxgreen += copy[i + k][j + l].rgbtGreen * 2 * l;
                            gyblue += copy[i + k][j + l].rgbtBlue * 2 * k;
                            gyred += copy[i + k][j + l].rgbtRed * 2 * k;
                            gygreen += copy[i + k][j + l].rgbtGreen * 2 * k;
                        }
                        else
                        {
                            gxred += copy[i + k][j + l].rgbtRed * l;
                            gyred += copy[i + k][j + l].rgbtRed * k;
                            gxblue += copy[i + k][j + l].rgbtBlue * l;
                            gyblue += copy[i + k][j + l].rgbtBlue * k;
                            gxgreen += copy[i + k][j + l].rgbtGreen * l;
                            gygreen += copy[i + k][j + l].rgbtGreen * k;
                        }
                    }

                }
            }


            int red = (int)round(sqrt(gxred * gxred + gyred * gyred));
            int blue = (int)round(sqrt(gxblue * gxblue + gyblue * gyblue));
            int green = (int)round(sqrt(gxgreen * gxgreen + gygreen * gygreen));

            if (red > 255)
            {
                red = 255;
            }
            if (red < 0)
            {
                red = 0;
            }
            if (blue > 255)
            {
                blue = 255;
            }
            if (blue < 0)
            {
                blue = 0;
            }
            if (green > 255)
            {
                green = 255;
            }
            if (green < 0)
            {
                green = 0;
            }

            image[i][j].rgbtRed = red;
            image[i][j].rgbtBlue = blue;
            image[i][j].rgbtGreen = green;
        }
    }

    void free(void *copy);
    return;
}
