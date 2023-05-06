from tadbir.tadbir import Tadbir

tadbir = Tadbir(whole_data=False ,base_url='https://fund.sabaamc.ir')
print(tadbir.get_returns())