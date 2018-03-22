from re import sub
from traceback import print_exc

from discord.ext import commands
from aiohttp import ClientSession
from async_timeout import timeout
from lxml.html import fromstring


class Translations:
    def __init__(self, lambdabot):
        self.lambdabot = lambdabot
    
    @commands.command()
    async def toleet(self, ctx, *, text):
        """Converts normal text into 'leet' text."""
        text = text.lower()

        text = text.replace('a', '4')
        text = text.replace('e', '3')
        text = text.replace('g', '6')
        text = text.replace('i', '1')
        text = text.replace('o', '0')
        text = text.replace('s', '5')
        text = text.replace('t', '7')

        await ctx.send(text)
    
    @commands.command()
    async def toasian(self, ctx, *, text):
        """Converts normal text into 'asian'."""
        text = text.lower()

        text = text.replace('a', '卂')
        text = text.replace('b', '乃')
        text = text.replace('c', '匚')
        text = text.replace('d', '刀')
        text = text.replace('e', '乇')
        text = text.replace('f', '下')
        text = text.replace('g', '厶')
        text = text.replace('h', '卄')
        text = text.replace('i', '工')
        text = text.replace('j', '丁')
        text = text.replace('k', '长')
        text = text.replace('l', '乚')
        text = text.replace('m', '从')
        text = text.replace('n', '𠘨')
        text = text.replace('o', '口')
        text = text.replace('p', '尸')
        text = text.replace('q', '㔿')
        text = text.replace('r', '尺')
        text = text.replace('s', '丂')
        text = text.replace('t', '丅')
        text = text.replace('u', '凵')
        text = text.replace('v', 'リ')
        text = text.replace('w', '山')
        text = text.replace('x', '乂')
        text = text.replace('y', '丫')
        text = text.replace('z', '乙')
        
        await ctx.send(text)
    
    @commands.command(aliases=['toemoji'])
    async def toemojis(self, ctx, *, text):
        """Converts normal text into emojis"""
        text = text.lower()
        
        result = ''
        for c in text:
            if c in "abcdefghijklmnopqrstuvwxyz":
                result += f':regional_indicator_{c}: '
            elif c in "0123456789":
                if c == "0":
                    result += ":zero: "
                elif c == "1":
                    result += ":one: "
                elif c == "2":
                    result += ":two: "
                elif c == "3":
                    result += ":three: "
                elif c == "4":
                    result += ":four: "
                elif c == "5":
                    result += ":five: "
                elif c == "6":
                    result += ":six: "
                elif c == "7":
                    result += ":seven: "
                elif c == "8":
                    result += ":eight: "
                elif c == "9":
                    result += ":nine: "
            elif c in "+-$":
                if c == "+":
                    result += ":heavy_plus_sign: "
                elif c == "-":
                    result += ":heavy_minus_sign: "
                elif c == "$":
                    result += ":heavy_dollar_sign: "
            elif c == " ":
                result += c

        await ctx.send(result)

    @commands.command(aliases=['binaryfromtext', 'ttb', 'bft'])
    async def texttobinary(self, ctx, *, text):
        """Will convert text to binary and send the result."""
        if text:
            bits = bin(int.from_bytes(text.encode(
                'utf-8', 'surrogatepass'), 'big'))[2:]
            bits = bits.zfill(8 * ((len(bits) + 7) // 8))
            result = ''
            for n in range(len(bits) // 8):
                result += bits[:8] + ' '
                bits = bits[8:]
            await ctx.send(result)
        else:
            await ctx.send("What do you want me to translate?")

    @commands.command(aliases=['textfrombinary', 'btt', 'tfb'])
    async def binarytotext(self, ctx, *, binary):
        """Will convert binary to text and send the result."""
        binary = ''.join(binary.split())
        try:
            n = int(binary, 2)
        except ValueError:
            await ctx.send("I need binary, not text")
            return
        await ctx.send(n.to_bytes((n.bit_length() + 7) // 8, 'big').decode('utf-8', 'surrogatepass') or '\0')
    
    @commands.command()
    async def tobraille(self, ctx, * ,text):
        text = text.lower()

        text = sub(r'a|1', '⠁', text)
        text = sub(r'b|2', '⠃', text)
        text = sub(r'c|3', '⠉', text)
        text = sub(r'd|4', '⠙', text)
        text = sub(r'e|5', '⠑', text)
        text = sub(r'f|6', '⠋', text)
        text = sub(r'g|7', '⠛', text)
        text = sub(r'h|8', '⠓', text)
        text = sub(r'i|9', '⠊', text)
        text = sub(r'j|0', '⠚', text)
        text = sub(r'k', '⠅', text)
        text = sub(r'l', '⠇', text)
        text = sub(r'm', '⠍', text)
        text = sub(r'n', '⠝', text)
        text = sub(r'o', '⠕', text)
        text = sub(r'p', '⠏', text)
        text = sub(r'q', '⠟', text)
        text = sub(r'r', '⠗', text)
        text = sub(r's', '⠎', text)
        text = sub(r't', '⠞', text)
        text = sub(r'u', '⠥', text)
        text = sub(r'v', '⠧', text)
        text = sub(r'w', '⠺', text)
        text = sub(r'x', '⠭', text)
        text = sub(r'y', '⠽', text)
        text = sub(r'z', '⠵', text)
        text = sub(r',', '⠂', text)
        text = sub(r';', '⠆', text)
        text = sub(r':', '⠒', text)
        text = text.replace('.', '⠲')
        text = sub(r'!', '⠖', text)
        text = text.replace('?', '⠦')

        await ctx.send(text)
    
    @commands.command()
    async def toascii(self, ctx, *, text):
        with ClientSession() as session:
            with timeout(10):
                async with session.get(f'http://www.patorjk.com/software/taag/#p=display&f=Big&t={text}') as resp:
                    text = resp.text()
                    for i in text:
                        await ctx.send(i)
                    # while len(text) < 2000:
                    #     await ctx.send(text[:2000])
                    #     text = text[2000:]
                    # await ctx.send(text)
                    # text = fromstring(resp.text()).xpath("//body/div[@id='maincontent']/div[@id='outputFigDisplay']/pre")


def setup(lambdabot):
    lambdabot.add_cog(Translations(lambdabot))
