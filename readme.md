# Linter С#

**Авторы:** Голик Тимофей, Суюндиков Руслан

**Описание:** Консольное приложение для вывода несовпадений стиля кода C# файла.

## Использование

Вывод в консоль работы линтера на одном из тестовых файлов

```
python linter.py -p
```

Запуск линтера на `TestFiles/Linter/test2.cs` и сохранение результата в `mismatches.txt` с последующим выводом данных в
консоль

```
python linter.py -f TestFiles/Linter/test2.cs -sf mismatches.txt -p
```

### Справка по ключам

- `-h`, `--help` -- вывод всех флагов
- `-conf` , `--config`  -- Путь до файла `.EditorConfig`(Пока не работает)
- `-sf` , `--save_file` -- Путь, куда сохранять. По умолчанию в файл `mismatches.txt`
- `-p`, `--print` -- Вывести результат в консоль
