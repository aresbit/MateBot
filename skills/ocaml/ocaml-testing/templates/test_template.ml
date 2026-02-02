(*---------------------------------------------------------------------------
  Copyright (c) {{YEAR}} {{AUTHOR_NAME}} <{{AUTHOR_EMAIL}}>. All rights reserved.
  SPDX-License-Identifier: {{LICENSE}}
 ---------------------------------------------------------------------------*)

(** Tests for {{PROJECT_NAME}} *)

let test_basic () =
  Alcotest.(check int) "same ints" 42 (21 + 21)

let test_string () =
  Alcotest.(check string) "same strings" "hello" "hello"

let basic_suite = [
  "basic arithmetic", `Quick, test_basic;
  "string equality", `Quick, test_string;
]

(* Add more test suites here *)

let () =
  Alcotest.run "{{PROJECT_NAME}}" [
    "basic", basic_suite;
  ]
