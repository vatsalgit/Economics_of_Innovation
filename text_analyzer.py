import slate
import os


class TextAnalyzer(object):

    def __init__(self, DIR='../Data', file_format='pdf', **kwargs):
        self.DIR = DIR
        self.file_format = file_format
        if file_format == 'pdf':
            self.extractTextfromPDF(DIR)

    @staticmethod
    def extractTextfromPDF(DIR):
        for file in os.listdir(DIR):
            if file.endswith(".pdf"):
                print(os.path.join("DIR", file))


if __name__ == "__main__":
    t = TextAnalyzer()
    
