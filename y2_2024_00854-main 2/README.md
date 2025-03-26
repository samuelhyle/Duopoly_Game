# Y2_2024_00854



## Projekti kurssille Y2 2024:

Täältä löytyy peliteoriaan mukautuva ohjelma, jossa kaksi yritystä kilpailevat keskenään markkinoilla tuottamalla hyödykkeitä, yrittäen maksimoida oman kumulatiivisen voittonsa koko pelin aikana.

## Peli
```
## Tiedostot

Pelin pääkoodi ja sen osat löytvät kansiosta ''Duopoly Game''. Peli rakentuu ''main_game_app'' tiedostosta, joka ajaa peliä, ja rakentaa tarvittavan interaktiivisen käyttöliittymän. Tämä päätieodsto hyödyntää pelitilanteiden arvioimiseen ''stats_analyze'' osaa, joka määrittää pelin tuotto/voitto/hinta matriisit, ja ''move_action'' tiedostosta, joka määrittää pelaajien seuraavia liikkeitä, pääasiassa vastapelaajan, eli koneen liikkeitä. 

## Asennusohje

Ohjelma tarvitsee pyöriäkseen seuraavat kirjastot: PySide6 / PyQt6, Numpy, Scipy ja Random. Nämä voi asentaa omalle koneelleen komennolla ''pip install requirements.txt''

## Käyttöohje

Ohjelma ajetaan tiedostolla ''main_game_app.py''.
