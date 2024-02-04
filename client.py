import http.client
import json


class PlaylistClient:

    def __init__(self):
        self.conn = http.client.HTTPConnection("localhost", 8080)

    def getAllPlaylists(self):
        request = self.conn.request("GET", "/playlist")
        try:
            response = self.conn.getresponse()
        except http.client.HTTPException as e:
            return f"Erro ao Adquirir as Playlists. Status: {e.status}"
        else:
            data = json.loads(response.read())
            return data
        
    def getAllLinkOfPlaylist(self, idplaylist):
        request = self.conn.request("GET", f"/playlist/{idplaylist}")
        try:
            response = self.conn.getresponse()
        except http.client.HTTPException as e:
            return f"Erro ao Adquirir os Links da Playlist. Status: {e.status}"
        else:
            data = json.loads(response.read())
            return data
    
    def postPlaylist(self, titulo, descricao):
        header = {"Content-Type": "application/json"}
        data = {"titulo": titulo, "descricao": descricao}
        body = json.dumps(data).encode()

        request = self.conn.request(method="POST", url="/playlist", headers=header, body=body)

        response = self.conn.getresponse()
        if response.status == 201:
            print("Playlist criada com sucesso!")
        else:
            print(f"Erro: {response.status} - {response.reason}")
    
    def postLinkToPlaylist(self, titulo, descricao, url, idplaylist):
        header = {"Content-Type": "application/json"}
        data = {"titulo": titulo, "descricao": descricao, "url": url, "idplaylist": idplaylist}
        body = json.dumps(data).encode()

        request = self.conn.request(method="POST", url=f"/playlist/{idplaylist}/addlink", headers=header, body=body)

        response = self.conn.getresponse()
        if response.status == 201:
            print("Link adicionado com sucesso!")
        else:
            print(f"Erro: {response.status} - {response.reason}")
    
    def deletePlaylist(self, idplaylist):
        self.conn.request("DELETE", f"/playlist/{idplaylist}")
        response = self.conn.getresponse()
        if response.status == 200:
            print("Playlist Deletada com sucesso!")
        else:
            print(f"Erro: {response.status} - {response.reason}")


class App:

    def __init__(self):
        self.client = PlaylistClient()
        self.start()
    
    def start(self):
        print("Playlist API - Gerencie suas Playlist de Maneira Fácil!\n")
        while True:
            opcao = input("Escolha uma Opcão:\n\n0 - Sair\n1 - Ver todas as Playlists\n2 - Ver links da Playlist\n3 - Adicionar Link a uma Playlist\n4 - Criar Nova Playlist\n5 - Apagar Playlist\n>>")
            if opcao == "0":
                print("Encerrando...")
                return False
            elif opcao == "1":
                self.playlists()
            elif opcao == "2":
                self.linksPlaylist()
            elif opcao == "3":
                self.adicionarLinkPlaylist()
            elif opcao == "4":
                self.criarPlaylist()

    def playlists(self):
        try:
            playlists = self.client.getAllPlaylists()
            print(f"\nForam Encontradas {len(playlists)} Playlists:\n")
            for playlist in playlists:
                print(f"ID({playlist['id']}) - {playlist['titulo']}")
            print("\n")
        except:
            print("Não foi possível exibir as Playlists!")
    
    def linksPlaylist(self):
        idplaylist = input("\nQual o ID da playlist?\n>>")
        try:
            idplaylist_int = int(idplaylist)
            try:
                links = self.client.getAllLinkOfPlaylist(idplaylist_int)
                print(f"\nForam Encontradas {len(links)} Links:\n")
                for link in links:
                    print(f"ID({link['id']}) - {link['titulo']} - URL: <{link['url']}>")
                print("\n")
            except:
                print("Não foi possível exibir os Links da Playlist!\n")
        except:
            print("Não foi digitado um ID válido!\n")
    
    def adicionarLinkPlaylist(self):
        idplaylist = input("Digite o ID da Playlist:\n>>")
        try:
            idplaylist = int(idplaylist)
        except:
            print("ID Inválido!")
            return
        titulo = input("\nQual o Título do Link?\n>>")
        if len(titulo) <= 5:
            print("Titulo Inválido | Deve ter pelo menos 5 caracteres!\n")
            return
        descricao = input("Qual a Descrição do Link?\n>>")
        url = input("\nQual o URL do Link?\n>>")
        if len(url) <= 15:
            print("URL Inválida!\n")
            return
        try:
            self.client.postLinkToPlaylist(titulo=titulo, descricao=descricao, url=url, idplaylist=idplaylist)
            print("Link Adicionado com Sucesso!\n")
        except:
            print("Não foi possivel Adicionar o Link!\n")
        
    def criarPlaylist(self):
        titulo = input("\nQual o Título da Playlist?\n>>")
        if len(titulo) <= 5:
            print("Titulo Inválido | Deve ter pelo menos 5 caracteres!\n")
            return
        descricao = input("Qual a Descrição da Playlist?\n>>")
        try:
            self.client.postPlaylist(titulo=titulo, descricao=descricao)
            print("Playlist Criada com Sucesso!\n")
        except:
            print("Não foi possivel Criar a Playlist!\n")
    
    def deletarPlaylist(self):
        idplaylist = input("Digite o ID da Playlist:\n>>")
        try:
            idplaylist = int(idplaylist)
        except:
            print("ID Inválido!")
            return
        try:
            self.client.deletePlaylist(idplaylist=idplaylist)
            print("Playlist Deletada com Sucesso!")
        except:
            print("Não foi possivel Deletar a Playlist!")
            return

App()
