import re
from functools import reduce
from task2.file_manager import FileManager


class Task2:
    def __init__(self):
        self.text_data = ""

    def solve(self):
        self.read_text_file()
        res = self.__show_text_parameters()
        res += self.__show_string_parameters()
        file_path = "task2_res.txt"
        file_path_zip = "task2_res_zip.zip"
        FileManager.save_to_file(file_path, res)
        FileManager.archive_file(file_path, file_path_zip)
        FileManager.get_archive_info(file_path_zip)

    def __show_text_parameters(self):
        reg_count_sentences = r"(\.|\.\.\.|\?|\!)"
        lst = self.count_occurrences(reg_count_sentences)
        print(f"Количество предложений в тексте: {len(lst)}")
        res = f"Количество предложений в тексте: {len(lst)}"
        print(f"Количество повествовательных предложений в тексте: {lst.count(".") + lst.count("...")}")
        res += f"Количество повествовательных предложений в тексте: {lst.count(".") + lst.count("...")}"
        print(f"Количество вопросительных предложений в тексте: {lst.count("?")}")
        res += f"Количество вопросительных предложений в тексте: {lst.count("?")}"
        print(f"Количество побудительных предложений в тексте: {lst.count("!")}")
        res += f"Количество побудительных предложений в тексте: {lst.count("!")}"

        prev_index = 0
        lens = []
        for i in range(len(lst)):
            txt = self.text_data
            index = self.text_data.find(lst[i])
            sent = txt[prev_index: index]
            lens.append(len([i for i in sent if i.isalpha()]))
            prev_index = index + 2

        print(f"Средняя длина предложений в символах: {sum(lens) / len(lens)}")
        res += f"Средняя длина предложений в символах: {sum(lens) / len(lens)}"

        reg_word = r"\b\w+\b"
        lst = self.count_occurrences(reg_word)

        print(f"Средняя длина слов в символах: {reduce(lambda x, y: x + len(y), lst, 0) / len(lst):.3f}")
        res += f"Средняя длина слов в символах: {reduce(lambda x, y: x + len(y), lst, 0) / len(lst):.3f}"

        reg = r"(:|;){1}\-*(\(|\)|\[|\])+"
        lst = self.count_occurrences(reg)
        print(f"Количество смайликов в заданном тексте: {len(lst)}")
        res += f"Количество смайликов в заданном тексте: {len(lst)}"

        reg = r"\d{4}-\d{2}-\d{2}"
        lst = self.count_occurrences(reg)
        print("Список дат в формате YYYY-MM-DD:")
        res += "Список дат в формате YYYY-MM-DD:"
        print(*lst)
        res += " ".join(lst)

        return res

    def __show_string_parameters(self):
        str_q = input("\nВведите строку на английском языке:\n")
        reg = r"\b[A-z]*[qwrtpsdfghjklzxcvbnmQWRTPSDFGHJKLZXCVBNM][aeiouyAEIOUY][A-z]\b"
        lst = self.count_occurrences(reg, str_q)
        print("Список слов, у которых третья с конца буква согласная, а предпоследняя – гласная:")
        res = "Список слов, у которых третья с конца буква согласная, а предпоследняя – гласная:"
        print(*lst)
        res += " ".join(lst)

        reg_word = r"\b\w+\b"
        lst = self.count_occurrences(reg_word, str_q)
        print(f"Количество слов в строке: {len(lst)}")
        res += f"Количество слов в строке: {len(lst)}"

        max_word = max(lst, key=lambda x: len(x))
        print(f"Самое длинное слово в строке: {max_word} под номером {lst.index(max_word) + 1}")
        res += f"Самое длинное слово в строке: {max_word} под номером {lst.index(max_word) + 1}"

        print(f"Нечетные слова в строке:")
        res += f"Нечетные слова в строке:"
        for i in range(len(lst)):
            if i % 2 == 1:
                print(lst[i], end=" ")
                res += f"{lst[i]} "
        print()
        res += "\n"
        return res

    def read_text_file(self, file_path="task2_data.txt"):
        try:
            with open(file_path, 'r') as file:
                self.text_data = file.read()
        except FileNotFoundError:
            print("File not found.")
            return None

    def count_occurrences(self, reg, txt=""):
        if txt == "":
            txt = self.text_data
        matches = re.findall(reg, txt)
        return matches
