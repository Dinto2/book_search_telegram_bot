# book_search_telegram_bot
A simple telegram bot that, when it receives text, explores a csv table and returns a list of links to files that match with the message sent.

In this case they're pdfs used for educational purposes. However, it can be applied for different purposes, due to the fact that the string search is performed on one column in order to return not only the match but also its link in the other column.

![bot_library](https://github.com/Dinto2/book_search_telegram_bot/assets/91417517/e9280dae-35c7-4f0a-875d-3f9625d3d636)

What you need:
1. Create a Telegram bot via @BotFather
2. A csv table (or another format) where the files you want to quickly browse are listed, and the links to each of these in the next column (So, for each file you have 'NAME' and 'LINK' columns).
   
How to use:
1. Once your Telegram bot is configured, you must modify the code with your token. Nothing else. Since the input does not need any command configured from Telegram, the code will work without any problem.
2. The bot will have a csv table loaded with two columns: one of text type with the names of the files to search, and another with the links of these (in case you store them in a drive folder or similar). When sending a text string, it will search for matches in the first column, and return up to five results: first the file name, and then the corresponding link.
 
