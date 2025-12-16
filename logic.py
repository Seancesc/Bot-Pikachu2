import aiohttp  # A library for asynchronous HTTP requests
import random

class Pokemon:
    pokemons = {}
    # Object initialisation (constructor)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.img = None
        self.power = random.randint(30,60)
        self.hp = random.randint(200,400)
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def get_name(self):
        # An asynchronous method to get the name of a pokémon via PokeAPI
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # URL API for the request
        async with aiohttp.ClientSession() as session:  # Opening an HTTP session
            async with session.get(url) as response:  # Sending a GET request
                if response.status == 200:
                    data = await response.json()  # Receiving and decoding JSON response
                    return data['forms'][0]['name']  # Returning a Pokémon's name
                else:
                    return "Pikachu"  # Return the default name if the request fails

    async def info(self):
        # A method that returns information about the pokémon
        if not self.name:
            self.name = await self.get_name()  # Retrieving a name if it has not yet been uploaded
        return f"""The name of your Pokémon: {self.name}
                Kekuatan Pokémon: {self.power}
                kesehatan Pokémon: {self.hp}"""

    async def show_img(self):
        # Metode asinkron untuk mendapatkan nama pokémon via PokeAPI
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # URL API untuk permintaan
        async with aiohttp.ClientSession() as session:  # Membuka HTTP session
            async with session.get(url) as response:  # Mengirim permintaan GET
                if response.status == 200:
                    data = await response.json()  # Menerima dan mendekode respons JSON
                    return data['sprites']['front_default']  # Mengembalikan nama Pokémon
                else:
                    return "None"  # Kembalikan nama default jika permintaan gagal

    async def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = random.randint(1,5)
            if chance == 1:
                return "Pokemon Penyihir menggunakan perisai dalam battle"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pertarungan @{self.pokemon_trainer} melawan @{enemy.pokemon_trainer}\nHP @{enemy.pokemon_trainer} sekarang {enemy.hp}"
        else:
            enemy.hp = 0
            return f"@{self.pokemon_trainer} menang melawan @{enemy.pokemon_trainer}"
        
class Wizard(Pokemon):
    pass

class Fighter(Pokemon):
    async def attack(self, enemy):
        super_power = random.randint(5,15)
        self.power += super_power
        result = await super().attack(enemy)
        self.power -= super_power
        return result + f"\nPetarung menggunakan serangan super dengan kekuatan:{super_power}"