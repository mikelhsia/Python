import logging

log_file_name = 'timehut.log'

logging.basicConfig(filename=log_file_name,
					format='%(asctime)s -%(name)s-%(levelname)s-%(module)s:%(message)s',
					datefmt='%Y-%m-%d %H:%M:%S %p',
					level=logging.DEBUG)


print(f"Module {__file__} is loaded...")
