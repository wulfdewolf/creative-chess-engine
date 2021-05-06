# Producing creative chess through chess engine selfplay
This repository contains the implementation of a creative system that outputs creative chess games by running a creative chess engine in selfplay.
The chess engine is an extension to Stockfish that consists of trying to force Stockfish to play more, human deemed creative, moves.
This project was made in the context of the _Computational Creativity_ course in my first master year in _computer science_ at [VUB](https://www.vub.be).

The used stockfish version can be found [here](https://github.com/official-stockfish/Stockfish).
The chess database used by the creativity grading framework can be found [here](https://www.chessdb.cn/cloudbookc_api_en.html).


## Installation

### 1. Cloning the repository
The Stockfish code is added as a submodule. However, this repository contains a pre-built Stockfish [binary](extended-engine/binary/stockfish). This means that you do not need to also pull the Stockfish submodule to run the creative chess engine.  
If you still want to, you can by pulling:
* Through ssh:
```console
git clone --recurse-submodules git@github.com:wulfdewolf/creative-chess engine.git
```
* Through https:
```console
git clone --recurse-submodules https://github.com/wulfdewolf/creative-chess engine.git
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

### 4. Running the creative system
To run the creative system and produce chess games, navigate to the root folder of the repository and run:
```console
python main.py -h
```
When a game is accepted by the internal evaluation of the creative system, it is printed, in [PGN](http://www.saremba.de/chessgml/standards/pgn/pgn-complete.htm) format, to a folder in the the [games folder](games/). The headers of the PGN format are used to store the evaluation values and the used weights, always in the following format: "[white][black]". Every move is also commented with an array that indicates how the engines classified the move. While the system is running its progress can be tracked in the **main.log** file. 