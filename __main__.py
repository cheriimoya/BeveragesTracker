from beverages_tracker import BeveragesTracker


def main():
    bev = BeveragesTracker(barcode_reader=True)
    bev.start_loop()


if __name__ == '__main__':
    main()
