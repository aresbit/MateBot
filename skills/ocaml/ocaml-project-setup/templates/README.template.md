# {{PROJECT_NAME_KEBAB}}

{{PROJECT_SYNOPSIS}}

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

### Using opam

```bash
opam install {{PROJECT_NAME}}
```

### From source

```bash
git clone {{GIT_URL}}
cd {{PROJECT_NAME_KEBAB}}
opam install . --deps-only
dune build
```

## Usage

```ocaml
open {{PROJECT_NAME_CAPITALIZED}}

let () =
  (* Your code here *)
  ()
```

## Documentation

API documentation is available at: https://{{GIT_ORG}}.github.io/{{PROJECT_NAME_KEBAB}}

Build locally with:

```bash
dune build @doc
open _build/default/_doc/_html/index.html
```

## Development

### Building

```bash
dune build
```

### Testing

```bash
dune runtest
```

### Formatting

```bash
dune fmt
```

## License

{{LICENSE}} License. See [LICENSE.md](LICENSE.md) for details.
