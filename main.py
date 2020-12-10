import json
import os


TYPES = {
    int: 'integer',
    str: 'string',
    list: 'array',
    dict: 'object',
    bool: 'boolean',
    type(None): 'null'
}


def load_json(path):
    with open(path, 'rt') as f:
        raw_json = f.read()
    try:
        result = json.loads(raw_json)
    except json.JSONDecodeError:
        return None
    else:
        return result


def check(event, schema):
    result = ''
    for required_key in schema['required']:
        if required_key not in event.keys():
            result += f'ERROR: Нет необходимого ключа {required_key}. Необходимо добавить пару ключ-значение\n'

        else:
            tmp = schema['properties'][required_key]['type']
            if type(tmp) != list:
                tmp = [tmp]
            if TYPES[type(event[required_key])] not in tmp:
                result += f'ERROR: Несоответсвие типов в поле {required_key}. Исправьте на тип {tmp}\n'

            else:
                if schema['properties'][required_key]['type'] == 'object':
                    result += check(event[required_key], schema['properties'][required_key])

                elif schema['properties'][required_key]['type'] == 'array':
                    for elem in event[required_key]:
                        result += check(elem, schema['properties'][required_key]['items'])

    return result


def main():
    out = open('result.txt', 'wt', encoding='UTF-8')

    for schema_filename in os.listdir(os.path.join(os.getcwd(), 'task_folder', 'schema')):
        schema = load_json(os.path.join(os.getcwd(), 'task_folder', 'schema', schema_filename))
        print('===' + os.path.basename(schema_filename) + '===', file=out)

        if schema is None:
            print('ERROR: Некорректный JSON.\n', file=out)
            continue

        for event_filename in os.listdir(os.path.join(os.getcwd(), 'task_folder', 'event')):
            event = load_json(os.path.join(os.getcwd(), 'task_folder', 'event', event_filename))
            print('---' + os.path.basename(event_filename) + '---', file=out)

            if event is None:
                print('ERROR: Некорректный JSON.\n', file=out)
                continue

            result = check(event, schema)
            if result == '':
                result = 'OK!\n'
            print(result, file=out)

    out.close()


if __name__ == '__main__':
    main()
