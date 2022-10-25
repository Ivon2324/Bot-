# This example requires the 'message_content' intent.

from datetime import date
from operator import contains
import os
import sqlite3
import discord
from email import message
import email
from tokenize import Token
from urllib import request, response

import requests
from dotenv import load_dotenv
load_dotenv()


# from dotenv import load_dotenv
# load_dotenv()


connectionDB = sqlite3.connect("tutorial.db")
cur = connectionDB.cursor()


intents = discord.Intents.default()
intents.message_content = True

# Token = os.environ['TOKEN']

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('!crearUsuario'):

        first_name = message.content.split(' ')[1]
        last_name = message.content.split(' ')[2]
        full_name = f'{first_name} {last_name}'
        email = message.content.split(' ')[3]
        password = message.content.split(' ')[4]
        confirm_pass = message.content.split(' ')[5]

        response = request.post('http://api.cup2022.ir/api/v1/user', data={
                                'name': full_name, 'email': email, 'password': password, 'Confirmpassword': confirm_pass})
        print(response.json().message)

        cur.execute('INSERT INTO users (discord_id, name) VALUES (?, ?)', [
                    message.author.id, full_name])
        connectionDB.commit()
        await message.channel.send('Usuario creado!')

    if message.content.startswith('!borrarUsuario'):

        cur.execute('DELETE FROM users WHERE discord_id = ?',
                    [message.author.id])
        connectionDB.commit()
        await message.channel.send('Usuario eliminado')

        print('hola')
