• One or more path components (the subset of characters and case sensitivity of path components must follow the path rules of a host filesystem).

• Slash characters separating components of the path.

The slash character ‘/’ is used in import paths irrespective of the host system. The backslash character is not used in this context.

In most file systems, an import path looks like a file path. Relative (see below) and non-relative import paths have different resolutions that map the import path to a file path of the host system.

The compiler uses its own algorithm to locate a module source that processes the import path. If the import path specifies no file extension, then the compiler can append some according to its own rules and priorities. If the import path refers to a folder, then the way to handle the case is determined by the actual compiler. If the compiler cannot locate a module source definitely, then a compile-time error occurs.

A relative import path starts with ‘./’ or ‘../’. Examples of relative paths are presented below:

"./components/entry"
"./constants/http"

Resolving relative import is relative to the importing file. Relative import is used on modules to maintain their relative location.

import * asUtils from"./mytreeutils"

Other import paths are non-relative.

Resolving a non-relative path depends on the compilation environment. The definition of the compiler environment can be particularly provided in a configuration file or environment variables.

The base URL setting is used to resolve a path that starts withத்‌த்‌த்‌த்‌

{
    "baseUrl": "/home/project",
    "paths": {
        "std": "/arkts/stdlib"
    }
}

In the example above, /net/http is resolved to /home/project/net/http, and std/components/treemap to /arkts/stdlib/components/treemap.

File name, placement, and format are implementation-specific.

If the above configuration is in effect, the first path maps directly to filesystem after applying baseUrl, while std in the second path is replaced for /arkts/stdlib. Examples of non-relative paths are presented below.

"/net/http"
"std/components/treemap"
