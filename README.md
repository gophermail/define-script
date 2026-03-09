This script was stolen from 'bread on penguins', and modified with AI as her script curled the definition from some api whereas i wanted a offline copy

highlight a word and press a key combo for the definition to pop up in a notification

you need a dictionary file i dont know if you can use any old one, as I have no idea how the python part of the script works lol, but i used a file located here, 
https://kaikki.org/dictionary/rawdata.html more specifically i used this file https://kaikki.org/dictionary/raw-wiktextract-data.jsonl.gz
this website may change over time, hopefully the links are still good

oh i guess dependencies , you need 

    1) sqlite3

    2) libnotify

    3)xclip or wl-paste depending on whether you're on X11 or Wayland

    4)a notification daemon (i used dunst)

    5)python3 (you probably already have this, most distros seem to use python for system stuffs)

and i think thats it for dependencies

the py script and the define script both assume all files are in ~/.local/bin/define-script/ 
so if you are keeping the files elsewhere those paths need to be modified in the scripts

run the python script on the dictionary file 

    python3 build-dictionary.py raw-wiktextract-data.jsonl.gz

(this made my t450s cpu spike over 85f on my bed, i had to move to a table lol)

make the script excutable 

    chmod +x define

if using dwm add the following for windows key + d;

    { Mod4Mask,                     XK_d,      spawn,          SHCMD("~/.local/bin/define-script/define") },

and then sudo make clean install, then quit dwm and startx/login whatever

if not using dwm, you need to run the script i guess by adding a keyboard 
shortcut however your distro does that, i dunno sorry

