#include<stdio.h>
#include<cs50.h>


int main(void)
{
    printf("Enter value in minutes: ");
    int minutes = get_int();
    int bottles = minutes * 12;
    printf("minutes: %d\n", minutes);
    printf("bottles: %d\n", bottles);
}