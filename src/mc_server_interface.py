import subprocess
import threading
from typing import IO, Callable

from mcstatus import JavaServer

def read_stream(stream: IO[str], callback: Callable[[str], None]):
    while True:
        output = stream.readline()

        # process was closed
        if not output:
            return

        # execute callback
        callback(output.strip())

def printInterfaceInfo(*values: object):
    separator = "---------------------"
    print(separator)
    print(' '.join([str(v) for v in values]))
    print(separator)


class MCServerInterface:
    def __init__(self, minGb: int = 1, maxGb: int = 7, serverFolder: str = '../IER Serverpack 4.3.1/', serverStartedInfo: str = "joined the game") -> None:
        # save args
        self.minGb = minGb
        self.maxGb = maxGb
        self.serverFolder = serverFolder
        self.serverStartedInfo = serverStartedInfo

        # track state
        self.isStarted = False
        self.didPlayersJoin = False
        self.playerCount = 0
        self.isStopping = False

        # setup communication interface
        self.stateReader = JavaServer.lookup("localhost:25565", timeout=10)

        # start server
        self._startMC()

        # read server output asynchronously
        self._startStreamReaders()

    def _startMC(self):
        self.serverProcess = subprocess.Popen(
            ['java', f'-Xmx{self.maxGb}G', f'-Xms{self.minGb}G', '-jar', 'forge-1.12.2-14.23.5.2860.jar', 'nogui'],
            cwd=self.serverFolder,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True,
            bufsize=1
        )

    def _startStreamReaders(self):
        # print logs and errors to python console
        self.infoThread = threading.Thread(target=read_stream, args=(self.serverProcess.stdout, self._onInfoOutput))   
        self.errorThread = threading.Thread(target=read_stream, args=(self.serverProcess.stderr, lambda e: print("Error:", e)))

        # start threads
        self.infoThread.start()
        self.errorThread.start()

    def executeCommand(self, command: str):
        # send command to server input
        self.serverProcess.stdin.write((command + "\n"))
        self.serverProcess.stdin.flush()

    def getStatus(self):
        return self.stateReader.status() if self.isStarted else None
    
    def _onInfoOutput(self, info: str):
        print(info)

        # server didn't start
        if not self._updateStartedState(info):
            return
        
        self._updatePlayerCount()
        self._updatePlayersJoined()

        # server is active
        if not self._checkIsServerAbandoned():
            return
        
        self._stop()
        
    def _updateStartedState(self, info: str):
        # server already finished starting
        if self.isStarted:
            return True
        
        # server still didn't start
        if not self.serverStartedInfo in info:
            return False

        # server started!
        self.isStarted = True
        printInterfaceInfo("Server started!")

        return True
    
    def _updatePlayerCount(self):
        # poll server for status
        info = self.getStatus()

        # server didn't start yet
        if not info:
            return
        
        # update player count
        self.playerCount = info.players.online        

    def _updatePlayersJoined(self):
        # no players joined
        if self.playerCount == 0:
            return

        # no need to update variable: It was already initialized
        if self.didPlayersJoin:
            return
        
        # players joined for the first time!
        self.didPlayersJoin = True

        printInterfaceInfo("Players joined for the first time!")

    def _checkIsServerAbandoned(self):
        # server can't be abandoned if no players joined
        if not self.didPlayersJoin:
            return False
        
        # players are active
        return self.playerCount == 0

    def _stop(self):
        # ennsure server starts stopping process only one time!
        if self.isStopping:
            return
        self.isStopping = True

        printInterfaceInfo("Stopping server")
        self.executeCommand("/stop")

    def waitForExit(self):
        # wait for threads to terminate
        self.infoThread.join()
        self.errorThread.join()

        # wait for server process to exit
        self.serverProcess.wait()