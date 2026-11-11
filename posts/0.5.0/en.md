---
title: Voxcade 0.5.0: sounds you roll, files you rename
date: 2026-11-11
summary: Sounds are files of your game now, with a sound maker in the IDE that rolls a coin, a jump or a blast. Songs are text to change and hear. The IDE renames, deletes and keeps up with the folder.
---
This version is about the IDE: more of a game is made without leaving it.

## Sounds are files

A sound is a file of your game now, `sounds/NAME.toml`: a few numbers, a line each, only what differs. Or a recording, `sounds/NAME.wav`. Its name is the file's name. The sounds the engine brings stand in the list too, marked "built in"; MAKE IT YOURS copies one into your game to change.

Coming from an older version with sounds in `conf.lua` (`c.sounds`)? `voxcade sounds GAME --to-files` writes them as files once.

## The sound maker

Open a sound in the IDE and a row of buttons stands over its text: COIN, JUMP, SHOT, BLAST, HIT, POWER UP, BLIP. Each rolls a fresh sound of its sort and plays it; press again for another. Five faders (PITCH, LENGTH, SLIDE, BRIGHT, PUNCH) shape it, UNDO steps back, LOOP plays it again and again while you change it. All of it only writes the text, so what you see is what the game plays. Under the text, USED lists the lines of your game that name the sound.

## Songs, too

A song (`.mml`) is text you change in the IDE, checked while you type; PLAY SONG plays it as it stands.

## The IDE keeps house

- **RENAME and DELETE** with a right click on a file. A rename offers to change the lines of your game that name the file. DELETE goes to the system's trash, with UNDO in the bar.
- **A plus in each heading** of the list makes a new file of that sort: a Lua file, a scenario, a model, a sound, a song.
- **The list follows the folder:** what an agent or another program makes appears by itself.
- **The game's keys** stand under the game while it plays, as your keyboard names them. AGAIN begins it anew; BACK TO THE GAME returns to a game waiting behind a file.
- **What is wrong with the game** is one red line over the main area, with TO THE LINE.
- **BUILD** works in the background and puts the package into your game's own `builds/` folder.
- **NEW** makes every game a git repository with its first commit, where git is installed.
- **No agent installed?** The console says what an agent is and where to get one, for example Claude Code. Everything else works without.

## The picture

Water and glass made of see-through cubes draw as one body instead of a grid of stripes, and show how deep they are. Bent arms and legs of posed figures no longer flicker. A mastering limiter at the end of the sound keeps loud moments clean.

## Getting it

Start Voxcade: the launcher says there is 0.5.0, and UPDATE NOW fetches it. Your games, settings and saves stay. New here? [Download it](/#download) and follow the [guide](/install.html).
