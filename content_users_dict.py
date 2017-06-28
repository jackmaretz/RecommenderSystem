import pandas as pd


ratings = pd.read_csv('BX-Book-Ratings.csv', sep=';', encoding='latin1')

ratings = pd.read_csv('BX-Book-Ratings.csv', sep=';', encoding='latin1')
ratings.drop(ratings[ratings['Book-Rating'] < 1].index, inplace=True)

fields = ['ISBN', 'Book-Author', 'Year-Of-Publication', 'Publisher']
books = pd.read_csv('BX-Books.csv', sep=';', encoding='latin1', skipinitialspace=True, usecols=fields)

matr = ratings.merge(books, left_on='ISBN', right_on='ISBN')
matr_cut = matr.iloc[:1000,:]

pivot = pd.pivot_table(matr_cut,values='Book-Rating',index='User-ID',columns='Book-Author')

piv_dic = pivot.to_dict(orient="index")


piv_dic2 = dict()
for user in piv_dic:
    piv_dic2[user] = dict()
    for author in piv_dic[user]:

        if not math.isnan(piv_dic[user][author]):
            piv_dic2[user][author] = piv_dic[user][author]
