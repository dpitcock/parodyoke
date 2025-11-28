import pyphen
dic = pyphen.Pyphen(lang='en_US')
words = ["parody", "karaoke", "computer"]
for w in words:
    ins = dic.inserted(w)
    c = len(ins.split('-'))
    print(f"'{w}' -> '{ins}' ({c})")
