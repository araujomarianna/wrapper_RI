#!/usr/bin/python
# -*- coding: latin-1 -*-

import time
import requests
from bs4 import BeautifulSoup

class EI(object):

    def __init__(self):
        self._OPICIONAIS = ['radio','CD', 'MP3 Player','MP3','alarme', 'airbag','dir.e','rodas liga','rodas liga leve','liga leve', 'vid'
            ,'sensor de r�','sensor de estacionamento', 'revestimento fum�', 'bancos de couro',
                            'Retrovisores el�tricos', 'volante com regulagem de altura']
        self._COMBUSTIVEL = ['g�s', 'gasolina', 'alcool', 'flex', 'total flex']

        self.FORD = ['focus', 'new fiesta', 'fiesta se', 'ka']

        self._Volkswagen = ['gol','fox', 'crossfox', 'voyage']

        self._Hyundai = ['hb20']

        self._Chevrolet = ['montana', 'agile']

        self._Fiat = ['strada', 'palio','siena', 'idea', 'uno']

        self._Honda = ['civic', 'city']

        self._Nissan = ['versa']

        self._Toyota = ['corola']

        self._Renault = ['duster']

        self._DIRECAO = ['hidraulica', 'dire��o hidraulica', 'hla', 'dire��o el�trica', 'el�trica']

        self._CAMBIO = ['Manual', 'autom�tico', 'autom�tica']

        self._COR = ['branco','preto', 'prata', 'azul', 'marrom', 'vermelho', 'amarelo', 'cinza']

        self._AR = ['ar', 'ar_condi', 'ar_condicionado']

        self.date = time.strftime("%d-%m-%Y")


    def classify(self, text):
        data = text.split(',')
        v_opcionais = []
        v_combustivel = ''
        v_direcao = ''
        v_cambio = ''
        v_cor = ''
        v_ar = 'n�o'

        for opcionais in data:
            for content in self._OPICIONAIS:
                if content != '' and content.lower() == opcionais.lower():
                    if content.lower() not in v_opcionais:
                        v_opcionais.append(content.lower())

        for combustivel in data:
            for content in self._COMBUSTIVEL:
                if content != '' and content.lower() == combustivel.lower():
                    v_combustivel = content.lower()

        for direcao in data:
            for content in self._DIRECAO:
                if content != '' and content.lower() == direcao.lower():
                    v_direcao = content.lower()


        for cor in data:
            for content in self._COR:
                if content != '' and content.lower() == cor.lower():
                    v_cor = content.lower()

        for ar in data:
            for content in self._AR:
                if content != '' and content.lower() == ar.lower():
                    v_ar = 'sim'

        self.preencher_template(v_ar, v_opcionais, v_combustivel, v_direcao, v_cambio, v_cor)


    def preencher_template(self, ar, opcionais, combustivel, direcao, cambio, cor,marcar, modelo,preco,motor,ano,km):
        template = OpenFiles("Swats/tarefa", self.date).generateFile()

        if combustivel != '':
            template.write("Combustivel: " + combustivel)
            template.write("\n")
        else:
            template.write("Combustivel: N/I")
            template.write("\n")

        if cambio != '':
            template.write("Cambio: " + cambio)
            template.write("\n")
        else:
            template.write("Cambio: N/I")
            template.write("\n")

        if direcao != '':
            template.write("Dire��o: " + direcao)
            template.write("\n")
        else:
            template.write("Dire��o: N/I")
            template.write("\n")

        if cor != '':
            template.write("Cor: " + cor)
            template.write("\n")
        else:
            template.write("Cor: N/I")
            template.write("\n")

        template.write("Ar: " + ar)
        template.write("\n")

        if opcionais:
            for op in opcionais:
                template.write ("Opcionais: " + op + ",")

            template.write ("\n")
        else:
            template.write("Opcionais: N/I")

    def get_page(self, url):
        htmlfile = requests.get(url)
        return htmlfile.text

    def parser(self, html):
        parsed_html = BeautifulSoup(html, "lxml")
        content = parsed_html.body.find('h1', class_='titulo-detalhe-do-produto')
        content2 = parsed_html.body.find_all('h4', class_='caracteristicas-valor')
        preco = parsed_html.body.find('h4', class_='preco-produto-sidebar')
        caracteristicas = parsed_html.body.find_all('li', class_='listagem-mais-detalhes-do-produto-item')
        info_adicional = parsed_html.body.find_all('p')




class OpenFiles(object):

    def __init__(self, name=None, date=None):
        self._file_name = name;
        self._date = date


    def generateFile(self):

        file_EI_create = self._file_name + "" + self._date + ".txt"
        file_EI = open("../communication/"+file_EI_create, 'a')
        file_EI.write("\n\nPreenchimento do Template" + "(" + self._date + "):\n\n")
        return file_EI


if __name__ == "__main__":
    EI().classify("branco,flex, hatch, completo,sensor de r�, 4 pneus novos, 76.000 kms. R$ 35.900,00")