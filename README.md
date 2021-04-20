# Adding creativity to a heuristics-based chess engine
A creative chess engine that consists of an extension to Stockfish to combine the Stockfish optimality scores with newly defined creativity scores. The optimal combination of scores was learned through training against Stockfish. This project was made in the context of the _Computational Creativity_ course in my first master year in _computer science_ at [VUB](https://www.vub.be).

The used stockfish version can be found [here](https://github.com/official-stockfish/Stockfish).
The chess database used by the creativity grading framework can be found [here](https://www.chessdb.cn/cloudbookc_api_en.html).


## Installation

### 1. Cloning the repository
The Stockfish code is added as a submodule. However, this repository contains a pre-built Stockfish [binary](extended-engine/binary/stockfish). This means that you do not need to also pull the Stockfish submodule to run the creative chess engine.  
If you still want to, you can by pulling:
* Through ssh:
```console
git clone --recurse-submodules git@github.com:wulfdewolf/creative-chess-engine.git
```
* Through https:
```console
git clone --recurse-submodules https://github.com/wulfdewolf/creative-chess-engine.git
```

### 2. Building Stockfish
To be able to run the creative chess engine, the Stockfish engine must be built. 
As mentioned above, the repository contains a pre-built Stockfish binary and thus you do not need to build it yourself.
If for some reason the binary does not work for your system, build it yourself by following the instructions in the Stockfish [README](https://github.com/official-stockfish/Stockfish/blob/master/README.md).

### 3. Installing requirements
Run the following command to install the required python packages:
```console
pip install -r requirements.txt
```

### 4. Running the application
To play against the engine via the terminal, navigate to the root folder of the repository and run:
```console
python play.py
```
