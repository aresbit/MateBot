#### 13.1.6 Several Bindings for One Import Path

The same bound entities can use the following:

• Several import bindings,

• One import directive, or several import directives with the same import path:


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>In one import directive</td><td style='text-align: center; word-wrap: break-word;'>import {sin, cos} from &quot;...</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>In several import directives</td><td style='text-align: center; word-wrap: break-word;'>import {sin} from &quot;...import {cos} from &quot;...</td></tr></table>

No conflict occurs in the above example, because the import bindings define disjoint sets of names.

The order of import bindings in an import declaration has no influence on the outcome of the import.

The rules below prescribe what names must be used to add bound entities to the declaration scope of the current module if multiple bindings are applied to a single name:
