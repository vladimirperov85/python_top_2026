from models import StoreManager

def main():
    store_manager = StoreManager('order_database.db')
    print('Create manufacturer')
    sony = store_manager.add_manufacturer('Sony')
    print('Sony')

if __name__ == '__main__':
    
    main()