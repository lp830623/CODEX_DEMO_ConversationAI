# Scenariusz Codex Ambassador — ConversationAI

## Przygotowanie

1. Pobierz repo, uruchom `docker compose up --build --wait` i otwórz localhost:8102.
2. Uruchom testy na main. To kompletna wersja awaryjna.
3. Zatrzymaj aplikację, przełącz `git switch demo/start`, przebuduj i zresetuj dane.
4. Zależności, obrazy i dostęp Codexa przygotuj przed pokazem. Aplikacja działa offline;
   sam Codex może wymagać internetu. W razie braku połączenia pokaż gotowy diff i main.
5. Zmiany wykonuj na roboczej gałęzi `git switch -c presentation/session`.

## 20 minut

| Czas | Działanie |
|---|---|
| 0–3 | Dashboard, CALL-001, odtwarzacz i transkrypcja |
| 3–6 | Porównaj deklarację w CALL-001 i sugestię w CALL-005 |
| 6–12 | Codex: analiza repo, mała implementacja i testy |
| 12–16 | Uruchom testy, obejrzyj diff i sprawdź przypadki graniczne |
| 16–20 | Powtórz scenariusz w UI, pytania i wnioski |

## Prompt

```text
Przeanalizuj AGENTS.md i architekturę. Zaimplementuj find_promises w Pythonie i findPromises w TypeScript. Zapisuj wyłącznie jawne zobowiązania konsultanta, cytat, właściciela, frazę terminu lub null, pewność reguły DEMO, evidenceId i status unverified. Sugestia kontaktu klienta nie jest zobowiązaniem konsultanta. Wykorzystaj istniejący widok Promise Tracker, uruchom testy i przeanalizuj CALL-001, CALL-004 oraz CALL-005. Nie zmieniaj kontraktów API.
```

## Kryteria sukcesu

- CALL-001: jawna deklaracja z oryginalnym terminem.
- CALL-004: deklaracja z terminem null.
- CALL-005: brak obietnicy konsultanta.
- Kliknięcie deklaracji pokazuje wypowiedź źródłową.
- Żaden wynik nie oznacza realizacji obietnicy.

## Plan awaryjny

Zachowaj zmiany na gałęzi roboczej, przełącz main, przebuduj i użyj resetu.
Przy problemie z backendem otwórz statyczny eksport `frontend/out` przez lokalny serwer HTTP.
Przy problemie z Codexem pokaż porównanie `demo/start...main` w GitHubie i omów testy.
Testy na demo/start celowo wskazują brak funkcji, więc nie przedstawiaj ich jako awarii środowiska.
