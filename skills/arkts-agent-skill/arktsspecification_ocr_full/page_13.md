## INTRODUCTION

This document presents complete information on the new common-purpose, multiparadigm programming language called ArkTS.

### 1.1 Overall Description

The ArkTS language combines and supports features that have already proven helpful and powerful in many well-known programming languages.

ArkTS supports imperative, object-oriented, functional, and generic programming paradigms, and combines them safely and consistently.

At the same time, ArkTS does not support features that allow software developers to write dangerous, unsafe, or inefficient code. In particular, the language uses the strong static typing principle. Object types are determined by their declarations, and no dynamic type change is allowed. The semantic correctness is checked at compile time.

ArkTS is designed as a part of the modern language manifold. To provide an efficient and safely executable code, the language takes flexibility and power from TypeScript and its predecessor JavaScript, and the static typing principle from Java and Kotlin. The overall design keeps the ArkTS syntax style similar to that of those languages, and some of its important constructs are almost identical to theirs on purpose.

In other words, there is a significant common subset of features of ArkTS on the one hand, and of TypeScript, JavaScript, Java, and Kotlin on the other. Consequently, the ArkTS style and constructs are no puzzle for the TypeScript and Java users who can intuitively sense the meaning of most constructs of the new language even if not understand them completely.

This stylistic and semantic similarity permits smoothly migrating the applications originally written in TypeScript, Java, or Kotlin to ArkTS.

Like its predecessors, ArkTS is a relatively high-level language. It means that the language provides no access to low-level machine representations. As a high-level language, ArkTS supports automatic storage management, i.e., all dynamically created objects are deallocated automatically soon after they are no longer available, and deallocating them explicitly is not required.

ArkTS is not merely a language, but rather a comprehensive software development ecosystem that facilitates the creation of software solutions in various application domains.

The ArkTS ecosystem includes the language along with its compiler, accompanying documents, guidelines, tutorials, the standard library (see Standard Library), and a set of additional tools that perform transition from other languages (currently, TypeScript and Java) to ArkTS automatically or semi-automatically.

The ArkTS language as a whole is characterized by the following:
