(*---------------------------------------------------------------------------
  Copyright (c) {{YEAR}} {{AUTHOR_NAME}} <{{AUTHOR_EMAIL}}>. All rights reserved.
  SPDX-License-Identifier: {{LICENSE}}
 ---------------------------------------------------------------------------*)

(** Eio mock-based tests for {{PROJECT_NAME}} *)

(* Test using mock backend - no real I/O *)
let test_with_mock_backend () =
  Eio_mock.Backend.run @@ fun () ->
  (* Your test code here *)
  Alcotest.(check bool) "mock test" true true

(* Test with deterministic clock *)
let test_with_mock_clock () =
  Eio_mock.Backend.run @@ fun () ->
  let clock = Eio_mock.Clock.make () in
  (* Advance time by 1 second *)
  Eio_mock.Clock.advance clock 1.0;
  (* Check that time-dependent logic works correctly *)
  Alcotest.(check bool) "clock advanced" true true

(* Test with mock flow (for stream/connection testing) *)
let test_with_mock_flow () =
  Eio_mock.Backend.run @@ fun () ->
  let flow = Eio_mock.Flow.make "test-flow" in
  (* Set up expected reads *)
  Eio_mock.Flow.on_read flow [
    `Return "hello";
    `Return "world";
    `Raise End_of_file;
  ];
  (* Your test reading from flow *)
  Alcotest.(check bool) "flow test" true true

(* Integration test with real I/O - use sparingly *)
let test_integration () =
  Eio_main.run @@ fun env ->
  let _fs = Eio.Stdenv.fs env in
  let _clock = Eio.Stdenv.clock env in
  (* Real I/O operations here *)
  Alcotest.(check bool) "integration" true true

let mock_suite = [
  "mock backend", `Quick, test_with_mock_backend;
  "mock clock", `Quick, test_with_mock_clock;
  "mock flow", `Quick, test_with_mock_flow;
]

let integration_suite = [
  "real I/O", `Slow, test_integration;
]

let () =
  Alcotest.run "{{PROJECT_NAME}}" [
    "mock tests", mock_suite;
    "integration", integration_suite;
  ]
