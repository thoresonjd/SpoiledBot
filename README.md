# **Spoiled Bot**

A Discord bot that behaves like a spoiled brat and screws with your messages!

## **Author**

Justin Thoreson

## **Spoiler Modes**

Spoiled Bot has four modes:
* `OFF` - Does nothing
* `SPOIL` - Unveils a message already marked as a spoiler
* `UNSPOIL` - Marks a visisble message as a spoiler
* `INVERT` - Hides visible parts of a message and reveals hidden parts of a message

## **Pain Levels**

Spoiled bot will mark message content as spoiler depending on two levels of pain:
* `NORMAl` - Marks the entire message as a spoiler 
* `AGONY` - Marks each individual character in a message as a spoiler

## **Example**

When the mode is set to `INVERT`, and the level is set to `AGONY`, the original message:

`Hello, ||world!||`

![](./assets/example-before.png)

becomes:

`||H||||e||||l||||l||||o||||,|||| ||world!`

![](./assets/example-after.png)