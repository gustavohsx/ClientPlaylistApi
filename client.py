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
            data = response.read().decode()
            return data
        
    def getAllLinkOfPlaylist(self, idplaylist):
        request = self.conn.request("GET", f"/playlist/{idplaylist}")
        try:
            response = self.conn.getresponse()
        except http.client.HTTPException as e:
            return f"Erro ao Adquirir os Links da Playlist. Status: {e.status}"
        else:
            data = response.read().decode()
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
        pass

client = PlaylistClient()
print(client.getAllPlaylists())
#print(client.postPlaylist(titulo="Videos Engraçados", descricao="Videos que fazem dar risada"))
#print(client.postLinkToPlaylist(titulo="TENTE NÃO RIR - Vídeos Engraçados 2024 e Melhores Memes - #85", descricao="", url="https://www.youtube.com/watch?v=zS6DIUTfE8o", idplaylist=2))