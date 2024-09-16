import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

import { AppConfig } from './app.config';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {
  title = 'admin-leaderboard';

  constructor() {
    if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
      const token = localStorage.getItem(AppConfig.signInKey);
      if (!!token) {
        AppConfig.isSignedIn = !!token;
        AppConfig.bearerToken = token;
      }
    }
  }
}
