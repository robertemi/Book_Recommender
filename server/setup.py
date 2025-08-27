'''
Run this to get the embeddings and save to ChromaDB the sample data in books.txt, otherwise the app won't work 

'''

from embeddings import embedd_and_persist


def embedd_and_save():
    embedd_and_persist()

embedd_and_save()