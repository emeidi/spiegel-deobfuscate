# spiegel-deobfuscate
Deobfuscates SPIEGEL Plus articles with mangled characters and outputs the HTML either to stdout or to an file named after the article

Das vorliegende Python-Script entschlüsselt chiffrierte SPIEGEL Plus Artikel und gibt den HTML-Code entweder auf stdout oder in eine HTML-Datei — benannt nach der URL — aus.

## Usage
``python spiegel-deobfuscate.py --url http://www.spiegel.de/kultur/gesellschaft/das-reich-warum-die-reichsbuerger-sich-den-falschen-begriff-ausgesucht-haben-a-1123110.html --output file``

``--url http://www.spiegel.de/...`` Self explanatory; the URL pointing to the SPIEGEL Plus article

``--output [stdout|file]`` Print the parsed HTML to

## Hint
Once you open the resulting HTML file in Safari, use Safari Reading Mode to get a nicely formatted and readable article layout (also suited for printing).

## History
Looking at the source code of a SPIEGEL Plus article about MH370 (available in ``example.txt``) I immediately spotted the string "NI481" showing up all over the text. At this moment it dawned upon me that the SPIEGEL web developers probably remembered [ROT13](https://en.wikipedia.org/wiki/ROT13) from their earlier coding days and decided to implement it as an accurate protection of their paywalled articles.
