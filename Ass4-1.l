%{
#include "y.tab.h"
#include <math.h>
#include <stdlib.h>
%}

%%

[0-9]+(\.[0-9]+)?    { yylval.dval = atof(yytext); return NUMBER; }

sin|cos|sqrt|log     { yylval.sval = strdup(yytext); return FUNC; }

[a-zA-Z][a-zA-Z0-9]* { yylval.sval = strdup(yytext); return VARIABLE; }

"="                  return '=';

"+"                  return '+';
"-"                  return '-';
"*"                  return '*';
"/"                  return '/';
"("                  return '(';
")"                  return ')';

[ \t]                ;

\n                   return '\n';

.                    { printf("Invalid character\n"); }

%%

int yywrap()
{
    return 1;
}
