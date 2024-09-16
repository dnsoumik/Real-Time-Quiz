import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AppConfig } from './app.config';


@Injectable({
  providedIn: 'root'
})
export class AppService {

  constructor(private http: HttpClient) {}

  getQuizById(quizId: string): Observable<any> {
    return this.http.get<any>(
      `${AppConfig.serverUrl}/play_quiz`,
      {
        params: {
          id: quizId
        }
      }
    );
  }

  postQuizById(body: any): Observable<any> {
    return this.http.post<any>(
      `${AppConfig.serverUrl}/play_quiz`,
      body
    );
  }

}
