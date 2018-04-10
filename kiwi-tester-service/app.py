def main():
    default_module_path = "kiwi_tester.test_cases"
    
    from kiwi_tester.KiwiTester import KiwiTester
    import argparse
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('module', type=str, help='The module to use within {}'.format(default_module_path))
    args = parser.parse_args()

    module_path = "{}.{}".format(default_module_path, args.module)
    print("Importing module {}".format(module_path))

    module_path_config = "{}.{}".format(module_path, "get_config")
    module_path_data = "{}.{}".format(module_path, "get_data")
    module_path_products = "{}.{}".format(module_path, "get_products")


    import importlib
    m_config = importlib.import_module(module_path_config)
    m_data = importlib.import_module(module_path_data)
    m_products = importlib.import_module(module_path_products)

    data = m_data.get_data()
    products = m_products.get_products()
    config = m_config.get_config()

    tester = KiwiTester(data, products, config)
    tester.start_full_procedure()

if __name__ == "__main__":
    main()
