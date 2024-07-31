import tkinter as tk  # Biblioteca para criar interfaces gráficas
from tkinter import messagebox  # Biblioteca para exibir caixas de mensagem

class RomanConverter:
    # Dicionário para conversão entre numerais romanos e inteiros
    roman_numerals = {
        'M': 1000,
        'CM': 900,
        'D': 500,
        'CD': 400,
        'C': 100,
        'XC': 90,
        'L': 50,
        'XL': 40,
        'X': 10,
        'IX': 9,
        'V': 5,
        'IV': 4,
        'I': 1
    }

    def __init__(self, value):
        self.value = value  # Armazena o valor fornecido (inteiro ou romano)

    def to_roman(self):
        """
        Converte um número inteiro para o formato romano.
        """
        num = self.value
        result = ''
        for roman, integer in RomanConverter.roman_numerals.items():
            while num >= integer:
                result += roman
                num -= integer
        return result

    @staticmethod
    def from_roman(roman):
        """
        Converte um número romano para o formato inteiro.
        """
        num = 0
        i = 0
        while i < len(roman):
            # Verifica se o próximo par de caracteres é um numeral romano válido
            if (i + 1 < len(roman)) and (roman[i:i + 2] in RomanConverter.roman_numerals):
                num += RomanConverter.roman_numerals[roman[i:i + 2]]
                i += 2
            else:
                num += RomanConverter.roman_numerals[roman[i]]
                i += 1
        return num

class RealToRomanConverter(RomanConverter):
    def __init__(self, value):
        # Verifica se o valor é um inteiro positivo
        if not isinstance(value, int) or value <= 0:
            raise ValueError("O valor deve ser um inteiro positivo.")
        super().__init__(value)

class RomanToRealConverter(RomanConverter):
    def __init__(self, roman):
        # Verifica se o valor é uma string não vazia
        if not isinstance(roman, str) or not roman:
            raise ValueError("O valor deve ser uma string não vazia.")
        super().__init__(roman)

    def to_real(self):
        """
        Converte um número romano para o formato inteiro.
        """
        return self.from_roman(self.value)

class ConverterApp:
    def __init__(self, root):
        self.root = root  # Armazena a janela principal da aplicação
        self.root.title("Conversor de Números Romanos")  # Define o título da janela

        # Cria e posiciona o rótulo e campo de entrada para números reais
        self.label_real = tk.Label(root, text="Número Real:")
        self.label_real.grid(row=0, column=0, padx=10, pady=10)
        self.entry_real = tk.Entry(root)
        self.entry_real.grid(row=0, column=1, padx=10, pady=10)

        # Cria o botão para converter números reais para romanos
        self.button_convert_to_roman = tk.Button(root, text="Converter para Romano", command=self.convert_to_roman)
        self.button_convert_to_roman.grid(row=0, column=2, padx=10, pady=10)

        # Cria e posiciona o rótulo e campo de entrada para números romanos
        self.label_roman = tk.Label(root, text="Número Romano:")
        self.label_roman.grid(row=1, column=0, padx=10, pady=10)
        self.entry_roman = tk.Entry(root)
        self.entry_roman.grid(row=1, column=1, padx=10, pady=10)

        # Cria o botão para converter números romanos para reais
        self.button_convert_to_real = tk.Button(root, text="Converter para Real", command=self.convert_to_real)
        self.button_convert_to_real.grid(row=1, column=2, padx=10, pady=10)

    def convert_to_roman(self):
        """
        Converte o número real fornecido para o formato romano e exibe o resultado.
        """
        try:
            real_value = int(self.entry_real.get())  # Obtém o valor real do campo de entrada
            converter = RealToRomanConverter(real_value)  # Cria uma instância do conversor
            roman_value = converter.to_roman()  # Converte o valor real para romano
            self.entry_roman.delete(0, tk.END)  # Limpa o campo de entrada de números romanos
            self.entry_roman.insert(0, roman_value)  # Insere o valor romano no campo de entrada
        except ValueError as e:
            messagebox.showerror("Erro", str(e))  # Exibe uma mensagem de erro em caso de entrada inválida

    def convert_to_real(self):
        """
        Converte o número romano fornecido para o formato real e exibe o resultado.
        """
        try:
            roman_value = self.entry_roman.get().upper()  # Obtém o valor romano do campo de entrada e converte para maiúsculas
            converter = RomanToRealConverter(roman_value)  # Cria uma instância do conversor
            real_value = converter.to_real()  # Converte o valor romano para real
            self.entry_real.delete(0, tk.END)  # Limpa o campo de entrada de números reais
            self.entry_real.insert(0, real_value)  # Insere o valor real no campo de entrada
        except ValueError as e:
            messagebox.showerror("Erro", str(e))  # Exibe uma mensagem de erro em caso de entrada inválida

if __name__ == "__main__":
    root = tk.Tk()  # Cria a janela principal da aplicação
    app = ConverterApp(root)  # Cria uma instância da aplicação
    root.mainloop()  # Inicia o loop principal da interface gráfica
