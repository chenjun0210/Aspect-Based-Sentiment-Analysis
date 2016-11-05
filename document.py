# coding=utf-8
from lxml import etree
from lxml import objectify
import pickle
import os
import re

class Document(object):
    """读取xml中的数据，保存在pkl文件中"""

    def __init__(self):
        super(Document, self).__init__()
        self.data = []
        self.text = []
        self.category = []
        self.polarity = []
        self.xml_path = ''
        self.pkl_path = ''

    def set_xml_path(self, xml_path):
        self.xml_path = xml_path

    def set_pkl_path(self, pkl_path):
        self.pkl_path = pkl_path

    def parse_xml(self):
        '''解析xml文件'''
        parsed = objectify.parse(open(self.xml_path))
        root = parsed.getroot()
        for sentence in root.getchildren():
            sen_data = {}
            for child in sentence.getchildren():
                if child.tag == 'text':
                    sen_data['text'] = child.pyval
                elif child.tag == 'aspectCategories':
                    categories = []
                    for category in child.getchildren():
                        catData = {}
                        catData['category'] = category.get('category')
                        catData['polarity'] = category.get('polarity')
                        categories.append(catData)
                    sen_data['aspectCategories'] = categories
            self.data.append(sen_data)
        self.parsed = None
        self.xml_path = None
        return self.data

    def prepareData(self):
        if os.path.exists(self.pkl_path):
            self.data = self.getLocalData()
        else:
            self.data = self.parse_xml()
            self.saveDataToLocal()

    def getLocalData(self):
        pkl_file = open(self.pkl_path, 'rb')
        data = pickle.load(pkl_file)
        pkl_file.close()
        return data

    def saveDataToLocal(self):
        pkl_file = open(self.pkl_path, 'wb')
        pickle.dump(self.data, pkl_file)
        pkl_file.close()

    def get_data(self):
        self.prepareData()
        return self.data

if __name__ == '__main__':
    document = Document()
    document.set_xml_path("ABSA2014/Train/Restaurants_Train.xml")
    document.set_pkl_path("train.pkl")
    data = document.get_data()
    print "data"
    print data[0:10]
    document.set_xml_path("ABSA2014/Gold/Restaurants_Gold.xml")
    document.set_pkl_path("gold.pkl")
    data = document.get_data()
    print "data"
    print data[0:10]
