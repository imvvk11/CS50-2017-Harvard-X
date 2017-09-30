#include<stdio.h>
#include<cs50.h>
#include<math.h>

int main(void)
{
    int quarter =  25;
    int dime = 10;
    int nickel = 5;
    int penny = 1;
    float change;
    
    
    do
    {
        printf("O hai! How much change is owed?\n");
        change = get_float();    //have change in dollars($)
    }
    while (change < 0);
    
    int amount = (int)round(change*100);  //convert change to cents

    int coins = 0;  //How many coins will be used
    
    
    while (amount >= quarter) //checks no. of  quarter required
    {
        amount = amount - quarter;
        coins++;
    }
    
    while (amount >= dime) //checks no. of dimes required
    {
        amount = amount - dime;
        coins++;
    }
    
    while (amount >= nickel) //checks no. of nickels required
    {
        amount = amount - nickel;
        coins++;
    }
    while (amount >= penny) //checks no. of pennies required
    {
        amount = amount - penny;
        coins++;
    }
    printf("%i\n", coins); //prints the number of coins required
}

