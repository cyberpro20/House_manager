class Flat:
    def __init__(self, flat_number, number_of_rooms, floor_number):
        self.flat_number = flat_number
        self.number_of_rooms = number_of_rooms
        self.floor_number = floor_number
        self.list_resident = []

    def __str__(self):
        residents_names = [resident.resident_name for resident in self.list_resident]
        return f"Flat Number: {self.flat_number}, Number of Rooms: {self.number_of_rooms}, Floor_number: {self.floor_number}, Residents: {', '.join(residents_names)}"

class Resident:
    def __init__(self, resident_name, resident_phone):
        self.resident_name = resident_name
        self.resident_phone = resident_phone
        self.flat_number = None

    def __str__(self):
        return f"Name: {self.resident_name}, Phone: {self.resident_phone}"

class House:
    def __init__(self):
        self.list_flats = []
        self.list_unassigned_residents = []

    def get_flats_by_floor_number(self, floor_number):
        return [flat for flat in self.list_flats if flat.floor_number == floor_number]

    def get_flats_by_room_count(self, number_of_rooms):
        return [flat for flat in self.list_flats if flat.number_of_rooms == number_of_rooms]

class Report:
    @staticmethod
    def all_residents_report(house):
        print("менканці які не закріплені за квартирою:")
        for resident in house.list_unassigned_residents:
            print(resident)

        print("менканці які закріплені за квартирою:")
        for flat in house.list_flats:
            for resident in flat.list_resident:
                print(resident)

    @staticmethod
    def all_flats_report(house):
        for flat in house.list_flats:
            print(flat)

    @staticmethod
    def specific_flat_report(house, flat_number):
        for flat in house.list_flats:
            if flat.flat_number == flat_number:
                print(flat)
                break

    @staticmethod
    def flats_on_specific_floor_report(house, floor_number):
        for flat in house.get_flats_by_floor_number(floor_number):
            print(flat)

    @staticmethod
    def flats_by_type_report(house, number_of_rooms):
        for flat in house.get_flats_by_room_count(number_of_rooms):
            print(flat)

class FileManager:
    @staticmethod
    def save_to_file(house, filename):
        with open(filename, 'w') as file:
            for resident in house.list_unassigned_residents:
                file.write(
                    f"Не закріплений мешканець: Name: {resident.resident_name}, Phone: {resident.resident_phone}\n")

            for flat in house.list_flats:
                file.write(
                    f"Квартира номер {flat.flat_number} на {flat.floor_number} поверсі. Кількість кімнат: {flat.number_of_rooms}. Кількість мешканців: {len(flat.list_resident)}\n")
                for resident in flat.list_resident:
                    file.write(f"Name: {resident.resident_name}, Phone:{resident.resident_phone}\n")

    @staticmethod
    def load_from_file(filename):
        house = House()
        with open(filename, 'r') as file:
            for line in file:
                data = line.strip()
                if data.startswith("Не закріплений мешканець:"):
                    name, phone_data = data.split("Name: ")[1].split(", Phone:")
                    house.list_unassigned_residents.append(Resident(name.strip(), phone_data.strip()))
                elif data.startswith("Квартира номер "):
                    flat_info = data.split(". ")
                    flat_number = int(flat_info[0].split()[2])
                    floor_number = int(flat_info[0].split()[4])
                    number_of_rooms = int(flat_info[1].split()[2])
                    house.list_flats.append(Flat(flat_number, number_of_rooms, floor_number))
                elif data.startswith("Name: "):
                    name, phone_data = data.split("Name: ")[1].split(", Phone:")
                    resident = Resident(name.strip(), phone_data.strip())
                    house.list_flats[-1].list_resident.append(resident)
        return house

class FlatManager:
    def __init__(self, house):
        self.house = house

    def add_flat(self, flat):
        if any(f.flat_number == flat.flat_number for f in self.house.list_flats):
            print("Квартира з таким номером вже існує!")
        else:
            self.house.list_flats.append(flat)

    def remove_flat_by_number(self, flat_number):
        flat_to_remove = next((f for f in self.house.list_flats if f.flat_number == flat_number), None)
        if flat_to_remove:
            self.house.list_flats.remove(flat_to_remove)

