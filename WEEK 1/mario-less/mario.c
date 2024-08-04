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
    while  (n < 1 );
        print_row(n);

}

void print_row(int n )
{
    for (int i = 0; i < n; i++)
    {
    for (int j = n - i; j > 1; j--)
    {
        printf(" ");
    }
    for (int k = 0; k <= i; k++)
    {
        printf("#");
    }
    printf("\n");
    }
}
