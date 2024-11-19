# Design and verification building blocks

## Overview

This section outlines the following:

 - The purpose of modules, programs, interfaces, checkers, and primitives
 - An overview of subroutines
 - An overview of packages
 - An overview of configurations
 - An overview of design hierarchy
 - Definition of compilation and elaboration
 - Declaration name spaces
 - Simulation time, time units, and time precision

This section defines several key SystemVerilog terms and concepts used throughout this document. It also provides an overview of the purpose and usage of modeling blocks used to represent a hardware design and its verification environment.

---

## Design elements

A design element is a SystemVerilog module, program, interface, checker, package, primitive or configuration. 

These constructs are introduced by the keywords module, program, interface, checker, package, primitive, and config respectively.

`Design elements are the primary building blocks used to model and build up a design and verification environment.` 

### Modules

The basic building block in SystemVerilog is the module, enclosed between the keywords `module` and `endmodule` 

Modules are primarily used to represent design blocks, but can also serve as containers for verification code and interconnections between verification blocks and design blocks. 

Some of the constructs that modules can contain include the following

 - Ports, with port declarations
 - Data declarations, such as nets, variables, structures, and unions
 - Constant declarations
 - User-defined type definitions
 - Class definitions
 - Imports of declarations from packages
 - Subroutine definitions
 - Instantiations of other modules, programs, interfaces, checkers, and primitives
 - Instantiations of class objects
 - Continuous assignments
 - Procedural blocks
 - Generate blocks
 - Specify blocks

```SystemVerilog
module mux2to1 (
  input wire a, b, sel, // combined port and type declaration
  output logic y
);
  always_comb begin 
    if (sel) y = a;
    else
  end 
  
  y = b;

endmodule : mux2to1
```

### Programs

The program building block is enclosed between the keywords `program`... `endprogram`

This construct is provided for modeling the testbench environment. The module construct works well for the description of hardware.

The program block serves the following three basic purposes :

- It provides an entry point to the execution of testbenches.
- It creates a scope that encapsulates program-wide data, tasks, and functions.
- It provides a syntactic context that specifies scheduling in the reactive region set.

The program construct serves as a clear separator between design and testbench, and, more importantly, it specifies specialized simulation execution semantics. Together with clocking blocks, the program construct provides for race-free interaction between the design and the testbench and enables cycle-level and transaction-level abstractions.

A program block can contain data declarations, class definitions, subroutine definitions, object instances, and one or more initial or final procedures. It cannot contain always procedures, primitive instances, module instances, interface instances, or other program instances.

```SystemVerilog
program test (input clk, input [16:1] addr, inout [7:0] data);
  initial begin
    ...
  end
endprogram 
```

### Interface

The interface construct, defined between the `interface` and `endinterface` keywords, encapsulates communication between design blocks and between design and verification blocks. This allows for a smooth transition from abstract system-level design to lower-level register transfer and structural views. By encapsulating communication, the interface construct also promotes design reuse.

At its core, an interface is a named collection of nets or variables. It is instantiated in a design and can be connected to the interface ports of other instantiated modules, interfaces, and programs.

An interface can be accessed through a port as a single entity, with its component nets or variables referenced as needed. A significant portion of a design often consists of port lists and port connection lists, which are repetitive. Replacing a group of names with a single name can significantly reduce the size of a description and improve maintainability.

The interface's power lies in its ability to encapsulate both functionality and connectivity, making it similar to a class template at its highest level. An interface can include `parameters`, `constants`, `variables`, `functions`, and `tasks`. The types of elements in an interface can be `declared` or passed in as `parameters`.

``` SystemVerilog
interface simple_bus(input logic clk); // Define the interface
  logic req, gnt;
  logic [7:0] addr, data;
  logic [1:0] mode; 
  logic start, rdy;
endinterface: simple_bus

module memMod(simple_bus a); // simple_bus interface port
  logic avail;
  
  // When memMod is instantiated in module top, a.req is the req
  // signal in the sb_intf instance of the 'simple_bus' interface
  
  always @(posedge a.clk) a.gnt <= a.req & avail;
endmodule

module cpuMod(simple_bus b); // simple_bus interface port
  ...
endmodule 

module top;
  logic clk = 0;
  simple_bus sb_intf(.clk(clk)); // Instantiate the interface
  memMod mem(.a(sb_intf)); // Connect interface to module instance
  cpuMod cpu(.b(sb_intf)); // Connect interface to module instance
endmodule
```

### Checkers 

The checker construct, enclosed by the keywords `checker` ... `endchecker`, represents a verification block encapsulating assertions along with the modeling code. The intended use of checkers is to serve as verification library units or as building blocks for creating abstract auxiliary models used in formal verification.

### Primitives 

