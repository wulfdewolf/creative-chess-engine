# Adding creativity to a heuristics-based chess engine
A creative chess engine that consists of an extension to Stockfish to combine the Stockfish optimality scores with newly defined creativity scores. The optimal combination of scores was learned through self-play. This project was made as part of the _Computational Creativity_ course in my first master year _computer science_ at [VUB](https://www.vub.be).

The used stockfish version can be found [here](https://github.com/official-stockfish/Stockfish).
The chess database used by the creativity grading framework can be found [here](https://www.chessdb.cn/cloudbookc_api_en.html).


## Installation

### 1. Cloning the repository
The Stockfish code is added as a submodule, this means that when cloning the repository you need to use following command to also pull the Stockfish repository:
```console
git clone --recurse-submodules git://github.com/foo/bar.git
```
### 2. Building Stockfish
To be able to run the creative chess engine, the Stockfish engine must be built. 
Follow the instructions Stockfish [readme](https://github.com/official-stockfish/Stockfish/blob/master/README.md).

### 3. Installing requirements
Run following command to install the required python packages:
```console
pip install -r requirements.txt
```

### 4. Running the program
To now run the creative chess engine do:
```console
python main.py
```