# datos del jugador
    if message.content.startswith('!Jugador'):
        # await message.channel.send(f'Cargando...')
        jugador_first_name = message.content.split(' ')[1]
        jugador_last_name = message.content.split(' ')[2]
        jugador_full_name = f'{jugador_first_name} {jugador_last_name}'
        idJugador = requests.get(
            f'https://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code=%27&name_part=%27{jugador_full_name}%25')
        response = idJugador.json()
        idJugador = response['search_player_all']['queryResults']['row']['player_id']

        infoJugadores = f'https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_213,q_auto:best/v1/people/{idJugador}/headshot/67/current'

        nombrejugador = response['search_player_all']['queryResults']['row']['name_display_first_last']
        fechaNacimientoJugador = response['search_player_all']['queryResults']['row']['birth_date']
        nacimientojugador = response['search_player_all']['queryResults']['row']['birth_country']
        ciudadnacimientojugador = response['search_player_all']['queryResults']['row']['birth_city']
        sobrenombrejugador = response['search_player_all']['queryResults']['row']['name_display_roster']
        pesojugador = response['search_player_all']['queryResults']['row']['weight']
        alturajugador = response['search_player_all']['queryResults']['row']['height_inches']
        equipojugador = response['search_player_all']['queryResults']['row']['team_full']
        debutjugador = response['search_player_all']['queryResults']['row']['pro_debut_date']
        posicionjugador = response['search_player_all']['queryResults']['row']['position']

        #date and debut
        nacimiento = fechaNacimientoJugador.split('T')[0]
        fechaDebut = debutjugador.split('T')[0]
        #weight in kg
        weight_kg = int(pesojugador) / 2.205
        peso = round(weight_kg, 2)
        #height in m
        height_m = int(alturajugador) / 3.281
        altura = round(height_m, 2)

        await message.channel.send(f'Foto: {infoJugadores}')
        await message.channel.send(f'Nombre y Apellido: {nombrejugador}')
        await message.channel.send(f'Fecha de nacimiento: {nacimiento}')
        await message.channel.send(f'Lugar de nacimiento: {nacimientojugador}')
        await message.channel.send(f'Ciudad de nacimiento: {ciudadnacimientojugador}')
        await message.channel.send(f'Sobrenombre: {sobrenombrejugador}')
        await message.channel.send(f'Peso: {peso}')
        await message.channel.send(f'Altura: {altura}')
        await message.channel.send(f'Equipo: {equipojugador}')
        await message.channel.send(f'Debut: {fechaDebut}')
        await message.channel.send(f'Posicion: {posicionjugador}')

        # Estadisticas

    if message.content.startswith('!Estadisticas'):
        jugador_first_name = message.content.split(' ')[1]
        jugador_last_name = message.content.split(' ')[2]
        año = message.content.split(' ')[3]
        jugador_full_name = f'{jugador_first_name} {jugador_last_name}'
        idJugador = requests.get(
            f'https://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code=%27&name_part=%27{jugador_full_name}%25')
        response = idJugador.json()
        idJugador = response['search_player_all']['queryResults']['row']['player_id']

        Estadisticas = requests.get(
            f'https://lookup-service-prod.mlb.com/json/named.sport_hitting_tm.bam?league_list_id=%27mlb%27&game_type=%27R%27&season={año}&player_id={idJugador}')
        response_stats = Estadisticas.json()

        infoJugadores = f'https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_213,q_auto:best/v1/people/{idJugador}/headshot/67/current'
        # Estadisticas = response_stats['search_player_all']['queryResults']['row']['player_id']
        nombrejugador = response['search_player_all']['queryResults']['row']['name_display_first_last']
        hitsjugador = response_stats['sport_hitting_tm']['queryResults']['row']['h']
        homerunjugador = response_stats['sport_hitting_tm']['queryResults']['row']['hr']
        basestotalesjugador = response_stats['sport_hitting_tm']['queryResults']['row']['tb']
        carrerasjugador = response_stats['sport_hitting_tm']['queryResults']['row']['r']
        ponchesjugador = response_stats['sport_hitting_tm']['queryResults']['row']['so']
        basesrobadasjugador = response_stats['sport_hitting_tm']['queryResults']['row']['sb']
        bbjugador = response_stats['sport_hitting_tm']['queryResults']['row']['bb']
        lobjugador = response_stats['sport_hitting_tm']['queryResults']['row']['lob']
        averegejugador = response_stats['sport_hitting_tm']['queryResults']['row']['avg']
        vecesalbatejugador = response_stats['sport_hitting_tm']['queryResults']['row']['ab']
        juegosjugador = response_stats['sport_hitting_tm']['queryResults']['row']['g']
        carrerasimpulsadasjugador = response_stats['sport_hitting_tm']['queryResults']['row']['rbi']
        añoseasonjugador = response_stats['sport_hitting_tm']['queryResults']['row']['season']

        await message.channel.send(f'Foto: {infoJugadores}')
        await message.channel.send(f'Nombre y Apellido: {nombrejugador}')
        await message.channel.send(f'Hits: {hitsjugador}')
        await message.channel.send(f'Home run: {homerunjugador}')
        await message.channel.send(f'TB: {basestotalesjugador}')
        await message.channel.send(f'Carreras anotadas: {carrerasjugador}')
        await message.channel.send(f'Ponches: {ponchesjugador}')
        await message.channel.send(f'Bases robadas: {basesrobadasjugador}')
        await message.channel.send(f'BB: {bbjugador}')
        await message.channel.send(f'LOB: {lobjugador}')
        await message.channel.send(f'AVG: {averegejugador}')
        await message.channel.send(f'AB: {vecesalbatejugador}')
        await message.channel.send(f'Juegos jugados: {juegosjugador}')
        await message.channel.send(f'Carreras Impulsadas: {carrerasimpulsadasjugador}')
        # await message.channel.send(f'Año buscado: {añoseasonjugador}')

    if message.content.startswith('!Stats'):
        jugador_first_name = message.content.split(' ')[1]
        jugador_last_name = message.content.split(' ')[2]
        jugador_full_name = f'{jugador_first_name} {jugador_last_name}'
        idJugador = requests.get(
            f'https://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code=%27&name_part=%27{jugador_full_name}%25')
        response = idJugador.json()
        idJugador = response['search_player_all']['queryResults']['row']['player_id']

        Estadisticas = requests.get(
            f'https://lookup-service-prod.mlb.com/json/named.sport_career_hitting.bam?league_list_id=%27mlb%27&game_type=%27R%27&player_id={idJugador}')
        response_stats = Estadisticas.json()

        infoJugadores = f'https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_213,q_auto:best/v1/people/{idJugador}/headshot/67/current'
        # Estadisticas = response_stats['search_player_all']['queryResults']['row']['player_id']
        nombrejugador = response['search_player_all']['queryResults']['row']['name_display_first_last']
        hitsjugador = response_stats['sport_career_hitting']['queryResults']['row']['h']
        homerunjugador = response_stats['sport_career_hitting']['queryResults']['row']['hr']
        basestotalesjugador = response_stats['sport_career_hitting']['queryResults']['row']['tb']
        carrerasjugador = response_stats['sport_career_hitting']['queryResults']['row']['r']
        ponchesjugador = response_stats['sport_career_hitting']['queryResults']['row']['so']
        basesrobadasjugador = response_stats['sport_career_hitting']['queryResults']['row']['sb']
        bbjugador = response_stats['sport_career_hitting']['queryResults']['row']['bb']
        lobjugador = response_stats['sport_career_hitting']['queryResults']['row']['lob']
        averegejugador = response_stats['sport_career_hitting']['queryResults']['row']['avg']
        vecesalbatejugador = response_stats['sport_career_hitting']['queryResults']['row']['ab']
        juegosjugador = response_stats['sport_career_hitting']['queryResults']['row']['g']
        carrerasimpulsadasjugador = response_stats['sport_career_hitting']['queryResults']['row']['rbi']
        # añoseasonjugador = response_stats['sport_career_hitting']['queryResults']['row']['season']

        await message.channel.send(f'Foto: {infoJugadores}')
        await message.channel.send(f'Nombre y Apellido: {nombrejugador}')
        await message.channel.send(f'Hits: {hitsjugador}')
        await message.channel.send(f'Home run: {homerunjugador}')
        await message.channel.send(f'TB: {basestotalesjugador}')
        await message.channel.send(f'Carreras anotadas: {carrerasjugador}')
        await message.channel.send(f'Ponches: {ponchesjugador}')
        await message.channel.send(f'Bases robadas: {basesrobadasjugador}')
        await message.channel.send(f'BB: {bbjugador}')
        await message.channel.send(f'LOB: {lobjugador}')
        await message.channel.send(f'AVG: {averegejugador}')
        await message.channel.send(f'AB: {vecesalbatejugador}')
        await message.channel.send(f'Juegos jugados: {juegosjugador}')
        await message.channel.send(f'Carreras Impulsadas: {carrerasimpulsadasjugador}')
        # await message.channel.send(f'Año buscado: {añoseasonjugador}')
    if message.content.startswith('!Ayuda'):

        await message.channel.send(f'Hola, veo que colocaste !Ayuda. Te ayudare a entender el Bot.')
        await message.channel.send(f'Para acceder a la informacion del jugador debes colocar !Jugador y el nombre del jugador que deseas buscar. ')
        await message.channel.send(f'Si te gustaria saber las Estadisticas segun el año dedes colocar !Estadisticas, luego coloca el nombre del jugador que deseas buscar y el año')
        await message.channel.send(f'Si te gustaria saber las Estadisticas segun la temporada solo debes colocar !Stats y luego el nombre del jugador')
        print('funciona')

        print('funciona')


client.run(os.environ['TOKEN'])
# if message.content.startswith('!Jugador'):
#     jugador_first_name = message.content.split(' ')[1]
#     jugador_last_name = message.content.split(' ')[2]
#     jugador_full_name = f'{jugador_first_name} {jugador_last_name}'
#     info = request.get(
#         f'http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code=&active_sw=&name_part={jugador_full_name}')

#     response = info.json()

#     await message.channel.send['birth_country']

#     print('funciona')

# if message.content.startswith('$cryto'):
#     moneda = message.content.split(' ')[1]
#     divisa = message.content.split(' ')[2]
#     info = request.get(
#         f'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={moneda}&tsyms={divisa}')

#     response = info.json()
#     price = response['DISPLAY'][moneda][divisa]['PRICE']
#     high = response['DISPLAY'][moneda][divisa]['HIGH24HOUR']
#     low = response['DISPLAY'][moneda][divisa]['LOW24HOUR']

#     await message.channel.send(f'Moneda: {divisa}, Cryptomoneda: {moneda}')
#     await message.channel.send(f'El precio: {price}')
#     await message.channel.send(f'Precio más alto: {high}')
#     await message.channel.send(f'Precio más bajo: {low}')


# client.run(Token)
