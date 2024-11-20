# Lexical Conventions

Lexical conventions define the basic syntax rules for writing code in a programming language. They specify how characters are combined to form tokens, which are the smallest units of meaning.

!!! tip
    These conventions ensure that the code is readable and unambiguous, making it easier for both humans and tools to understand and process.

## Overview

This section describes the following:

  - Lexical tokens (white space, comments, operators)
  - Integer, real, string, array, structure, and time literals
  - Built-in method calls
  - Attributes

## Lexical tokens

SystemVerilog source text files shall be a stream of lexical tokens. A lexical token shall consist of one or more characters. The layout of tokens in a source file shall be free format; that is, spaces and newline characters shall not be syntactically significant other than being token separators, except for escaped identifiers.

!!! abstract "Defination"
    A lexical token is the smallest unit of text in source code that has a meaning in the language.

The types of lexical tokens in the language are as follows:

  - **White space** 
  - **Comment** 
  - **Operator**
  - **Number** 
  - **String literal** 
  - **Identifier** 
  - **Keyword**

Sure, here's the information in Markdown format:

### White Space

White space includes characters like spaces, tabs, newlines, formfeeds, and the end of file. These characters are generally ignored except when they are used to separate other lexical tokens. However, in string literals, spaces and tabs are considered significant characters.

### Comments

SystemVerilog supports two types of comments:

  - **One-line comments**: Start with `//` and end with a newline character.
  
  - **Block comments**: Start with `/*` and end with `*/`. 
  
  Block comments cannot be nested. Within block comments, the `//` token has no special meaning, and within one-line comments, the `/*` and `*/` tokens have no special meaning.

### Operators

Operators in SystemVerilog can be single, double, or triple-character sequences used in expressions. 
  
  - **Unary operators**: Appear to the left of their operand.
  - **Binary operators**: Appear between their operands.
  - **Conditional operators**: Have two operator characters that separate three operands.

### Identifiers, keywords, and system names

#### Identifiers in Programming

An identifier uniquely names an object for referencing, there are two types : **simple identifiers** and **escaped identifiers**.

##### Simple Identifiers

  - Sequence of letters, digits, `$`, and `_`.
  - **Cannot** be a keyword.
  - **Cannot** start with a digit or `$`.
  - **Case sensitive**.

!!! example "Examples"
    - `shiftreg_a`
    - `busa_index`
    - `error_condition`
    - `merge_ab`
    - `_bus3`
    - `n$657`

!!! note
     Maximum length is 1024 characters. Exceeding this limit will report an error.

