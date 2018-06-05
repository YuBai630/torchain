from typing import Dict
import sys


def read_eg(egs: str, chunksize: int=10000) -> Dict[str, int]:
    token2position = {}
    pos = 0
    chunk = b''

    with open(egs, 'rb') as f:
        while True:
            _read = f.read(chunksize)
            if _read == b'':
                break
            chunk += _read
            while True:
                try:
                    index = chunk.index(b'<Nnet3ChainEg>')
                except ValueError:
                    break
                else:
                    try:
                        sindex = chunk.index(b'</Nnet3ChainEg>') + len(b'</Nnet3ChainEg> ')
                    except ValueError:
                        sindex = 0
                    # uttid b'\x00B'<Nnet3ChainEg>...uttid b'\x00B'<Nnet3ChainEg>...
                    if sindex > index - len(b' \x00B'):
                        token = chunk[:index - len(b' \x00B')]
                    else:
                        token = chunk[sindex:index - len(b' \x00B')]
                    p = pos + index - len(b'\x00B')
                    token2position[token] = p
                    # print("sindex: {}, index{}", sindex, index - len(b' \x00B'))
                    print("{} {}:{}".format(token.decode(), egs, p))
                    chunk = chunk[index + len(b'<Nnet3ChainEg>'):]
                    pos += index + len(b'<Nnet3ChainEg>')
    return token2position


if __name__ == '__main__':
    egs = sys.argv[1]
    # egs = '/data/work44/public/kaldi-22fbdd9/egs/chime5/s5/exp/chain_train_worn_u100k_cleaned/tdnn1a_sp/egs/combine.cegs'
    # egs = '/data/work70/skarita/exp/chime5/kaldi-22fbdd/egs/chime5/s5/exp/chain_train_worn_u100k_cleaned/tdnn1a_sp/egs/cegs.1.ark'
    read_eg(egs)
