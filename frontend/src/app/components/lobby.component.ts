import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { GameService, AvailableGame } from '../services/game.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-lobby',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './lobby.component.html',
  styleUrls: ['./lobby.component.css']
})
export class LobbyComponent implements OnInit {
  playerName: string = '';
  availableGames: AvailableGame[] = [];
  showCreateGame = false;
  loading = false;
  hostName: string = '';
  errorMessage: string = '';

  constructor(
    private gameService: GameService,
    private router: Router
  ) {}

  ngOnInit() {
    this.loadGames();
    // Refresh games every 2 seconds
    setInterval(() => this.loadGames(), 2000);
  }

  loadGames() {
    this.gameService.listGames().subscribe({
      next: (games) => {
        this.availableGames = games;
      },
      error: (err) => {
        console.error('Error loading games:', err);
      }
    });
  }

  createGame() {
    if (!this.hostName.trim()) {
      this.errorMessage = 'Please enter your name';
      return;
    }

    this.loading = true;
    this.gameService.createGame(this.hostName).subscribe({
      next: (response) => {
        this.playerName = this.hostName;
        this.router.navigate(['/game', response.game_id], {
          state: { playerName: this.hostName, isHost: true }
        });
      },
      error: (err) => {
        console.error('Error creating game:', err);
        this.errorMessage = 'Failed to create game';
        this.loading = false;
      }
    });
  }

  joinGame(gameId: string) {
    if (!this.playerName.trim()) {
      this.errorMessage = 'Please enter your name';
      return;
    }

    this.loading = true;
    this.gameService.joinGame(gameId, this.playerName).subscribe({
      next: () => {
        this.router.navigate(['/game', gameId], {
          state: { playerName: this.playerName, isHost: false }
        });
      },
      error: (err) => {
        console.error('Error joining game:', err);
        this.errorMessage = 'Failed to join game';
        this.loading = false;
      }
    });
  }

  toggleCreateGame() {
    this.showCreateGame = !this.showCreateGame;
    this.errorMessage = '';
  }
}
