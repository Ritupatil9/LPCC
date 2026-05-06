%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

void yyerror(char *s);
int yylex();

typedef struct
{
    char name[20];
    double value;
} variable;

variable vars[100];
int var_count = 0;

double get_var(char *name)
{
    for(int i=0; i<var_count; i++)
    {
        if(strcmp(vars[i].name, name) == 0)
            return vars[i].value;
    }

    printf("Undefined variable %s\n", name);
    return 0;
}

void set_var(char *name, double value)
{
    for(int i=0; i<var_count; i++)
    {
        if(strcmp(vars[i].name, name) == 0)
        {
            vars[i].value = value;
            return;
        }
    }

    strcpy(vars[var_count].name, name);
    vars[var_count].value = value;
    var_count++;
}

%}

%union
{
    double dval;
    char *sval;
}

%token <dval> NUMBER
%token <sval> VARIABLE FUNC

%type <dval> expr

%left '+' '-'
%left '*' '/'

%%

input:
      | input line
      ;

line:
        expr '\n'
        {
            printf("Result = %lf\n", $1);
        }

      | VARIABLE '=' expr '\n'
        {
            set_var($1, $3);
            printf("%s = %lf\n", $1, $3);
        }
      ;

expr:
        NUMBER
        {
            $$ = $1;
        }

      | VARIABLE
        {
            $$ = get_var($1);
        }

      | expr '+' expr
        {
            $$ = $1 + $3;
        }

      | expr '-' expr
        {
            $$ = $1 - $3;
        }

      | expr '*' expr
        {
            $$ = $1 * $3;
        }

      | expr '/' expr
        {
            $$ = $1 / $3;
        }

      | '(' expr ')'
        {
            $$ = $2;
        }

      | FUNC '(' expr ')'
        {
            if(strcmp($1, "sin") == 0)
                $$ = sin($3);

            else if(strcmp($1, "cos") == 0)
                $$ = cos($3);

            else if(strcmp($1, "sqrt") == 0)
                $$ = sqrt($3);

            else if(strcmp($1, "log") == 0)
                $$ = log($3);
        }
      ;

%%

void yyerror(char *s)
{
    printf("Error: %s\n", s);
}

int main()
{
    printf("Enter expressions:\n");
    yyparse();
    return 0;
}


yacc -d calc.y
lex calc.l
gcc y.tab.c lex.yy.c -lm
./a.out
