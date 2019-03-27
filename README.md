# Yet Another Bombuj Plugin

![Yet Another Bombuj Plugin](plugin.video.yabop/icon.png)

## Kodi Video Plugin / YABoP

Plugin prehrá obsah z Bombuj.eu.
Používa na to android api, ktoré používa aj oficiálna [android aplikácia](https://play.google.com/store/apps/details?id=com.tosi.bombujmanual).  
(Ľudia z bombuj, keď toto čítate, nemajte mi to za zlé a neblokujte to, mohli ste takýto plugin spraviť aj vy kedykoľvek..)

Kategórie sú presne podľa bombuj. Názvy filmov a seriálov sú trochu jazykovo pomixované, ale tak to vracia api.  
Je tam aj jednoduché vyhľadávanie (ako posledná kategória v sekcii), výsledky sú rovnako podľa api.

Plugin aktuálne rozoznáva tieto share stránky:
- openload.io - prehrá a aj sa pokúsi stiahnuť a použiť titulky priamo z openload
- streamango.com - prehrá a aj sa pokúsi stiahnuť a použiť titulky priamo zo streamango
- exashare.com - už neexistuje
- netu.tv - nevie prehrať (aj samotné netu nezmyselne presmeruje)

Na ostatné vypíše chybovú hlášku a údaje z nej môžte nahlásiť v diskusii.

Pri openload.io treba každé 4 hodiny potvrdzovať párovanie na [https://olpair.com/](https://olpair.com/) z tej istej siete, z ktorej sa snaží prehrávať.
Je jedno z akého zariadenia, vkľude pozerajte na Android TV a párujte z mobilu na rovnakej wifi, podstatné je, aby šlo o rovnaké pripojenie (rovnaká verejná adresa).

Ak si to zapnete v nastaveniach, pokúsi sa otvoriť systémový prehliadač s olpair.com, ak je to potrebné. Je to ale len experiment, keď to nefunguje alebo skončí chybou, vypnite si to.

Pribalené sú tri jazyky - en, sk a cz podľa slováka :-)

## Podpora
Nezabudnite, že bombuj funguje vďaka reklamám, takže občas zájdite na ich stránku bez adblockeru a poklikajte tam cielene na reklamy na stránke :)

## Nastavenia
V plugine pribudli nastavenia:
- cachovanie dát; default zapnuté
- stránkovanie v zoznamoch; default vypnuté
- počet na stránku; default 20
- experimentálne otvorenie olpair.com v prehliadači; default vypnuté

## Závislosti
Plugin vyžaduje [script.module.resolveurl](https://github.com/jsergio123/script.module.resolveurl), ktorý si môžte stiahnuť a manuálne nainštalovať ZIP z linkovaného github repozitáru - stlačte zelené tlačidlo "Clone or download" a následne "Download ZIP".

Odporúčal by som ale inštaláciu kodi repozitáru [repository.tva.common](https://github.com/tvaddonsco/tva-resolvers-repo/tree/master/zips/repository.tva.common), kde je tento plugin publikovaný a teda aj bude aktualizovaný.
ZIP stiahnete kliknutím na detail a následne tlačidlom Download. Resolveurl sa potom nainštaluje samo pri inštalácii tohto pluginu.

Ostatné potrebné knižnice by si mal stiahnuť sám z oficiálneho kodi repozitára.

## Inštalácia a aktualizácia
Aktuálnu verziu nájdete vždy v časti [repository](https://github.com/cache-sk/YABoP/tree/master/repository/plugin.video.yabop) a stiahnete rovnako, ako spomínaný kodi repozitár vyššie.
Plugin následne slúži aj sám sebe ako repozitár, takže vždy keď sem vypublikujem novú verziu, tak sa aktualizuje aj u Vás.

Predpokladám, že inštaláciu zo ZIP súboru a povolenie takejto inštalácie zvládnete sami.

Plugin som kódil na Windows 10 s Kodi verzie 18.1 a otestoval aj s rovnakou verziou na Android TV a Android Boxe z číny - obe nainštalované z Google Play. Iné zariadenia bohužiaľ nemám.

## Známa chyba
Postrehol som, že niekedy sa stream načítava načítava a nič sa nezačne prehrávať. V logu je potom nasledovná chyba:  
ERROR: CDVDDemuxFFmpeg::Open - Error, could not open file https...  
ERROR: CVideoPlayer::OpenDemuxStream - Error creating demuxer

A keď zapnete debug log, tak je predtým ešte toto:  
ERROR: ffmpeg[1A00]: [mov,mp4,m4a,3gp,3g2,mj2] error reading header

Pričom tá resolvnutá url z logu začne v prehliadači prehrávať.  
Chyba bude zrejme vo ffmpeg, môžte googliť. Hádam to niekedy fixnú a zmeny sa potom dostanú aj do kodi samotného..

## Diskusia
[https://www.xbmc-kodi.cz/prispevek-yet-another-bombuj-plugin](https://www.xbmc-kodi.cz/prispevek-yet-another-bombuj-plugin)

## Epilóg
Plugin vznikol ako moje programátorské cvičenie, Kodi samotné som prvý krát nainštaloval 2 týždne predtým a python som dovtedy tiež nevidel.
Z toho dôvodu nedokážem zaručiť, že bude fungovať navždy.  
Pri práci mi pomohli [plugin.video.example](https://github.com/romanvm/plugin.video.example), [plugin.video.bombuj.filmyserialy](https://github.com/KubiszDeny/plugin.video.bombuj.filmyserialy), [plugin.video.sl](https://github.com/Sorien/plugin.video.sl) a samozrejme aj [ujo Google](https://www.google.sk/) ;-)