The primitive building block is used to represent low-level logic gates and switches. SystemVerilog includes a number of built-in primitive types. Designers can supplement the built-in primitives with user-defined primitives (UDPs). A UDP is enclosed between the keywords `primitive` ... `endprimitive`. 

The built-in and UDP constructs allow modeling timing-accurate digital circuits, commonly referred to as gate-level models.

### Subroutines 

Subroutines provide a mechanism to encapsulate executable code that can be invoked from one or more places. There are two forms of subroutines, tasks and functions.

A task is called as a statement. A task can have any number of input, output, inout, and ref arguments, but does not return a value. Tasks can block simulation time during execution. That is, the task exit can occur at a later simulation time than when the task was called.

A function can return a value or can be defined as a void function, which does not return a value. A nonvoid function call is used as an operand within an expression. A void function is called as a statement. A function can have input, output, inout, and ref arguments. Functions execute without blocking simulation time, but can fork off processes that do block time.

### Packages 

Modules, interfaces, programs, and checkers provide a local name space for declarations. Identifiers declared within a module, interface, program, or checker are local to that scope, and do not affect or conflict with declarations in other building blocks.

Packages provide a declaration space, which can be shared by other building blocks. Package declarations can be imported into other building blocks, including other packages. A package is defined between the keywords `package` ... `endpackage`. 

```SystemVerilog
package ComplexPkg;
  typedef struct {
    shortreal i, r;
  } Complex;

  function Complex add(Complex a, b);
    add.r = a.r + b.r;
    add.i = a.i + b.i;
  endfunction 

  function Complex mul(Complex a, b);
    mul.r = (a.r * b.r) - (a.i * b.i);
    mul.i = (a.r * b.i) + (a.i * b.r);
  endfunction 
endpackage : ComplexPkg
```

### Configurations 

SystemVerilog provides the ability to specify design configurations, which specify the binding information of module instances to specific SystemVerilog source code.

Configurations utilize libraries. A library is a collection of `modules`, `interfaces`, `programs`, `checkers`, `primitives`, `packages`, and other configurations. Separate library map files specify the source code location for the cells contained within the libraries.

### Hierarchy 

The basic building blocks of modules, programs, interfaces, checkers, and primitives are used to build up a design hierarchy. Hierarchy is created by one building block instantiating another building block. 

When a module contains an instance of another module, interface, program, or checker, a new level of hierarchy is created. Communication through levels of hierarchy is primarily through connections to the ports of the instantiated module, interface, program, or checker.

```SystemVerilog
module top; // module with no ports
  logic in1, in2, select; // variable declarations
  wire out1; // net declaration
  
  // module instance
  mux2to1 m1 (
    .a(in1), 
    .b(in2), 
    .sel(select), 
    .y(out1)
  );

endmodule : top

module mux2to1 (
  input wire a, b, sel, // combined port and type declaration
  output logic y
);

  // netlist using built-in primitive instances 
  not g1 (sel_n, sel);

  and g2 (a_s, a, sel_n);
  
  and g3 (b_s, b, sel);
  
  or g4 (y, a_s, b_s);

endmodule : mux2to1 
```

Modules can instantiate other modules, programs, interfaces, checkers, and primitives, creating a hierarchy tree. 

Interfaces can also instantiate other building blocks and create a hierarchy tree. 

Programs and checkers can instantiate other checkers. Primitives cannot instantiate other building blocks; they are leaves in a hierarchy tree.

!!! Note
    SystemVerilog permits multiple top-level blocks.

### Compilation and elaboration 

#### Compilation

It is the process of reading in SystemVerilog source code, decrypting encrypted code, and analyzing the source code for syntax and semantic errors.

SystemVerilog supports both single file and multiple file compilation through the use of compilation units.

#### Elaboration

It is the process of binding together the components that make up a design. These components can include module instances, program instances, interface instances, checker instances, primitive instances, and the top level of the design hierarchy.

Elaboration occurs after parsing the source code and before simulation; and it involves expanding instantiations, computing parameter values, resolving hierarchical names, establishing net connectivity and in general preparing the design for simulation.

#### Compilation units 

SystemVerilog supports separate compilation using compiled units.

  - **Compilation unit**: A collection of one or more SystemVerilog source files compiled together.
  
  - **Compilation-unit Scope**: A scope that is local to the compilation unit. It contains all declarations that lie outside any other scope.

  - **$unit**: The name used to explicitly access the identifiers in the compilation-unit scope.

The exact mechanism for defining which files constitute a compilation unit is tool-specific.

