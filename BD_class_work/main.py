from models import StoreManager
import os
def main():
    db_path = "Mvideo.db"
    store = StoreManager(db_path)
    print(f'База данных создана по пути {os.path.abspath(db_path)}')
    
    try:
        nokia = store.find_manufacturer_by_id(1)
        if not nokia:
            all_manufacturers = store.get_manufacturers()
            nokia = next((m for m in all_manufacturers if 'Nokia' in m.name),None)
        if nokia:
            phone = store.add_product(
                name = '3310',
                manufacturer_id = nokia.id,
                category='Смартфон',
                price = 50000,
                serial_number = 'SN-NK-004565'
            )
            print(f'Добавлен {nokia}')
        else:
            print('Производитель не найден')
    except Exception as e:
        print(f'Error {e}')

        


if __name__ == '__main__':
    main()

