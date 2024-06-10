from django.apps import AppConfig


class CoinmarketcapAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coinmarketcap_app'
    
    # def ready(self) -> None:
    #     import coinmarketcap_app.signals