##### Escaped Identifiers

  - Begin with a backslash (`\`), end with whitespace.
  - Allow inclusion of printable ASCII characters (decimal values 33 through 126).
  - Treated same as nonescaped identifiers, except for escaped keywords.

!!! example "Examples"
    - `\busa+index`
    - `\-clock`
    - `\***error-condition***`
    - `\net1/\net2`
    - `\{a,b}`
    - `\a*(b+c)`
    - `\net`  

### Keywords

Keywords are predefined nonescaped identifiers that are used to define the language constructs. A SystemVerilog keyword preceded by an escape (backslash) character is not interpreted as a keyword. All keywords are defined in lowercase only. 

!!! example "Examples"
    `"net"` is a keyword.

    `"\net "` becomes a user-defined identifier.

## System tasks and system functions

The dollar sign `$` introduces a language construct that enables development of user-defined system tasks and system functions. 

System constructs are not design semantics, but refer to simulator functionality. A name following the `$` is interpreted as a system task or a system function.

SystemVerilog defines a standard set of system tasks and system functions.

!!! examples
    ```sv
    $finish;

    $display ("display a message");
    ```

## Compiler directives 

Compiler directives are special instructions provided in the source code that direct the compiler to perform specific actions or modify its behavior during the compilation process.

The ` character (the ASCII value 0x60, called grave accent) introduces a language construct used to implement compiler directives. 

Compiler directives allow programmers to control the compilation environment and make the code more adaptable to different conditions and configurations.

**Syntax** ``define wordsize 32`

### Compiler Directives and Their Effects

**Immediate Effect**:
  
  - When the compiler encounters a compiler directive, it immediately takes effect.

  - The directive remains active for the entire compilation unit unless overridden by another directive.

**Scope of Influence**:

  - A compiler directive in one file can control the behavior in multiple description files.

  - However, it does **not** affect other compilation units.

!!! Note "Key Points"

    1. **Immediate Activation**: The moment a compiler reads a directive, it applies the specified behavior.
    2. **Duration**: This behavior lasts throughout the compilation unit unless another directive changes it.
    3. **Cross-File Control**: One directive can influence multiple files within the same compilation unit.
    4. **Independence of Compilation Units**: Directives in one compilation unit do not impact other units.

## Numbers

In SystemVerilog, constant numbers can be specified in various formats, each serving different purposes and providing flexibility in representing numerical values.

### Decimal Numbers
- **Format**: A sequence of digits without any prefix.
- **Example**: `123` represents a decimal number.
- **Usage**: Commonly used for general numerical values in code.

### Binary Numbers
- **Format**: Prefixed with `b` or `B` followed by a sequence of binary digits (0 or 1).
- **Example**: `4'b1010` represents a 4-bit binary number.
- **Usage**: Useful for representing values in digital logic design, where binary representation is essential.

### Octal Numbers
- **Format**: Prefixed with `o` or `O` followed by a sequence of octal digits (0-7).
- **Example**: `8'o17` represents an octal number.
- **Usage**: Less common but can be used in specific applications where octal representation is preferred.

### Hexadecimal Numbers
- **Format**: Prefixed with `h` or `H` followed by a sequence of hexadecimal digits (0-9, A-F).
- **Example**: `16'h1A3F` represents a hexadecimal number.
- **Usage**: Widely used in digital design and programming for representing large binary values compactly.

### Real Numbers
- **Format**: Can be written in decimal notation with a fractional part or in scientific notation.
- **Examples**: `3.14` (decimal notation) or `1.23e4` (scientific notation).
- **Usage**: Used for representing floating-point values in simulations and calculations.

!!! example

    ```verilog
    module number_examples;
      // Decimal number
      int decimal_num = 123;

      // Binary number
      reg [3:0] binary_num = 4'b1010;

      // Octal number
      int octal_num = 8'o17;

      // Hexadecimal number
      int hex_num = 16'h1A3F;

      // Real number
      real real_num = 3.14;
      real sci_num = 1.23e4;
    endmodule
    ```

These conventions ensure that numbers are represented clearly and unambiguously in the code, making it easier for both humans and tools to understand and process them.

## Casting

Casting, or type casting, is the process of converting a variable from one data type to another. This is often necessary when performing operations on variables of different types.

!!! example

    ```sv
    int i = 42;
    real r = real'(i); // Static cast from int to real

    real r = 42.5;
    int i = int'(r); // Static cast from real to int

    int i = 42;
    bit [31:0] b = bit'(i); // Static cast from int to bit

    bit [31:0] b = 32'h2A;
    int i = int'(b); // Static cast from bit to int

    int i = 42;
    shortint s = shortint'(i); // Static cast from int to shortint

    shortint s = 42;
    int i = int'(s); // Static cast from shortint to int

    int i = 42;
    longint l = longint'(i); // Static cast from int to longint

    longint l = 42;
    int i = int'(l); // Static cast from longint to int

    int i = 42;
    byte b = byte'(i); // Static cast from int to byte

    byte b = 42;
    int i = int'(b); // Static cast from byte to int

    int i = 42;
    shortreal sr = shortreal'(i); // Static cast from int to shortreal

    shortreal sr = 42.5;
    int i = int'(sr); // Static cast from shortreal to int
    ```

These examples demonstrate how to cast between different number data types in SystemVerilog. 

Each cast ensures that the variable is converted to the desired type, allowing for proper operations and manipulations.

## String literals 

A string literal is a sequence of characters enclosed by a single pair of double quotes `""`, called a quoted string, or a triple pair of double quotes `"""..."""`, called a triple-quoted string. There is no predefined limit to the length of a string literal.

Within a string literal, nonprintable and other special characters can be represented by a string escape sequence. 

!!! note
    Support for nonescaped nonprintable ASCII characters is implementation dependent.

!!! example

    ```sv
    $display("Humpty Dumpty sat on a wall. \
      Humpty Dumpty had a great fall.");

    print: Humpty Dumpty sat on a wall. Humpty Dumpty had a great fall.

    $display("Humpty Dumpty sat on a wall.\n\
      Humpty Dumpty had a great fall.");
    
    print: Humpty Dumpty sat on a wall.
           Humpty Dumpty had a great fall.
    ```

Triple-quoted string literals differ from quoted string literals in two ways:

  - Triple-quoted string literals allow for a newline character to be inserted directly without using the `\n` escape sequence.
  
  - Triple-quoted string literals allow for a " character to be inserted directly without using the \" escape sequence.

In all other ways, the two constructs are identical. This means that an escaped newline in a triple-quoted string literal is treated exactly like an escaped newline in a single-quoted string literal.

!!! example

    ```sv
    $display("""Humpty Dumpty sat on a "wall".
      Humpty Dumpty had a great fall. """);
    
    prints: Humpty Dumpty sat on a "wall".
            Humpty Dumpty had a great fall.
    
    $display("""Humpty Dumpty sat on a wall. \
      Humpty Dumpty had a great fall. """);
    
    prints: Humpty Dumpty sat on a wall. Humpty Dumpty had a great fall.
    
    $display("""Humpty Dumpty \n sat on a wall. \n
      Humpty Dumpty had a great fall. """);
    
    prints: Humpty Dumpty
            sat on a wall.
            Humpty Dumpty had a great fall.
    ```

### Special characters in strings

Certain ASCII characters can only be represented in string literals using an escape sequence.

| Escape sequence | Character produced by escape sequence  |                                            
| :-------------: | :------------------------------------  |                                            
| \n              | Newline character                      |                                            
| \t              | Tab character                          |                      
| \\              | \ character                            |                   
| \"              | " character                            |                
| \v              | Vertical tab                           |                
| \f              | Form feed                              |                 
| \a              | Bell                                   |               
| \ddd            | A character specified in 1 to 3 octal_digits. If fewer than three digits are used, the following character shall not be an octal_digit. Implementations may issue an error if the character represented is greater than \377. It shall be illegal for an octal_digit in an escape sequence to be an x_digit or a z_digit. |          
| \xdd            | A character specified in 1 to 2 hex_digits. If only one digit is used, the following character shall not be a hex_digit. It shall be illegal for a hex_digit in an escape sequence to be an x_digit or a z_digit. |          

## Attributes


A mechanism is included for specifying properties about objects, statements, and groups of statements in the SystemVerilog source that can be used by various tools, including simulators, to control the operation or behavior of the tool. These properties are referred to as attributes.

An attribute_instance can appear in the SystemVerilog description as a prefix attached to a declaration, a module item, a statement, or a port connection. It can appear as a suffix to an operator or a function name in an expression.

The default type of an attribute with no value is bit, with a value of 1. Otherwise, the attribute takes the type of the expression. 

If the same attribute name is defined more than once for the same language element, the last attribute value shall be used, and a tool can issue a warning that a duplicate attribute specification has occurred.

Nesting of attribute instances is disallowed. It shall be illegal to specify the value of an attribute with a constant expression that contains an attribute instance.

`(* attr1 = (* attr2 = value *) *)  // Illegal: Nested attribute instances`

## Built-in methods

SystemVerilog uses a C++-like class method calling syntax, in which a subroutine is called using the dot notation (.):

`object.task_or_function()`

In general, a built-in method is preferred over a system task when a particular functionality applies to all data types or when it applies to a specific data type.

`dynamic_array.size, associative_array.num, and string.len`

These are all similar concepts, but they represent different things. A dynamic array has a size, an associative array contains a given number of items, and a string has a given length. Using the same system task, such as `$size`, for all of them would be less clear and intuitive.

When a subroutine built-in method call specifies no arguments, the empty parentheses, (), following the subroutine name are optional. This is also true for subroutines that require arguments, when all arguments have defaults specified. For a method, this rule allows simple calls to appear as properties of the object or built-in type. 

!!! note
    The exception to this rule when using a built-in method call as an implicit variable, wherein the parentheses are always required even when empty.

