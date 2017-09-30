#include<stdio.h>
#include<cs50.h>


int main(void)
{
    int n;
    do
    {
        printf("Height: \n");
        n = get_int();
    }
    while (n < 0 || n > 23);

    for (int i =0; i < n; i ++)
    {
        for (int j = 0; j < n - i - 1; j ++)
        {
            printf(" ");
        }

        for (int k = 0; k < 2 + i; k ++)
        {
            printf("#");
        }

        printf("\n");
    }

}

