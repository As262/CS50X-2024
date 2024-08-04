#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int sum_all(string word);
int PNT[] = { 1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10 };
int main(void)
{
 string word1 = get_string("Player 1: ");
 string word2 = get_string("Player 2: ");

 int score1 = sum_all(word1);
 int score2 = sum_all(word2);

 if ( score1 > score2 )
 {
    printf("Player 1 Wins!\n");
 }
 else if ( score1 < score2 )
{
    printf("Player 2 Wins!\n");
 }
 else
 {
    printf("Tie!\n");
 }
}

int sum_all(string word)
{
    int score = 0;
    for(int i = 0, length = strlen(word); i < length; i++)
    {
        if (isupper(word[i]))
        {
            score += PNT[word[i] - 'A'];
        }
        else if (islower(word[i]))
        {
            score += PNT[word[i] - 'a'];
        }
    }
    return score;
}
