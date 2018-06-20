import MeCab
import CaboCha
import itertools
import re


class Mecab:

    def __init__(self,sentence):
        self._sentence = sentence
        self._wordclass = self.__getWordClass(sentence)
        self._surfacewords = self.__getSurfaceWords(sentence)
        self._number_of_wc = {'0':'助詞','1':'助動詞','2':'形容詞','3':'形容動詞','4':'動詞','5':'副詞','6':'接続詞','7':'名詞'}

    """ 形態素解析する """
    def parse(self):
        return self._surfacewords

    """  wc_str : str
    '0' : 助詞     '1' : 助動詞  '2' : 形容詞   '3' : 形容動詞
    '4' : 動詞     '5' : 副詞    '6' : 接続詞   '7' : 名詞
    ex) 助動詞、動詞、名詞を抜き出したい時 → wc_n_lst = '047'
    """
    def parse_if(self,wc_str):
        wc_lst = self.__change_to_wc(wc_str)
        return [word for word,wc in zip(self._surfacewords,self._wordclass) if wc in wc_lst]

    def __change_to_wc(self,s):
        return [self._number_of_wc[n] for n in s]

    def __getSurfaceWords(self,sentence):
        words = []
        mecab = MeCab.Tagger('mecabrc')
        mecab.parse("")
        node = mecab.parseToNode(sentence)
        while node:
            words.append(node.surface.lower())
            node = node.next
        return words

    def __getWordClass(self,sentence):
        wordclass = []
        mecab = MeCab.Tagger('mecabrc')
        mecab.parse("")
        node = mecab.parseToNode(self._sentence)
        while node:
            wordclass.append(node.feature.split(",")[0])
            node = node.next
        return wordclass

class Cabocha:

    def __init__(self,sentence,cformat):
        self._sentence = sentence
        self._tokens = self.__parseTree(sentence,cformat)

    """ 動詞とその目的語を抜き出す """
    def dependencyWordList(self):
        chunknodes = self.__makeChunkNodes()
        chunktokens = self.__searchChunkToken()
        links = self.__findChunkTokenLink(chunktokens)
        frontwords = self.__mapping(self.__concatTokens, chunktokens, chunknodes, range(len(links)))
        backwords = self.__mapping(self.__concatTokens, chunktokens, chunknodes, links)
        return [frontwords,backwords]

    def __makeChunkNodes(self):
        chunknodes = []
        for token in self._tokens:
            chunknodes.append([]) if self.__hasChunk(token) else chunknodes[len(chunknodes) - 1].append(token)
        return chunknodes

    def __hasChunk(self,token):
        return token.chunk is not None

    def __parseTree(self,sentence,cformat):
        cp = CaboCha.Parser(cformat)
        tree = cp.parse(sentence)
        return [tree.token(i) for i in range(tree.size())]

    def __searchChunkToken(self):
        chunktokens = list(filter(self.__hasChunk, self._tokens))
        return chunktokens

    def __findChunkTokenLink(self,chunktokens):
        links = list(map(lambda x: x.chunk.link, chunktokens))
        return links

    def __concatTokens(self,index, chunktokens, chunknodes):
        if index == -1:
            return None
        word = chunktokens[index].surface
        lastwords = list(map(lambda x: x.surface, chunknodes[index]))
        return word + ''.join(lastwords)

    def __mapping(self,f,lst1,lst2,lst3):
        return list(map(lambda x: f(x, lst1, lst2),lst3))

    def object(self,sentence):
        c = CaboCha.Parser ()
        tree =  c.parse (sentence)
        size = tree.size()
        myid,ku_id,ku_link,kakari_joshi,kaku_joshi = 0,0,0,0,0
        ku_list = []
        ku = ''
        for i in range (0, size):
            token = tree.token (i)
            if token.chunk:
                if (ku!=''):
                    ku_list.append((ku, ku_id, ku_link, kakari_joshi, kaku_joshi))  #前 の句をリストに追加
                kakari_joshi,kaku_joshi = 0,0
                ku = token.normalized_surface
                ku_id = myid
                ku_link = token.chunk.link
                myid=myid+1
            else:
                ku = ku + token.normalized_surface
            m = (token.feature).split(',')
            if (m[1] == u'係助詞'):
               kakari_joshi = 1
            if (m[1] == u'格助詞'):
               kaku_joshi = 1
        ku_list.append((ku, ku_id, ku_link, kakari_joshi, kaku_joshi))  # 最後にも前の句をリストに追加
        obj,pred,jutsugo_id = "","",""
        for k in ku_list:
            if (k[2]==-1):  # link==-1?      # 述語である
                jutsugo_id = ku_id  # この時のidを覚えておく
        for k in ku_list:
            if (k[2]==jutsugo_id):  # jutsugo_idと同じidをリンク先に持つ句を探す
                if (k[4] == 1):
                     obj = k[0]
            if (k[1] == jutsugo_id):
                 pred = k[0]
        return [obj,pred]
