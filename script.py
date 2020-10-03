import csv
import random


class NaiveBayes:

    data = []
    learning_testing_proportion = []  # armazena as proporções da repartição entre dados para aprendizado e para teste
    learning_data = {"0": [], "1": []}   # dados para treinamento divididos entre as classes
    test_data = [] # dados para teste
    tests_ratings_array = [] # aqui serão armazenadas as taxas de sucesso global e específica de cada classe de cada uma das 30 testagens


    def __init__(self, data, learning_proportion, test_proportion):
        self.data = data
        self.learning_testing_proportion = (learning_proportion, test_proportion)

    def display_raw_data(self):

        total_zero = 0
        total_one = 0

        for row in self.data:
            if row[4] == "0":
                total_zero += 1
            
            if row[4] == "1":
                total_one += 1

        print(f"Total de zeros: {total_zero}")
        print(f"Total de uns: {total_one}")


    # acrescenta rows aos dados de treinamento para afastar o problema da frequência zero
    def add_rows_with_possible_values(self):

        self.learning_data["0"].append(["F","a - Ate 25 anos ","Fundamental","a", "0"])
        self.learning_data["0"].append(["M","b - 26 a 35 anos","Médio","b", "0"])
        self.learning_data["0"].append(["F","c - 36 a 45 anos","Superior","c", "0"])
        self.learning_data["0"].append(["M","d - 46 a 55 anos","Fundamental","d", "0"])
        self.learning_data["0"].append(["F","e - Mais 56 anos","Médio", "e", "0"])

        self.learning_data["1"].append(["F","a - Ate 25 anos ","Fundamental","a", "1"])
        self.learning_data["1"].append(["M","b - 26 a 35 anos","Médio","b", "1"])
        self.learning_data["1"].append(["F","c - 36 a 45 anos","Superior","c", "1"])
        self.learning_data["1"].append(["M","d - 46 a 55 anos","Fundamental","d", "1"])
        self.learning_data["1"].append(["F","e - Mais 56 anos","Médio", "e", "1"])
   
    # embaralha os dados extraídos do .csv e limpa as arrays que guardam os dados de treinamento e dados de teste 
    # como um estágio preparatório para uma nova testagem
    def shuffle_and_clean_data(self): 

        random.shuffle(self.data)
        self.learning_data = {"0": [], "1": []}  
        self.test_data = []

    # reparte os dados entre dados de treinamento (de acordo com a classe) e dados de teste conforme a proporção
    def get_learning_and_test_data(self):

        quantity_learning = self.learning_testing_proportion[0]
        quantity_test = self.learning_testing_proportion[1]
        indexes_learning = []
        indexes_test = []


        while len(indexes_learning) < quantity_learning:
            
            index = random.randint(0, 999)
    
            if index not in indexes_learning: 
                indexes_learning.append(index)

        for i in indexes_learning:   
            
            if self.data[i][4] == "0":
                self.learning_data["0"].append(self.data[i])
            if self.data[i][4] == "1":
                self.learning_data["1"].append(self.data[i])


        while len(indexes_test) < quantity_test:
            
            index2 = random.randint(0, 999)
    
            if index2 not in indexes_learning and index2 not in indexes_test: 
                indexes_test.append(index2)

        for j in indexes_test:   
            self.test_data.append(self.data[j])

        self.add_rows_with_possible_values()

    # helper method genérico para contar ocorrência de um valor numa coluna de uma matriz
    def count_values(self, data, col, val):
        count = 0

        for row in data:
            if row[col] == val:
                count += 1

        return count

    # calcula as probabilidades de uma classe e realiza a classificação, retornando True se houver acerto
    def calculate_class_probabilities_and_classify(self, row):

        probs_class_0 = {
            "gender": 0,
            "age": 0,
            "scolarity": 0,
            "profession": 0,
            "h": 0,
        }

        probs_class_1 = {
            "gender": 0,
            "age": 0,
            "scolarity": 0,
            "profession": 0,
            "h": 0,
        }

        row_gender, row_age, row_scolarity, row_profession, row_class = row

        total_class_0 = len(self.learning_data["0"])
        total_class_1 = len(self.learning_data["1"])
        total_learning_rows = total_class_0 + total_class_1
        prob_class_0 = total_class_0 / total_learning_rows
        prob_class_1 = total_class_1 / total_learning_rows
        
        probs_class_0["gender"] = self.count_values(self.learning_data["0"], 0, row_gender) / total_class_0
        probs_class_0["age"] = self.count_values(self.learning_data["0"], 1, row_age) / total_class_0
        probs_class_0["scolarity"] = self.count_values(self.learning_data["0"], 2, row_scolarity) / total_class_0
        probs_class_0["profession"] = self.count_values(self.learning_data["0"], 3, row_profession) / total_class_0
        probs_class_0["h"] = probs_class_0["gender"] * probs_class_0["age"] * probs_class_0["scolarity"] * probs_class_0["profession"] * prob_class_0
        
        probs_class_1["gender"] = self.count_values(self.learning_data["1"], 0, row_gender) / total_class_1
        probs_class_1["age"] = self.count_values(self.learning_data["1"], 1, row_age) / total_class_1
        probs_class_1["scolarity"] = self.count_values(self.learning_data["1"], 2, row_scolarity) / total_class_1
        probs_class_1["profession"] = self.count_values(self.learning_data["1"], 3, row_profession) / total_class_1
        probs_class_1["h"] = probs_class_1["gender"] * probs_class_1["age"] * probs_class_1["scolarity"] * probs_class_1["profession"] * prob_class_1

        classification = "0" if probs_class_0["h"] >= probs_class_1["h"] else "1"

        if classification == row_class:
            return True
        else:
            return False

    def make_tests(self):

        results = {
            "class_0": {"rights":0, "wrongs": 0},
            "class_1": {"rights":0, "wrongs": 0},
        }

        for row in self.test_data:
            
            if row[4] == "0":
                if self.calculate_class_probabilities_and_classify(row):
                    results["class_0"]["rights"] += 1
                else:
                    results["class_0"]["wrongs"] += 1

            if row[4] == "1":
                if self.calculate_class_probabilities_and_classify(row):
                    results["class_1"]["rights"] += 1
                else:
                    results["class_1"]["wrongs"] += 1

        return results

    def tests_analysis(self):
        
        tests_results = self.make_tests()

        

        results_analysis = {
            "success_rate": round(( tests_results["class_0"]["rights"] + tests_results["class_1"]["rights"] ) / self.learning_testing_proportion[1], 2),
            "success_rate_class_0": round(tests_results["class_0"]["rights"] / ( tests_results["class_0"]["rights"] + tests_results["class_0"]["wrongs"] ), 2),
            "success_rate_class_1": round(tests_results["class_1"]["rights"] / ( tests_results["class_1"]["rights"] + tests_results["class_1"]["wrongs"] ), 2),
        }

        return results_analysis

    def execute_thirty_times(self):

        arr = []

        for _ in range(30):
            self.shuffle_and_clean_data()
            self.get_learning_and_test_data()
            arr.append(self.tests_analysis())

        self.tests_ratings_array = arr
        self.exhibit_results()

    def exhibit_results(self):

        max_success_rate_global = max(test_rating["success_rate"] for test_rating in self.tests_ratings_array)
        avg_success_rate_global = round(sum(test_rating["success_rate"] for test_rating in self.tests_ratings_array) / len(self.tests_ratings_array), 2)
        min_success_rate_global = min(test_rating["success_rate"] for test_rating in self.tests_ratings_array)
        max_success_rate_class_0 = max(test_rating["success_rate_class_0"] for test_rating in self.tests_ratings_array)
        avg_success_rate_class_0 = round(sum(test_rating["success_rate_class_0"] for test_rating in self.tests_ratings_array) / len(self.tests_ratings_array), 2)
        max_success_rate_class_1 = max(test_rating["success_rate_class_1"] for test_rating in self.tests_ratings_array)       
        avg_success_rate_class_1 = round(sum(test_rating["success_rate_class_1"] for test_rating in self.tests_ratings_array) / len(self.tests_ratings_array), 2)

        print("----*" * 40)
        print("Rodada de testes concluída. Análise final:")
        print("Maior taxa de sucesso global:")
        print(max_success_rate_global)
        print("Média da taxa de sucesso global:")
        print(avg_success_rate_global)
        print("Menor taxa de sucesso global:")
        print(min_success_rate_global)
        print("Maior taxa de sucesso da classe 0:")
        print(max_success_rate_class_0)
        print("Média da taxa de sucesso da classe 0:")
        print(avg_success_rate_class_0)
        print("Maior taxa de sucesso da classe 1:")
        print(max_success_rate_class_1)
        print("Média da taxa de sucesso da classe 1:")
        print(avg_success_rate_class_1)



