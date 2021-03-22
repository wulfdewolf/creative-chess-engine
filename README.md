# Adding creativity to a heuristics-based chess engine
A creative chess engine that consists of an extension to Stockfish to combine the Stockfish optimality scores with newly defined creativity scores. The optimal combination of scores was learned through self-play. This project was made as part of the _Computational Creativity_ course in my first master year _computer science_ at [VUB](https://www.vub.be).

The used stockfish version can be found [here](https://github.com/official-stockfish/Stockfish).
The chess database used by the creativity grading framework can be found [here](https://www.chessdb.cn/cloudbookc_api_en.html).


## Installation

### 1. Cloning the repository
The Stockfish code is added as a submodule. However, this repository contains a pre-build Stockfish [binary](extended-engine/binary/stockfish). This means that you do not need to also pull the Stockfish submodule to run the creative chess engine. 
If you still want to, pull using:
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
Follow the instructions in the Stockfish [README](https://github.com/official-stockfish/Stockfish/blob/master/README.md).

### 3. Installing requirements
Run the following command to install the required python packages:
```console
pip install -r requirements.txt
```

### 4. Running the program
To play against the engine via the terminal, navigate to the root folder of the repository and run:
```console
python play.py
```

To let two instances of the engine play against each other for some amount of games and see what the weights they learn are, navigate to the root folder of the repository and run:
```console
python learn.py NUMBER_OF_GAMES
```
