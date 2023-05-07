from tadbir.tadbir import Tadbir

tadbir = Tadbir(whole_data=False, base_url='https://fund.sabaamc.ir', se='123456789')
print(tadbir.get_historical_units())
