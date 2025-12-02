import { Component, OnInit, OnDestroy, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { GameService, GameState } from '../services/game.service';
import * as THREE from 'three';

@Component({
  selector: 'app-game',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.css']
})
export class GameComponent implements OnInit, OnDestroy {
  @ViewChild('gameCanvas') canvasRef!: ElementRef<HTMLCanvasElement>;

  gameId: string = '';
  playerName: string = '';
  isHost: boolean = false;
  gameState: GameState | null = null;
  errorMessage: string = '';
  selectedOrientation: string = 'v'; // 'v' for vertical, 'h' for horizontal
  pendingMove: { line: number; height: number; orientation: string } | null = null;
  previewMove: { line: number; height: number; orientation: string } | null = null;

  private scene: THREE.Scene | null = null;
  private camera: THREE.PerspectiveCamera | null = null;
  private renderer: THREE.WebGLRenderer | null = null;
  private blocks: THREE.Mesh[] = [];
  private previewBlock: THREE.Mesh | null = null;
  private animationFrameId: number | null = null;
  private selectedPosition: { line: number; height: number } | null = null;

  constructor(
    private gameService: GameService,
    private route: ActivatedRoute,
    private router: Router
  ) {
    this.gameId = this.route.snapshot.paramMap.get('gameId') || '';
    const state = this.router.getCurrentNavigation()?.extras.state as any;
    if (state) {
      this.playerName = state['playerName'] || '';
      this.isHost = state['isHost'] || false;
    }
  }

  ngOnInit() {
    if (!this.gameId || !this.playerName) {
      this.router.navigate(['/']);
      return;
    }

    this.gameService.joinGameRoom(this.gameId, this.playerName);
    
    // Subscribe to WebSocket game state updates
    this.gameService.gameState$.subscribe((state) => {
      if (state) {
        this.gameState = state;
        this.updateVisualization();
        // Auto-start game when 2 players are present and game hasn't started
        if (!state.started && this.isHost && Object.keys(state.players).length === 2) {
          setTimeout(() => this.startGame(), 500);
        }
      }
    });
    
    this.loadGameState();
    
    setTimeout(() => {
      this.initThreeJS();
    }, 100);

    // Poll for game state updates
    const pollInterval = setInterval(() => {
      this.gameService.getGameState(this.gameId).subscribe({
        next: (state) => {
          this.gameService.updateGameState(state);
        },
        error: (err) => {
          console.error('Error polling game state:', err);
        }
      });
    }, 1000);

    this.route.params.subscribe(() => {
      clearInterval(pollInterval);
    });
  }

  loadGameState() {
    this.gameService.getGameState(this.gameId).subscribe({
      next: (state) => {
        this.gameState = state;
        this.gameService.updateGameState(state);
      },
      error: (err) => {
        console.error('Error loading game state:', err);
        this.errorMessage = 'Failed to load game state';
      }
    });
  }

  startGame() {
    this.gameService.startGame(this.gameId).subscribe({
      next: (state) => {
        this.gameState = state;
        this.gameService.updateGameState(state);
      },
      error: (err) => {
        console.error('Error starting game:', err);
        this.errorMessage = 'Failed to start game';
      }
    });
  }

  private initThreeJS() {
    const canvas = this.canvasRef?.nativeElement;
    if (!canvas) return;

    const width = canvas.clientWidth;
    const height = canvas.clientHeight;

    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x1a1a2e);

    this.camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    this.camera.position.set(4.5, 7, 12);
    this.camera.lookAt(4.5, 3, 4.5);

    this.renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
    this.renderer.setSize(width, height);
    this.renderer.setPixelRatio(window.devicePixelRatio);

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    this.scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(10, 10, 10);
    this.scene.add(directionalLight);

    // Grid lines
    this.drawGrid();

    // Mouse events
    canvas.addEventListener('click', (event) => this.onCanvasClick(event));
    window.addEventListener('resize', () => this.onWindowResize());

    this.animate();
  }

  private drawGrid() {
    if (!this.scene) return;

    const gridHelper = new THREE.GridHelper(9, 9, 0x444444, 0x222222);
    gridHelper.position.y = 0;
    this.scene.add(gridHelper);

    // Draw vertical lines for depth
    const lineGeometry = new THREE.BufferGeometry();
    for (let i = 0; i <= 9; i++) {
      const points = [
        new THREE.Vector3(i, 0, 0),
        new THREE.Vector3(i, 9, 0)
      ];
      lineGeometry.setFromPoints(points);
      const line = new THREE.Line(lineGeometry, new THREE.LineBasicMaterial({ color: 0x444444 }));
      this.scene!.add(line);
    }
  }

  private updateVisualization() {
    if (!this.scene || !this.gameState) return;

    // Remove old blocks
    this.blocks.forEach((block) => {
      this.scene!.remove(block);
    });
    this.blocks = [];

    // Track which cells have been rendered to avoid duplicates
    const rendered = new Set<string>();

    // Add new blocks
    for (let line = 0; line < 9; line++) {
      for (let height = 0; height < 9; height++) {
        const occupant = this.gameState.board[line][height];
        if (occupant !== null) {
          const key = `${line}-${height}`;
          if (!rendered.has(key)) {
            const orientation = this.gameState.orientations?.[line]?.[height] || 'v';
            // Only render the "primary" block (not the secondary part of a 1x2)
            if (orientation === 'v' && (height === 0 || this.gameState.board[line][height - 1] !== occupant)) {
              // This is the bottom of a vertical block, render it
              this.createBlockVisual(line, height, occupant, 'v');
              rendered.add(key);
              rendered.add(`${line}-${height + 1}`); // Mark the top as rendered too
            } else if (orientation === 'h' && (line === 0 || this.gameState.board[line - 1][height] !== occupant)) {
              // This is the left of a horizontal block, render it
              this.createBlockVisual(line, height, occupant, 'h');
              rendered.add(key);
              rendered.add(`${line + 1}-${height}`); // Mark the right as rendered too
            }
          }
        }
      }
    }

    // Add preview block if there's a pending move
    if (this.previewMove) {
      this.createPreviewBlock(this.previewMove.line, this.previewMove.height, this.previewMove.orientation);
    }
  }

  private createBlockVisual(line: number, height: number, playerId: number, orientation: string = 'v') {
    if (!this.scene) return;

    const color = playerId === 1 ? 0xff6b6b : 0x4ecdc4;
    const material = new THREE.MeshPhongMaterial({
      color,
      shininess: 100,
      emissive: playerId === this.gameState?.players[this.playerName] ? 0x333333 : 0
    });

    let geometry: THREE.BoxGeometry;
    let block: THREE.Mesh;
    let posX: number, posY: number, posZ: number;

    if (orientation === 'v') {
      // Vertical: 1x1x2 (occupies two height levels)
      geometry = new THREE.BoxGeometry(1.0, 1.0, 2.0);
      block = new THREE.Mesh(geometry, material);
      posX = line;
      posY = height + 0.5; // Center of the 2-unit height
      posZ = 4.5;
      block.userData = { line, height, playerId, orientation: 'v' };
    } else {
      // Horizontal: 2x1x1 (occupies two line positions)
      geometry = new THREE.BoxGeometry(2.0, 1.0, 1.0);
      block = new THREE.Mesh(geometry, material);
      posX = line + 0.5; // Center of the 2-unit width
      posY = height;
      posZ = 4.5;
      block.userData = { line, height, playerId, orientation: 'h' };
    }

    block.position.set(posX, posY, posZ);

    const edges = new THREE.EdgesGeometry(geometry);
    const lineMaterial = new THREE.LineBasicMaterial({ color: 0x000000 });
    const wireframe = new THREE.LineSegments(edges, lineMaterial);
    block.add(wireframe);

    this.scene.add(block);
    this.blocks.push(block);
  }

  private createPreviewBlock(line: number, height: number, orientation: string) {
    if (!this.scene) return;

    // Remove old preview block if exists
    if (this.previewBlock) {
      this.scene.remove(this.previewBlock);
    }

    const geometry: THREE.BoxGeometry = orientation === 'v' 
      ? new THREE.BoxGeometry(1.0, 1.0, 2.0)
      : new THREE.BoxGeometry(2.0, 1.0, 1.0);

    // Semi-transparent preview material - white/light color
    const material = new THREE.MeshPhongMaterial({
      color: 0xffffff,
      shininess: 50,
      transparent: true,
      opacity: 0.4,
      emissive: 0x888888
    });

    this.previewBlock = new THREE.Mesh(geometry, material);

    let posX: number, posY: number, posZ: number;
    if (orientation === 'v') {
      posX = line;
      posY = height + 0.5;
      posZ = 4.5;
    } else {
      posX = line + 0.5;
      posY = height;
      posZ = 4.5;
    }

    this.previewBlock.position.set(posX, posY, posZ);

    // Add dashed outline to preview
    const edges = new THREE.EdgesGeometry(geometry);
    const lineColor = new THREE.LineBasicMaterial({
      color: 0xffff00,
      linewidth: 2,
      transparent: true,
      opacity: 0.7
    });
    const wireframe = new THREE.LineSegments(edges, lineColor);
    this.previewBlock.add(wireframe);

    this.scene.add(this.previewBlock);
  }

  private onCanvasClick(event: MouseEvent) {
    if (!this.scene || !this.camera || !this.renderer || !this.gameState || !this.gameState.started) return;

    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    const canvas = this.canvasRef?.nativeElement;
    const rect = canvas.getBoundingClientRect();

    mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

    raycaster.setFromCamera(mouse, this.camera);
    
    // Check for block intersections first
    const blockIntersects = raycaster.intersectObjects(this.blocks);
    if (blockIntersects.length > 0) {
      const intersection = blockIntersects[0].object as THREE.Mesh;
      const userData = intersection.userData as any;
      this.selectedPosition = { line: userData['line'], height: userData['height'] };
      return;
    }
    
    // Check for grid position intersection
    const gridPlane = new THREE.Plane(new THREE.Vector3(0, 0, 1), -4.5);
    const intersectionPoint = new THREE.Vector3();
    raycaster.ray.intersectPlane(gridPlane, intersectionPoint);
    
    const line = Math.round(intersectionPoint.x - 0.5);
    const height = Math.round(intersectionPoint.y - 0.5);
    
    // Validate position is within bounds and empty
    if (line >= 0 && line < 9 && height >= 0 && height < 9 && this.gameState.board[line][height] === null) {
      this.makeMove(line, height);
    }
  }

  makeMove(line: number, height: number) {
    if (!this.gameState || this.gameState.game_over) {
      this.errorMessage = 'Game is over';
      return;
    }

    if (this.gameState.current_player !== this.playerName) {
      this.errorMessage = 'Not your turn';
      return;
    }

    // Store the pending move and show preview
    this.pendingMove = { line, height, orientation: this.selectedOrientation };
    this.previewMove = { line, height, orientation: this.selectedOrientation };
    this.errorMessage = '';
  }

  submitMove() {
    if (!this.pendingMove) {
      this.errorMessage = 'No move selected';
      return;
    }

    this.gameService.makeMove(
      this.gameId,
      this.playerName,
      this.pendingMove.line,
      this.pendingMove.height,
      this.pendingMove.orientation
    ).subscribe({
      next: (state) => {
        this.gameState = state;
        this.gameService.updateGameState(state);
        this.pendingMove = null;
        this.previewMove = null;
        this.errorMessage = '';
      },
      error: (err) => {
        console.error('Error making move:', err);
        this.errorMessage = 'Invalid move';
      }
    });
  }

  undoMove() {
    this.pendingMove = null;
    this.previewMove = null;
    this.errorMessage = '';
  }

  private animate = () => {
    if (this.renderer && this.scene && this.camera) {
      this.animationFrameId = requestAnimationFrame(this.animate);
      this.renderer.render(this.scene, this.camera);
    }
  };

  private onWindowResize() {
    if (!this.camera || !this.renderer) return;

    const canvas = this.canvasRef?.nativeElement;
    if (!canvas) return;

    const width = canvas.clientWidth;
    const height = canvas.clientHeight;

    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height);
  }

  ngOnDestroy() {
    if (this.animationFrameId !== null) {
      cancelAnimationFrame(this.animationFrameId);
    }
    if (this.renderer) {
      this.renderer.dispose();
    }
  }

  goBack() {
    this.router.navigate(['/']);
  }
}
