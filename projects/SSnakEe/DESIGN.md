# SsnakEe — Dizaina dokuments

## 1. Nosaukums un žanrs
**SsnakEe** — Snake žanrs.

## 2. Mērķis
- **Uzvara:** piepildīt visu spēles laukumu ar savu čūsku.
- **Zaudēšana:** galva ieskrien sienā, savā vai pretinieka ķermenī.

## 3. Vadība
- **P1:** W (up), S (down), A (left), D (right)
- **P2:** bultiņas ↑ ↓ ← →
- **P:** pauze
- **R:** restart
- **M:** menu
- **ESC:** atpakaļ

## 4. Pamata cikls
Sāc spēli → Pagriez čūsku → Apēd ēdienu → Punkti un garums →
Ieskrien sienā/ķermenī → Game Over → Rekords saglabāts

## 5. Divas custom mehānikas

### Mehānika #1: Local 2-player (Slither.io stils)
Divi spēlētāji uz viena monitora. P1 WASD, P2 bultiņas. Ja viena
čūska ar galvu pieskaras otras **ķermenim**, tā mirst.

### Mehānika #2: Magnēts
Parādās tikai, ja ieslēgts Multi-Food. Paņemot → visi ēdieni tiek
savākti, +5 punkti par katru, čūska izaug.

## 6. Grūtības līmeņi
Čūska paātrinās ik pēc 20 sekundēm (×0.9). Bāze no iestatījumiem.

## 7. Punkti
- Ēdiens: +5
- Magnēts: +5 × ēdienu skaits
- Katra sekunde: +1

## 8. Saglabāšana
Highscore JSON (`highscores.json`). Pozīcija netiek saglabāta.