#!/usr/bin/env python3

import os
import sys
import os.path
import argparse
import requests
from bs4 import BeautifulSoup


class pdfdownload:
    def __init__(self, valor, pages):
        self.valor = valor
        self.pages = pages
        self.urls = list()

    def geturls(self):
        for x in range(self.pages):
            for url in BeautifulSoup(requests.get("https://www.google.com/search?q={}+filetype:pdf&sxsrf=ALeKk02cufcUtDUvzRbO4NONSchxqwoGXQ:1591737468701&ei=fPzfXruqKsPCgwfk9qj4Bw&start={}0&sa=N&ved=2ahUKEwi72JaT1PXpAhVD4eAKHWQ7Cn8Q8tMDegQIEhAw&biw=1536&bih=750".format(self.valor.replace(" ", "+"), x)).text, "html.parser").find_all("a"):
                if url.attrs["href"][:7] == "/url?q=":
                    if url.attrs["href"][7:].split("&")[0][-4:] == ".pdf":
                        self.urls.append(url.attrs["href"][7:].split("&")[0])

    def descargar(self):
        print("Archivos a descargar: "+str(len(self.urls)))
        for x in self.urls:
            if os.path.isdir("downloads/"+self.valor):
                if os.path.isfile("downloads/{}/{}".format(self.valor, x.split("/")[len(x.split("/"))-1])):
                    print("El archivo {} ya existe".format(
                        x.split("/")[len(x.split("/"))-1]))
                else:
                    try:
                        print("Descargando: {}".format(
                            x.split("/")[len(x.split("/"))-1]))
                        open("downloads/{}/{}".format(self.valor, x.split("/")
                                                      [len(x.split("/"))-1]), 'wb').write(requests.get(x).content)
                    except OSError:
                        print("Error: al dedcargar: %s" %
                              x.split("/")[len(x.split("/"))-1])
                        pass
            else:
                try:
                    os.mkdir("downloads/"+self.valor)
                except OSError:
                    print("La creación del directorio %s falló" % self.valor)
                else:
                    print("Se ha creado el directorio: %s " % self.valor)


def main():
    parser = argparse.ArgumentParser(description='pdfDownloader')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-n', '--name', metavar='N', action="store",
                               help='an integer for the accumulator', required=True)
    requiredNamed.add_argument('-p', '--pages', type=int, action="store",
                               help='sum the integers (default: find the max)', required=True)
    args = parser.parse_args()

    pdf = pdfdownload(args.name, args.pages)
    pdf.geturls()
    pdf.descargar()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Hasta la proxima ;D")
