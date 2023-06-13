TEXT = {
    'start':
    'Привет я работаю с Google таблицами\nПомогу тебе создать таблицу либо модифицировать существующую.\n\
Для начала работы введите /work',
}

CALLBACK = {
    'create_table': 'create_new_table',
    'mod_table': 'modification_table',
    'insert_row': 'insert_row_in_table',
    'append_row': 'append_row_in_table',
    'set_in_cell': 'set_value_in_cell',
    'rename_table': 'update table title'
}

CONNECT_STATUS = {
    'Invalid': 'invalid',
    'Api Error': 'api_error'
}

INSTRUCTION = {
    'Use row': 'Введите строку которую хотите вставить\n\
Слова будут поделены по пробелам\nЕсли хотите поместить 2 слова в одну ячейку\nвведите их через нижнее подчеркивание\n\n\
                Пример\n\n\
Ввод: Имя Фамилия Отчество ->\nВывод: ["Имя", "Фамилия", "Отчество"]\n\n\
Ввод: Возраст Место_жительста Группа_крови ->\nВывод: ["Возраст", "Место жительства", "Группа крови"]',

'Set value in table': ['Введите номер ячейки в формате:\n\nA1', 'Введите данные которые нужно вставить в ячейку']
}