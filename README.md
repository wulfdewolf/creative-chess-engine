# Producing creative chess through chess-engine selfplay
This repository contains the implementation of a creative system that outputs creative chess games by running a creative chess-engine in selfplay.
The creative chess-engine is an extension to Stockfish that consists of trying to force Stockfish to play more, human deemed creative, moves.
This project was made in the context of the _Computational Creativity_ course in my first master year in _computer science_ at [VUB](https://www.vub.be).

The used stockfish version can be found [here](https://github.com/official-stockfish/Stockfish).
The chess database used by the creativity grading framework can be found [here](https://www.chessdb.cn/cloudbookc_api_en.html).


## Installation

### 1. Cloning the repository
The Stockfish code is added as a submodule. However, this repository contains a pre-built Stockfish [binary](extended-engine/binary/stockfish). This means that you do not need to also pull the Stockfish submodule to run the creative chess-engine.  
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
To be able to run the creative chess-engine, the Stockfish engine must be built. 
As mentioned above, the repository contains a pre-built Stockfish binary and thus you do not need to build it yourself.
If for some reason the binary does not work for your system, build it yourself by following the instructions in the Stockfish [README](https://github.com/official-stockfish/Stockfish/blob/master/README.md).

### 3. Installing requirements
Run the following command to install the required python packages:
```console
pip install -r requirements.txt
```

### 4. Running the creative system
To run the creative system and produce chess games, navigate to the root folder of the repository and run:
```console
python main.py NUMBER_OF_GAMES
```
The system can be ran in "otherplay" (one creative chess-engine vs. Stockfish) by running:
```console
python main_otherplay.py NUMBER_OF_GAMES
```

The created games are written to the [games folder](games/), in [PGN](http://www.saremba.de/chessgml/standards/pgn/pgn-complete.htm) format. The evaluation of the games is written to a .txt file in the [evaluation folder](evaluation/), the names will always be the same as the corresponding .pgn files.