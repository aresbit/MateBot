Letter
: UNICODE_CLASS_LU
| UNICODE_CLASS_LL
| UNICODE_CLASS_LT
| UNICODE_CLASS_LM
| UNICODE_CLASS_LO
;
UnicodeDigit
: UNICODE_CLASS_ND
;

See Grammar Summary for the Unicode character categories UNICODE_CLASS_LU, UNICODE_CLASS_LL, UNICODE_CLASS_LT, UNICODE_CLASS_LM, UNICODE_CLASS_LO, and UNICODE_CLASS_ND.

### 2.7 Keywords

Keywords are reserved words with meanings permanently predefined in ArkTS. Keywords are case-sensitive, and their exact spelling is presented in the following four tables. The kinds of keywords are discussed below.

1. The following hard keywords are reserved in any context, and cannot be used as identifiers:


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>abstract</td><td style='text-align: center; word-wrap: break-word;'>enum</td><td style='text-align: center; word-wrap: break-word;'>let</td><td style='text-align: center; word-wrap: break-word;'>this</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>as</td><td style='text-align: center; word-wrap: break-word;'>export</td><td style='text-align: center; word-wrap: break-word;'>native</td><td style='text-align: center; word-wrap: break-word;'>throw</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>async</td><td style='text-align: center; word-wrap: break-word;'>extends</td><td style='text-align: center; word-wrap: break-word;'>new</td><td style='text-align: center; word-wrap: break-word;'>true</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>await</td><td style='text-align: center; word-wrap: break-word;'>false</td><td style='text-align: center; word-wrap: break-word;'>null</td><td style='text-align: center; word-wrap: break-word;'>try</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>break</td><td style='text-align: center; word-wrap: break-word;'>final</td><td style='text-align: center; word-wrap: break-word;'>overload</td><td style='text-align: center; word-wrap: break-word;'>typeof</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>case</td><td style='text-align: center; word-wrap: break-word;'>for</td><td style='text-align: center; word-wrap: break-word;'>override</td><td style='text-align: center; word-wrap: break-word;'>undefined</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>class</td><td style='text-align: center; word-wrap: break-word;'>function</td><td style='text-align: center; word-wrap: break-word;'>private</td><td style='text-align: center; word-wrap: break-word;'>while</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>const</td><td style='text-align: center; word-wrap: break-word;'>if</td><td style='text-align: center; word-wrap: break-word;'>protected</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>constructor</td><td style='text-align: center; word-wrap: break-word;'>implements</td><td style='text-align: center; word-wrap: break-word;'>public</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>continue</td><td style='text-align: center; word-wrap: break-word;'>import</td><td style='text-align: center; word-wrap: break-word;'>return</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>default</td><td style='text-align: center; word-wrap: break-word;'>in</td><td style='text-align: center; word-wrap: break-word;'>static</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>do</td><td style='text-align: center; word-wrap: break-word;'>instanceof</td><td style='text-align: center; word-wrap: break-word;'>switch</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>else</td><td style='text-align: center; word-wrap: break-word;'>interface</td><td style='text-align: center; word-wrap: break-word;'>super</td><td style='text-align: center; word-wrap: break-word;'></td></tr></table>

2. Names and aliases of predefined types are hard keywords, and cannot be used as identifiers:
