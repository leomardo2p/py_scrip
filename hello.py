import asyncio
from telethon import TelegramClient # type: ignore
from telethon import functions
from telethon.tl.types import *
import pickle

# Use your own values from my.telegram.org
api_id = 29068923
api_hash = '72035fc7d10fc5bd2847e23ecad1a850'
client = TelegramClient("anon",api_id,api_hash)

# The first parameter is the .session file name (absolute paths allowed)
#with TelegramClient('anon', api_id, api_hash) as client:
#    client.loop.run_until_complete(client.send_message('me', 'Hello, myself!'))

async def main():
  
    #me = await client.get_me()
    #print(me.stringify)
    
    print("Sesion iniciada")
    
    canal_destino=-1002498350107
    canal_show=-1001949008583
    canal_serie=-1001926526437
    canal_pelicula=-1001931348646
    canal_sub=-1001570987246
    canal_anime=-1001890238805
    canal_variado=-1001507263093
    
    
    # print(me.username)
    # print(me.phone)
    #async for dialog in client.iter_dialogs():
    #    print(dialog.name, " su id es ", dialog.id)
        
  # Obtener la entidad del canal fuente
    source_channel_show = await client.get_entity(PeerChannel(canal_show))
    source_channel_serie = await client.get_entity(PeerChannel(canal_serie))
    source_channel_pelicula = await client.get_entity(PeerChannel(canal_pelicula))
    source_channel_sub = await client.get_entity(PeerChannel(canal_sub))
    source_channel_anime = await client.get_entity(PeerChannel(canal_anime))
    source_channel_variado = await client.get_entity(PeerChannel(canal_variado))
    

   #  Obtener la entidad del canal destino
    destination_channel = await client.get_entity(PeerChannel(canal_destino))

   #Obtener todos los mensajes de los canales
    print("Recolectando mensajes")
    channs=[source_channel_sub,source_channel_anime,source_channel_pelicula,source_channel_serie,source_channel_show,source_channel_variado]
    
    cant_mens=0
    num_mens=0
    for ch in reversed(channs):
      
      async for mess in reversed(client.iter_messages(ch)):
        
        if(mess.media):
          if (cant_mens ==1000):
            print("Se ha llegado a 1000 mensajes, esperando 1 hora...")
            cant_mens=0
            await asyncio.sleep(3600)
            continue
          text = mess.text if mess.text else ""
          newtext= text.replace("✅ DISPONIBLE POR VIP (SIN CONSUMO DE MEGAS)", "")
          newtext= newtext.replace("Interesados: @LAW_OP","")
          newtext= newtext.replace("TVAditcos", "")
          newtext= newtext.replace("@LAW_OP", "")
          newtext= newtext.replace("💎:VIP nube: @Itachi_Uchia01","")
          newtext= newtext.replace("VIP: @Itachi_Uchia01","")
          newtext= newtext.replace("Vip: @Itachi_Uchia01","")
          newtext= newtext.replace("Disponible en  (https://t.me/+niDj9adTu31kMmRh)TVadictosPeliculas (https://t.me/+rEH9Hu97eWw5YTYx)","")
          newtext= newtext.replace("💎VIP nube: @Itachi_Uchia01","")
          print("Nombre del archivo: " , newtext)
          if isinstance(mess.media, MessageMediaPhoto):
            await client.send_message(destination_channel, file=mess.media.photo, message=newtext)
          elif isinstance(mess.media, MessageMediaDocument):
            await client.send_message(destination_channel, file=mess.media.document, message=newtext)
            # elif isinstance(message.media, MessageMediaWebPage):
            #     await client.send_message(destination_channel, file=message.media.webpage, message=text)
          elif isinstance(mess.media, MessageMediaUnsupported):
            print("Mensaje no soportado, no enviado")
          num_mens=num_mens+1
          cant_mens=cant_mens+1
          print("Mensaje enviado numero:", num_mens )
          print("Esperando 1 segundo...")
          await asyncio.sleep(1)
          
    print("Se tiene un total de: " , num_mens , " mensajes")
    print("Scrip finalizado")
    await client.send_message(destination_channel,"Finalizado")
        
    
    #messages = await client.get_messages(source_channel_show, limit=None)

  #   #--------------------------------------
  #   #       Copiador de contenido
  #   #--------------------------------------
  #   # for message in reversed(messages):
  #   #     if message.media:
  #   #         try:
  #   #         # Verificar el tipo de contenido multimedia
  #   #             if isinstance(message.media, (MessageMediaPhoto, MessageMediaDocument, MessageMediaWebPage)):
  #   #                 # Reenviar el mensaje al canal destino
  #   #                 await client.forward_messages(destination_channel, message)
  #   #                 print(f"Mensaje multimedia reenviado: {message.id}")
  #   #                 await asyncio.sleep(1)  # Esperar 1 segundo entre mensajes para no saturar la API
  #   #             elif isinstance(message.media, MessageMediaUnsupported):
  #   #                 print(f"Mensaje multimedia no soportado {message.id} no sera reenviado")
  #   #             else:
  #   #                 print(f"Otro tipo de mensaje multimedia encontrado {message.id}")
  #   #         except Exception as e:
  #   #             print(f"Error al reenviar mensaje {message.id}: {e}")
    
  #   #--------------------------------------------
  #          #Borrar historial de un canal
    #await client.delete_messages(destination_channel,[msg.id async for msg in client.iter_messages(destination_channel)])
    #print("Historial del canal eliminado")
  #   #--------------------------------------------
    
with client:
    client.loop.run_until_complete(main())
