import requests  # Biblioteca para fazer requisições HTTP
import matplotlib.pyplot as plt  # Biblioteca para criar gráficos e visualizações

class TreeMap:
    def __init__(self, data, labels, colors=None):
        # Inicializa a instância da classe com dados, rótulos e cores
        self.data = data
        self.labels = labels
        # Se não forem fornecidas cores, usa as cores padrão do matplotlib
        self.colors = colors if colors is not None else plt.cm.tab20c.colors

    def squarify(self, x, y, width, height, values):
        """
        Divide os dados em retângulos proporcionais para o gráfico do tipo "treemap".
        """
        if not values:
            return []

        total = sum(values)  # Soma total dos valores para calcular proporções
        rects = []  # Lista para armazenar os retângulos
        cumulative = 0  # Soma cumulativa dos valores
        prev_cumulative = 0  # Soma cumulativa anterior para calcular largura/altura de cada retângulo

        # Divide os valores em retângulos baseados em suas proporções
        for i, value in enumerate(values):
            cumulative += value
            proportion = cumulative / total  # Proporção acumulada dos valores
            split = proportion * width if width > height else proportion * height  # Calcula a divisão

            if width > height:
                # Adiciona um retângulo para o caso em que a largura é maior que a altura
                rects.append((x + prev_cumulative * width / total, y, (cumulative - prev_cumulative) * width / total, height))
            else:
                # Adiciona um retângulo para o caso em que a altura é maior que a largura
                rects.append((x, y + prev_cumulative * height / total, width, (cumulative - prev_cumulative) * height / total))

            prev_cumulative = cumulative  # Atualiza a soma cumulativa anterior

        # Divide o restante do espaço se necessário
        if width > height:
            remaining_values = values[len(rects):]  # Valores restantes para o próximo nível
            if remaining_values:
                remaining_width = width - (cumulative - prev_cumulative) * width / total
                # Chama a função recursivamente para preencher o restante do espaço
                rects.extend(self.squarify(x + (cumulative - prev_cumulative) * width / total, y, remaining_width, height, remaining_values))
        else:
            remaining_values = values[len(rects):]  # Valores restantes para o próximo nível
            if remaining_values:
                remaining_height = height - (cumulative - prev_cumulative) * height / total
                # Chama a função recursivamente para preencher o restante do espaço
                rects.extend(self.squarify(x, y + (cumulative - prev_cumulative) * height / total, width, remaining_height, remaining_values))

        return rects

    def plot(self):
        """
        Cria e exibe o gráfico do tipo "treemap".
        """
        fig, ax = plt.subplots(1, figsize=(12, 8))  # Cria uma figura e um eixo para o gráfico

        rects = self.squarify(0, 0, 100, 100, self.data)  # Divide os dados em retângulos

        # Plota cada retângulo no gráfico
        for i, (x, y, width, height) in enumerate(rects):
            color = self.colors[i % len(self.colors)]  # Escolhe a cor para o retângulo
            ax.bar(
                x,
                height,
                width=width,
                bottom=y,
                color=color,
                edgecolor='black',
                linewidth=1
            )
            # Adiciona o rótulo ao centro do retângulo
            ax.text(
                x + width / 2,
                y + height / 2,
                self.labels[i],
                ha='center',
                va='center'
            )

        ax.axis('off')  # Desliga os eixos para um visual mais limpo
        plt.show()  # Exibe o gráfico

def fetch_stock_data(symbol, api_key):
    """
    Busca o preço de fechamento mais recente de uma ação usando a API Alpha Vantage.
    """
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)  # Faz a requisição HTTP
    data = response.json()  # Converte a resposta para JSON
    if 'Time Series (Daily)' in data:
        latest_date = list(data['Time Series (Daily)'].keys())[0]  # Obtém a data mais recente
        close_price = float(data['Time Series (Daily)'][latest_date]['4. close'])  # Obtém o preço de fechamento
        return close_price
    else:
        return None  # Retorna None se não encontrar os dados

def main():
    """
    Função principal que busca dados das ações e plota o gráfico do tipo "treemap".
    """
    api_key = "Q9SUCHJ5ONFK1L4H"  # Chave da API Alpha Vantage
    symbols = ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA', 'ABEV3.SA']  # Símbolos das ações
    labels = ['Petrobras', 'Vale', 'Itaú', 'Bradesco', 'Ambev']  # Rótulos para o gráfico
    data = []

    # Busca os preços de fechamento das ações
    for symbol in symbols:
        price = fetch_stock_data(symbol, api_key)
        if price:
            data.append(price)

    # Plota o gráfico se todos os dados foram encontrados
    if len(data) == len(labels):
        treemap = TreeMap(data, labels)  # Cria uma instância da classe TreeMap
        treemap.plot()  # Plota o gráfico
    else:
        print("Erro ao buscar os dados das ações.")  # Mensagem de erro caso falhe na busca dos dados

if __name__ == "__main__":
    main()  # Executa a função principal
