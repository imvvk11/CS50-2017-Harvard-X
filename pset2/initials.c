#include<stdio.h>
#include<cs50.h>
#include<string.h>
#include<ctype.h>


int main(void)
{
    printf("Provide your full name: \n");
    string s = get_string();
    printf("%c", toupper(s[0]));
    if (s != NULL) {
        for(int i = 1, len = strlen(s); i < len; i++)
        if(s[i-1] == ' ')
        {
            printf("%c", toupper(s[i]));
        }
        printf("\n");

    }
    
}