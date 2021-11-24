import speech_recognition as sr
# Do this in your ipython notebook or analysis script
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import json

class Luna:
    
    def __init__(self):
        self.main()
    # Reconhecimento de fala
    def falar(self):
        #Habilita o microfone para ouvir o usuario
        microfone = sr.Recognizer()
        with sr.Microphone() as source:
            #Chama a funcao de reducao de ruido disponivel na speech_recognition
            microfone.adjust_for_ambient_noise(source)
            #Avisa ao usuario que esta pronto para ouvir
            print("Assistente ligada, qual o comando? ")
            #Armazena a informacao de audio na variavel
            audio = microfone.listen(source)
        try:
            #Passa o audio para o reconhecedor de padroes do speech_recognition
            frase = microfone.recognize_google(audio,language='pt-BR')

            print(f'Você falou: {frase}')
            #Caso nao tenha reconhecido o padrao de fala, exibe esta mensagem
        except sr.UnkownValueError:
            frase = "Desculpa, não entendi..."
        return frase
    #Tratando intrucao e guardando em array
    def tratar_instrucao(self,palavras, comandos_instrucao):
        palavras_selecionadas = []
        res = ''
        tokens = word_tokenize(palavras, 'portuguese')
        eliminar_palavra = set(stopwords.words('portuguese'))
        
        #Algoritimo que valida instruções.
        if tokens:
            #Populando o array com as palavras já filtradas
            for palavra in tokens:
                if palavra not in eliminar_palavra:
                    palavras_selecionadas.append(palavra)
                    
            #Se o array tem 3 ou mais indices então podemos ter assistente, acao e objeto
            if len(palavras_selecionadas) >= 3:
                #Verifica se o primeiro indice é o nome da assitente
                if comandos_instrucao[0]['nome'] == palavras_selecionadas[0].lower():
                        for acao in comandos_instrucao[0]['acoes']:
                            if acao['nome'].lower() == palavras_selecionadas[1].lower():
                                if acao['objeto'].lower() in palavras_selecionadas[2].lower():
                                    res = True 
                                    break
                                else:
                                    res = 'Luna Responde: Ainda não conheço ainda esse objeto'
                            else:
                                res = 'Luna Responde: Desculpa não entendi o comando'
                else:
                    res = 'Para utilizar a assitente precisa chama-lá pelo nome..'
            else:
                res = 'Favor, seguir a ordem correta do comando [Nome assistente->ação->objeto] '
        else: 
            res = 'Desculpa, não entendi o comando'
        return res
    #Funcao para ler arquivo de comandos
    def obter_config_comandos(self):
               
        with open('comandos.json', "r") as instrucoes_json:
            data = []
            try:
               res_json = json.load(instrucoes_json)
               data.append(res_json)
               instrucoes_json.close()
            except: 
                #print('Não econtrei o json.')
                return False
            return data
    #Defini a acao da assistente
    def definir_acao(self,res_):
        if res_ == True:
            print(f'Luna responde: Entendido, tarefa executada!')
        else:
            print(res_)
    #Funcao main da classe
    def main(self):
        fala = self.falar()
        comandos_instrucao = self.obter_config_comandos()
        trata_instrucao = self.tratar_instrucao(fala, comandos_instrucao)
        defini_acao = self.definir_acao(trata_instrucao)

#Instâncio o objeto Luna
luna = Luna()
luna.main


