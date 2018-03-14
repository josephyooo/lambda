from discord.ext import commands


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
    
    @commands.command()
    async def makelarge(self, ctx, *, text):
        """Converts normal text into emojis"""
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


def setup(lambdabot):
    lambdabot.add_cog(Translations(lambdabot))
