import sqlite3

db_file = 'metinler.db'

def create_db():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS metinler (id INTEGER PRIMARY KEY, metin TEXT)''')
    conn.commit()
    conn.close()

def insert_metin(metin):   
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("INSERT INTO metinler (metin) VALUES (?)", (metin,))
    conn.commit()
    conn.close()

def similarity(text1, text2):
    words1 = text1.split()
    words2=text2.split()
   
    similarCount=0
    totalCount= len(words1) + len(words2)
    
    for i in range(len(words1)):
        for j in range(len(words2)):
            if words1[i]==words2[j]: 
                similarCount +=1
                totalCount-=1
    
    return similarCount / totalCount

def jaccard_similarity(text1,text2):
    words1 = set(text1.split())  
    words2 = set(text2.split())  

    intersection = words1 & words2  
    union = words1 | words2         

    if len(union) == 0:
        return 0  

    jaccard_similarity = len(intersection) / len(union) 
    return jaccard_similarity

def levenshtein_distance(text1, text2):
    # İki metnin uzunluklarını al
    m = len(text1)
    n = len(text2)

    # Boş bir m x n boyutunda matris oluştur
    matris = [[0] * (n + 1) for _ in range(m + 1)]

    # İlk sütun ve satırı doldur
    for i in range(m + 1):
        matris[i][0] = i
    for j in range(n + 1):
        matris[0][j] = j

    # Levenshtein mesafesini hesapla
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                changeCost = 0
            else:
                changeCost = 1

            matris[i][j] = min(matris[i - 1][j] + 1,       # Deletion
                           matris[i][j - 1] + 1,       # Insertion
                           matris[i - 1][j - 1] + changeCost)  # Substitution

    # Son hücredeki değer Levenshtein mesafesini verir
    return matris[m][n]


def main():
   
    metin1 = input("Birinci metni giriniz: ")
    metin2 = input("İkinci metni giriniz: ")

    create_db()
    insert_metin(metin1)
    insert_metin(metin2)

    similarity_score = similarity(metin1, metin2)
    jaccard_score=jaccard_similarity(metin1,metin2)
    leven_score= levenshtein_distance(metin1,metin2)
   
    print(f"Metinler arasındaki benzerlik katsayısı: {similarity_score}")
    print(f"Metinler arasındaki jaccard benzerlik katsayısı: {jaccard_score}")
    print(f"Metinler arasındaki levenshtein mesafesi: {leven_score}")

    with open('benzerlik_durumu.txt', 'w') as f:
        f.write(f"Metinler arasindaki benzerlik katsayisi: {similarity_score}\n")
        f.write(f"Metinler arasindaki jaccard benzerlik katsayisi: {jaccard_score}\n")
        f.write(f"Metinler arasindaki levenshtein mesafesi: {leven_score}")

if __name__ == "__main__":
    main()
