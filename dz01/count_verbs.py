import ast
import os
import collections
from nltk import pos_tag, download


def convert_to_flat_list(old_list):
    """ Return a flat list [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    flat_list_of_words = sum([list(item) for item in old_list], [])
    return flat_list_of_words


def is_verb(word):
    if not word:
        return False

    tagged_word = pos_tag([word])
    word, tag = tagged_word[0]
    attribute_of_verb = 'VB'
    return tag == attribute_of_verb


def collect_file_names(dir_name, files, file_names):

    for file in files:
        if not file.endswith('.py'):
            continue
        file_names.append(os.path.join(dir_name, file))

    return file_names


def create_file_names(path):
    file_names = []

    for dir_name, dirs, files in os.walk(path, topdown=True):
        file_names = collect_file_names(dir_name, files, file_names)

    return file_names


def generate_trees(path, with_file_names=False, with_file_content=False):
    file_names = create_file_names(path)
    trees = []

    for filename in file_names:
        with open(filename, 'r', encoding='utf-8') as attempt_handler:
            main_file_content = attempt_handler.read()
        try:
            tree = ast.parse(main_file_content)
        except SyntaxError as e:
            print(e)
            tree = None

        if with_file_names:
            if with_file_content:
                trees.append((filename, main_file_content, tree))
            else:
                trees.append((filename, tree))
        else:
            trees.append(tree)

    filtered_trees = [tree for tree in trees if tree]
    return filtered_trees


def eject_verbs_from_function_name(function_name):
    verbs = [word for word in function_name.split('_') if is_verb(word)]
    return verbs


def is_magic_name(func):
    return func.startswith('__') and func.endswith('__')


def extract_functions_from_tress(filtered_trees):
    list_of_function = [[node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                        for tree in filtered_trees]

    flat_list_of_names = convert_to_flat_list(list_of_function)
    names_of_functions = [func for func in flat_list_of_names if not (is_magic_name(func))]
    return names_of_functions


def find_top_verbs_in_path(path, top_size=10):
    filtered_trees = generate_trees(path)

    names_of_fuctions = extract_functions_from_tress(filtered_trees)

    full_list_of_words = [eject_verbs_from_function_name(function_name) for function_name in names_of_fuctions]
    verbs = convert_to_flat_list(full_list_of_words)
    top_verbs = collections.Counter(verbs).most_common(top_size)
    return top_verbs


def calculate_verbs():
    projects = [
        'django',
        'flask',
        'pyramid',
        'reddit',
        'requests',
        'sqlalchemy',
    ]

    verbs_with_frequency = []
    for project in projects:
        path = os.path.join('.', project)
        top_verbs = find_top_verbs_in_path(path)
        verbs_with_frequency += top_verbs

    return verbs_with_frequency


def show_occurrence_of_verbs(verbs_with_frequency):

    top_size = 200
    print('total %s words, %s unique' % (len(verbs_with_frequency), len(set(verbs_with_frequency))))
    word_with_occurence = collections.Counter(verbs_with_frequency).most_common(top_size)
    for word, occurence in word_with_occurence:
        print(word, occurence)


if __name__ == '__main__':
    verbs_with_frequency = calculate_verbs()
    show_occurrence_of_verbs(verbs_with_frequency)
