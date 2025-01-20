import asyncio
from telethon import TelegramClient, events, sync, types
from telethon import functions
from telethon.tl.types import *
import time
import pickle

# Use your own values from my.telegram.org
api_id = 29068923
api_hash = '72035fc7d10fc5bd2847e23ecad1a850'
bot_token = "7540665471:AAETu4-Er84bqm-QdYQlYMvpLIOpQ2rptxU"
client = TelegramClient("bot",api_id,api_hash).start(bot_token=bot_token)


class Client():
    
    def __init__(self, fin:int, nam):
        self.__mesini=time.localtime().tm_mon 
        self.__mesfinal=fin*31  #cantidad de dias total
        self.__name=nam
        self.__cant_dias=0 #contador de dias
        
    
    @property    
    def mesini(self):
        return self.__mesini
    
    @property    
    def cant_dias(self):
        return self.__cant_dias

    @property
    def mesfinal(self):
        return self.__mesfinal
    
    @property
    def name(self):
        return self.__name
    
    @mesini.setter
    def mesini(self, newini):
        self.__mesini=newini

    @mesfinal.setter
    def mesfinal(self, newfinal):
        self.__mesfinal=newfinal
        
    @name.setter
    def name(self, newname):
        self.__name=newname
        
     
    def add_dias(self):
        self.__cant_dias=self.cant_dias+1
    
    
class Control():
    
    def __init__(self):
        self.__borrados:Client=[]
        self.__clientes:Client=[]
        
        
    @property
    def borrados(self):
        return self.__borrados
    
    @borrados.setter
    def borrados(self, newlista):
        self.__borrados=newlista
        
    @property
    def get_clientes(self):
        return self.__clientes
    
    @borrados.setter
    def clientes(self, newlista):
        self.__clientes=newlista
        
    def add_cliente(self, cliente:Client):
        self.__clientes.append(cliente)
        print("Cliente agregado con exito")
        #print(len(self.__clientes))
        
    def clearList(self):
        self.__borrados.clear()
        
    def del_cliente(self, cliente:Client):
        self.__borrados.append(cliente)
        self.__clientes.remove(cliente)
    
    def get_cliente(self, n):
        return self.__clientes [n]
    
    def guardar_datos(self):
        ubi_lista=open("datos.dat","wb")
        pickle.dump(self.__clientes,ubi_lista)
        ubi_lista.close
        print("Lista Guardada")
        
    def cargar_datos(self):
        ubi_lista=open("datos.dat","rb")
        self.__clientes=pickle.load(ubi_lista)
        print("Lista Cargada")
    
    def revisar_limite(self):
        self.clearList()
        for client in self.__clientes:
            if isinstance(client, Client):
                client.add_dias()
                #print("Nombre de usuario: ", client.name, " , dias restantes: " , client.mesfinal-client.cant_dias)
                #print("Cambiando de usuario")
                if(client.mesfinal-client.cant_dias == 0):
                    print("El usuario ", client.name , " ha terminado su suscriccion")
                    self.del_cliente(client)
        return self.__borrados
    
    def borrar_datos(self):
        self.clearList()
        self.__clientes.clear()
        self.guardar_datos()
        



print("Iniciando")
controladora=Control()


@client.on(events.NewMessage)
async def handle_new_message(event):
    #print(len(controladora.get_clientes))
    sender = await event.get_sender()
    chat = await event.get_chat()
    mesage=event.message.message
    #print(sender.id)
    #print(chat)
    if(sender.id == 968663996 or sender.id == 847369429):
        if(mesage=="/help"):
            await event.reply("Escribe en este formato al nuevo sub: '/sub,cant_meses,@name' ejemplo: '/sub,1,@leonardo2004'")
            
        elif(mesage[0:5] == "/sub,"):
            controladora.cargar_datos()
            #index=mesage.find(" ")
            mesage=mesage.split(",")
            cant=int(mesage[1])
            #print(mesage)
            user=mesage[2]
            #print(user)
            newcl = Client(cant,user)
            controladora.add_cliente(newcl)
            await event.reply("Cliente añadido")
            controladora.guardar_datos()
        
        elif(mesage== "/ver"):
            lista=controladora.cargar_datos()
            lista=controladora.revisar_limite()
            list_del=controladora.borrados
            if(len(list_del) != 0):
                for user in list_del:
                    if isinstance(user, Client):
                        await event.reply("Cliente: "+ user.name + " vencio su suscripcion" )
                controladora.guardar_datos()
            else:
                await event.reply("No hay usuarios con suscripcion vencida")
                controladora.guardar_datos()
                
        elif(mesage== "/list"):
            controladora.cargar_datos()
            ls="Clientes: \n"
            cont=0
            lista=controladora.get_clientes
            #print(len(lista))
            for user in lista:
                cont=cont+1
                if isinstance(user, Client):
                    ls=ls+"Cliente " + str(cont) + ": "+ user.name + " dias restantes: " + str(user.mesfinal-user.cant_dias) +"\n"
                    #await client.send_message(chat,"Cliente " + cont + ": "+ user.name + " dias restantes: " + str(user.mesfinal-user.cant_dias) +"/n")
                    #await event.reply("Cliente: " +  user.name + " dias restantes: " + str(user.mesfinal-user.cant_dias))
            await client.send_message(chat,ls)
            
        elif(mesage== "/borrar_clientes"):
            controladora.borrar_datos()
            await event.reply("Borrando lista de clientes....")
            
        elif(mesage== "/guardar"):
            controladora.guardar_datos()
            await event.reply("Guardando datos...")
   
         
with client:
    client.run_until_disconnected()