if __name__ == "__main__":

    print("Extraindo Dados do arquivo .csv")

    with open("classificacao_Q3.csv") as data_csv:

        data = [] # colunas: gênero, idade, escolaridade, profissão, valor

        for row in csv.reader(data_csv):
            data.append(row)
        
        data.pop(0) # eliminar o row com os headers da tabela
    


    # Primeira rodada de testes!
    print("Rodada 1: 10% dos dados para treinamento e  90% dos dados para teste:")
    print("Carregando...")
    first_round_naive_bayes = NaiveBayes(data, 100, 900)

    first_round_naive_bayes.display_raw_data()
    breakpoint()


    first_round_naive_bayes.execute_thirty_times()

    # Segunda rodada de testes!
    print("Rodada 2: 20% dos dados para treinamento e  80% dos dados para teste:")
    print("Carregando...")
    random.shuffle(data)
    second_round_naive_bayes = NaiveBayes(data, 200, 800)
    second_round_naive_bayes.execute_thirty_times()

    # Terceira rodada de testes!
    print("Rodada 3: 30% dos dados para treinamento e  70% dos dados para teste:")
    print("Carregando...")
    random.shuffle(data)
    third_round_naive_bayes = NaiveBayes(data, 300, 700)
    third_round_naive_bayes.execute_thirty_times()

    # Quarta rodada de testes!
    print("Rodada 4: 40% dos dados para treinamento e  60% dos dados para teste:")
    print("Carregando...")
    random.shuffle(data)
    fourth_round_naive_bayes = NaiveBayes(data, 400, 600)
    fourth_round_naive_bayes.execute_thirty_times()

    # Quinta rodada de testes!
    print("Rodada 5: 50% dos dados para treinamento e  50% dos dados para teste:")
    print("Carregando...")
    random.shuffle(data)
    fifth_round_naive_bayes = NaiveBayes(data, 500, 500)
    fifth_round_naive_bayes.execute_thirty_times()

    # Sexta rodada de testes!
    print("Rodada 6: 60% dos dados para treinamento e  40% dos dados para teste:")
    print("Carregando...")
    random.shuffle(data)
    sixth_round_naive_bayes = NaiveBayes(data, 600, 400)
    sixth_round_naive_bayes.execute_thirty_times()

    # Sétima rodada de testes!
    print("Rodada 7: 70% dos dados para treinamento e  30% dos dados para teste:")
    print("Carregando...")
    random.shuffle(data)
    seventh_round_naive_bayes = NaiveBayes(data, 700, 300)
    seventh_round_naive_bayes.execute_thirty_times()

    # Oitava rodada de testes!
    print("Rodada 8: 80% dos dados para treinamento e  20% dos dados para teste:")
    print("Carregando...")
    random.shuffle(data)
    eighth_round_naive_bayes = NaiveBayes(data, 800, 200)
    eighth_round_naive_bayes.execute_thirty_times()
    
    # Última rodada de testes!
    print("Rodada x: 90% dos dados para treinamento e  10% dos dados para teste:")
    print("Carregando...")
    random.shuffle(data)
    last_round_naive_bayes = NaiveBayes(data, 900, 100)
    last_round_naive_bayes.execute_thirty_times()
    
    

    


    







