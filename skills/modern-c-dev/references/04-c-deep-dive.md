# Source: https://hackmd.io/@sysprog/c-programming

---
tags: DYKC, CLANG, C LANGUAGE
---

# 「[你所不知道的 C 語言](https://hackmd.io/@sysprog/c-prog/)」系列講座

副標題: ==深度學習 C 語言==
回歸第一手資料，透過反思 C 語言程式設計的細節，重新學習電腦原理 -- [jserv](https://wiki.csie.ncku.edu.tw/User/jserv)

:::warning
:warning: 注意
- 本講座針對「已實際撰寫 C 程式」的人，若你無相關背景知識，請參見李根逸博士的 [C 語言入門](https://feis.studio/c)
- 歡迎遞交想學習和探討的子項目，請 [編輯「許願池」頁面](https://hackmd.io/@sysprog/By9B9jZcm)
:::

<img style="display:block; margin:auto;" src="https://i.imgur.com/hx96Iy3.png"></img>

## 講座說明

在大學教了幾年嵌入式系統課程後，我深深體會到這個事實：與其說學生對嵌入式系統掌握度不足，不如說為數眾多的人根本只是學了 C 程式語言的語法，而從未想過背後的原理、語言設計者的思維和理念，以及在真實環境中的關聯。

古希臘 Delphi 神殿前，有一則神諭寫道 "[Know Thyself](https://en.wikipedia.org/wiki/Know_thyself)"，也就是「誠實面對自己」，我們程式設計師就該從技術、團隊合作、理性思考，以及培養堅忍不拔精神等方面， 找到自我，從而建立自信。

於是，從 2015 年秋季開始，我做了一系列的調整，重新探討 C 語言程式設計，安排了「你所不知道的 C 語言」系列講座，透過實體和線上直播課程，整理這二十年來程式設計經驗，帶著學員參考第一手的資料 (例如 [ISO/IEC 9899](http://www.open-std.org/jtc1/sc22/wg14/www/standards.html) C 語言規格)，並善用系統開發工具 (如 GNU Debugger)，屏棄過往臆測為主的學習方式，探究實際 C 程式的行為並反思箇中原理，讓更多人得以正視自己的盲點，從而打下穩固的基礎。

:::info
C is not a legacy language.
C is not an antique language.

Get your marketecture right:
C is an artisanal language for programmers obsessed with hand-crafting the smallest details of their programs.
:::


## 你所不知道的 C 語言

* [為什麼要深入學習 C 語言？](https://hackmd.io/@sysprog/c-standards) (2017.05)
    * 與其瞎猜，不如從第一手材料研讀起
    * 掌握 C 語言規格和演化
    * 熟悉 GDB 在內的工具程式
* [指標篇](https://hackmd.io/@sysprog/c-pointer) (2015.11) (2016.09) (2018.02)
    * 解讀 C 語言規格書的 "object"
    * 重讀 "type" 的定義，並且理解 incomplete type 的意義
    * 三位一體: Array, function, pointer types
        * 都稱為 _derived declarator types_
    * `void *` 的設計考量
    * C-style string
* [函式呼叫篇](https://hackmd.io/@sysprog/c-function) (2015.12) (2016.02) (2017.10) (2022.01) (2026.03)
    * process memory layout
    * application binary interface (ABI)
    * stack pointer
    * 遞迴呼叫
    * 重新檢閱 Heap: malloc() / free() 的實作
* [記憶體管理、對齊及硬體特性](https://hackmd.io/@sysprog/c-memory) (2018.09)
    * 硬體的行為
    * 消除對於 alignment, padding, memory allocator 的誤解
    * 探討高效能 memory pool 的設計
    * C11 標準的 aligned_alloc
* [編譯器和最佳化原理篇](https://hackmd.io/@sysprog/c-compiler-optimization) (2016.01) (2017.10)
    * 以 GNU Toolchain 為探討對象，簡述[編譯器如何運作，以及如何落實最佳化](http://www.slideshare.net/jserv/how-a-compiler-works-gnu-toolchain)
    * C 語言程式如何轉換為機械碼，以及最佳化的空間和限制
* [C 編譯器原理和案例分析](https://hackmd.io/@sysprog/c-compiler-construction) (2018.08)
    * 從[一個簡易的 JIT compiler](http://www.slideshare.net/jserv/jit-compiler)，回顧 code generator / JIT compiler
    * 用不到一千行 C 程式，實作小型 C 語言編譯器
* [物件導向程式設計篇](https://hackmd.io/@sysprog/c-oop) (2016.04) (2016.05) (2018.09)
    * Linux 核心、Apache HTTP 伺服器，以及 Gtk+ / GNOME 這些專案原始程式碼背後都應用大量物件導向設計方法
    * 實踐物件導向，並強調帶來的效益
    * 展示 GoF 的《Design Patterns》如何用 C 語言實作
* [前置處理器應用篇](https://hackmd.io/@sysprog/c-preprocessor) (2016.06) (2022.02)
    * 回顧 C99/C11 的 macro 特徵，探討 C11 新的關鍵字 `_Generic`
    * 探討 C 語言程式的物件導向程式設計、抽象資料型態 (ADT) / 泛型程式設計 (Generics)、程式碼產生器、模仿其他程式語言，以 preprocessor 搭配多種工具程式的技巧
* [動態連結器](https://hackmd.io/@sysprog/c-dynamic-linkage) (2016.08) (2018.10)
    * symbol 的奧義, dynamic linker 的行為, 用 GDB 追蹤 C 語言程式
* [連結器和執行檔資訊](https://hackmd.io/@sysprog/c-linker-loader) (2019.02)
* [執行階段程式庫 (CRT)](https://hackmd.io/@sysprog/c-runtime) (2018.10)
* [技巧篇](https://hackmd.io/@sysprog/c-trick) (2017.03) (2019.07)
    * 以矩陣運算的案例，實踐物件導向、指標操作、函式呼叫等觀念
* [數值系統篇](https://hackmd.io/@sysprog/c-numerics) (2017.04) (2019.08)
* [浮點數運算](https://hackmd.io/@sysprog/c-floating-point) (2020.03)
* [bitwise 操作](/@sysprog/c-bitwise) (2020.02)
* [從打造類似 Facebook 網路服務探討整合開發](/s/B1s8hX1yg) (2017.04)
* [goto 和流程控制](https://hackmd.io/@sysprog/c-control-flow) (2017.11)
* [linked list 和非連續記憶體操作](https://hackmd.io/@sysprog/c-linked-list) (2018.01) (2022.01)
* [Stream I/O, EOF 和例外處理](https://hackmd.io/@sysprog/c-stream-io) (2018.03) (2019.04)
* [未定義行為篇](https://hackmd.io/@sysprog/c-undefined-behavior) (2018.07)
