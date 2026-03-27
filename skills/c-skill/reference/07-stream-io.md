# Source: https://hackmd.io/@sysprog/c-stream-io

---
tags: DYKC, C, CLANG, C LANGUAGE
---

# [你所不知道的C語言](https://hackmd.io/@sysprog/c-prog/): Stream I/O, EOF 和例外處理
Copyright (**慣C**) 2018, 2019 [宅色夫](http://wiki.csie.ncku.edu.tw/User/jserv)

==[直播錄影](https://youtu.be/6BUlahVE6FE)==

## 資料處理流程

![](https://i.imgur.com/tb1ak2D.png)
data flow for the standard input (0), output (1), and error (2) streams
[ [source](http://www.rozmichelle.com/pipes-forks-dups/) ]


在 UNIX 的設計哲學是 "Everything is a file"，扣除少數的例外 (如 BSD socket)，任何資源都可當作檔案來操作，不過當我們查閱 C 語言手冊和文獻時，"file" 的操作被分類在 stream I/O 中，聽起來有點奇怪吧？而 stream I/O 是 C 語言心裡最軟的一塊，這話怎説？

我們先來看 [<ctype.h>](http://www.cplusplus.com/reference/cctype/) 標頭檔宣告的 [islower()](http://www.cplusplus.com/reference/cctype/islower/) 函式，其作用很單純，就是判定輸入的「字元」是否為英文小寫字元，不過在宣告中，[islower()](http://www.cplusplus.com/reference/cctype/islower/) 函式的參數卻是 int 型態，類似的現象也出現於 getchar() 函式的回傳值，也是 int 型態。在現行 64 位元處理器架構上運作的作業系統常用 32-bit 表示 int 型態，甚至某些作業系統用 64-bit 表示 int 型態，讓我們不禁納悶：「C 語言不是很講究效率嗎？能用 1 個 byte (char) 處理的資料，為何要用 4 個 bytes 甚至更多 (int) 去表達呢？」

簡單來說，要考慮到 EOF (end-of-file)！後者跟編譯器與執行環境有關，上述的 islower() 或 getchar() 之所以將原本 char 型態可保存的資料「擴充」為 int 型態，即是考慮到輸入和輸出的過程可能被某種情況或條件給「打斷」，倘若要深入理解更多， 就得回到 stream I/O 的原理。此外，從 C89, C99 規格就存在的 [signal](http://man7.org/linux/man-pages/man2/signal.2.html)，依據手冊的說法，這是 "ANSI C signal handling"，實務上會在 Stream I/O 使用中作為例外處理機制，本議程預計分析現有開放原始碼專案中的情境，探討 Stream I/O, EOF 和 signal 之間的微妙關聯。
> 延伸閱讀: [Redirection in bash](https://blog.hexrabbit.io/2019/10/22/Redirection-in-bash/)

## 有沒有 C++ 標準幫 Apple 背書的八卦

C++ 標準函式庫竟然有 [ios::good](http://www.cplusplus.com/reference/ios/ios/good/)
![](https://i.imgur.com/erYYXIq.png)
「iOS 真棒！」


## EOF 的發生往往不是單一程式的事

C99 規格書 7.19.6.2 談及 `fscanf` 一類函式的行為, 第 5 段:  

> "A directive composed of white-space character(s) is executed by reading input up to the first non-white-space character (which remains unread), or until no more characters can be read."

end-of-file 的設定是由輸入函式在讀取資料的過程中設定的。 

搜尋 [glibc 原始程式碼](https://sourceware.org/git/?p=glibc.git)，可發現 `EOF` 定義在 `libio/stdio.h`，但這是 `Define ISO C stdio on top of C++ iostreams`

```c
/* The value returned by fgetc and similar
   functions to indicate the end of the file.  */
#define EOF (-1)
```

`ctype.h` 實作於 glibc 原始程式碼的 `ctype/ctype.h`

這裡要補充一點, 在有些系統 (特別是 UNIX 系統) 上, 每一行資料 (這裡只指 text 資料) 必須以 end-of-line 來分割, 包括最後一行. 否則, 某些程式語言在, 或系統處理最後一行時有可能會出問題。

```
〔資料〕<EOL>  
．．．  
〔資料〕<EOF> <-- 有可能會造成問題
```

最好是這樣:
```
〔資料〕<EOL>  
．．．  
〔資料〕<EOL>  
<EOF>
```

以 ctrl-Z 做文字檔的 end-of-file marker 源自 DEC 早期的系統, 後來被 CP/M 借用, 再後來用在 MS-DOS 上。 
  
使用 ctrl-Z 的原因是因為在早期的檔案系統，檔案長度是以 128-byte 的 sector 為單位的, 當檔案的大小不是 sector 的整數倍數的話, ctrl-Z 用來標示檔案的真正結尾, 並以 ctrl-Z 把剩餘的 sector 填滿。

自 MS-DOS 2.0 起就可以正確的記綠檔案的正確長度, 已可不需要用 ctrl-Z 的機制了. 但這個機制到目前還在支援. 因為在某個情況下它非常有用。
  
當你在 console 上用鍵盤來輸入資料時, 可以用 ctrl-Z 來產生 end-of-file 訊息。

```
〔執行〕
1 2 3 4
5 6 7 8^Z
you entered 8 numbers.
```

UNIX 系統上用 ctrl-D 來 signal end-of-file.
  
以目前的系統來說, EOF 只是一個概念上的存在, 文字檔並不需要這個 marker，文字編輯器不會自動的加入這個 marker。

在 MS-Windows  上, ctrl-Z 不再做為檔案大小的依據, 也不會導致 file truncation. Ctrl-Z 可以存在文字檔內, 但它會影響輸入函式的行為: 如果檔案是以 text mode 來開啟的話, ctrl-Z 會終結輸入，即使 ctrl-Z 後面還有資料也是一樣。

[Standard I/O](https://blog.kuoe0.tw/posts/2013/02/22/acm-icpc-about-io/)
C++ iostream 的 `cin`, `cout` 和 C stdio 的 `scanf`, `printf` 效能比較

## signal

```cpp
#include <signal.h>

void (*signal(int sig, void (*func)(int)))(int);
```

或者透過 typedef 得到的等效且簡短的宣告:

```cpp
typedef void (*sig_t) (int);
sig_t signal(int sig, sig_t func);     
```


[C Notes for Professionals](https://goalkicker.com/CBook/CNotesForProfessionals.pdf)
Chapter 31 (對應 Page 208)

[signal numbers](https://en.wikipedia.org/wiki/C_signal_handling#Standard_signals) can be synchronous (like SIGSEGV– segmentation fault) when they are triggered by a malfunctioning of the program itself or asynchronous (like SIGINT - interactive attention) when they are initiated from outside the program, e.g by a keypress as Cntrl-C.

合法的 C11 程式:
```cpp
#include <signal.h> /* signal() */
#include <stdio.h>  /* printf() */
#include <stdlib.h> /* abort()  */

void handler_nonportable(int sig)
{
    /* undefined behavior, maybe fine on specific platform */
    printf("Catched: %d\n", sig);

    /* abort is safe to call */
    abort();
}

sig_atomic_t volatile finished = 0;

void handler(int sig)
{
    switch (sig) {
        /* hardware interrupts should not return */
    case SIGSEGV:
    case SIGFPE:
    case SIGILL:
        /* quick_exit is safe to call */
        quick_exit(EXIT_FAILURE);

    default:
        /* Reset the signal to the default handler,
         * so we will not be called again if things go
         * wrong on return.
         */
        signal(sig, SIG_DFL);

        /* let everybody know that we are finished */
        finished = sig;
        return;
    }
}
int main(void)
{
    /* Catch the SIGSEGV signal, raised on segmentation faults
     * (i.e NULL ptr access)
     */
    if (signal(SIGSEGV, &handler) == SIG_ERR) {
        perror("could not establish handler for SIGSEGV");
        return EXIT_FAILURE;
    }

    /* Catch the SIGTERM signal, termination request */
    if (signal(SIGTERM, &handler) == SIG_ERR) {
        perror("could not establish handler for SIGTERM");
        return EXIT_FAILURE;
    }

    /* Ignore the SIGINT signal, by setting the handler to `SIG_IGN`. */
    signal(SIGINT, SIG_IGN);

    /* Do something that takes some time here, and leaves
     * the time to terminate the program from the keyboard.
     */

    /* Then: */
    if (finished) {
        fprintf(stderr, "we have been terminated by signal %d\n",
                (int) finished);
        return EXIT_FAILURE;
    }

    /* Try to force a segmentation fault, and raise a SIGSEGV */
    {
        char *ptr = 0;
        *ptr = 0;
    }

    /* This should never be executed */
    return EXIT_SUCCESS;
}
```

注意 [quick_exit](https://en.cppreference.com/w/c/program/quick_exit) 在 C11 才出現，在 C99 可改寫為:
```cpp
_exit(EXIT_FAILURE);
```

POSIX recommends the usage of [sigaction()](http://man7.org/linux/man-pages/man2/sigaction.2.html) instead of signal(), due to its underspecified behavior and significant implementation variations. POSIX also defines [many more signals](https://en.wikipedia.org/wiki/Unix_signal#POSIX_signals) than ISO C standard, including SIGUSR1 and SIGUSR2, which can be used freely by the programmer for any purpose.

signal 的存在並非總是「善後」的行為，而是藉由其同步和非同步的處理，讓程式設計者能先專注在 business logic，再來思考例外狀況該如何回應。以 [mazu-editor](https://github.com/jserv/mazu-editor) (媽祖程式碼編輯器) 為例:
```cpp
void init_editor() {
    signal(SIGWINCH, handle_sigwinch);
}

void handle_sigwinch() {
    update_window_size();
    if (ec.cursor_y > ec.screen_rows)
        ec.cursor_y = ec.screen_rows - 1;
    if (ec.cursor_x > ec.screen_cols)
        ec.cursor_x = ec.screen_cols - 1;
    refresh_screen();
}
```

當使用者嘗試調整終端機模擬程式的有效寬度和高度，從原本:
![image](https://hackmd.io/_uploads/HJxoZ7dA6.png)

到後來:
![image](https://hackmd.io/_uploads/HyPiZmO0p.png)

就涉及到刷新畫面的操作，但若程式都要週期性更新，這樣不足以反映操作，於是可藉由 `SIGWINCH` (Window size change) signal 及其註冊的 handler 來實作更新。


## 回顧 CS:APP 第 8 章

- [x] [Exceptional Control Flow: Exceptions and Processes](https://www.cs.cmu.edu/afs/cs/academic/class/15213-m19/www/lectures/14-ecf-procs.pdf) 

![image](https://hackmd.io/_uploads/H1bcbmuRp.png)

* [Error Handling in C programs](https://www.geeksforgeeks.org/error-handling-c-programs/)
    * `errno`
    * `perror`, `strerror`
    * `EXIT_SUCCESS`, `EXIT_FAILURE`

```c
int dividend = 50;
int divisor = 0;
int quotient;

quotient = (dividend/divisor); /* This will produce a runtime error! */
```

觸發 SIGFPE signal

根據 IEEE 754 7.2 節的說明，會產生 quiet NAN 的運算如下：
1. any general-computational or signaling-computational operation on a signaling NaN (see 6.2), except for some conversions (see 5.12)
2. multiplication: multiplication(0, ∞) or multiplication(∞, 0) fusedMultiplyAdd: fusedMultiplyAdd(0, ∞, c) or fusedMultiplyAdd(∞, 0, c) unless c  is a quiet NaN; if c is a quiet NaN then it is implementation defined whether the invalid operation exception is signaled
3. addition or subtraction or fusedMultiplyAdd: magnitude subtraction of infinities, such as: addition(+∞, −∞)
4. division: division(0, 0) or division(∞, ∞)
5. remainder: remainder(x, y), when y is zero or x is infinite and neither is NaN
6. squareRoot if the operand is less than zero
7. quantize when the result does not fit in the destination format or when one operand is finite and the other is infinite

會產生 signal NAN 的運算如下：
1. conversion of a floating-point number to an integer format, when the source is NaN, infinity, or a value that would convert to an integer outside the range of the result format under the applicable rounding attribute
2. comparison by way of unordered-signaling predicates listed in Table 5.2, when the operands are unordered
3. logB(NaN), logB(∞), or logB(0) when logBFormat is an integer format (see 5.3.3).

![image](https://hackmd.io/_uploads/Byg2-X_Cp.png)

![image](https://hackmd.io/_uploads/Hy01MQ_Cp.png)

Page fault

![image](https://hackmd.io/_uploads/ByYlfXO06.png)

> "Time is an illusion. Lunchtime doubly so."
> ― Douglas Adams, The Hitchhiker's Guide to the Galaxy

![image](https://hackmd.io/_uploads/r1yZG7_Ap.png)

* POSIX 中，[exit](http://man7.org/linux/man-pages/man3/exit.3.html) 沒有返回值
* [execve](http://man7.org/linux/man-pages/man2/execve.2.html) 在成功執行時沒有返回值

![image](https://hackmd.io/_uploads/B15-GXd0p.png)

* [fork](https://linux.die.net/man/2/fork)，呼叫 1 次，返回 2 次
* 在 1969 年開發的 UNIX 第一版就提供 fork 系統呼叫，至今超過 50 年，但其在現代計算機架構上運作的類似 UNIX 作業系統 (如 Linux 和 FreeBSD)，實作有其彆扭之處，例如經典的 fork+exec 的「最佳化」(透過 lazy fork)，於是來自 Microsoft Research, Boston University, ETH Zurich 等單位的研究人員，提交論文 [A fork() in the road](https://www.microsoft.com/en-us/research/uploads/prod/2019/04/fork-hotos19.pdf)，回顧這 50 年間 fork 系統呼叫的發展和探討其侷限，建議人們改用 posix_spawn (這是 POSIX.1-2001 規範的一部分) 並徹底捨棄 fork 的使用
* [一個 fork 的面試題](https://coolshell.cn/articles/7965.html)
    + 假設 fork.c 編譯出來的結果是 ``fork``，則可用這個命令計算 '-' 數量: ``./fork | wc -c``
* [In fork() which will run first, parent or child?](http://stackoverflow.com/questions/21586292/in-fork-which-will-run-first-parent-or-child)
    + ``sudo sysctl -w kernel.sched_child_runs_first=1``
* 在 GNU/Linux 上測試：事先開啟兩個虛擬終端機視窗，如下圖
![image](https://hackmd.io/_uploads/r1I7zQO0T.png)
    + 右邊是測試程式 (test.c)，使用 ``watch -n 1 ./test`` 每秒更新執行結果一次。耐心凝視結果一陣子，是否發現輸出結果會跳動？
    + 使用左邊執行 ``sudo sysctl -w kernel.sched_child_runs_first=1``，以便要求 Linux 排程器 (CFS) 讓 child process 優先於 parent process 執行
* [How a fix in Go 1.9 sped up our Gitaly service by 30x](https://about.gitlab.com/2018/01/23/how-a-fix-in-go-19-sped-up-our-gitaly-service-by-30x/)
    * Gitlab 在運作過程中發現其 RPC 處理程式 Gitaly 的 latency 日漸增加，CPU 的使用率也顯著提高, 原本工程團隊以為是 resource leaking 問題，然而透過 pprof 與 cAdivisor (cgroup 分析工具) 分析發現並沒有 leak 的現象, 最後追蹤到 SIGABRT thread dump 中發現問題在於系統呼叫 ForkLock 而該問題指向 clone() 的方式，而這問題在於 Go 1.8 中使用的 fork 方式會複製 parent process memory space，因此當系統逐漸增大後 fork cost 就會變高，於是在 Go 1.9 後改採用 `posix_spawn` 以避免該問題。
* [posix-spawn](https://github.com/rtomayko/posix-spawn)
    > fork(2) calls slow down as the parent process uses more memory due to the need to copy page tables. In many common uses of fork(), where it is followed by one of the exec family of functions to spawn child processes (Kernel#system, IO::popen, Process::spawn, etc.), it's possible to remove this overhead by using special process spawning interfaces (posix_spawn(), vfork(), etc.)
    ![image](https://hackmd.io/_uploads/SyiBz7dAa.png)

- [ ] [Exceptional Control Flow: Signals and Nonlocal Jumps](https://www.cs.cmu.edu/~213/lectures/20-ecf-sigs.pdf)

![image](https://hackmd.io/_uploads/SkJwfmOCa.png)
![image](https://hackmd.io/_uploads/H1tDGmuCp.png)

## 待整理
* [Tearing apart printf()](https://www.maizure.org/projects/printf/)
* [Your terminal is not a terminal: An Introduction to Streams](https://lucasfcosta.com/2019/04/07/streams-introduction.html)
* [The TTY demystified](https://www.linusakesson.net/programming/tty/)