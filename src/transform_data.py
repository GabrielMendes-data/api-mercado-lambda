from datetime import datetime

from src.infra.fetch_data import (
    FocusFetchData,
    IbgeFetchData
)

class TransformFocusData:
    def __init__(self, indicators: list[str], date: str, temporal_series: str):
        self.indicators = indicators

        # Adicionar proximo ano na data
        dt_date = datetime.strptime(date,"%d/%m/%Y").date()
        self.date = [date,dt_date.replace(year = dt_date.year + 1).strftime("%d/%m/%Y")]
        
        self.temporal_series = temporal_series

    def transform(self) -> dict:
        """
        Transforma os dados da API Focus em um dicionário.
        """
        result_focus = []

        for indicator in self.indicators:
            for date in self.date:

                fetch_data = FocusFetchData().fetch_data(indicator, date, self.temporal_series)
                
                dict_filtered = fetch_data[-1]

                keys = ['Indicador','Data','DataReferencia','Mediana']

                dict_filtered = {key: dict_filtered[key] for key in keys}

                result_focus.append(dict_filtered)

        return result_focus

class TransformIbgeData:
    def __init__(self, date: str):
        self.date = date

    def transform(self) -> dict:
        """
        Transforma os dados da API IBGE em um dicionário.
        """

        fetch_data = IbgeFetchData().fetch_data(self.date)

        keys = ['MN','V','D2C','D2N','D3C','D3N']

        variaveis = ['63','2265']

        result_ibge = [
            {key: item[key] for key in keys}
            for item in fetch_data[1:]
            if item.get('D3C') in variaveis
            ]

        return result_ibge
