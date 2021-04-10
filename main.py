import re as regex
import discord 
import requests

class Nitro(discord.Client):
    def __init__(self, **options):
        super().__init__(**options)
        self.token = "" # YOUR TOKEN HERE

    async def on_connect(self):
        print(f"Connected as {self.user.name}")

    async def claim_code(self, code: str):
        head = {
            "Authorization": self.token,
            "Content-Type": "application/json",
        }
        req = requests.post(f"https://discordapp.com/api/v6/entitlements/gift-codes/{code}/redeem", headers=head, json={"channel_id": None, "payment_source_id": None})
        if "subscription_plan" not in req.text:
            try:
                message = req.json()["message"]
            except:
                message = "CloudFlare ratelimiting Error"
            return {"valid": False, "message": message}
        else:
            return {"valid": True, "message": req.json()}
              
    async def on_message(self, message):
        try:
            code = regex.search(r'(discord.com/gifts/|discordapp.com/gifts/|discord.gift/)([a-zA-Z0-9]+)',
                             message.content)
            tok = code.group(2)
            if code:
                if len(tok) == 16 or len(tok) == 24:
                    data = await self.claim_code(tok)
                    data_message = data['message']
                    if "subscription_plan" in data_message:
                        print(f"Successfully claimed nitro!")
                    else:
                        print(f"Invalid nitro code.")
        except AttributeError:
            pass

    def master(self):
        try:
            super().run(self.token, bot=False)
        except discord.errors.LoginFailure as e:
            print(f"Cannot connect: {e}")
            quit()

if __name__ == "__main__":
    client = Nitro()
    client.master()
