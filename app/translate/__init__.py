import i18n

i18n.set("fallback", "vn")
i18n.set("locale", "vn")
def run():
    i18n.load_path.append('D:\\Eclip\\work-space\\NowProject\\backend\\app\\transation\\lang')
    print(i18n.t("food_type.drink"))

def setLocalte(lang):
    valids = ['vn', 'en']
    if lang not in valids: raise "lang not support!"
    i18n.set("locale", lang)
    