The contents of files included using one or more `include directives become part of the compilation unit of the file within which they are included.

The following items are visible in all compilation units: modules, primitives, programs, interfaces, and packages. 

Items defined in the compilation-unit scope cannot be accessed by name from outside the compilation unit. The items in a compilation-unit scope can be accessed using the PLI, which shall provide an iterator to traverse all the compilation units.

**$unit** is the name of the scope that encompasses a compilation unit. Its purpose is to allow the unambiguous reference to declarations at the outermost level of a compilation unit (i.e., those in the compilation-unit scope). This is done via the same scope resolution operator used to access package items.

=== "Allowed"
    ```SystemVerilog
    bit b;

    task t;
      int b;
      b = 5 + $unit::b;
    endtask
    ``` 

=== "Not-Allowed"
    ```SystemVerilog
    task t;
      int x;
      x = 5 + b;
      
      // illegal - "b" is defined later
      x = 5 + $unit::b; // illegal - $unit adds no special forward referencing
    endtask 
    bit b;
    ```

### Name spaces

SystemVerilog has eight name spaces for identifiers: two global (definitions and package), two global to the compilation unit (compilation unit and text macro), and four local. Here's a brief overview:

1. **Definitions Name Space**: Unifies non-nested module, primitive, program, and interface identifiers defined outside other declarations. Once used, a name cannot be reused for another non-nested module, primitive, program, or interface.

2. **Package Name Space**: Unifies package identifiers across all compilation units. A name used for a package cannot be reused for another package.

3. **Compilation-Unit Scope Name Space**: Exists outside module, interface, package, checker, program, and primitive constructs. Unifies definitions of functions, tasks, checkers, parameters, named events, net declarations, variable declarations, and user-defined types.

4. **Text Macro Name Space**: Global within the compilation unit. Text macro names, introduced with a leading ‘ character, remain unambiguous with any other name space. Subsequent definitions override previous ones.

5. **Module Name Space**: Introduced by module, interface, package, program, checker, and primitive constructs. Unifies definitions within the enclosing construct.

6. **Block Name Space**: Introduced by named or unnamed blocks, specify, function, and task constructs. Unifies definitions within the enclosing construct.

7. **Port Name Space**: Introduced by module, interface, primitive, and program constructs. Specifies connections between objects in different name spaces. Overlaps module and block name spaces.

8. **Attribute Name Space**: Enclosed by (* and *) constructs attached to a language element. An attribute name can only be defined and used in this name space.

!!! warning
    Within a name space, redeclaring a name already declared by a prior declaration is illegal.

### Simulation time units and precision 

An important aspect of simulation is time. The term simulation time is used to refer to the time value maintained by the simulator to model the actual time it would take for the system description being simulated. The term time is used interchangeably with simulation time.

Time values are used in design elements to represent propagation delays and the amount of simulation time between when procedural statements execute. Time values have two components, a time unit and a time precision. 

  - The time unit represents the unit of measurement for times and delays, and can be specified in units ranging from 100 second units down to 1 femtosecond units.

  - The time precision specifies the degree of accuracy for delays. 

Both the time units and time precision are represented using one of the character strings : `s`, `ms`, `us`, `ns`, `ps`, and `fs` with an order of magnitude of 1, 10, or 100. 

**The definition of these character strings is given in below table.**

<!-- below two thing can be used -->

#### Time unit strings

<!-- | Character string | Unit of measurement |
| :--------------: | :-----------------: |
| s                | seconds             |            
| ms               | milliseconds        |                 
| us               | microseconds        |                 
| ns               | nanoseconds         |                
| ps               | picoseconds         |                
| fs               | femtoseconds        |                   -->
 
{{ read_csv('tables\sv_time_unit_strings.csv') }}

!!! warning
     The time precision of a design element shall be at least as precise as the time unit; it cannot be a longer unit of time than the time unit.

#### Time value rounding

Within a design element (module, program, or interface), time precision determines how delay values are rounded for simulation. Time precision is relative to time units:

- If precision equals time units, delay values are rounded to whole numbers.
- If precision is one order of magnitude smaller than time units, delay values are rounded to one decimal place.

!!! example
    For example, with a time unit of 1ns and precision of 100ps (0.1ns), a delay of 2.75ns is rounded to 2.8ns. Time values in a design element are accurate to the specified time precision, even if a smaller precision is specified elsewhere.

#### Specifying time units and precision

The time unit and time precision can be specified in the following two ways:

  - Using the compiler directive ``timescale` 

    !!! example
        ```SystemVerilog
        `timescale time_unit / time_precision
        ```
  - Using the keywords `timeunit` and `timeprecision` 

    !!! example
        ```SystemVerilog
        timeunit 100ps;
        timeprecision 10fs;
        ```

#### Simulation time unit

The `global time precision`, or `simulation time unit`, is the smallest value among all time precision statements, timeunit declarations, and `timescale compiler directives in the design. The step time unit equals the global time precision and cannot be used to set or modify the precision or time unit.
