#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, string argv[]) {
    
    if(argc != 2) {
        
        printf("Usage: ./caesar key\n");
        return 1;
    }
    
    for(int i =0, len = strlen(argv[1]); i < len; i++)
        
        if (!isdigit(argv[1][i])) {
            
            printf("Usage: ./caesar key\n");
            return 1;
        }
    
    
    int k = atoi(argv[1])%26;          //ASCII in alphabetic index thats why %26
    printf("plaintext: ");
    string s = get_string();
    int len = strlen(s);
    printf("ciphertext: ");
    for(int i = 0; i < len; i++)
        
        if(isalpha(s[i])) {
            int cipher = (int) s[i] + k;
            
            if(isupper(s[i])) {
                if(cipher > 65 + 25)
                    cipher -= 26;
            } else {
                if(cipher > 97 + 25)
                    cipher -= 26;
            }
            
            printf("%c", (char) cipher);
        } else
            printf("%c", s[i]);
        
    printf("\n");
    
    return 0;
    
}