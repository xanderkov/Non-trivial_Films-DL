from ufal.udpipe import Model, Pipeline
import os
import re
import sys


class PrepText():
    def __init__(self):
        print('\nLoading the model...', file=sys.stderr)
        self.model = Model.load("udpipe_syntagrus.model")

    def num_replace(self, word):
        newtoken = 'x' * len(word)
        return newtoken

    def clean_token(self, token, misc):
        out_token = token.strip().replace(' ', '')
        if token == 'Файл' and 'SpaceAfter=No' in misc:
            return None
        return out_token

    def clean_lemma(self, lemma, pos):
        out_lemma = lemma.strip().replace(' ', '').replace('_', '').lower()
        if '|' in out_lemma or out_lemma.endswith('.jpg') or out_lemma.endswith('.png'):
            return None
        if pos != 'PUNCT':
            if out_lemma.startswith('«') or out_lemma.startswith('»'):
                out_lemma = ''.join(out_lemma[1:])
            if out_lemma.endswith('«') or out_lemma.endswith('»'):
                out_lemma = ''.join(out_lemma[:-1])
            if out_lemma.endswith('!') or out_lemma.endswith('?') or out_lemma.endswith(',') \
                    or out_lemma.endswith('.'):
                out_lemma = ''.join(out_lemma[:-1])
        return out_lemma

    def process(self, pipeline, text='Строка', keep_pos=True, keep_punct=False):
        entities = {'PROPN'}
        named = False
        memory = []
        mem_case = None
        mem_number = None
        tagged_propn = []

        # обрабатываем текст, получаем результат в формате conllu:
        processed = pipeline.process(text)

        # пропускаем строки со служебной информацией:
        content = [l for l in processed.split('\n') if not l.startswith('#')]

        # извлекаем из обработанного текста леммы, тэги и морфологические характеристики
        tagged = [w.split('\t') for w in content if w]

        for t in tagged:
            if len(t) != 10:
                continue
            (word_id, token, lemma, pos, xpos, feats, head, deprel, deps, misc) = t
            token = self.clean_token(token, misc)
            lemma = self.clean_lemma(lemma, pos)
            if not lemma or not token:
                continue
            if pos in entities:
                if '|' not in feats:
                    tagged_propn.append('%s_%s' % (lemma, pos))
                    continue
                morph = {el.split('=')[0]: el.split('=')[1] for el in feats.split('|')}
                if 'Case' not in morph or 'Number' not in morph:
                    tagged_propn.append('%s_%s' % (lemma, pos))
                    continue
                if not named:
                    named = True
                    mem_case = morph['Case']
                    mem_number = morph['Number']
                if morph['Case'] == mem_case and morph['Number'] == mem_number:
                    memory.append(lemma)
                    if 'SpacesAfter=\\n' in misc or 'SpacesAfter=\s\\n' in misc:
                        named = False
                        past_lemma = '::'.join(memory)
                        memory = []
                        tagged_propn.append(past_lemma + '_PROPN ')
                else:
                    named = False
                    past_lemma = '::'.join(memory)
                    memory = []
                    tagged_propn.append(past_lemma + '_PROPN ')
                    tagged_propn.append('%s_%s' % (lemma, pos))
            else:
                if not named:
                    if pos == 'NUM' and token.isdigit():  # Заменяем числа на xxxxx той же длины
                        lemma = self.num_replace(token)
                    tagged_propn.append('%s_%s' % (lemma, pos))
                else:
                    named = False
                    past_lemma = '::'.join(memory)
                    memory = []
                    tagged_propn.append(past_lemma + '_PROPN ')
                    tagged_propn.append('%s_%s' % (lemma, pos))

        if not keep_punct:
            tagged_propn = [word for word in tagged_propn if word.split('_')[1] != 'PUNCT']
        if not keep_pos:
            tagged_propn = [word.split('_')[0] for word in tagged_propn]
        return tagged_propn

    def tag_ud(self, text='Текст нужно передать функции в виде строки!'):
        process_pipeline = Pipeline(self.model, 'tokenize', Pipeline.DEFAULT, Pipeline.DEFAULT, 'conllu')

        output = self.process(process_pipeline, text=text)

        ret = " ".join(output)
        return ret

if __name__ == '__main__':
    prep = PrepText()
    print(prep.tag_ud())
