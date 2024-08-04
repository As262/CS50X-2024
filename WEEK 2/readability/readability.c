#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <math.h>
#include <string.h>

int no_letter(string text);
int no_word(string text);
int no_sent(string text);
int main(void)
{
    string text = get_string("Text: ");
    int i = strlen(text);
    int letters = no_letter(text);
    int words = no_word(text);
    int sent = no_sent(text);

    float L = ((float)letters /(float)words) * 100;
    float s = ((float)sent / (float)words) * 100;
    float index = 0.0588 * L - 0.296 * s - 15.8;

    int sindex = round(index);
    if (sindex > 16)
    {
        printf("Grade 16+\n");
    }
    else if (sindex < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", sindex);
    }
}

int no_letter(string text)
{
int letter = 0;
for (int i = 0, n = strlen(text); i < n; i++)
{
    char c = text[i];
if(isalpha(c) != 0)
{
    letter++;
}
}
return letter;
}

int no_word(string text)
{
    int word = 1;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        char c = text[i];
        if (c == ' ')
        {
            word++;
        }
    }
return word;
}

int no_sent(string text)
{
    int sent = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        char c = text[i];
        if(c == '.' || c == '!' || c == '?' )
        {
            sent++;
        }
    }
    return sent;
}
