grammar Modelica;

//  B.2.1 Stored Definition - Within
stored_definition :
    (l_within='within' l_within_name=name? ';')?
    (l_final='final'? l_class_definition=class_definition ';')*
    ;

//  B.2.2 Class Definition
class_definition :
    l_encapsulated='encapsulated'?
    l_prefixes=class_prefixes
    l_specifier=class_specifier
    ;

class_prefixes : 
    l_partial='partial'?
    (
        l_class='class'
        | l_class='model'
        | l_modifier='operator'? l_class='record'
        | l_class='block'
        | l_modifier='expandable'? l_class='connector'
        | l_class='type'
        | l_class='package'
        | l_pure=('pure' | 'impure')? l_modifier='operator'? l_class='function'
        | l_class='operator'
    )
    ;

class_specifier :
    l_ident=IDENT l_string_comment_composition=string_comment composition 'end' IDENT
    | l_ident=IDENT '=' l_base_prefix_name=base_prefix name l_array_subscripts=array_subscripts?
        l_class_modification=class_modification? l_comment=comment
    | l_ident=IDENT '=' l_enumeration='enumeration' '(' (l_enum_list=enum_list? | ':') ')'
        l_comment=comment
    | l_ident=IDENT '=' l_der='der' '(' l_der_f=name ',' l_der_t+=IDENT (',' l_der_t+=IDENT )* ')'
        l_comment=comment
    | l_extends='extends' l_ident=IDENT l_class_modification=class_modification?
        l_comment=string_comment
        l_composition=composition 'end' IDENT
    ;

base_prefix :
    l_type_prefix=type_prefix
    ;

enum_list :
    l_enum+=enumeration_literal (',' l_enum+=enumeration_literal)*
    ;
 
enumeration_literal :
    l_ident=IDENT l_comment=comment
    ;

composition :
    l_elements=element_list
    (
        'public' l_public_elements+=element_list
        | 'protected' l_protected_elements+=element_list
        | l_equations_sections+=equation_section
        | l_algorithm_sections+=algorithm_section
    )*
    ( 'external' l_external_language_specification=language_specification?
        l_external_function_call=external_function_call?
        l_external_annotation=annotation? ':')?
    (l_annotation=annotation ';')?
    ;

language_specification :
    l_string=STRING
    ;

external_function_call :
    (l_component_reference=component_reference '=')?
    l_ident=IDENT '(' l_expression_list=expression_list? ')'
    ;

element_list : 
    (element ';')*
    ;

element :
    import_clause
    | extends_clause
    | 'redeclare'? 'final'? 'inner'? 'outer'?
        ((class_definition | component_clause)
         | 'replaceable' (class_definition | component_clause)
            (constraining_clause comment)?
        );

import_clause :
    'import' ( IDENT '=' name
        | name ('.' ( '*' | '{' import_list '}' ) )? ) comment
    ;

import_list : 
    IDENT (',' import_list)*
    ;

// B.2.3 Extends
extends_clause :
    'extends' name class_modification? annotation?
    ;

constraining_clause:
    'constrainedby' name class_modification?
    ;

// B.2.4 Component Clause
component_clause :
    type_prefix type_specifier array_subscripts? component_list
    ;

type_prefix :
    ('flow' | 'stream')?
    ('discrete' | 'parameter' | 'constant')?
    ('input' | 'output')?
    ;

type_specifier:
    name
    ;

component_list:
    l_components+=component_declaration ( ',' l_components+=component_declaration)*
    ;

component_declaration :
    l_declaration=declaration l_condition=condition_attribute? l_comment=comment
    ;

condition_attribute :
    'if' l_expression=expression
    ;

declaration :
    IDENT l_array_subscripts=array_subscripts? l_modification=modification?
    ;

// B.2.5 Modification
modification :
    class_modification ('=' expression)?
    | '=' expression
    | ':=' expression
    ;

class_modification :
    '(' argument_list? ')'
    ;

argument_list :
    argument (',' argument)*
    ;

argument :
    element_modification_or_replaceable
    | element_redeclaration
    ;

element_modification_or_replaceable:
    'each'?
    'final'?
    (element_modification | element_replaceable)
    ;

element_modification :
    name modification? string_comment
    ;

element_redeclaration :
    'redeclare'
    'each'?
    'final'?
    ( (short_class_definition | component_clause1)
      | element_replaceable)
    ;

element_replaceable:
    'replaceable'
    (short_class_definition | component_clause1)
    constraining_clause?
    ;

component_clause1 :
    type_prefix type_specifier component_declaration1
    ;

component_declaration1 :
    declaration comment
    ;

short_class_definition :
    class_prefixes IDENT '='
    ( base_prefix name array_subscripts?
        class_modification? comment
        | 'enumeration' '(' (enum_list? | ':') ')' comment)
    ;

// B.2.6 Equations

equation_section :
    'initial'? 'equation' (equation ';')*
    ;

algorithm_section :
    'initial'? 'algorithm' (statement ';')*
    ;

equation :
    (
        simple_expression '=' expression
        | if_equation
        | for_equation
        | connect_clause
        | when_equation
        | name function_call_args
    )
    comment
    ;

