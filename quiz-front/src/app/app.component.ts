import { Component } from '@angular/core';
import { ActivatedRoute, RouterOutlet } from '@angular/router';
import { MatToolbarModule } from '@angular/material/toolbar';
import { AppService } from './app.service';
import { HttpClientModule } from '@angular/common/http';
import { provideHttpClient, withFetch } from '@angular/common/http';
import { MatCardModule } from '@angular/material/card';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { CommonModule } from '@angular/common';
import { MatDividerModule } from '@angular/material/divider';
import { MatRadioModule } from '@angular/material/radio';
import { MatButtonModule } from '@angular/material/button';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatIconModule } from '@angular/material/icon';
import { FormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    MatToolbarModule,
    HttpClientModule,
    MatCardModule,
    MatProgressBarModule,
    CommonModule,
    MatDividerModule,
    MatRadioModule,
    MatButtonModule,
    MatTooltipModule,
    MatIconModule,
    FormsModule,
    MatInputModule,
    MatFormFieldModule,
  ],
  providers: [AppService],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {
  quizId: string | null = '';

  isLoading = 1;

  quizName: string = '';
  errorMessage: string = '';
  quizzesData: Array<any> = [];
  fullName: string = '';
  phoneNumber: string = '';

  constructor(private appService: AppService, private route: ActivatedRoute) {
    this.isLoading = 1;
  }

  ngOnInit(): void {
    const cntx = this;
    this.route.queryParamMap.subscribe((params) => {
      this.quizId = params.get('quizId');
      cntx.isLoading = 1;
      setTimeout(() => {
        this.getQuizInfo();
      }, 2000);
    });
  }

  onRefresh(): void {
    const userConfirmed = window.confirm(
      'Are you sure? You will lose your progress :('
    );
    if (userConfirmed) {
      this.isLoading = 1;
      setTimeout(() => {
        this.getQuizInfo();
      }, 2000);
    } else {
      // If the user selects "No", simply return and do nothing
      return;
    }
  }

  getQuizInfo(): void {
    this.isLoading = 1;
    if (this.quizId != null)
      this.appService.getQuizById(this.quizId).subscribe({
        next: (response) => {
          console.log(response);
          if (response.status) {
            const data = response.result[0];
            this.quizName = data.quizName;
            this.quizzesData = data.questions;
            this.isLoading = 2;
          } else {
            this.errorMessage = response.message;
            this.isLoading = 3;
          }
        },
        error: (error) => {
          this.errorMessage = 'Error fetching Quiz';
          this.isLoading = 3;
        },
      });
  }

  onSubmitResult(): void {
    const body = {
      fullName: this.fullName,
      phoneNumber: this.phoneNumber,
      _id: this.quizId,
      questions: this.quizzesData,
    };
    if (this.quizId != null)
      this.appService.postQuizById(body).subscribe({
        next: (response) => {
          console.log(response);
          if (response.status) {
            const userConfirmed = window.confirm(response.message);
            if (userConfirmed) {
              setTimeout(() => {
                this.errorMessage = response.message;
                this.isLoading = 3;
              }, 200);
            } else {
              // If the user selects "No", simply return and do nothing
              return;
            }
          } else {
            alert(response.message);
          }
        },
        error: (error) => {
          alert('Error fetching Quiz');
        },
      });
  }
}
