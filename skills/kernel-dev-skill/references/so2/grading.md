<div class="wy-grid-for-nav">

<div class="wy-side-scroll">

<div class="wy-side-nav-search">

[The Linux Kernel](../index.html)

<div class="version">

5.10.14

</div>

<div role="search">

</div>

</div>

<div class="wy-menu wy-menu-vertical" data-spy="affix" role="navigation" aria-label="Navigation menu">

  - [Operating Systems 2](index.html)
      - [SO2 - General Rules and Grading](#)
          - [General Rules](#general-rules)
              - [1. Laboratory](#laboratory)
              - [2. Final deadline for submitting assignments](#final-deadline-for-submitting-assignments)
              - [3. Assignment Presentations](#assignment-presentations)
              - [4. Rules on Assignments](#rules-on-assignments)
              - [5. Penalties for Plagiarized Assignments](#penalties-for-plagiarized-assignments)
              - [6. Retake/Grade Increase](#retake-grade-increase)
              - [7. Class Redo](#class-redo)
          - [Grading](#grading)
              - [1. Lectures (3 points)](#lectures-3-points)
              - [2. Laboratory (2 points)](#laboratory-2-points)
              - [3. Assignments (5 points + Extra)](#assignments-5-points-extra)
      - [SO2 Lecture 01 - Course overview and Linux kernel introduction](lec1-intro.html)
      - [SO2 Lecture 02 - System calls](lec2-syscalls.html)
      - [SO2 Lecture 03 - Processes](lec3-processes.html)
      - [SO2 Lecture 04 - Interrupts](lec4-interrupts.html)
      - [SO2 Lecture 05 - Symmetric Multi-Processing](lec5-smp.html)
      - [SO2 Lecture 06 - Address Space](lec6-address-space.html)
      - [SO2 Lecture 07 - Memory Management](lec7-memory-management.html)
      - [SO2 Lecture 08 - Filesystem Management](lec8-filesystems.html)
      - [SO2 Lecture 09 - Kernel debugging](lec9-debugging.html)
      - [SO2 Lecture 10 - Networking](lec10-networking.html)
      - [SO2 Lecture 11 - Architecture Layer](lec11-arch.html)
      - [SO2 Lecture 12 - Virtualization](lec12-virtualization.html)
      - [SO2 Lab 01 - Introduction](lab1-intro.html)
      - [SO2 Lab 02 - Kernel API](lab2-kernel-api.html)
      - [SO2 Lab 03 - Character device drivers](lab3-device-drivers.html)
      - [SO2 Lab 04 - I/O access and Interrupts](lab4-interrupts.html)
      - [SO2 Lab 05 - Deferred work](lab5-deferred-work.html)
      - [SO2 Lab 06 - Memory Mapping](lab6-memory-mapping.html)
      - [SO2 Lab 07 - Block Device Drivers](lab7-block-device-drivers.html)
      - [SO2 Lab 08 - File system drivers (Part 1)](lab8-filesystems-part1.html)
      - [SO2 Lab 09 - File system drivers (Part 2)](lab9-filesystems-part2.html)
      - [SO2 Lab 10 - Networking](lab10-networking.html)
      - [SO2 Lab 11 - Kernel Development on ARM](lab11-arm-kernel-development.html)
      - [SO2 Lab 12 - Kernel Profiling](lab12-kernel-profiling.html)
      - [Collaboration](assign-collaboration.html)
      - [Assignment 0 - Kernel API](assign0-kernel-api.html)
      - [Assignment 1 - Kprobe based tracer](assign1-kprobe-based-tracer.html)
      - [Assignment 2 - Driver UART](assign2-driver-uart.html)
      - [Assignment 3 - Software RAID](assign3-software-raid.html)
      - [Assignment 4 - SO2 Transport Protocol](assign4-transport-protocol.html)
      - [Assignment 7 - SO2 Virtual Machine Manager with KVM](assign7-kvm-vmm.html)

<span class="caption-text">Lectures</span>

  - [Introduction](../lectures/intro.html)
  - [System Calls](../lectures/syscalls.html)
  - [Processes](../lectures/processes.html)
  - [Interrupts](../lectures/interrupts.html)
  - [Symmetric Multi-Processing](../lectures/smp.html)
  - [Address Space](../lectures/address-space.html)
  - [Memory Management](../lectures/memory-management.html)
  - [Filesystem Management](../lectures/fs.html)
  - [Debugging](../lectures/debugging.html)
  - [Network Management](../lectures/networking.html)
  - [Architecture Layer](../lectures/arch.html)
  - [Virtualization](../lectures/virt.html)

<span class="caption-text">Labs</span>

  - [Infrastructure](../labs/infrastructure.html)
  - [Introduction](../labs/introduction.html)
  - [Kernel modules](../labs/kernel_modules.html)
  - [Kernel API](../labs/kernel_api.html)
  - [Character device drivers](../labs/device_drivers.html)
  - [I/O access and Interrupts](../labs/interrupts.html)
  - [Deferred work](../labs/deferred_work.html)
  - [Block Device Drivers](../labs/block_device_drivers.html)
  - [File system drivers (Part 1)](../labs/filesystems_part1.html)
  - [File system drivers (Part 2)](../labs/filesystems_part2.html)
  - [Networking](../labs/networking.html)
  - [Kernel Development on ARM](../labs/arm_kernel_development.html)
  - [Memory mapping](../labs/memory_mapping.html)
  - [Linux Device Model](../labs/device_model.html)
  - [Kernel Profiling](../labs/kernel_profiling.html)

<span class="caption-text">Useful info</span>

  - [Recommended Setup](../info/vm.html)
  - [Virtual Machine Setup](../info/vm.html#virtual-machine-setup)
  - [Customizing the Virtual Machine Setup](../info/extra-vm.html)
  - [Contributing to linux-kernel-labs](../info/contributing.html)

</div>

</div>

<div class="section wy-nav-content-wrap" data-toggle="wy-nav-shift">

** [The Linux Kernel](../index.html)

<div class="wy-nav-content">

<div class="rst-content">

<div role="navigation" aria-label="Page navigation">

  - [](../index.html)
  - [Operating Systems 2](index.html)
  - SO2 - General Rules and Grading
  - [View page source](../_sources/so2/grading.rst.txt)

-----

</div>

<div class="document" role="main" itemscope="itemscope" itemtype="http://schema.org/Article">

<div itemprop="articleBody">

<div id="so2-general-rules-and-grading" class="section">

# SO2 - General Rules and Grading[¶](#so2-general-rules-and-grading "Permalink to this headline")

<div id="general-rules" class="section">

## General Rules[¶](#general-rules "Permalink to this headline")

<div id="laboratory" class="section">

### 1\. Laboratory[¶](#laboratory "Permalink to this headline")

There is no formal rule for dividing students; everyone can participate in any laboratory as long as the following rules are respected. Priority for participation is given to students from the respective group (34xC3 or optional). The limit of students in a laboratory is 14 people. Starting from the third week, the participation list in the laboratory is "frozen". Students who have a retake can participate in any laboratory as long as there are available spots. Like other students, the participation list is "frozen" starting from the third week. The division is done on the laboratory hours division page. You can make up for a maximum of 2 laboratories (you can attend another subgroup) (in those laboratories where there are available spots). Laboratories cannot be made up retroactively. You cannot make up a laboratory from the previous week within the same laboratory week. Laboratory activities take place only in the laboratory room. We encourage you to go through the brief and laboratory exercises at home. You can solve exercises at home, but you will have to start from scratch in the laboratory.

</div>

<div id="final-deadline-for-submitting-assignments" class="section">

### 2\. Final deadline for submitting assignments[¶](#final-deadline-for-submitting-assignments "Permalink to this headline")

The final deadline for submitting SO2 assignments is **Wednesday, May 29, 2024, 23:59.**. Beyond this date, assignments cannot be submitted anymore. Please ensure timely submission of assignments with complete information to be graded. We will not accept assignments submitted after this date or assignments not submitted on vmchecker-next. For the testing part, assignments will receive the score indicated from testing on vmchecker-next; tests failed due to reasons unrelated to vmchecker-next will not be graded. Assignments cannot be submitted for the special June 2023 exam session. Assignments can be resubmitted after TODO for the September 2024 exam session. The deadline for submitting assignments for the Fall 2024 session is TODO.

</div>

<div id="assignment-presentations" class="section">

### 3\. Assignment Presentations[¶](#assignment-presentations "Permalink to this headline")

The SO2 team reserves the right to request presentations for some homework assignments. A presentation involves a discussion with at least two assistants about the completion of the assignment, the solution used, and any encountered issues. The purpose of the assignment presentation sessions is to clarify any uncertainties regarding the completion of the assignment and to verify its correctness. Individuals who will present an assignment will be contacted at least 24 hours in advance by the laboratory assistant. Most likely, a 15-minute slot before/after the SO2 class or at the end of the SO2 laboratory session will be used.

</div>

<div id="rules-on-assignments" class="section">

### 4\. Rules on Assignments[¶](#rules-on-assignments "Permalink to this headline")

The assignments for Operating Systems 2 are individual, except when explicitly stated that an assignment can be solved in a team. This is because the primary objective of the assignments is for you to acquire or deepen your practical skills. If the level of collaboration is too high or if you seek solutions online, this objective will not be achieved. Each assignment is to be completed by a student without consulting the source code of their peers.

We understand that teamwork is important, but we do not have the environment to carry out team projects in the Operating Systems 2 course. If you encounter any problems in completing an assignment, use the discussion list or ask the laboratory assistants or course instructors. Our role is to help you solve them. Feel free to rely on the SO2 team.

You can discuss among yourselves within the bounds of common sense; that is, you should not dictate a solution to someone, but you can offer a general idea. If you are the one being asked and providing explanations, please consider redirecting to the discussion list and the SO2 team. It is not allowed to request the solution to an assignment on a site like StackExchange, Rent a Coder, ChatGPT etc. You can ask more generic questions, but do not request the solution to the assignment.

You can freely use code from the laboratory, skeletons provided by us. You can use external resources (GitHub, open-source code, or others) as long as they do not represent obvious solutions to the assignments, publicly available with or without intention. See also the next paragraph.

It is not allowed to publish assignment solutions (even after the end of the course). If you find assignment solutions on GitHub or elsewhere, report them to the discussion list or privately to the laboratory assistant or course instructor. We reiterate that if you need clarification that you would address to older colleagues or other forums, StackExchange, or other sources, use the discussion list and the SO2 team. It is the safest and most honest way to solve problems.

It is not allowed to transfer files between yourselves. In general, we recommend not to screen-share with another colleague, whether for inspiration or to help them with their assignment. Avoid testing an assignment on a colleague's system. There may be exceptions; you can help someone troubleshoot, but please ensure that it does not transition from "let's solve this problem together" to "let me solve your assignment for you". However, we recommend using the discussion list or the SO2 team to ask questions.

</div>

<div id="penalties-for-plagiarized-assignments" class="section">

### 5\. Penalties for Plagiarized Assignments[¶](#penalties-for-plagiarized-assignments "Permalink to this headline")

In general, we consider punitive measures as a last resort. As long as the assignment is completed individually, without problematic source code contribution from external sources, then it is not a plagiarized assignment.

The notion of a plagiarized assignment refers to, without limitation, situations such as:

> 
> 
> <div>
> 
>   - Two assignments that are similar enough to draw this conclusion;
>   - Using source code from the internet that is an obvious solution to the assignment;
>   - Using pieces of code from another colleague;
>   - Accessing another colleague's code during the assignment;
>   - Modifying an existing assignment;
>   - Following another colleague's code;
>   - Direct assistance in completing the assignment (someone else wrote or dictated the code);
>   - Someone else wrote the assignment (voluntarily, for payment, or other benefits).
>   - If two assignments are considered plagiarized, both the source and destination will be penalized equally, without discussions about who plagiarized from whom and whose fault it is.
> 
> </div>

<div class="admonition warning">

Warning

Plagiarizing an assignment results in the elimination of points for the assignments completed up to that session. Any assignment submitted until that session receives a score of 0 and cannot be resubmitted during the current academic year. If there were instances of plagiarized assignments during the semester, it will be possible to obtain points in the summer, for the September session, from assignments **not yet** submitted. We reiterate that our goal is not and will not be penalization for plagiarism. We consider cheating to be dishonest behavior that will be punished if it occurs. However, our goal is to prevent cheating; for this purpose, we offer support and resources from the team in all its forms (discussion list, face-to-face discussions with the SO2 team). Please use them with confidence; we believe that an honest approach to completing assignments will also result in a gain of knowledge and skills for you.

</div>

</div>

<div id="retake-grade-increase" class="section">

### 6\. Retake/Grade Increase[¶](#retake-grade-increase "Permalink to this headline")

In the retake/grade increase session in September, only assignments can be submitted, only the final exam can be retaken, or both. You can continue to submit assignments with the deadlines from the semester, meaning you can achieve a maximum grade of 7 for each assignment. Assignments are submitted using the vmchecker-next interface. If you did not have plagiarized assignments during the semester, you can (re)submit any assignments. If there were instances of plagiarized assignments during the semester, you can submit only assignments not yet submitted during the semester. The submission deadline is TODO

If you do not wish to retake the final exam, you can choose not to participate in the exam. Grades will be recorded in the official catalog, according to the SO2 catalog.

In the special retake/grade increase session in June, only the final exam can be retaken, and no homework assignments can be submitted.

The exam in the retake session will consist of 11 equally weighted topics (for a total of 3 points - one topic is a bonus). Passing the exam is conditional on obtaining 1 point out of the 3 points assigned to the course. In practice, this means correctly solving 3 out of the 11 topics in the exam.

In the case of retaking the final exam, the higher grade will be retained (between the semester grade and the grade from the retake session).

You can participate in only one exam during a session.

</div>

<div id="class-redo" class="section">

### 7\. Class Redo[¶](#class-redo "Permalink to this headline")

If you prefer, you can keep the score from the previous academic year for the entire semester's activity (labs, assignments, course work), and only retake the final exam. You cannot keep the score for individual components of the semester (only assignments or only course work).

If you want to keep the score from the previous academic year for the entire semester's activity, you must announce this at the begining of the semester. Otherwise, the score from the previous academic year's semester will be reset according to the default mode.

By default, the score for the academic year will be reset on October 1. If you do not graduate from the course during the current academic year, you will need to retake it completely during the next academic year.

</div>

</div>

<div id="grading" class="section">

## Grading[¶](#grading "Permalink to this headline")

You must achieve at least 4.5 points out of 10 to pass.

<div id="lectures-3-points" class="section">

### 1\. Lectures (3 points)[¶](#lectures-3-points "Permalink to this headline")

  - Completion of the course is conditioned by obtaining 30% (3 out of 10) of the course score.

  - The lecture score will be obtained from 11 lecture quizzes to be completed before each class (one quiz is a bonus).

  -   - Each course assignment contains a set of 4 questions from the material covered in the previous class (one question is a bonus).
        
          - There will be no final exam.
          - Each question is scored with 0 or 1.
          - A question is scored only if it is fully and correctly answered.
          - A question answered incompletely or one answered completely but with incorrect specifications or errors will not be scored.
          - Course assignments cannot be redone.
          - Each assignment lasts 3 minutes.
          - The score is obtained from the formula min(sum\_of\_assignment\_scores / 10 \* 4/3, 10).
          - The assignments are closed book.

  -   - For those who cannot attend the course assignments or wish to improve their course score, an assignment will be given at the end of the semester (during the last class) covering all the course material.
        
          - The end-of-semester assignment (last class) consists of 11 questions for the 3 course points and lasts 60 minutes.
          - The end-of-semester assignment is open-book. You are allowed to use class notes, books, slides, laptops, or tablets without internet access.
          - Access with mobile phones is not permitted. Phones must be turned off/silent/deactivated during the exam.
          - You may download course materials, labs, or other resources for offline use.

</div>

<div id="laboratory-2-points" class="section">

### 2\. Laboratory (2 points)[¶](#laboratory-2-points "Permalink to this headline")

  - The laboratories are held in EG106, EG306, and PR706.
  - Completion of the laboratory exercises leads to obtaining 10 or 11 points allocated for the laboratory.
  - The final grade for the laboratory is calculated using the formula (sum(l1:l12) / 12).

</div>

<div id="assignments-5-points-extra" class="section">

### 3\. Assignments (5 points + Extra)[¶](#assignments-5-points-extra "Permalink to this headline")

  -   - There are 4 Assignments:
        
          - Assignment 0 - "Kernel API" - 0.5 points
          - Assignment 1 - "Kprobe based tracer" - 1.5 points
          - Assignment 2 - "Driver UART" 1.5 points
          - Assignment 3 - "Software RAID" - 1.5 points

  -   - Extra activities:
        
          - SO2 transport protocol - 2 points
          - SO2 Virtual Machine Manager with KVM - 2 points

  -   - In case the total score for assignments + "Extra" activities exceeds 5 points, the following procedure will be followed:
        
          - 5 points are considered as part of the total score.
          - The difference between the total score and 5 points will be proportionally adjusted relative to the grade obtained in the lecture.

<div class="highlight-c">

<div class="highlight">

    S = A0 + A1 + A2 + A3 + Extra;
    if (S <= 5)
        assignment_grade = S;
    else
        assignment_grade = 5 + (S - 5) * course_grade / 3; // 0 <= course_grade <=3

</div>

</div>

  -   - The verification and scoring of assignments:
        
          - Assignments are tested against plagiarism.
          - Assignments will be automatically verified using the [vmchecker-next](https://github.com/systems-cs-pub-ro/vmchecker-next/wiki/Student-Handbook) infrastructure integrated with moodle.
          - The verification tests are public.
          - Students who upload their assignments on Moodle must wait for the checker's feedback in the feedback section of the assignment upload page.
          - The grade listed in the feedback section will be the final grade for the assigment.
          - There may be exceptional situations where this rule is not considered (for example, if the assignment is implemented solely to pass the tests and does not meet the assignment requirements).
          - The verification system deducts points (automatically) for certain situations (segmentation faults, unhandled exceptions, compilation errors, or warnings) regardless of the test results.
          - Deductions are specified in the instructions list and in the assignment statement.
          - Deductions are subtracted from the assignment grade (maximum of 10) not from the assignment score.

  -   - Late assignments
        
          - Each assignment has a deadline of 2 weeks from the publication date. (exception\! Assignment 0)
          - After the deadline, 0.25 points per day (out of 10, the maximum grade for each assignment) will be deducted for 12 days (up to a maximum grade of 7).
          - The deduction is from the grade (maximum 10), not from the score. An assignment incurs deductions of 0.25 points per day from the maximum grade (10), regardless of its score.
          - For example, if for assignment 3 (scored with 1.5 points) the delay is 4 days, you will receive a deduction of 4 \* 0.25 = 1 point from the grade, resulting in a maximum grade of 9, equivalent to a maximum score of 1.35 points.
          - After 12 days, no further deductions will be made; a maximum grade of 7 can be obtained for an assignment submitted 13 days after the deadline expiration, or 50 days, or more, including during the retake session.

</div>

</div>

</div>

</div>

</div>

<div class="rst-footer-buttons" role="navigation" aria-label="Footer">

[<span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous](index.html "Operating Systems 2") [Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span>](lec1-intro.html "SO2 Lecture 01 - Course overview and Linux kernel introduction")

</div>

-----

<div role="contentinfo">

© Copyright The kernel development community.

</div>

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).

</div>

</div>

</div>

</div>
