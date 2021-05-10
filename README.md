# Producing creative chess through chess engine selfplay
This repository contains the implementation of a creative system that outputs creative chess games by running a creative chess engine in selfplay.
The chess engine is an extension to Stockfish that consists of trying to force Stockfish to play more, human deemed creative, moves.
This project was made in the context of the _Computational Creativity_ course in my first master year in _computer science_ at [VUB](https://www.vub.be).

The used stockfish version can be found [here](https://github.com/official-stockfish/Stockfish).
The chess database used by the creativity grading framework can be found [here](https://www.chessdb.cn/cloudbookc_api_en.html).

The slides of my final presentation are [here](documentation/presentation.pdf), the paper I wrote on the system can be found [here](documentation/paper.pdf).

Underneath you can find my contact information.

| Name     | Student id | Email address    | Linkedin |
| :---     | :---       |:---              | :---     |
| Wolf De Wulf | 0546395 | [wolf.de.wulf@vub.be](mailto:wolf.de.wulf@vub.be) | https://www.linkedin.com/in/wolf-de-wulf/         |


## Installation

### 1. Cloning the repository
The Stockfish code is added as a submodule. However, this repository contains a pre-built Stockfish [binary](extended-engine/binary/stockfish). This means that you do not need to also clone the Stockfish submodule to run the creative chess system.  
If you still want to, you can by cloning like this:
* Through ssh:
```console
git clone --recurse-submodules git@github.com:wulfdewolf/creative-chess engine.git
```
* Through https:
```console
git clone --recurse-submodules https://github.com/wulfdewolf/creative-chess engine.git
```

### 2. Building Stockfish
To be able to run the creative chess system, the Stockfish engine must be built. 
As mentioned above, the repository contains a pre-built Stockfish binary and thus you do not need to build it yourself.
If for some reason the binary does not work for your system, build it yourself by following the instructions in the Stockfish [README](https://github.com/official-stockfish/Stockfish/blob/master/README.md).

### 3. Installing requirements
Run the following command to install the required python packages:
```console
pip install -r requirements.txt
```

### 4. Running the creative chess system
To run the creative system and produce chess games, navigate to the root folder of the repository and run:
```console
python main.py -h
```
When a game is accepted by the internal evaluation of the creative system, its [PGN](http://www.saremba.de/chessgml/standards/pgn/pgn-complete.htm) format is printed to a folder in the [games folder](games/). The headers of the PGN format are used to store the evaluation values and the used weights, always in the following format: "[white][black]". Every move is also commented with an array that indicates how the engines classified the move. While the system is running its progress can be tracked in the **main.log** file. 
