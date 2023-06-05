# Przypadki dla czterech błędów w wiadomości

## 1)

### Oryginalna wiadomość

[9, 9, 13, 2, 3, 8, 2, 4, 3, 14, 0, 15, 5, 0, 13]

### Popsuta wiadomość

[9, 15, 13, 8, 3, 1, 2, 4, 6, 14, 0, 15, 5, 0, 13]

### Odkodowana wiadomość

[9, 15, 13, 8, 3, 1, 2, 4, 6, 14, 0, 15, 5, 0, 13]

### Powód

Syndrom wyniósł zero -> Wiadomość została zamieniona na inną, ale dalej poprawną wiadomość dla której syndrom wyniósł
zero

## 2)

Z reszty obserwacji, dla wszystkich wiadomości z czterema błędami powodem poprawnego odkodowania wiadomości były
przypadki, kiedy syndromy wiadomości wyniosły zero. Ciężko coś z takim przypadkiem zrobić, ponieważ musielibyśmy zawsze
pesymistycznie zakładać, że każda wiadomość zawiera minimum jeden błąd

# Przypadki dla czterech błędów w wiadomości i dwóch w części korekcyjnej

## 1)

### Oryginalna wiadomość

[4, 6, 2, 8, 1, 8, 7, 8, 7, | 0, 11, 11, 10, 8, 15]

### Popsuta wiadomość

[13, 6, 2, 8, 12, 8, 12, 8, 14, | 11, 11, 11, 15, 8, 15]

### Odkodowana wiadomość

[13, 8, 2, 8, 12, 8, 12, 8, 14, | 11, 2, 11, 3, 8, 15]

### Hamming-distance(Oryginalna, popsuta)

6

### Hamming-distance(Odkodowana, popsuta)

3

### Hamming-distance(Oryginalna, odkodowana)

8

## 2)

### Oryginalna wiadomość

[15, 9, 7, 13, 9, 2, 1, 8, 13, | 6, 6, 15, 7, 1, 13]

### Popsuta wiadomość

[15, 11, 5, 13, 14, 13, 1, 8, 13, | 6, 6, 15, 3, 2, 13]

### Odkodowana wiadomość

[15, 11, 13, 13, 14, 13, 1, 8, 13, | 6, 6, 1, 3, 2, 14]

### Hamming-distance(Oryginalna, popsuta)

6

### Hamming-distance(Odkodowana, popsuta)

3

### Hamming-distance(Oryginalna, odkodowana)

8

## 3)

### Oryginalna wiadomość

[6, 15, 7, 11, 1, 2, 9, 6, 14, | 9, 3, 0, 10, 14, 0]

### Popsuta wiadomość

[13, 9, 3, 11, 1, 2, 9, 6, 12, | 4, 3, 0, 10, 14, 11]

### Odkodowana wiadomość

[13, 3, 3, 3, 1, 2, 13, 6, 12, | 4, 3, 0, 10, 14, 11]

### Hamming-distance(Oryginalna, popsuta)

6

### Hamming-distance(Odkodowana, popsuta)

3

### Hamming-distance(Oryginalna, odkodowana)

8