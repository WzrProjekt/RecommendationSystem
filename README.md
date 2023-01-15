# RecommendationSystem

Projekt zaliczeniowy z przedmiotu Inżynieria Oprogramowania. 

Projekt polega na stworzeniu systemu rekomendacji filmów.
Dane pochodzą ze strony TMDB.com, a pobrane zostały za pomocą autorskiego skryptu wykorzystując api udostępniane przez TMDB.com oraz bibliotekę requests.
Dane zostały następnie przetworzone przy użyciu bibliotek pandas oraz numpy oraz załadowane do bazy MongoDB.
Do stworzenia rekomendacji wykorzystany został algortym najbliższych sąsiadów, zaimplementowany w bibliotece scikit-learn.
Strona internetowa powstała przy użyciu biblioteki Flask.

Przykładowe wyszukiwania filmów

![image](https://user-images.githubusercontent.com/122667171/212541093-e3189f19-6c54-4594-9dc4-6f31d7973f20.png)

![image](https://user-images.githubusercontent.com/122667171/212541214-5219748b-e46d-465c-8098-0c91154ecfae.png)

![image](https://user-images.githubusercontent.com/122667171/212541235-448f2840-ac63-4bc4-adc7-962067051f9b.png)

Przykład danych surowych (przed obróbką)

![image](https://user-images.githubusercontent.com/122667171/212541728-8c9cf166-0212-4e04-9a7c-b67b07ad71cf.png)

Przykład danych po obróbce (ostatnie kolumny to tytuł z rokiem produkcji, opis i link do plakatu)

![image](https://user-images.githubusercontent.com/122667171/212541363-feeceec3-9383-411e-a09a-bb158ff3aa9c.png)
