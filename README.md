# Dokumentacja - Przewidywanie Cen Mieszkań w Warszawie

## Streszczenie

Aplikacja służy do przewidywania cen mieszkań w Warszawie z wykorzystaniem modelu uczenia maszynowego. Wykorzystywana będzie zarówno przez osoby chcące sprzedać mieszkanie, jak i przez osoby chcące takie mieszkanie kupić. 

**Dla kupujących:**  
Aplikacja pozwala sprawdzić, czy cena mieszkania jest sprawiedliwa, okazyjna lub znacznie zbyt wysoka.  Porównując cenę od sprzedawcy z ceną z aplikacji, nawet bez żadnego doświadczenia ani wiedzy o rynku mieszkaniowym będziesz w stanie negocjować lub szukać sprawiedliwych cen. 

**Dla sprzedających:**  
Możesz sprawdzić, w jakiej cenie wystawić mieszkanie, oszczędzając czas i omijając koszty związane z tradycyjną wyceną. 

Aplikacja znacznie ułatwia proces kupna/sprzedaży mieszkań i czyni go bezpieczniejszym dla każdej ze stron. 

### Moduły aplikacji: 
- **Moduł API** (FastAPI) - backend RESTful API
- **Moduł UI** (Streamlit) - interfejs graficzny użytkownika

---

## Wykorzystany model regresyjny

**Algorytm:** Gradient Boosting Regressor

**Metryki jakości modelu:**

| Metryka        | Wartość          |
|----------------|------------------|
| **R² Score**   | 0.9646           |
| **MAE**        | 44,982.03 PLN    |

**Dane treningowe:** 4,539 rzeczywistych ogłoszeń z rynku warszawskiego

---

## 1. Dane Wejściowe

Aplikacja przyjmuje następujące parametry wejściowe: 

### 1.1 Parametry wymagane

| Parametr             | Typ    | Opis                         | Zakres wartości |
|----------------------|--------|------------------------------|-----------------|
| `district`           | tekst  | Dzielnica Warszawy           | Bemowo, Białołęka, ... |
| `surface`            | liczba | Powierzchnia mieszkania (m²) | 14 - 102        |
| `rooms_num`          | liczba | Liczba pokoi                 | 1 - 6           |
| `construction_status`| tekst  | Stan wykończenia             | do zamieszkania, do wykończenia, do remontu |
| `market`             | tekst  | Typ rynku                    | pierwotny, wtórny |
| `build_year`         | liczba | Rok budowy                   | 1900 - 2025     |
| `floor_no`           | liczba | Numer piętra                 | 0 - 10          |
| `building_floors_num`| liczba | Liczba pięter w budynku      | 1 - 30          |
| `transit_dur_m`      | liczba | Czas dojazdu do centrum (min)| 5 - 230         |


### 1.2 Ograniczenia walidacji

- Liczba pięter w budynku musi być większa lub równa numerowi piętra mieszkania

---

## 2. Dane Wyjściowe

Aplikacja zwraca przewidywaną cenę mieszkania w formacie: 

| Pole              | Opis                              |
|-------------------|-----------------------------------|
| `predicted_price` | Cena mieszkania w PLN (np. 1344949.96) |

---

### 3 Dostępne endpointy API

#### 3.1 GET /model/options

Zwraca dostępne opcje dla pól kategorycznych (dzielnice, statusy, typy rynku).

Przykładowa odpowiedź:

```
{
"districts": ["Bemowo", "Białołęka", ... ],
"construction_statuses": ["do zamieszkania", "do wykończenia", "do remontu"],
"markets": ["pierwotny", "wtórny"]
}
```
#### 3.2 POST /model/predict

Wykonuje predykcję ceny mieszkania na podstawie podanych parametrów.

Przykładowe żądanie:

```
{
"district": "Mokotów",
"surface": 60.5,
"rooms_num": 3,
"construction_status": "do zamieszkania",
"market": "wtórny",
"build_year": 2005,
"floor_no": 2,
"building_floors_num": 5,
"transit_dur_m": 30
}
```
Przykładowa odpowiedź:

```
{
"predicted_price": "1344949.96"
}
```

## 4. Instalacja i Uruchomienie

### 4.1 Wymagania systemowe

- **Python 3.13.7** zainstalowany i dodany do zmiennych środowiskowych

### 4.2 Kroki instalacji i uruchomienia aplikacji

**Krok 1: Pobranie aplikacji**
1. Wejdź na stronę:  https://github.com/diroxxx/Warsaw_flat_prediction_ml
2. Kliknij przycisk **`Code`**
3. Wybierz opcję **`Download ZIP`**

**Krok 2: Rozpakowanie**
1. Znajdź pobrany plik `Warsaw_flat_prediction_ml-main.zip`
2. Rozpakuj archiwum
3. Przejdź do wypakowanego folderu `Warsaw_flat_prediction_ml`

**Krok 3: Uruchomienie**
1. W folderze `Warsaw_flat_prediction_ml` znajdź plik **`start.bat`**
2. Kliknij dwukrotnie na plik `start.bat`
3. Poczekaj, aż otworzy się okno przeglądarki (pierwsze uruchomienie może zająć kilka minut)

**Krok 4: Korzystanie z aplikacji**
- Aplikacja automatycznie otworzy się w przeglądarce pod adresem: **http://localhost:8501/**
- Jeśli nie otworzyła się automatycznie, wpisz adres ręcznie w przeglądarce

## 5. Struktura Projektu

```
Warsaw_flat_prediction_ml
│
├── start.bat                   # Skrypt uruchamiający aplikację       
├── requirements. txt
├── README.md
|
├── app/                      
│   ├──  streamlit_app.py       # Interfejs graficzny (frontend)
│   └──  api.py                 # Moduł API (backend)   
│
├── model/                      
│   ├── input_model.py          # Definicja danych wejściowych
│   └── model_function.py       # Funkcja predykcji
│
├── ml_model/                  
│   └── flat_model. pkl          # Model uczenia maszynowego
│
├── data/                       # Dane treningowe
│   └── warsaw_flats.csv        
│
└── images/                     
    └── warsaw_image.jpg        
```
