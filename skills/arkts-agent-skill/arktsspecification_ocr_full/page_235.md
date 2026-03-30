exportDirective:
    selectiveExportDirective
| singleExportDirective
| exportTypeDirective
| reExportDirective
;

#### 13.5.1 Selective Export Directive

Top-level declarations can be made exported by using a selective export directive. The selective export directive provides an explicit list of names of the declarations to be exported. Optional renaming allows having the declarations exported with new names.

The syntax of selective export directive is presented below:

selectiveExportDirective:
'export' selectiveBindings
;

A selective export directive uses the same selective bindings as an import directive:

export { d1, d2 as d3 }

The above directive exports ‘d1’ by its name, and ‘d2’ as ‘d3’. The name ‘d2’ is not accessible (see Accessible) in the modules that import this module.

#### 13.5.2 Single Export Directive

Single export directive allows specifying the declaration to be exported from the current module by using the declaration's own name, or anonymously.

The syntax of single export directive is presented below:

singleExportDirective:
  'export'
  (identifier
    | 'default' (expression | identifier)
    | '{' identifier 'as' 'default' '}'
)
;

If default is present, then only one such export directive is possible in the current module. Otherwise, a compile-time error occurs.

The directive in the example below exports variable 'v' by its name:
