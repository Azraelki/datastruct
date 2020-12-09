import pandas as pd

word_dict = {
    'body_part': 'nhb',
    'crowd': 'nhc',
    'disease': 'nhd',
    'examination': 'nhe',
    'hospital': 'nth',
    'inspection': 'nhi',
    'medicine': 'nhm',
    'physical': 'nhp',
    'symptom': 'nhs',
    'treatment': 'nht',
    'unit': 'wh'
}


def convert():
    for key in word_dict.keys():
        df = pd.read_csv(key + '.dic.default', sep='\t')
        result = []
        for index, row in df.iterrows():
            result.append([row[0], word_dict[key], 1])
        pd.DataFrame(result).to_csv(key + '.csv', index=None, header=None, encoding='utf-8')


if __name__ == '__main__':
    convert()
