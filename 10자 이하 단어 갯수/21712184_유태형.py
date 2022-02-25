def word_count():
    f=open("words.txt","r")
    count=0
    print("10자 이하인 단어:")
    for line in f:
        word = line.split('\n')
        if len(word[0]) <= 10:
            count +=1
            print(word[0])
            
    print()
    print("10자 이하인 단어의 갯수 :",count)
    f.close()


word_count()
