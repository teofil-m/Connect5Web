import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { io, Socket } from 'socket.io-client';

export interface GameState {
  id: string;
  host: string;
  players: { [key: string]: number | null };
  started: boolean;
  current_player: string;
  board: (number | null)[][];
  orientations?: (string | null)[][];
  game_over: boolean;
  winner: number | null;
  valid_moves: Array<{ line: number; height: number; orientation: string }>;
}

export interface AvailableGame {
  id: string;
  host: string;
  players_count: number;
  created_at: string;
}

@Injectable({
  providedIn: 'root'
})
export class GameService {
  private apiUrl = 'http://localhost:5000/api';
  private socket: Socket | null = null;
  private gameStateSubject = new BehaviorSubject<GameState | null>(null);
  public gameState$ = this.gameStateSubject.asObservable();

  constructor(private http: HttpClient) {
    this.initSocket();
  }

  private initSocket() {
    this.socket = io('http://localhost:5000', {
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: 5
    });

    this.socket.on('board_updated', (state: GameState) => {
      this.gameStateSubject.next(state);
    });

    this.socket.on('game_started', (state: GameState) => {
      this.gameStateSubject.next(state);
    });

    this.socket.on('game_state_updated', (state: GameState) => {
      this.gameStateSubject.next(state);
    });

    this.socket.on('error', (data: any) => {
      console.error('Socket error:', data);
    });
  }

  listGames(): Observable<AvailableGame[]> {
    return this.http.get<AvailableGame[]>(`${this.apiUrl}/games`);
  }

  createGame(hostName: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/games`, { host_name: hostName });
  }

  joinGame(gameId: string, playerName: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/games/${gameId}/join`, { player_name: playerName });
  }

  getGameState(gameId: string): Observable<GameState> {
    return this.http.get<GameState>(`${this.apiUrl}/games/${gameId}`);
  }

  startGame(gameId: string): Observable<GameState> {
    return this.http.post<GameState>(`${this.apiUrl}/games/${gameId}/start`, {});
  }

  makeMove(gameId: string, playerName: string, line: number, height: number, orientation: string = 'v'): Observable<GameState> {
    return this.http.post<GameState>(`${this.apiUrl}/games/${gameId}/move`, {
      player_name: playerName,
      line,
      height,
      orientation
    });
  }

  joinGameRoom(gameId: string, playerName: string) {
    if (this.socket) {
      this.socket.emit('join_game_room', { game_id: gameId, player_name: playerName });
    }
  }

  emitGameMove(gameId: string, playerName: string, line: number, height: number) {
    if (this.socket) {
      this.socket.emit('game_move', {
        game_id: gameId,
        player_name: playerName,
        line,
        height
      });
    }
  }

  updateGameState(state: GameState) {
    this.gameStateSubject.next(state);
  }
}
