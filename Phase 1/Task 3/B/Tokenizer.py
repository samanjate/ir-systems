if __name__ == '__main__':
    f = open('README.txt','a')
    f.write('Just to initialize variable, please delete me before runnig the indexer on tokenized corpus')
    with open('cacm_stem.txt') as corpus:
        for line in corpus:
            if "#" in line:
                f.close()
                filename = 'CACM-' + '{0:04}'.format(int(line.split()[1])) + '.txt'
                continue
            else:
                f = open(filename,'a')
                terms = line.split()
                for term in terms:
                    f.write(term + '\n')

