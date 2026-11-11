---
title: Voxcade 0.5.0: Geräusche würfeln, Dateien umbenennen
date: 2026-11-11
summary: Geräusche sind jetzt Dateien deines Spiels, und ein Geräuschmacher in der IDE würfelt eine Münze, einen Sprung oder einen Knall. Songs sind Text zum Ändern und Anhören. Die IDE benennt um, löscht und folgt dem Ordner.
---
In dieser Version geht es um die IDE: Mehr von einem Spiel entsteht, ohne sie zu verlassen.

## Geräusche sind Dateien

Ein Geräusch ist jetzt eine Datei deines Spiels, `sounds/NAME.toml`: ein paar Zahlen, je eine Zeile, nur was abweicht. Oder eine Aufnahme, `sounds/NAME.wav`. Sein Name ist der Dateiname. Die Geräusche, die die Engine mitbringt, stehen auch in der Liste, als „built in“ markiert; MAKE IT YOURS kopiert eins in dein Spiel, damit du es ändern kannst.

Kommst du von einer älteren Version mit Geräuschen in `conf.lua` (`c.sounds`)? `voxcade sounds SPIEL --to-files` schreibt sie einmal als Dateien.

## Der Geräuschmacher

Öffne ein Geräusch in der IDE, und über seinem Text steht eine Reihe Knöpfe: COIN, JUMP, SHOT, BLAST, HIT, POWER UP, BLIP. Jeder würfelt ein neues Geräusch seiner Sorte und spielt es; noch ein Druck würfelt das nächste. Fünf Regler (PITCH, LENGTH, SLIDE, BRIGHT, PUNCH) formen es, UNDO geht einen Schritt zurück, LOOP spielt es immer wieder, während du änderst. Alles schreibt nur den Text: Was du siehst, spielt das Spiel. Unter dem Text listet USED die Zeilen deines Spiels, die das Geräusch nennen.

## Songs auch

Ein Song (`.mml`) ist Text, den du in der IDE änderst und der beim Tippen geprüft wird; PLAY SONG spielt ihn, wie er dasteht.

## Die IDE hält Ordnung

- **RENAME und DELETE** mit einem Rechtsklick auf eine Datei. Beim Umbenennen bietet die IDE an, die Zeilen deines Spiels zu ändern, die die Datei nennen. DELETE legt in den Papierkorb des Systems, mit UNDO in der Leiste.
- **Ein Plus in jeder Überschrift** der Liste legt eine neue Datei der Sorte an: eine Lua-Datei, ein Szenario, ein Modell, ein Geräusch, einen Song.
- **Die Liste folgt dem Ordner:** Was ein Agent oder ein anderes Programm anlegt, erscheint von selbst.
- **Die Tasten des Spiels** stehen unter dem Spiel, solange es läuft, so wie deine Tastatur sie nennt. AGAIN beginnt es neu; BACK TO THE GAME führt zu einem Spiel zurück, das hinter einer Datei wartet.
- **Was am Spiel nicht stimmt,** steht als eine rote Zeile über dem Hauptbereich, mit TO THE LINE.
- **BUILD** arbeitet im Hintergrund und legt das Paket in den Ordner `builds/` deines Spiels.
- **NEW** macht jedes Spiel zu einem Git-Repository mit erstem Commit, wo Git installiert ist.
- **Kein Agent installiert?** Die Konsole sagt, was ein Agent ist und wo es einen gibt, zum Beispiel Claude Code. Alles andere geht ohne.

## Das Bild

Wasser und Glas aus durchsichtigen Würfeln werden als ein Körper gezeichnet statt als Gitter aus Streifen und zeigen, wie tief sie sind. Gebeugte Arme und Beine von Figuren in Pose flimmern nicht mehr. Ein Mastering-Limiter am Ende des Tons hält laute Momente sauber.

## So bekommst du sie

Starte Voxcade: Der Launcher meldet, dass es 0.5.0 gibt, und UPDATE NOW holt sie. Deine Spiele, Einstellungen und Spielstände bleiben. Neu hier? [Lad es herunter](/de/#download) und folg der [Anleitung](/de/install.html).
