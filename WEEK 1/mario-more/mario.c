#include<stdio.h>
#include<cs50.h>

void print_row(int n );

int main(void)
{
    int n;
    do
    {
       n = get_int("Height: ");
    }
    while  (n < 1 || n > 8);
        print_row(n);

}

void print_row(int n )
{
     for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            if (i + j < n - 1)
                printf(" ");
            else
                printf("#");
        }
            printf("  ");
            for (int j = 0; j < n; j++)
                {
                    if (n - i < j + 2)
                        printf("#");
                }
                printf("\n");
    }
}