statement :
    (
        component_reference (':=' expression | function_call_args)
        | '(' output_expression_list ')' ':='
            component_reference function_call_args
        | 'break'
        | 'return'
        | if_statement
        | for_statement
        | while_statement
        | when_statement 
    )
    comment
    ;

if_equation :
    'if' expression 'then'
        (equation ';')*
    ('elseif' expression 'then'
        (equation ';')*
    )*
    ('else'
        (equation ';')*
    )?
    'end' 'if'
    ;

if_statement :
    'if' expression 'then'
        (statement ';')*
    ('elseif' expression 'then'
        (statement ';')*
    )*
    ('else'
        (statement ';')*
    )?
    'end' 'if'
    ;

for_equation :
    'for' for_indices 'loop'
        (equation ';')*
    'end' 'for'
    ;

for_statement :
    'for' for_indices 'loop'
        (statement ';')*
    'end' 'for'
    ;

for_indices :
    for_index (',' for_index)*
    ;

for_index :
    IDENT ('in' expression)?
    ;

while_statement:
    'while' expression 'loop'
        (statement ';')*
    'end' 'while'
    ;

when_equation:
    'when' expression 'then'
        (equation ';')*
    ('elsewhen' expression 'then'
        (equation ';')*
    )*
    'end' 'when'
    ;

when_statement:
    'when' expression 'then'
        (statement ';')*
    ('elsewhen' expression 'then'
        (statement ';')*
    )*
    'end' 'when'
    ;

connect_clause :
    'connect' '(' component_reference ',' component_reference ')'
    ;

// B.2.7 Expressions

expression :
    simple_expression
    | 'if' expression 'then' expression
    ( 'elseif' expression 'then' expression)*
    'else' expression
    ;

simple_expression :
    logical_expression (':' logical_expression
        (':' logical_expression)?)?
    ;

logical_expression :
    logical_term ('or' logical_term)*
    ;

logical_term :
    logical_factor ('and' logical_factor)*
    ;

logical_factor :
    'not'? relation
    ;

relation :
    arithmetic_expression (rel_op arithmetic_expression)?
    ;

rel_op :
    ('<' | '<=' | '>' | '>=' | '==' | '<>')
    ;

arithmetic_expression :
    ops+=add_op?
    terms+=term
    (ops+=add_op terms+=term)*
    ;

add_op :
    ('+' | '-' | '.+' | '.-')
    ;

term :
    factors+=factor
    (ops+=mul_op factors+=factor)*;

mul_op :
    ('*' | '/' | '.*' | './')
    ;

factor :
    base=primary (op=('^' | '.^') exp=primary)?
    ;

primary :
    UNSIGNED_NUMBER     # primary_unsigned_number
    | STRING            # primary_string
    | 'false'           # primary_false
    | 'true'            # primary_true
    | (l_name=name | l_der='der' | l_initial='initial') function_call_args     # primary_function
    | component_reference                               # primary_component_reference
    | '(' output_expression_list ')'                    # primary_output_expression_list
    | '[' expression_list (';' expression_list)* ']'    # primary_expression_list
    | '{' function_arguments '}'                        # primary_function_argument
    | 'end'                                             # primary_end
    ;

name :
    l_name='.'? IDENT ('.' IDENT)*
    ;

component_reference :
    '.'? IDENT array_subscripts? ('.' IDENT array_subscripts?)*
    ;

function_call_args :
    '(' args=function_arguments? ')'
    ;

function_arguments :
    function_argument (',' function_arguments | 'for' for_indices)?
    | named_arguments
    ;

named_arguments : named_argument (',' named_arguments)?
    ;

named_argument : IDENT '=' function_argument
    ;

function_argument :
    'function' name '(' named_arguments? ')'
    | expression
    ;

output_expression_list :
    expression? (',' expression)*
    ;

expression_list :
    expression (',' expression)*
    ;

array_subscripts :
    '[' subscript (',' subscript)* ']'
    ;

subscript :
    ':' | expression
    ;

comment :
    string_comment annotation?
    ;

string_comment :
    (STRING ('+' STRING)*)?
    ;

annotation :
    'annotation' class_modification
    ;

IDENT : NONDIGIT ( DIGIT | NONDIGIT )* | Q_IDENT;
STRING :
    '\"' (S_CHAR|S_ESCAPE)* '\"';
UNSIGNED_NUMBER : UNSIGNED_INTEGER  ( '.' UNSIGNED_NUMBER? )* ( [eE] [+-]? UNSIGNED_INTEGER)?;

fragment Q_IDENT : '\'' ( Q_CHAR | S_ESCAPE)+;
fragment NONDIGIT : [_a-zA-Z];
fragment S_CHAR : [A-Za-z\u0000-\u00FF];
fragment Q_CHAR : NONDIGIT | DIGIT | [!#$%&()*+,-./:;<>=?@[\]^{}|! ];
fragment S_ESCAPE : [\'\"\?\\\a\b\f\n\r\t\v];
fragment DIGIT :  [0-9];
fragment UNSIGNED_INTEGER : DIGIT+;

COMMENT :
    ('/' '/' .*? '\n' | '/*' .*? '*/') -> channel(HIDDEN)
    ;

WS  :   [ \r\n\t]+ -> skip ; // toss out whitespace

// vi:ts=4:sw=4:expandtab:
