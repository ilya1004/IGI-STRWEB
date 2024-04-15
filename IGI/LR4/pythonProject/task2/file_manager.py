from zipfile import ZipFile, ZIP_DEFLATED


class FileManager:

    @staticmethod
    def save_to_file(file_path, data):
        try:
            with open(file_path, 'w') as file:
                file.writelines(data)
                file.close()
        except FileNotFoundError:
            print("File not found.")
            return None
        except IOError:
            print("Cannot write to file")
            return None

    @staticmethod
    def archive_file(file_path, zip_path):
        with ZipFile(zip_path, 'w', compression=ZIP_DEFLATED, compresslevel=3) as myzip:
            myzip.write(file_path)

    @staticmethod
    def get_archive_info(zip_path):
        try:
            with ZipFile(zip_path, "r") as myzip:
                for item in myzip.infolist():
                    if item.is_dir():
                        print(f"Папка: {item.filename}")
                    else:
                        print(f"Файл: {item.filename}")
                    print(f'Название файла(папки): {item.filename},\n'
                          f'Размер: {item.file_size},\n'
                          f'дата создания: {item.date_time}')
        except FileNotFoundError:
            print("File not found.")
            return None
        except IOError:
            print("Cannot write to file")
            return None
