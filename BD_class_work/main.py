from models import StoreManager
import os
def main():
    db_path = "Mvideo.db"
    store = StoreManager(db_path)
    print(f'База данных создана по пути {os.path.abspath(db_path)}')
    try:
        pass
        
        # found = store.find_manufacturer_by_id(3)
        # if found:
        #     print(found)
        # else:
        #     print('Not found')
        # upd = store.update_manufacturer(3, 'MICROSOFT')
        # if upd:
        #     upd = store.find_manufacturer_by_id(3)
        #     print(f'Обновлен {upd}')
        # else:
        #     print('Not found')
        # manufacturers = store.get_manufacturers()
        # for manufacturer in manufacturers:
        #     print(manufacturer)
        




    except Exception as e:
        print(f'{e}')
        
    


if __name__ == '__main__':
    main()

