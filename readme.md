# Linter С#

**Описание:** Консольное приложение для вывода несовпадений стиля кода C# файла.

## Использование
Сначала нужно установить все модули из `requirements.txt`

```
pip install -r requirements.txt
```

### Примеры использования


- Вывод в консоль работы линтера на файле `TestFiles/Linter/Program.cs`

    ```
    python Scripts/linter.py -p
    ```


- Запуск линтера на `./TestFiles/Linter/Simple/test_offsets_in_block.cs` c использованием флагов из `./TestFiles/Linter/Simple/ttt.txt` и сохранение результата в `test_test.txt`(которого может изначально не существовать) с последующим выводом данных в
консоль(должна быть ошибка)
- 
    ```
    python Scripts/linter.py -f ./TestFiles/Linter/Simple/test_offsets_in_block.cs -conf ./TestFiles/Linter/Simple/ttt.txt -sf test_test.txt -p
    ```
- Запуск линтера на нескольких фалах c выводом данных в консоль

    ```
    python Scripts/linter.py -f ./TestFiles/Linter/Main/Clean/class.cs , ./TestFiles/Linter/Main/WithMistakes/class.cs , ./TestFiles/Linter/Main/WithMistakes/foreach.cs -p
    ```
  
  > На linux перечисление файлов без запятых:
  > ```
  > python Scripts/linter.py -f ./TestFiles/Linter/Main/Clean/class.cs  ./TestFiles/Linter/Main/WithMistakes/class.cs ./TestFiles/Linter/Main/WithMistakes/foreach.cs -p
  > ``` 

## Тестирование
Запуск тестов через `pytest`
 ```
 pytest
 ```


### Справка по ключам

- `-h`, `--help` -- вывод всех флагов
- `-conf` , `--config`  -- Путь до файла с флагами. По умолчанию файл `flags.txt`
- `-sf` , `--save_file` -- Путь, куда сохранять. По умолчанию в файл `mismatches.txt`
- `-p`, `--print` -- Вывести результат в консоль
