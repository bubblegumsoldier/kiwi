def main():
    default_module_path = "kiwi_tester.test_cases"
    
    from kiwi_tester.KiwiTester import KiwiTester
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('module', type=str, help='The module to use within {}'.format(default_module_path))
    parser.add_argument('statout', type=str, help='Filepath to output the stats to')    
    parser.add_argument('--skiptesting', "-t", help='skip testing', action='store_true')
    parser.add_argument('--notestingfeedback', "-ntf", help='No testing feedback', action='store_true')
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
    if args.statout is not None:
        config.stats_output = args.statout
    if args.skiptesting is True:
        config.skip_testing = True
    if args.notestingfeedback is True:
        config.no_testing_feedback = True

    print("Saving stats file to {}".format(config.stats_output))
    tester = KiwiTester(data, products, config)
    tester.start_full_procedure()

if __name__ == "__main__":
    main()
