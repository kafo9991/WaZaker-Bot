import asyncio
import random
import nextcord
from nextcord import Interaction
from nextcord.ext import commands, tasks
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TOKEN")

time = 1
intents = nextcord.Intents.default()
intents.message_content = True

# ✅ استخدم commands.Bot بدلاً من InteractionBot
bot = commands.Bot(command_prefix="/", intents=intents)

# قائمة الصوتيات
audio_files_list = [
    "bot audio/استغفر الله وأتوب اليه.mp3",
    "bot audio/الحمدلله.mp3",
    "bot audio/اللَّهُمَّ أَنْتَ رَبِّي.mp3",
    "bot audio/اللهم صلي على سيدنا محمد.mp3",
    "bot audio/بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيٌ فِيْ الأَرْضِ وَلَا فِي السَّمَاءِ وَ هُوَ الْعَلِيُّ الْعَظِيمُ.mp3",
    "bot audio/سُبْحَانَ اللَّهِ وَ بِحَمْدِهِ سُبْحَانَ اللَّهِ الْعَظِيمِ.mp3",
    "bot audio/سبحان الله.mp3",
    "bot audio/لا اله الا الله.mp3",
    "bot audio/لا اله الا انت سبحانك اني كنت من الظالمين.mp3",
    "bot audio/سُبْحَانَ اللَّهِ عَدَدَ خَلْقِهِ وَرِضَا نَفْسِهِ وَزِنَةَ عَرْشِهِ.mp3",
]

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user.name}")
    try:
        await bot.sync_all_application_commands()  # ✅ مزامنة أوامر Slash
        print(f"✅ Slash Commands Synced!")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")

# ✅ أمر Slash Command يعمل الآن
@bot.slash_command(name="test", description="اختبار أوامر Slash")
async def test(interaction: Interaction):
    await interaction.response.send_message("✅ Slash command يعمل بنجاح!")

# تشغيل الصوت
async def play_audio(vc):
    if not vc or not vc.is_connected():
        return
    audio = random.choice(audio_files_list)
    vc.play(nextcord.FFmpegPCMAudio(audio))
    while vc.is_playing():
        await asyncio.sleep(1)

@bot.slash_command(name="hello", description= "التحية")
async def hello(interaction: Interaction):
    await interaction.response.send_message("Hello, World!")

@bot.slash_command(name="work", description= "التأكد من العمل")
async def work(interaction: Interaction):
    await interaction.response.send_message("ياعم شغال")

@bot.slash_command(name="join", description= "الدخول للقناة الصوتية")
async def join(interaction: Interaction):
    if interaction.user.voice:
        channel = interaction.user.voice.channel
        if not interaction.guild.voice_client:
            await channel.connect()
            await interaction.response.send_message("✅ انا جيت ")
        else:
            await interaction.response.send_message("❌ انا بالفعل داخل القناة")
    else:
        await interaction.response.send_message("❌ والله ابدا ادخل انت الأول ")

@bot.slash_command(name="leave", description= "الخروج من القناة الصوتية")
async def leave(interaction: Interaction):
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("❌ انا خرجت ")
    else:
        await interaction.response.send_message("❌ ياعم انا مش جوه")

@bot.slash_command(name="start_tazker", description= "البدء بتشغيل التذكير")
async def startTazker(interaction: Interaction):
    if not interaction.guild.voice_client:
        await interaction.response.send_message("❌ البوت ليس في قناة صوتية. استخدم أمر `!join` أولاً!")
        return
    if not play_periodic_audio.is_running():
        play_periodic_audio.start()
        await interaction.response.send_message("✅ تم بدء تشغيل الصوتيات كل 1 دقائق!")
    else:
        await interaction.response.send_message("❌ التذكير يعمل بالفعل!")

@bot.slash_command(name="stop_tazker", description= "ايقاف التذكير")
async def stop_tazker(interaction: Interaction):
    if play_periodic_audio.is_running():
        play_periodic_audio.stop()
        await interaction.response.send_message("✅ تم إيقاف تشغيل التذكير!")
    else:
        await interaction.response.send_message("❌ لم يتم بدء التشغيل حتى الآن!")

@tasks.loop(minutes = 1)
async def play_periodic_audio():
    vc = nextcord.utils.get(bot.voice_clients)
    if vc and vc.is_connected():
        await play_audio(vc)

@bot.slash_command(name="zekr", description= "بدا الأذكار")
async def zekr(interaction: Interaction):
    await join(interaction)
    await startTazker(interaction)

@bot.slash_command(name = "timer", description= "تغير الزمن بين التذكير")
async def timer(interaction: Interaction, input: int):
    global time

    if input < 1:
        await interaction.response.send_message(f'يجب اداخل زمن اكبر من 1 دقيقة')
        return
    time = input
    if play_periodic_audio.is_running():
        play_periodic_audio.cancel()
    
    play_periodic_audio.change_interval(minutes=time)
    play_periodic_audio.start()
    
    await interaction.response.send_message(f"✅ تم تغيير الزمن إلى {time} دقيقة بين التذكير!")
bot.run(TOKEN)
