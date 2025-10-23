# Skład drużyny
* Justyna Bladowska
* Daria Grzelak
* Wiktoria Jarząb
* Dominika Szulc

# O projekcie
Zdecydowałyśmy się na stworzenie aplikacji z grą Blackjack. To popularna gra karciana, która cieszy się uznaniem wśród szerokiego grona odbiorców. Szybkie tempo rozgrywki sprawia, że jest ona niezwykle emocjonująca, a przez liczne możliwości taktyczne Blackjack rozwija zdolności planowania graczy oraz uczy podejmowania strategicznych decyzji. Jednocześnie zasady gry są łatwe do zrozumienia, dzięki czemu jest świetnym źródłem rozrywki.

# Instrukcja użytkowania
Aby gra dobrze zadziałała, należy posiadać zainstalowanego Pythona (testowane na Anacondzie) oraz biblioteki pygame, random i textwrap. Należy uruchomić plik blackjack.py. Wyświetli się ekran startowy z opcją uruchomienia nowej gry oraz przejścia do zasad. Po kliknięciu przycisku „Zasady” pojawią się szczegółowa instrukcja użytkowania oraz zasady gry w Blackjacka.

# Historia zmian (planów)
## Faza 1
Blackjack doskonale nadaje się do przeniesienia na aplikację. Gotowy projekt umożliwi użytkownikom grę w Blackjack. Naszym celem jest stworzenie prostej w obsłudze aplikacji z atrakcyjnym interfejsem graficznym.

Tuż po jej uruchomieniu, użytkownicy zobaczą menu, zawierające opcje rozpoczęcia nowej gry oraz instrukcję. Rozgrywka będzie przebiegała między użytkownikiem oraz komputerem. Gracz będzie musiał dokonać wyboru pomiędzy dwoma możliwymi ruchami: Hit (dobranie kolejnej karty) oraz Stand (zaprzestanie dobierania kart, co wiąże się z końcem rundy gracza). Po upływie tury komputera, gra się kończy, a zwycięzca zostaje wyłoniony. 

Elementy, które powinny zostać wykonane, aby aplikacja działała zgodnie z planem, to:
* okienko gry,
* karty,
* implementacja wybierania losowych kart,
* opcje zachowania gracza (warunki, które trzeba spełnić, żeby wygrać),
* opcje zachowania komputera,
* menu (rozpoczęcie nowej rozgrywki oraz wyświetlenie instrukcji),
* dodatkowe elementy dźwiękowe (sygnalizacja rozpoczęcia kolejki gracza itd.).

Aplikacja zostanie oparta przede wszystkim na bibliotece pygame, która zapewni nam podstawowe funkcjonalności.
Inne biblioteki, z których planujemy skorzystać, to pillow – do wyświetlania obrazów – oraz librosa, zapewniająca funkcjonalności muzyczne.

## Faza 2
Plan działania na najbliższy czas:
* zaprogramowanie komputera (zastąpi on krupiera) – jego opcje działania,
* dodanie instrukcji gry blackjack,
* dodanie elementów dźwiękowych,
* poprawienie efektu wizualnego aplikacji (m.in. elementów graficznych – przycisków, dodanie pliku z tyłem karty do obsługi kart nieodkrytych),
* po ukończeniu projektu wyczyszczenie repozytorium z niepotrzebnych plików, dla przejrzystości.

## Ostateczna wersja
Zaprogramowałyśmy działanie komputera oraz wyniki gry. Dodałyśmy zasady, lepszą nawigację pomiędzy poszczególnymi elementami gry (w tym mozliwość rozpoczęcia nowej rozgrywki po zakończeniu poprzedniej) oraz efekty dźwiękowe. Uzupełniłyśmy resztę przycisków i dodałyśmy logo.

Zrezygnowałyśmy z bibliotek pillow i librosa, gdyż ich funkcjonalności zapewnia również biblioteka Pygame. Użyłyśmy natomiast biblioteki textwrap do zawijania tekstu w grze.
