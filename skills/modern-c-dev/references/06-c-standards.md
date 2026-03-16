# Source: https://hackmd.io/@sysprog/c-standards

---
tags: DYKC, CLANG, C LANGUAGE
---

# [你所不知道的 C 語言](https://hackmd.io/@sysprog/c-prog/): 開發工具和規格標準

Copyright (**慣C**) 2015, 2017 [宅色夫](http://wiki.csie.ncku.edu.tw/User/jserv)

==[直播錄影](https://www.youtube.com/watch?v=scLFY2CRtFo)==

:::success
"If I had eight hours to chop down a tree, I’d spend six hours sharpening my axe." -- Abraham Lincoln
> 「如果我有 8 小時可以砍 1 棵樹，我會花 6 小時把斧頭磨利。」(類似漢語「工欲善其事，必先利其器」的精神) -- 亞伯拉罕．林肯

語言規格:
C89/[C90](https://www.iso.org/standard/17782.html) -> [C99](https://www.iso.org/standard/29237.html) -> [C11](https://www.iso.org/standard/57853.html) -> C17/[C18](https://www.iso.org/standard/74528.html) -> C2x
:::

## C 語言老爸的評論

「C 很彆扭又缺陷重重，卻異常成功。固然有歷史的巧合推波助瀾，可也的確是因為它能滿足於系統軟體實作的程式語言期待：既有相當的效率來取代組合語言，又可充分達到抽象且流暢，能用於描述在多樣環境的演算法。」

> C is quirky, flawed, and an enormous success. Although accidents of history surely helped, it evidently satisfied a need for a system implementation language efficient enough to displace assembly language, yet sufficiently abstract and fluent to describe algorithms and interactions in a wide variety of environments. —— [Dennis M. Ritchie](https://en.wikipedia.org/wiki/Dennis_Ritchie)

![](https://i.imgur.com/1gWHzfd.png)

[Jonathan Adamczewski](https://twitter.com/twoscomplement) 貼出經典著作《The C Programming Language》，然後評註說:
> "**C++: The Good Parts**"

[K&R C](https://en.wikipedia.org/wiki/C_(programming_language)#K&R_C) 的 "K" 即 [Brian Kernighan](https://en.wikipedia.org/wiki/Brian_Kernighan) 教授，而非 Ken Thompson。

{%youtube ci1PJexnfNE %}
> [David Brailsford](http://www.cs.nott.ac.uk/~psadb1/) 教授的訪談，從大型主機 (mainframe) 時代談起，早期的機器甚至不是 [byte addressing](https://en.wikipedia.org/wiki/Byte_addressing)，這使得高階程式語言和電腦硬體無法直接對應，而 C 語言恰好彌補系統層級程式設計的需求，再藉由 UNIX 作業系統的影響，改變今日我們所處的資訊世界。

![](https://i.imgur.com/4Uzmkvi.png)

C++ 可以美得令人不知所措 [[source](https://twitter.com/jfbastien/status/730963193799938051)]


## 為什麼我不探討 C++

* 在台灣發文好像愛用「為什麼我不」開頭，後面可接「念研究所」、「待在大公司」等描述
* C++ 自稱為物件導向的程式語言，卻不願意對物件在執行時期的表現負責任
    * 若說 C 語言給了你足夠的繩子吊死自己，那麼 C++ 給的繩子除了夠你上吊之外，還夠綁住你身邊的朋友
    * 相較之下，Java 讓你在吊死自己之際仍有親友監視著，雖然死不了，但事後會更想死
    * [ [source](https://twitter.com/RichRogersHDS/status/666798359244611584) ]
        * In Ruby, everything is an object.
        * In Clojure, everything is a list.
        * In Javascript, everything is a terrible mistake.
        * in C, everything is a representation (unsigned char [sizeof(TYPE)]).
* Linus Torvalds [在 2010 年的解釋](http://www.realworldtech.com/forum/?threadid=104196&curpostid=104208)
* C++ 實際上已經是截然不同的程式語言
    * C++ 老爸 Bjarne Stroustrup 的文章: "[Learning Standard C++ as a New Language](http://www.stroustrup.com/new_learning.pdf)"
* 最重要的是，C++ 改版飛快，C++ 17 即將推出，但我還沒看懂 C++ 98

![](https://i.imgur.com/ITVm6gI.png)

* [ [source](https://isocpp.org/std/status) ]

## 延伸閱讀

* [沒有 C 語言之父，就沒有 Steve Jobs](https://buzzorange.com/techorange/2015/10/19/without-dennis-ritchie-there-would-be-no-steve-jobs/) ([原文](https://www.zdnet.com/article/without-dennis-ritchie-there-would-be-no-jobs/))
* [第一個 C 語言編譯器是怎樣編寫的？](https://kknews.cc/zh-tw/tech/bx2r3j.html)

![image](https://hackmd.io/_uploads/B1obBdBL0.png)

## 讀規格書可大幅省去臆測

在 [ISO/IEC 9899 (a.k.a C99 Standard)](http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1256.pdf) 中 5.1.2.2.1 內有提到 C Standard 要求 main 函式必須這樣寫
```c
int main(void) { /* ... */};
```
或者:
```c
int main(int argc, char *argv[]) { /* ... */ };
```

C++ 之父 Bjarne Stroustrup 的個人網頁內有個 [FAQ](http://www.stroustrup.com/bs_faq2.html#void-main) 裡面有個問題叫 **Can I write "void main()"?**

然而在 C++ 與 C 的標準中從來沒出現過這樣的寫法，也就是說，```void main()``` 這個寫法從來沒正確過

延伸閱讀
* [C 語言中 int main() 和 void main() 有何區別？](https://www.zhihu.com/question/60047465)
* [ C++ 的 void main() / int main() … 不要再用 void main() 了! | Peter Dave Hello's Blog](https://www.peterdavehello.org/2014/10/void-main-int-main-in-c-and-cpp/)
* [void main(void) - the Wrong Thing](https://www.ty-penguin.org.uk/~auj/voidmain/)
* [Linux 核心原始程式碼的整數除法](https://hackmd.io/@sysprog/linux-intdiv): 不讀規格書連除法都會算錯

---

## ISO/IEC 9899 (簡稱 "C99")

- 從[一則笑話](https://twitter.com/SoManyHs/status/675505383008415744)談起
  - "Programming in C: if it doesn't work, just add a star. Or multiple stars. Or ampersands."

- 葉秉哲博士的[推文](https://twitter.com/william_yeh/status/705031736371982336)：「==溯源能力==是很重要的，才不會被狀似革新，實則舊瓶裝新酒或跨領域借用的『新觀念』所迷惑」

- [規格書](http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1256.pdf) (PDF) 搜尋 "***object***"，共出現 735 處
  - 搜尋 "***pointer***"，共出現 637 處。有趣的是，許多教材往往不談 object，而是急著談論 pointer，殊不知，這兩者其實就是一體兩面
  - object != object-oriented
    - 前者的重點在於「資料表達法」，後者的重點在於 "everything is object"
  - C11 ([ISO/IEC 9899:201x](http://www.open-std.org/jtc1/sc22/WG14/www/docs/n1570.pdf)) / [網頁版](http://port70.net/~nsz/c/c11/n1570.html)

- 從第一手資料學習：大文豪寫作都不免要查字典，庸俗的軟體開發者如我們，難道不需要翻閱語言規格書嗎？難道不需要搞懂術語定義和規範嗎？

- `&` 不要都念成 and，涉及指標操作的時候，要讀為 "address of"
  - C99 標準 [6.5.3.2] Address and indirection operators 提到 '==&==' address-of operator

- C99 [3.14] ***object***
  - region of data storage in the execution environment, the contents of which can represent values
  - 在 C 語言的物件就指在執行時期，==資料==儲存的區域，可以明確表示數值的內容
  - 很多人誤認在 C 語言程式中，(int) 7 和 (float) 7.0 是等價的，其實以資料表示的角度來看，這兩者截然不同，前者對應到二進位的 "111"，而後者以 IEEE 754 表示則大異於 "111"
<img style="display:block; margin:auto;" src="https://i.imgur.com/BkxFbFh.png"></img>

  - A pointer to void shall have the same representation and alignment requirements as a pointer to a character type.  
    > 關鍵描述！規範 `void *` 和 `char *` 彼此可互換的表示法

```c
void *memcpy(void *dest, const void *src, size_t n);
```

- C99 規格書的解說就比很多書本清楚，何必捨近求遠呢？
    - **EXAMPLE 1**: The type designated as `float *` has type "pointer to float". Its type category is pointer, not a floating type. The const-qualified version of this type is designated as `float * const` whereas the type designated as "`const float *` is not a qualified type — its type is "pointer to const qualified float" and is a pointer to a qualified type.
    - **EXAMPLE 2**: The type designated as "`struct tag (*[5])(float)` has type "array of pointer to function returning struct tag". The array has length five and the function has a single parameter of type float. Its type category is array.

- [Understand more about C](https://www.slideshare.net/YiHsiuHsu/understand-more-about-c) 提及若干肇因於不同的 C 語言標準，而使得程式碼行為不同的案例


### 規格不能只看新的，過往也要熟悉

![](https://i.imgur.com/oerJv9s.png)
[source](https://twitter.com/0xdeadb/status/766293771663339520)
- 空中巴士 330 客機的娛樂系統裡頭執行 14 年前的 Red Hat Linux，總有人要為「古董」負責
- 而且空中巴士 380 客機[也是如此](https://twitter.com/AlxRogan/status/766382294038872064)

為何 C 語言標準函式庫裡頭的函式名稱如此簡短？像是
* strcpy
* strlen

最初連結器有 6 到 8 個字元的輸入限制!
> Translation limits
> 6 significant initial characters in an external identifier
* 延伸閱讀:
    * [Why did ANSI only specify six characters for the minimum number of significant characters in an external identifier?](https://stackoverflow.com/questions/38035628/c-why-did-ansi-only-specify-six-characters-for-the-minimum-number-of-significa/38042724#38042724)
    * [Identifier](https://en.cppreference.com/w/c/language/identifier)

[The Design and Evolution of C++](http://www.stroustrup.com/dne.html) 一書對應的解說:
![](https://i.imgur.com/rDNRibU.jpg)


## 英文很重要

安裝 `cdecl` 程式，可以幫你產生 C 程式的宣告。
```shell
$ sudo apt-get install cdecl
```

使用案例

```shell
$ cdecl
cdecl> declare a as array of pointer to function returning pointer to function returning pointer to char
```

會得到以下輸出:

```c
char *(*(*a[])())()
```

把前述 C99 規格的描述帶入，可得:

```shell
cdecl> declare array of pointer to function returning struct tag
```
```c
struct tag (*var[])()
```

如果你沒辦法用英文來解說 C 程式的宣告，通常表示你不理解！

`cdecl` 可以解釋 C 程式宣告的意義，比方說：

```shell
cdecl> explain char *(*fptab[])(int)
declare fptab as array of pointer to function (int) returning pointer to char
```

---

## 只用 printf 觀察資料，有問題嗎？

![](https://i.imgur.com/5pwv9bT.png)

[ [source](https://twitter.com/alang198611/status/735312419715612673) ]

- 只用 `printf()` 觀察的話，永遠只看到你設定的框架 (format string) 以內的資料，但很容易就忽略資料是否合法、範圍是否正確，以及是否看對地方
- `printf()` 大概是最早被記下來的函式，也困擾很多人，有意思的是，1960 年代初期 MIT 開發的 [CTSS 作業系統](https://en.wikipedia.org/wiki/Compatible_Time-Sharing_System) 中，終端機命令就包含了 printf，後者一路從 Multics 和 Unix 繼承至今
- 在 CTSS 原始程式碼的檔案 com3 中可見到這行 `STMTDC PRINTF,11,T,T25`，前一行註解寫 "The following tables are the dictionaries of statement types"


## 不要急著印出位址，善用 GDB

![](https://hackpad-attachments.s3.amazonaws.com/embedded2015.hackpad.com_s0rlzR8wVtm_p.299401_1474178146663_undefined)

[source](https://twitter.com/noreenahertz/status/593761269930434560): NASA before PowerPoint, 1961

- 「學會了 GDB，我有種山頂洞人==學會用火==的感動」 -- 張至
- [GDB Rocks!](http://www.slideshare.net/chenkaie/gdb-rocks-16951548) (on slideshare)
- [Introduction to gdb](http://www.slideshare.net/owenhsu/introduction-to-gdb-3790833) (on slideshare)
- [Debugging with GDB](http://www.slideshare.net/linaroorg/connect12-q2-gdb) (on slideshare)
    - [clewn, pyclewn on sourceforge](https://sourceforge.net/projects/pyclewn/)
    - [gdb to kernel](https://reverse.put.as/tags/gdb/)
    - [GDB 的妙用](https://blog.vgod.tw/2006/06/21/gdb%E7%9A%84%E5%A6%99%E7%94%A8/)
    - [Kaie's Blog](https://chenkaie.blogspot.com/2011/12/gdb-tricks-file-descriptor-hijacking.html#)
    - [GDB Documentation](https://www.sourceware.org/gdb/documentation/)
- [除錯程式: gdb](https://v.im.cyut.edu.tw/~ckhung/b/c/gdb.php)
- [Introduction to GDB a tutorial - Harvard CS50](https://www.youtube.com/watch?v=sCtY--xRUyI) (教學影片)
- [透過 GDB 學習 C 語言](https://jasonblog.github.io/note/gdb/tongguo_gdb_xue_xi_c_yu_yan.html)


## GDB

* [Kernel command using Linux system calls](https://developer.ibm.com/tutorials/l-system-calls/)
* video: [Linux basic anti-debug](https://www.youtube.com/watch?v=UTVp4jpJoyc)
* video: [C Programming, Disassembly, Debugging, Linux, GDB](https://www.youtube.com/watch?v=twxEVeDceGw)
* [rr](http://rr-project.org/) (Record and Replay Framework)
    * video: [Quick demo](https://www.youtube.com/watch?v=hYsLBcTX00I)
    * video: [Record and replay debugging with "rr"](https://www.youtube.com/watch?v=ytNlefY8PIE)

## 整合開發環境

Visual Studio Code (VS Code) 是 Microsoft 主導的開放原始碼專案，關於其操作說明和解說錄影可參見 [共筆](https://hackmd.io/s/rJPKpohsx)。

## C23

C 語言規格一直在變革，此刻最新的標準是 C17，其正式名稱為ISO/IEC 9899:2018，是在 2017 年準備、隔年發布的規範。C23 則是現行開發中規格的簡稱，預計在 2023 年進行投票並發佈新標準，稱為 C23。預計納入的特徵如下:
* typeof 運算子，過往是 GNU extension，這可用來實作 `container_of` 一類的巨集
* 強制規範 `call_once` 的支援，後者在並行 (concurrent) 環境中，得以確保某段程式碼始終只會執行一次
* 納入 `char8_t` 的支援，以 `_t` 結尾的慣例說明這由編譯器供應商提供的 typedef，這對 Unicode 更友好，於是我們可以書寫為 `u8"💣"[0]`
* 提供 `unreachable()`，讓編譯器得以進行更激進的最佳化，過往是 GNU extension
* 以 `= {}` 取代 `memset` 函式的呼叫
* 支援 ISO/IEC 60559:2020，這是最新 IEEE 754 浮點數運算標準
* 針對 C11 納入的 `_Static_assert`，允許單一參數
* 納入 C++11 風格的 attribute 語法，例如 `nodiscard`, `maybe_unused`, `deprecated`, 和 `fallthrough`
* 新的函式: memccpy(), strdup(), strndup() – 類似 POSIX/SVID 中 C 函式庫的擴充
* 強制規範使用二補數符號表示
* 不再支援 K&R 風格的函式定義
* 二進位表達式 (Binary literals)，例如 `0b10101010` (很難想像 1970 年代發展的 C 語言，要到 2023 年或稍晚，才能直接指定二進位表示吧？) 和對應 printf() 的 `%b`
* Type generic functions for performing checked integer arithmetic (Integer overflow)
* `_BitInt(N)` and `UnsignedBitInt(N)` types for bit-precise integers
* 支援 `#elifdef` 和 `#elifndef`
* 允許在數值表示中加上分隔符號，易於閱讀，例如 `0xFFFF'FFFF`

延伸閱讀:
* [Ever Closer - C23 Draws Nearer](https://thephd.dev/ever-closer-c23-improvements) 和 [C23 is Finished: Here is What is on the Menu](https://thephd.dev/c23-is-coming-here-is-what-is-on-the-menu)
* [A cheatsheet of modern C language and library features](https://github.com/AnthonyCalandra/modern-c-features)
* [Checked integer arithmetic in the prospect of C23](https://gustedt.wordpress.com/2022/12/18/checked-integer-arithmetic-in-the-prospect-of-c23/) / [jtckdint](https://github.com/friendlyanon/jtckdint)