class ResidentsManager:
    def __init__(self, house):
        self.house = house

    def add_resident(self, resident):
        self.house.list_unassigned_residents.append(resident)

    def remove_unassigned_resident(self, resident_name):
        resident_to_remove = next((r for r in self.house.list_unassigned_residents if r.resident_name == resident_name), None)
        if resident_to_remove:
            self.house.list_unassigned_residents.remove(resident_to_remove)


def menu():
    house_obj = House()
    flat_mgr = FlatManager(house_obj)
    res_mgr = ResidentsManager(house_obj)

    while True:
        print("--------- Меню ---------")
        print("1. Додати мешканця")
        print("2. Видалити мешканця")
        print("3. Додати квартиру")
        print("4. Видалити квартиру")
        print("5. Закріпити мешканця за квартирою.")
        print("6. Відкрипити мешканця від квартири.")
        print("7. Зберегти інформацію у файл")
        print("8. Завантажити інформацію з файлу")
        print("9. Створити звіт")
        print("10. Вихід")

        choice = input("Ваш вибір: ")
        if choice == "1":
            name = input("Введіть ім'я мешканця: ")
            phone = input("Введіть номер телефону мешканця: ")
            res_mgr.add_resident(Resident(name, phone))
            print(f"Мешканець {name} доданий")
        elif choice == "2":
            if not res_mgr.house.list_unassigned_residents:
                print("Відсутні незакріплені мешканці за квартирою")
            else:
                name = input("Введіть ім'я мешканця для видалення: ")

                if any(r.resident_name == name for r in res_mgr.house.list_unassigned_residents):
                    res_mgr.remove_unassigned_resident(name)
                    print(f"Мешканець {name} видалений")
                else:
                    print(f"Мешканця з ім'ям {name} не знайдено")
        elif choice == "3":
            flat_number = int(input("Введіть номер квартири: "))
            num_rooms = int(input("Введіть кількість кімнат: "))
            floor_number = int(input("Введіть поверх: "))
            flat_mgr.add_flat(Flat(flat_number, num_rooms, floor_number))
        elif choice == "4":
            if not house_obj.list_flats:
                print("Ще не додано жодної квартири")
            else:
                flat_number = int(input("Введіть номер квартири для видалення: "))
                flat_mgr.remove_flat_by_number(flat_number)
        elif choice == "5":
            if not house_obj.list_flats:
                print("Ще не додано жодної квартири")
            else:
                print("Виберіть мешканця із списку:")
                for index, resident in enumerate(house_obj.list_unassigned_residents, 1):
                    print(f"{index}. {resident.resident_name}")

                resident_choice = int(input("Ваш вибір: "))
                selected_resident = house_obj.list_unassigned_residents[resident_choice - 1]

                print("Виберіть квартиру із списку:")
                for index, flat in enumerate(house_obj.list_flats, 1):
                    print(f"{index}. Квартира номер {flat.flat_number} (Кімнат:{flat.number_of_rooms}) на {flat.floor_number} поверсі")

                flat_choice = int(input("Ваш вибір: "))
                selected_flat = house_obj.list_flats[flat_choice - 1]

                selected_flat.list_resident.append(selected_resident)

                house_obj.list_unassigned_residents.remove(selected_resident)
                print(
                    f"Мешканець {selected_resident.resident_name} закріплений за квартирою номер {selected_flat.flat_number}")

        elif choice == "6":
            resident_mappings = []
            for flat in house_obj.list_flats:
                for resident in flat.list_resident:
                    resident_mappings.append((resident, flat))
                    print(f"{len(resident_mappings)}. {resident.resident_name} - Квартира {flat.flat_number}, (Кімнат:{flat.number_of_rooms}) на {flat.floor_number} поверсі")

            if not resident_mappings:
                print("Немає жодного мешканця для відкріплення.")
                continue

            resident_choice = int(input("Виберіть мешканця для відкріплення: "))
            selected_resident, selected_flat = resident_mappings[resident_choice - 1]

            selected_flat.list_resident.remove(selected_resident)

            house_obj.list_unassigned_residents.append(selected_resident)

            print(
                f"Мешканець {selected_resident.resident_name} відкріплений від квартири номер {selected_flat.flat_number}")
        elif choice == "7":
            filename = input("Введіть назву файлу для збереження та вкажіть .txt: ")
            FileManager.save_to_file(house_obj, filename)
            print(f"Інформацію збережено до файлу під назвою {filename}")
        elif choice == "8":
            filename = input("Введіть назву файлу для завантаження та вкажіть .txt: ")
            house_obj = FileManager.load_from_file(filename)
            print(f"Інформацію завантажено із файлу під назвою {filename}")

            flat_mgr = FlatManager(house_obj)
            res_mgr = ResidentsManager(house_obj)
        elif choice == "9":
            print("--------- Звіти ---------")
            print("1. Відобразити повний список мешканців.")
            print("2. Відобразити повний перелік квартир.")
            print("3. Відобразити інформацію про певну квартиру.")
            print("4. Відобразити інформацію про квартири на певному поверсі.")
            print("5. Відобразити інформацію про квартири одного типу.")

            report_choice = input("Ваш вибір звіту: ")

            if report_choice == "1":
                for flat in house_obj.list_flats:
                    for resident in flat.list_resident:
                        print(
                            f"Ім'я: {resident.resident_name}, Телефон: {resident.resident_phone}, Квартира: {flat.flat_number}")

                for resident in house_obj.list_unassigned_residents:
                    print(
                        f"Ім'я: {resident.resident_name}, Телефон: {resident.resident_phone}, Квартира: Не закріплений")

            elif report_choice == "2":
                if not house_obj.list_flats:
                    print("Ще не додано жодної квартири")
                else:
                    for flat in house_obj.list_flats:
                        print(f"Квартира номер {flat.flat_number} на {flat.flat_number} поверсі. Кількість кімнат: {flat.number_of_rooms}. Кількість мешканців: {len(flat.list_resident)}")

            elif report_choice == "3":
                flat_number = int(input("Введіть номер квартири: "))
                selected_flat = next((flat for flat in house_obj.list_flats if flat.flat_number == flat_number), None)
                if selected_flat:
                    print(
                        f"Квартира номер {selected_flat.flat_number} на {selected_flat.floor_number} поверсі. Кількість кімнат: {selected_flat.number_of_rooms}. Кількість мешканців: {len(selected_flat.list_resident)}")
                else:
                    print("Квартира не знайдена.")
            elif report_choice == "4":
                floor_number = int(input("Введіть номер поверху: "))
                flats_on_floor_number = [flat for flat in house_obj.list_flats if flat.floor_number == floor_number]
                for flat in flats_on_floor_number:
                    print(
                        f"Квартира номер {flat.flat_number}. Кімнат: {flat.number_of_rooms}. Кількість мешканців: {len(flat.list_resident)}")

            elif report_choice == "5":
                try:
                    number_of_rooms = int(input("Введіть кількість кімнат у квартирі (наприклад, 'однокімнатна = 1'): "))
                    flats_of_type = [flat for flat in house_obj.list_flats if flat.number_of_rooms == number_of_rooms]
                    if not flats_of_type:
                        print("Квартири з такою кількістю кімнат не знайдено.")
                    for flat in flats_of_type:
                        print(
                            f"Квартира номер {flat.flat_number} на {flat.floor_number} поверсі. Кількість мешканців: {len(flat.list_resident)}")
                except ValueError:
                    print("Будь ласка, введіть дійсне числове значення.")
        elif choice == "10":
            print("До побачення!")
            break
        else:
            print("Будь ласка, введіть коректний варіант вибору з меню.")

menu()