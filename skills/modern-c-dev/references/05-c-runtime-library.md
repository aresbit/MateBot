# Source: https://hackmd.io/@sysprog/c-runtime

---
tags: DYKC, C, CLANG, C LANGUAGE
---

# [你所不知道的 C 語言](https://hackmd.io/@sysprog/c-prog/): 執行階段程式庫 (CRT)
Copyright (**慣C**) 2018 [宅色夫](http://wiki.csie.ncku.edu.tw/User/jserv)

==[直播錄影](https://youtu.be/qAVdTrC7YyU)==

![](https://i.imgur.com/Jhsq82t.png)

## 動機

你想過 C 程式 `int main(int argc, char *argv[])` 背後的運作原理嗎？想過 C 程式既然「從 main() 開始執行」，那從哪裡獲取 argv[] 的內容呢？以及最後 main 函式 return 數值時，又做了什麼處理，才能讓作業系統得知程式執行結果呢？又，atexit() 一類的函式如何確保在 C 程式執行終止階段，得以執行註冊的函式？

要解答上述疑惑，我們就需要理解就 C Run-Time Library (執行階段程式庫)。C 語言開發後 (1973 年)，貝爾實驗室的 Dennis Ritchie 和 Brian Kernighan 就用 C 重寫了絕大多數 UNIX 系統函式，並把其中最常用的部分獨立出來，逐漸演化我們熟知的 `<stdio.h>` 和 `<stdlib.h>` 等標頭檔，而 C run-time library 也是如此成形。隨著 C 語言的廣泛流通，各個 C 編譯器的生產商/個體/團體都遵循老的傳統，在不同平台上都有相對應的 Standard Library，但大部分實現都是與各個平台有關的。為了縮減不同 C 編譯器間的落差，ANSI C 詳細規定 C 語言各個要素的具體含義和編譯器實作要求。
:::info
1972 年到 1973 年間，[C 語言及編譯器](https://www.bell-labs.com/usr/dmr/www/primevalC.html) 就發展出來，1973 年的 [UNIX 第 5 版以 C 語言重寫完成](http://www.unix.org/what_is_unix/history_timeline.html)，驗證了 C 語言和編譯器的可靠度。但 C 語言一直到 1989 年才落實標準化，Dennis M. Ritchie 撰寫的 [The Development of the C Language](https://www.bell-labs.com/usr/dmr/www/chist.html) 提及標準化的緩慢過程
:::

C Run-Time Library 內部包含初始化程式碼，還有錯誤處理機制 (例如 divide by zero 處理)。

## C 語言關鍵字獨到之處

和 C 語言之前的高階語言相比，如 COBOL, Fortran 和 PL/I 等程式語言，C 語言不僅相當低階 (披著高階語言皮的組合語言，從硬體的觀點是 [WYSIWYG](https://en.wikipedia.org/wiki/WYSIWYG))，而且關鍵字和 I/O 無關，換言之，C 語言程式需要透過標準函式庫的函式或者特製的替代品來進行。
* [COBOL Reserved Words](https://www.ibm.com/support/knowledgecenter/zh-tw/SSZJPZ_9.1.0/com.ibm.swg.im.iis.ds.mfjob.dev.doc/topics/r_dmnjbref_COBOL_Reserved_Words.html) 指出 COBOL 程式語言的保留字有 `INPUT` 和 `PRINTING`
* [Fortran Wiki](http://fortranwiki.org/fortran/show/Keywords) 指出自 FORTRAN 77 即有 `input` 這個關鍵字

## 先看 Microsoft 的文件怎麼說

摘錄自 [DLL 和 Visual C++ 執行階段程式庫行為](https://docs.microsoft.com/zh-tw/cpp/build/run-time-library-behavior?view=vs-2017):

* 指定使用動態連結程式庫 (DLL) 時，預設連結器就會包含 Visual C++ 執行階段程式庫 (VCRuntime)
* VCRuntime 包含初始化及終止 C/C++ 可執行檔所需的程式碼。
* VCRuntime 程式碼會提供內部 ==DLL 進入點函式呼叫==
* `_DllMainCRTStartup` 函式會執行基本工作，例如堆疊緩衝區安全性設定，C 執行階段程式庫 (CRT) 初始化及終止，而且會呼叫==建構函式和解構函式==
* `_DllMainCRTStartup` 也呼叫攔截函式的其他程式庫，例如 WinRT、 MFC 和 ATL 來執行他們自己的初始化及終止。如果沒有這些初始化程序，CRT 和其他程式庫，以及靜態變數，就會處於未初始化的狀態。
* 無論你的 DLL 使用的是靜態連結的 CRT，或動態連結的 CRT DLL，都會呼叫 `VCRuntime` 內部初始化和終止常式。

Universal CRT (UCRT) 包含 C99 執行時期的函式與全局變數。`UCRT` 是 Windows component，伴隨 Windows 10 安裝。UCRT 的靜態函式庫、DLL 的 export libraryt、標頭檔是 Windows 10 SDK 的一部分。

`vcruntime` 包含 Visual C++ CRT 實作相關的程式碼，如例外處理、偵錯支援、執行時檢查、類型資訊、實現細節與特定擴充函式。

CRT 初始化庫處理行程啟動（CRT startup)、內部的逐執行緒的初始化、終止。

延伸閱讀:
* [How To Use the C Run-Time](https://support.microsoft.com/en-us/help/94248/how-to-use-the-c-run-time)

## 回到編譯流程

複習 [你所不知道的 C 語言：編譯器和最佳化原理篇](https://hackmd.io/s/Hy72937Me)

思考以下程式的執行: (`hello.c`)
```c
int main() { return 1; }
```

當你在 GNU/Linux 下編譯和執行後 (`gcc -o hello hello.c ; ./hello`)，可用 `echo $?` 來取得程式返回值，也就是 `1`，可是這個返回值總有機制來處理吧？所以你需要一套小程式來做，這就是 C runtime (簡稱 crt)。此外，還有 `atexit` 一類的函式，也需要 C runtime 的介入才能實現。

C 語言和一般的程式語言有個很重要的差異，就是 C 語言設計來滿足系統程式的需求，首先是作業系統核心，再來是一系列的工具程式，像是 ls, find, grep 等等，而我們如果忽略指標操作這類幾乎可以直接對應於組合語言的指令的特色，C 語言之所以需要 runtime，有以下幾個地方：
1.  `int main() { return 1; }` 也就是 `main()` 結束後，要將 exit code 傳遞給作業系統的程式，這部份會放在 `crt0`
2.  exception handling，不要懷疑，C 語言當然有這個特徵，只是透過 `setjmp` 和 `longjmp` 函式來存取，這需要額外的函式庫 (如 libgcc) 來協助處理 stack
3.  算術操作，特別在硬體沒有 FPU 時，需要 [libgcc](https://gcc.gnu.org/onlinedocs/gccint/Libgcc.html) 來提供浮點運算協助
    > 延伸閱讀: [你所不知道的C語言：數值系統篇](https://hackmd.io/s/BkRKhQGae)
    > [ArmHardFloatPort](https://wiki.debian.org/ArmHardFloatPort/VfpComparison) 指出在 gcc 針對 Arm 平台上有三種浮點數處理機制，也就是參數 `-mfloat-abi` 的選項有:
    > * soft - this is pure software
    > * softfp - this supports a hardware FPU, but the ABI is soft compatible.
    > * hard - the ABI uses float or VFP registers.

* 在核心裡的「驗證執行檔」步驟，是要驗證什麼？
* UNIX 的「執行檔」有很多種可能，一個是依據特定格式保存的機械碼，也可能是透過額外程式去解析的 shell script，作業系統核心必須得事先解析並確認這個合法的執行檔，才能著手去執行
* 近來還有對執行檔進行簽章的機制，請見: [ELF executable signing and verification ](https://lwn.net/Articles/532710/)


### `int main(int argc, char *argv[])` 背後的學問

有些書上使用 `void main()` 的函式宣告，這是錯誤的。C++ 之父 Bjarne Stroustrup 在他的 [C++ Style and Technique FAQ](http://www.stroustrup.com/bs_faq2.html#void-main) 中明確地寫著
> "The definition void main( ) { /* … */ } is not and never has been C++, nor has it even been C."

C 語言規範 5.1.2.2.1 :
> It shall be defined with a return type of int and with no parameters or with two parameters (argc and argv) 

複習名詞:
* Arguments: expressions passed into a function
* Parameters: values received by the function
* Caller & callee [呼叫者(通常就是在其他函式呼叫的function) 與 被呼叫者(被呼叫的 function)]


![K2XsAUi](https://hackmd.io/_uploads/BJvJ-u9LC.png)


"argument" 和 "parameter" 在中文翻譯一般寫「參數」或「引數」，常常混淆

- [ ] "argument" 的重點是「傳遞給函式的形式」
* 稱 `argc` 是 argument count
* 稱 `argv` 是 argument vector

- [ ] "parameter" 的重點是「接受到的數值」，比方說 C++ 有 [parameterized type](https://isocpp.org/wiki/faq/templates#param-types)，就是說某個型態可以當作另外一個型態的「參數」，換個角度說，「型態」變成像是數值一樣的參數。
* 延伸閱讀: [Parameter (computer programming)](https://en.wikipedia.org/wiki/Parameter_(computer_programming))
    > These pieces of data are the values of the arguments (often called actual arguments or actual parameters) with which the subroutine is going to be called/invoked. An ordered list of parameters is usually included in the definition of a subroutine, so that, each time the subroutine is called, its arguments for that call are evaluated, and the resulting values can be assigned to the corresponding parameters.

程式會使用函式呼叫，在上圖中高階語言直接將參數傳入即可，那麼在組合語言的時候是如何實作的呢？是透過暫存器? Stack ? memory ?順序又如何呢？所以我們必須要有明確規範。
* 延伸閱讀: [你所不知道的C語言：函式呼叫篇](https://hackmd.io/@sysprog/c-function?)

我們看到包含 `envp` 的宣告:
```c
int main(int argc, char *argv[], char *envp[])
{ ... }
```

故意改寫為以下:
```c
#include <stdio.h>
int main(int argc, char (*argv)[0])
{
    puts(((char **) argv)[0]);
    return 0;
}
```

使用 gdb 觀察:
```shell
(gdb) b main
(gdb) r
(gdb) print *((char **) argv)
$1 = 0x7fffffffe7c9 "/tmp/x"
```

這裡符合預期，但接下來：
```shell
(gdb) x/4s (char **) argv
0x7fffffffe558: "\311\347\377\377\377\177"
0x7fffffffe55f: ""
0x7fffffffe560: ""
0x7fffffffe561: ""
```

看不懂了，要換個方式：
```shell
(gdb) x/4s ((char **) argv)[0]
0x7fffffffe7c9: "/tmp/x"
0x7fffffffe7d0: "LC_PAPER=zh_TW"
0x7fffffffe7df: "XDG_SESSION_ID=91"
0x7fffffffe7f1: "LC_ADDRESS=zh_TW"
```

![](https://i.imgur.com/QndglVq.png)

原來後 3 項是 envp (environment variables)，在 C run-time 傳遞進來的內容和 `printenv` 輸出一致

假設 PID = 31114，那麼我們可觀察:
```shell
cat /proc/31114/cmdline
cat /proc/31114/environ
```

讀取 `argv[0]` 和 `cmdline` 來判斷執行的程式名稱，有個非常巧妙的應用: [BusyBox - The Swiss Army Knife of Embedded Linux](https://busybox.net/downloads/BusyBox.html)

延伸閱讀:
* [深度剖析 C 語言 main 函式](https://blog.csdn.net/z_ryan/article/details/80985101)
* [Advanced Programming in the UNIX® Environment](http://www.apuebook.com/apue3e.html)


## GNU Toolchain

* gcc : GNU compiler collection
* as : GNU assembler
* ld : GNU linker
* gdb : GNU debugger

(過度精簡的) 編譯的流程還有格式

![9c0k1v0](https://hackmd.io/_uploads/SyNH-d98R.png)


.coff 和 .elf 分別表示以下:
* [COFF (common object file format)](https://en.wikipedia.org/wiki/COFF) : 是種用於執行檔、目的碼、共享函式庫 (shared library) 的檔案格式
* [ELF (extended linker format)](https://en.wikipedia.org/wiki/Elf) : GNU/Linux 和 *BSD 上最常用的執行檔格式，用於執行檔、目的碼、共享函式庫和核心的標準檔案格式，用來取代 COFF

依據 [Computer Science from the Bottom Up](https://www.bottomupcs.com/) 來探討
* [GNU Toolchain](https://www.bottomupcs.com/compiling.xhtml)
* [Libraries](https://www.bottomupcs.com/libraries.xhtml)

## 隱藏的 `crt0`

[crt0](https://en.wikipedia.org/wiki/Crt0) (也稱為 `c0`)

[newlib/i386 的實作程式碼](https://github.com/eblot/newlib/blob/master/newlib/libc/sys/linux/machine/i386/crt0.c)
```c
extern char **environ;
extern int main(int argc, char **argv, char **envp);

extern char _end;
extern char __bss_start;

void _start(int args) {
    /*
     * The argument block begins above the current stack frame, because we
     * have no return address. The calculation assumes that sizeof(int) ==
     * sizeof(void *). This is okay for i386 user space, but may be invalid in
     * other cases.
     */
    int *params = &args - 1;
    int argc = *params;
    char **argv = (char **) (params + 1);

    environ = argv + argc + 1;

    /* Note: do not clear the .bss section.  When running with shared
     *       libraries, certain data items such __mb_cur_max or environ
     *       may get placed in the .bss, even though they are initialized
     *       to non-zero values.  Clearing the .bss will end up zeroing
     *       out their initial values.
     */

    tzset(); /* initialize timezone info */
    exit(main(argc, argv, environ));
}
```

延伸閱讀:
* [Creating a C Library](https://wiki.osdev.org/Creating_a_C_Library)