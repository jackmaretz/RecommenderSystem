ratings = pd.read_csv('BX-Book-Ratings.csv', sep=';', encoding='latin1')

ratings = pd.read_csv('BX-Book-Ratings.csv', sep=';', encoding='latin1')
ratings.drop(ratings[ratings['Book-Rating'] < 1].index, inplace=True)

fields = ['ISBN', 'Book-Author', 'Year-Of-Publication', 'Publisher']
books = pd.read_csv('BX-Books.csv', sep=';', encoding='latin1', skipinitialspace=True, usecols=fields)

matr = ratings.merge(books, left_on='ISBN', right_on='ISBN')
matr_cut = matr.iloc[:1000,:]

pivot = pd.pivot_table(matr_cut,values='Book-Rating',index='User-ID',columns='Book-Title')

piv_dic = pivot.to_dict(orient="index")
