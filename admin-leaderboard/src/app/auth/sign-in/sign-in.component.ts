import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../auth.service';
import { AppConfig } from '../../app.config';

@Component({
  selector: 'app-sign-in',
  // standalone: true,
  templateUrl: './sign-in.component.html',
  styleUrl: './sign-in.component.scss'
})
export class SignInComponent {
  username: string = '';
  password: string = '';

  constructor(private authService: AuthService, private router: Router) {}

  onSignIn() {
    this.authService.signIn(this.username, this.password).subscribe({
      next: (response) => {
        if (response.status) {
          // Assuming the response contains a token
          localStorage.setItem(AppConfig.signInKey, response.result[0]);
          AppConfig.bearerToken = response.result[0];
          AppConfig.isSignedIn = true;
          // Navigate to the dashboard or some other protected route
          this.router.navigate(['/pages/dashboard']);
        } else {
          alert(response.message);
        }
      },
      error: (error) => {
        alert('Invalid credentials');
        console.error('Sign in error', error);
      }
    });
  }
}