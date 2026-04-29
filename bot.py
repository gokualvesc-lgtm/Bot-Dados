import discord
import random
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

#@bot.command()
#async def rolar(ctx, dado):
#    resultados = []
#    lados = quantidade = bonus = 0
#    resultado = 0
#    quantidade, lados = dado.split("d")
#    quantidade = int(quantidade)
#    lados = lados.split("+")
#    try:
#        bonus = int(lados[1])
#    except IndexError:
#        print("Não tem bonus")
#    lados = int(lados[0])
#
#    for _ in range(0, quantidade):
#        giro = random.randint(1, lados)
#        resultados.append(giro)
#        resultado += giro
#    resultado += bonus
#    await ctx.send(f"{dado} {resultados}: {resultado}")

class RerollView(discord.ui.View):
    def __init__(self, dado, autor):
        super().__init__(timeout=60)
        self.dado = dado
        self.autor = autor

    @discord.ui.button(label="Reroll", style=discord.ButtonStyle.green, emoji="🎲")
    async def reroll(self, interaction: discord.Interaction, button: discord.ui.Button):
        resultados = []
        lados = quantidade = bonus = 0
        resultado = 0
        quantidade, lados = self.dado.split("d")
        quantidade = int(quantidade)
        lados = lados.split("+")
        try:
            bonus = int(lados[1])
        except IndexError:
            print()
        lados = int(lados[0])

        for _ in range(quantidade):
            giro = random.randint(1, lados)
            resultados.append(giro)
            resultado += giro
        resultado += bonus
        embed = discord.Embed(
            title=f"Girando {self.dado}",
            description = f"{self.dado} {resultados}: {resultado}\nAUTOR DO GIRO: {self.autor}"
            )
        await interaction.response.send_message(embed=embed ,view=self)


@bot.command()
async def porcentagem(ctx, numero, porcentagem, defesa):
    try:
        numero = int(numero)
        porcentagem = int(porcentagem)
        defesa = int(defesa)
        resultado = numero * porcentagem / 100 - defesa
    except ValueError:
        print("Erro não foi possivel fazer a conta")
        await ctx.send("Você mandou um caracter invalido para fazer contas!")
    embed = discord.Embed(
    title="Resultado",
    description=f"O resultado da porcentagem do numero {numero} e porcentagem {porcentagem} ja contando com a defesa de {defesa} é {resultado}",
    color = discord.Color.green()
)
    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        print(f"Message do bot: {message.content}")
        return
    if "Daniel" in message.content or "DANIEL" in message.content or "daniel" in message.content:
        await message.channel.send("Daniel? É o meu criador, ele é muito FODA!!")
    try:
        if "d" in message.content:
            resultados = []
            lados = quantidade = bonus = 0
            resultado = 0
            quantidade, lados = message.content.split("d")
            quantidade = int(quantidade)
            lados = lados.split("+")
            try:
                bonus = int(lados[1])
            except IndexError:
                print()
            lados = int(lados[0])
            for _ in range(0, quantidade):
                giro = random.randint(1, lados)
                resultados.append(giro)
                resultado += giro
            resultado += bonus
            with open("historico", "a", encoding="utf-8") as arquivo:
                arquivo.write(f"---\n {message.content} {resultados}: {resultado}  \nAUTOR DO GIRO: @{message.author}\nSERVIDOR USADO: {message.guild.name}")
            embed = discord.Embed(
                title=f"Girando {message.content}",
                description = f"{message.content} {resultados}: {resultado}\nAUTOR DO GIRO: {message.author.mention}"
            )
            view = RerollView(message.content, message.author.mention)
            await message.channel.send(embed=embed, view=view)
        print(f"{message.author}: {message.content}")
    except ValueError:
        print("Não executado devido não contem um valor de dado correto")
        return
    
class BotaoLegal(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.button(label="Button", style=discord.ButtonStyle.green, emoji="💰")
    async def clicar(self, interaction=discord.interactions, button=discord.ui.Button):
        embed = discord.Embed(
        title="Teste",
        description="Testando o botão para ver se é bão mesmo"
    )   
        await interaction.response.send_message(embed=embed, view=self)

@bot.command()
async def teste(ctx):
    embed = discord.Embed(
        title="Teste",
        description="Testando o botão para ver se é bão"
    )
    view = BotaoLegal()
    await ctx.send(embed=embed, view=view)

bot.run("MTQ5ODY4MDMzNjgyODIwNzE0NA.GQ-bap.QikBvV0MYimRtMgxu3V6Wn_jftLjaTR8zmfyHE")
