import eikon as ek
ek.set_app_key('704b9a7d4c834f9ca3dc573767c59f3de985a9a8')

df = ek.get_data('.SPX', ['TR.IndexConstituentRIC'])
print("Test")

print(df[0])