# Yet Another Bombuj Plugin

![Yet Another Bombuj Plugin](plugin.video.yabop/icon.png)

## Kodi Video Plugin / YABoP

Plugin prehrá obsah z Bombuj.eu
Používa na to android api, ktoré používa aj oficiálna [android aplikácia](https://play.google.com/store/apps/details?id=com.tosi.bombujmanual).
(Ľudia z bombuj, keď toto čítate, nemajte mi to za zlé a neblokujte to, mohli ste takýto plugin spraviť aj vy kedykoľvek..)

Kategórie sú presne podľa bombuj. Názvy filmov a seriálov sú trochu jazykovo pomixované, ale tak to vracia api.
Je tam aj jednoduché vyhľadávanie (ako posledná kategória v sekcii), výsledky sú rovnako podľa api.

Plugin aktuálne rozoznáva tieto share stránky:
- openload.io - prehrá a aj sa pokúsi stiahnuť a použiť titulky priamo z openload
- streamango.com - prehrá
- exashare.com - už neexistuje
- netu.tv - nevie prehrať (aj samotné netu nezmyselne presmeruje)
Na ostatné vypíše chybovú hlášku a údaje z nej môžte nahlásiť v diskusii.

Pri openload.io treba každé 4 hodiny potvrdzovať párovanie na [https://olpair.com/](https://olpair.com/) z tej istej siete, z ktorej sa snaží prehrávať.
Je jedno z akého zariadenia, vkľude pozerajte na Android TV a párujte z mobilu na rovnakej wifi, podstatné je, aby šlo o rovnaké pripojenie (rovnaká verejná adresa).

Postrehol som, že niekedy sa stream načítava načítava a nič sa nezačne prehrávať. V logu je potom nasledovná chyba:
ERROR: CDVDDemuxFFmpeg::Open - Error, could not open file https...
ERROR: CVideoPlayer::OpenDemuxStream - Error creating demuxer

A keď zapnete debug log, tak je predtým ešte toto:
ERROR: ffmpeg[1A00]: [mov,mp4,m4a,3gp,3g2,mj2] error reading header

Pričom tá resolvnutá url z logu začne v prehliadači prehrávať.
Chyba bude zrejme vo ffmpeg, môžte googliť. Hádam to niekedy fixnú a zmeny sa potom dostanú aj do kodi samotného..

Pribalené sú tri jazyky - en, sk a cz podľa slováka :-)

## Závislosti
Plugin vyžaduje [script.module.resolveurl](https://github.com/jsergio123/script.module.resolveurl), ktorý si môžte stiahnuť a manuálne nainštalovať priamo z linkovaného github repozitáru stlačením zeleného tlačitka "Clone or download" a následne "Download ZIP".

Odporáčal by som ale inštaláciu repozitáru [repository.tva.common](https://github.com/tvaddonsco/tva-resolvers-repo/tree/master/zips/repository.tva.common), kde je tento plugin publikovaný a teda aj aktualizovaný. ZIP stiahnete kliknutím na detail a následne tlačitkom Download.
Resolveurl sa potom nainštaluje samo.

## Inštalácia a aktualizácia
Aktuálnu verziu nájdete vždy v časti [repository](https://github.com/cache-sk/YABoP/tree/master/repository/plugin.video.yabop) a stiahnete rovnako, ako spomínaný repozitár vyššie.
Plugin následne slúži aj sám sebe ako repozitár, takže vždy keď sem vypublikujem novú verziu, tak sa aktualizuje aj u Vás.

## Diskusia
[https://www.xbmc-kodi.cz/not-yet](https://www.xbmc-kodi.cz/not-yet)

