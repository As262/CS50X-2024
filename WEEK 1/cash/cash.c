#include<stdio.h>
#include <cs50.h>

int calculate_quarters(int i);
int cal_penny(int i);
int cal_nickel(int i);
int cal_dimes(int i);
int main(void)
{
    int i;
    do
    {
        i = get_int("Change owned: ");
    }
    while (i < 0);
    int quarters = calculate_quarters(i);
    i = i - (quarters * 25);
    int dimes = cal_dimes(i);
    i = i - (dimes * 10);
    int nickel = cal_nickel(i);
    i = i - (nickel * 5);
    int penny = cal_penny(i);
    i = i - (penny * 1);
    int n = quarters + dimes + nickel + penny;
    printf(" %i\n", n);
}


int calculate_quarters(int i)
{
    int quarters = 0;
    while (i >= 25)
    {
        quarters++;
        i = i - 25;
    }
    return quarters;
}

int cal_penny(int i)
{
    int penny = 0;
    while (i >= 1)
    {
        penny++;
        i = i - 1;
    }
    return penny;
}

int cal_dimes(int i)
{
    int dimes = 0;
    while (i >= 10)
    {
        dimes++;
        i = i - 10;
    }
    return dimes;
}

int cal_nickel(int i)
{
    int nickel = 0;
    while (i >= 5)
    {
        nickel++;
        i = i - 5;
    }
    return nickel;
}
