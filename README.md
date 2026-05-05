# FireStation Locator – Optymalizacja Lokalizacji Służb Ratunkowych

Projekt ma na celu znalezienie optymalnego miejsca na budowę remizy straży pożarnej w wybranym obszarze, minimalizując maksymalną odległość do najdalszego punktu.

## Cel projektu
Algorytm rozwiązuje problem optymalizacji lokalizacji służb ratunkowych, stosując kryterium **minimax**. Celem jest zapewnienie, że w najgorszym możliwym scenariuszu czas dojazdu straży pożarnej do dowolnego budynku w miasteczku będzie jak najkrótszy.

## Algorytm i Teoria
Projekt opiera się na teorii grafów i problemie **centrum grafu** (p-center problem dla p=1):
1.  **Reprezentacja**: Miasteczko jest modelowane jako graf ważony $G = (V, E)$, gdzie $V$ to budynki/skrzyżowania, a $E$ to drogi.
2.  **Macierz odległości**: Wyznaczana za pomocą algorytmu **Dijkstry**.
3.  **Optymalizacja**: Wybór wierzchołka $u$, który minimalizuje wartość $e(u) = \max_{v \in V} d(u, v)$.

## Technologie
- **Python 3.x**
- **Matplotlib**: Wizualizacja wyników na płaszczyźnie.
- **Pandas**: Przetwarzanie danych o infrastrukturze.

## Struktura Projektu
- `data/`: Dane wejściowe (pliki CSV).
- `src/`: 
    - `logic.py`: Implementacja algorytmu wyznaczania centrum.
    - `visualization.py`: Skrypty do generowania map.
- `main.py`: Główny punkt wejścia do aplikacji.
