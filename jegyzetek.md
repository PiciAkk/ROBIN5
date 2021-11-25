# Jegyzetek

## `parameterTeszt(args)`

A `main()` függvény paraméter-tesztelését végző függvény kivitelezhető lenne egy több sorba tördelt egysoros `if`es expressionnel (kifejezéssel) is. 

```python
def parameterTeszt(args):
    futtatandoKod = (
        """raise Exception("Csomagnév nincs specifikálva!")""" \
            if len(args) < 3 else \
        """raise Exception("Túl sok paraméter")""" \
            if len(args) > 3 else \
        """"""
    ); exec(futtatandoKod)
```

itt azért szükséges a tripla idézőjel, mert a stringben többször is szerepel egy idézőjel.

## `parameterTeszt(args)`

Ez a függvény kivitelezhető lenne a mostani formájában a `csomagkezelő` osztályba/classba áthelyezve is.

## `listazas()`

Ez a függvény kivitelezhető lenne `yield`-elés nélkül is, ha egy `return`-nel visszaadnánk egy listát, ami a `for` ciklusban (az eddig `yield`-elt elemekkel) töltődik fel.

```python
def listazas():
    csomagNevek = []
    modulok = os.listdir("csomagok")
    for modul in modulok:
        csomagNevek.append(os.path.splitext(modul)[0])
    return csomagNevek
```

Ebben az esetben nem is kéne listává alakítani a visszatérési értéket, mert a függvény nem `generator`-t adna vissza, hanem egy listát.