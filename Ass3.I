%{
#include <stdio.h>
#include <string.h>
%}

/* Define patterns */
NOUN      Ram|Shyam|dog|cat|food|apple
VERB      eat|eats|run|runs|play|plays
ADJ       good|bad|tasty|big|small
ADV       quickly|slowly|silently
PREP      in|on|at|under|over

%%

{NOUN}     { printf("%s -> Noun\n", yytext); }
{VERB}     { printf("%s -> Verb\n", yytext); }
{ADJ}      { printf("%s -> Adjective\n", yytext); }
{ADV}      { printf("%s -> Adverb\n", yytext); }
{PREP}     { printf("%s -> Preposition\n", yytext); }

[a-zA-Z]+  { printf("%s -> Unknown\n", yytext); }
[ \t\n]+   ;   /* Ignore spaces */

.          ;   /* Ignore other characters */

%%

int main() {
    printf("Enter a sentence:\n");
    yylex();
    return 0;
}

int yywrap() {
    return 1;
}



lex file-name.l
gcc lex.yy.c -o file-name -ll
./file-name

input sent : Ram eats tasty food 
